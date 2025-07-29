"""API Client for IRM KMI weather"""
import asyncio
import hashlib
import json
import logging
import socket
import time
import urllib.parse
from datetime import datetime, timedelta
from statistics import mean
from typing import List, Dict
from zoneinfo import ZoneInfo

import aiohttp
import async_timeout

from .const import MAP_WARNING_ID_TO_SLUG as SLUG_MAP, WWEVOL_TO_ENUM_MAP
from .const import STYLE_TO_PARAM_MAP, WEEKDAYS
from .data import (AnimationFrameData, CurrentWeatherData, Forecast,
                   IrmKmiForecast, IrmKmiRadarForecast, RadarAnimationData,
                   WarningData)
from .pollen import PollenParser

_LOGGER = logging.getLogger(__name__)


class IrmKmiApiError(Exception):
    """Exception to indicate a general API error."""


class IrmKmiApiCommunicationError(IrmKmiApiError):
    """Exception to indicate a communication error."""


class IrmKmiApiParametersError(IrmKmiApiError):
    """Exception to indicate a parameter error."""


class IrmKmiApiClient:
    """API client for IRM KMI weather data"""
    COORD_DECIMALS = 6
    _cache_max_age = 60 * 60 * 2  # Remove items from the cache if they have not been hit since 2 hours
    _cache = {}

    def __init__(self, session: aiohttp.ClientSession, user_agent: str) -> None:
        self._session = session
        self._base_url = "https://app.meteo.be/services/appv4/"
        self._user_agent = user_agent

    async def get_forecasts_coord(self, coord: Dict[str, float | int]) -> dict:
        """
        Get forecasts for given location.

        :param coord: dict with the following keys: 'lat', 'long' (both float or int)
        :return: raw forecast as python dict
        :raise: IrmKmiApiError when communication with the API fails
        """
        assert 'lat' in coord
        assert 'long' in coord
        coord['lat'] = round(coord['lat'], self.COORD_DECIMALS)
        coord['long'] = round(coord['long'], self.COORD_DECIMALS)

        response: bytes = await self._api_wrapper(
            params={"s": "getForecasts", "k": self._api_key("getForecasts")} | coord
        )
        response: dict = json.loads(response)

        _LOGGER.debug(f"Observation for {response.get('cityName', '')}: {response.get('obs', '{}')}")
        _LOGGER.debug(f"Full data: {response}")
        return response

    async def get_image(self, url, params: Dict[str, str] | None = None) -> bytes:
        """
        Get the image at the specified url with the parameters

        :param url: URL to fetch
        :param params: query parameters to add to the request
        :return: response body as bytes
        :raise: IrmKmiApiError when communication with the API fails
        """
        r: bytes = await self._api_wrapper(base_url=url, params={} if params is None else params)
        return r

    async def get_svg(self, url, params: Dict[str, str] | None = None) -> str:
        """
        Get SVG as str at the specified url with the parameters

        :param url: URL to fetch
        :param params: query parameters to add to the request
        :return: request body decoded as utf-8 str
        :raise: IrmKmiApiError when communication with the API fails
        """
        r: bytes = await self._api_wrapper(base_url=url, params={} if params is None else params)
        return r.decode()

    def expire_cache(self) -> None:
        """
        Expire items from the cache which have not been accessed since self._cache_max_age (default 2h).
        Must be called regularly to clear the cache.
        """
        now = time.time()
        keys_to_delete = set()
        for key, value in self._cache.items():
            if now - value['timestamp'] > self._cache_max_age:
                keys_to_delete.add(key)
        for key in keys_to_delete:
            del self._cache[key]
        _LOGGER.info(f"Expired {len(keys_to_delete)} elements from API cache")

    async def _api_wrapper(
            self,
            params: dict,
            base_url: str | None = None,
            path: str = "",
            method: str = "get",
            data: dict | None = None,
            headers: dict | None = None,
    ) -> bytes:
        """Get information from the API."""
        url = f"{self._base_url if base_url is None else base_url}{path}"

        if headers is None:
            headers = {'User-Agent': self._user_agent}
        else:
            headers['User-Agent'] = self._user_agent

        if url in self._cache:
            headers['If-None-Match'] = self._cache[url]['etag']

        try:
            async with async_timeout.timeout(60):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params
                )
                response.raise_for_status()

                if response.status == 304:
                    _LOGGER.debug(f"Cache hit for {url}")
                    self._cache[url]['timestamp'] = time.time()
                    return self._cache[url]['response']

                if 'ETag' in response.headers:
                    _LOGGER.debug(f"Saving in cache {url}")
                    r = await response.read()
                    self._cache[url] = {'etag': response.headers['ETag'], 'response': r, 'timestamp': time.time()}
                    return r

                return await response.read()

        except asyncio.TimeoutError as exception:
            raise IrmKmiApiCommunicationError("Timeout error fetching information") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise IrmKmiApiCommunicationError("Error fetching information") from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise IrmKmiApiError(f"Something really wrong happened! {exception}") from exception

    @staticmethod
    def _api_key(method_name: str) -> str:
        """Get API key."""
        return hashlib.md5(f"r9EnW374jkJ9acc;{method_name};{datetime.now().strftime('%d/%m/%Y')}".encode()).hexdigest()


class IrmKmiApiClientHa(IrmKmiApiClient):
    """API client for IRM KMI weather data with additional methods to integrate easily with Home Assistant"""

    def __init__(self, session: aiohttp.ClientSession, user_agent: str, cdt_map: dict) -> None:
        super().__init__(session, user_agent)
        self._api_data = dict()
        self._cdt_map = cdt_map

    async def refresh_forecasts_coord(self, coord: Dict[str, float | int]) -> None:
        """
        Update the weather data by contacting the remote API.  Keep the data in memory for future methods calls.

        :param coord: dict with the following keys: 'lat', 'long' (both float or int)
        :raise: IrmKmiApiError when communication with the API fails
        """
        self._api_data = await self.get_forecasts_coord(coord)

    def get_current_weather(self, tz: ZoneInfo) -> CurrentWeatherData:
        """
        Parse the API data we currently have to build a CurrentWeatherData.

        :param tz: time zone to use to interpret the timestamps in the forecast (generally is Europe/Brussels)
        :return: current weather
        """

        now_hourly = self._get_now_hourly(tz)
        uv_index = self._get_uv_index()

        try:
            pressure = float(now_hourly.get('pressure', None)) if now_hourly is not None else None
        except (TypeError, ValueError):
            pressure = None

        try:
            wind_speed = float(now_hourly.get('windSpeedKm', None)) if now_hourly is not None else None
        except (TypeError, ValueError):
            wind_speed = None

        try:
            wind_gust_speed = float(now_hourly.get('windPeakSpeedKm', None)) if now_hourly is not None else None
        except (TypeError, ValueError):
            wind_gust_speed = None

        try:
            temperature = float(self._api_data.get('obs', {}).get('temp'))
        except (TypeError, ValueError):
            temperature = None

        try:
            dir_cardinal = now_hourly.get('windDirectionText', {}).get('en') if now_hourly is not None else None
            if dir_cardinal == 'VAR' or now_hourly is None:
                wind_bearing = None
            else:
                wind_bearing = (float(now_hourly.get('windDirection')) + 180) % 360
        except (TypeError, ValueError):
            wind_bearing = None

        current_weather = CurrentWeatherData(
            condition=self._cdt_map.get(
                (self._api_data.get('obs', {}).get('ww'), self._api_data.get('obs', {}).get('dayNight')), None),
            temperature=temperature,
            wind_speed=wind_speed,
            wind_gust_speed=wind_gust_speed,
            wind_bearing=wind_bearing,
            pressure=pressure,
            uv_index=uv_index
        )

        if self._api_data.get('country', '') == 'NL':
            current_weather['wind_speed'] = self._api_data.get('obs', {}).get('windSpeedKm')
            if self._api_data.get('obs', {}).get('windDirectionText', {}).get('en') == 'VAR':
                current_weather['wind_bearing'] = None
            else:
                try:
                    current_weather['wind_bearing'] = (float(
                        self._api_data.get('obs', {}).get('windDirection')) + 180) % 360
                except ValueError:
                    current_weather['wind_bearing'] = None

        # Since June 2024, the NL weather does not include the condition in the 'ww' key, so we get it from the current
        # hourly forecast instead if it is missing
        if current_weather['condition'] is None:
            try:
                current_weather['condition'] = self._cdt_map.get(
                    (int(now_hourly.get('ww')), now_hourly.get('dayNight')), None)
            except (TypeError, ValueError, AttributeError):
                current_weather['condition'] = None

        return current_weather

    def get_radar_forecast(self) -> List[IrmKmiRadarForecast]:
        """
        Create a list of short term forecasts for rain based on the data provided by the rain radar

        :return: chronologically ordered list of 'few'-minutes radar forecasts
        """
        data = self._api_data.get('animation', {})

        if not isinstance(data, dict):
            return []
        sequence = data.get("sequence", [])
        unit = data.get("unit", {}).get("en", None)
        ratios = [f['value'] / f['position'] for f in sequence if f['position'] > 0]

        if len(ratios) > 0:
            ratio = mean(ratios)
        else:
            ratio = 0

        forecast = list()
        for f in sequence:
            forecast.append(
                IrmKmiRadarForecast(
                    datetime=f.get("time"),
                    native_precipitation=f.get('value'),
                    rain_forecast_max=round(f.get('positionHigher') * ratio, 2),
                    rain_forecast_min=round(f.get('positionLower') * ratio, 2),
                    might_rain=f.get('positionHigher') > 0,
                    unit=unit
                )
            )
        return forecast

    def get_hourly_forecast(self, tz: ZoneInfo) -> List[Forecast]:
        """
        Parse data from the API to create a list of hourly forecasts

        :param tz: time zone to use to interpret the timestamps in the forecast (generally is Europe/Brussels)
        :return: chronologically ordered list of hourly forecasts
        """
        data = self._api_data.get('for', {}).get('hourly')

        if data is None or not isinstance(data, list) or len(data) == 0:
            return []

        forecasts = list()
        day = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)

        for idx, f in enumerate(data):
            if 'dateShow' in f and idx > 0:
                day = day + timedelta(days=1)

            hour = f.get('hour', None)
            if hour is None:
                continue
            day = day.replace(hour=int(hour))

            precipitation_probability = None
            if f.get('precipChance', None) is not None:
                precipitation_probability = int(f.get('precipChance'))

            ww = None
            if f.get('ww', None) is not None:
                ww = int(f.get('ww'))

            wind_bearing = None
            if f.get('windDirectionText', {}).get('en') != 'VAR':
                try:
                    wind_bearing = (float(f.get('windDirection')) + 180) % 360
                except (TypeError, ValueError):
                    pass

            forecast = Forecast(
                datetime=day.isoformat(),
                condition=self._cdt_map.get((ww, f.get('dayNight', None)), None),
                native_precipitation=f.get('precipQuantity', None),
                native_temperature=f.get('temp', None),
                native_templow=None,
                native_wind_gust_speed=f.get('windPeakSpeedKm', None),
                native_wind_speed=f.get('windSpeedKm', None),
                precipitation_probability=precipitation_probability,
                wind_bearing=wind_bearing,
                native_pressure=f.get('pressure', None),
                is_daytime=f.get('dayNight', None) == 'd'
            )

            forecasts.append(forecast)

        return forecasts

    def get_daily_forecast(self, tz: ZoneInfo, lang: str) -> List[IrmKmiForecast]:
        """
        Parse the API data we currently have to build the daily forecast list.

        :param tz: time zone to use to interpret the timestamps in the forecast (generally is Europe/Brussels)
        :param lang: langage to get data for (must be 'fr', 'nl', 'de' or 'en')
        :return: chronologically ordered list of daily forecasts
        """
        data = self._api_data.get('for', {}).get('daily')
        if data is None or not isinstance(data, list) or len(data) == 0:
            return []

        forecasts = list()
        forecast_day = datetime.now(tz)

        for (idx, f) in enumerate(data):
            precipitation = None
            if f.get('precipQuantity', None) is not None:
                try:
                    precipitation = float(f.get('precipQuantity'))
                except (TypeError, ValueError):
                    pass

            native_wind_gust_speed = None
            if f.get('wind', {}).get('peakSpeed') is not None:
                try:
                    native_wind_gust_speed = int(f.get('wind', {}).get('peakSpeed'))
                except (TypeError, ValueError):
                    pass

            wind_bearing = None
            if f.get('wind', {}).get('dirText', {}).get('en') != 'VAR':
                try:
                    wind_bearing = (float(f.get('wind', {}).get('dir')) + 180) % 360
                except (TypeError, ValueError):
                    pass

            is_daytime = f.get('dayNight', None) == 'd'

            day_name = f.get('dayName', {}).get('en', None)
            timestamp = f.get('timestamp', None)
            if timestamp is not None:
                forecast_day = datetime.fromisoformat(timestamp)
            elif day_name in WEEKDAYS:
                forecast_day = self._next_weekday(forecast_day, WEEKDAYS.index(day_name))
            elif day_name in ['Today', 'Tonight']:
                forecast_day = datetime.now(tz)
            elif day_name == 'Tomorrow':
                forecast_day = datetime.now(tz) + timedelta(days=1)

            sunrise_sec = f.get('dawnRiseSeconds', None)
            if sunrise_sec is None:
                sunrise_sec = f.get('sunRise', None)
            sunrise = None
            if sunrise_sec is not None:
                try:
                    sunrise = (forecast_day.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
                               + timedelta(seconds=float(sunrise_sec)))
                except (TypeError, ValueError):
                    pass

            sunset_sec = f.get('dawnSetSeconds', None)
            if sunset_sec is None:
                sunset_sec = f.get('sunSet', None)
            sunset = None
            if sunset_sec is not None:
                try:
                    sunset = (forecast_day.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
                              + timedelta(seconds=float(sunset_sec)))
                except (TypeError, ValueError):
                    pass

            forecast = IrmKmiForecast(
                datetime=(forecast_day.strftime('%Y-%m-%d')),
                condition=self._cdt_map.get((f.get('ww1', None), f.get('dayNight', None)), None),
                condition_2=self._cdt_map.get((f.get('ww2', None), f.get('dayNight', None)), None),
                condition_evol=WWEVOL_TO_ENUM_MAP.get(f.get('wwevol'), None),
                native_precipitation=precipitation,
                native_temperature=f.get('tempMax', None),
                native_templow=f.get('tempMin', None),
                native_wind_gust_speed=native_wind_gust_speed,
                native_wind_speed=f.get('wind', {}).get('speed'),
                precipitation_probability=f.get('precipChance', None),
                wind_bearing=wind_bearing,
                is_daytime=is_daytime,
                text=f.get('text', {}).get(lang, ""),
                sunrise=sunrise.isoformat() if sunrise is not None else None,
                sunset=sunset.isoformat() if sunset is not None else None
            )
            # Swap temperature and templow if needed
            if (forecast['native_templow'] is not None
                    and forecast['native_temperature'] is not None
                    and forecast['native_templow'] > forecast['native_temperature']):
                (forecast['native_templow'], forecast['native_temperature']) = \
                    (forecast['native_temperature'], forecast['native_templow'])

            forecasts.append(forecast)

        return forecasts

    def get_animation_data(self, tz: ZoneInfo, lang: str, style: str, dark_mode: bool) -> RadarAnimationData:
        """
        Get all the image URLs and create the radar animation data object.

        :param tz: time zone to use to interpret the timestamps in the forecast (generally is Europe/Brussels)
        :param lang: langage to get data for (must be 'fr', 'nl', 'de' or 'en')
        :param style: style of the radar (key of STYLE_TO_PARAM_MAP)
        :param dark_mode: true if dark mode
        :return: animation data that can be used to download the images and build the rain graph animation
        """
        animation_data = self._api_data.get('animation', {}).get('sequence')
        localisation_layer_url = self._api_data.get('animation', {}).get('localisationLayer')
        country = self.get_country()

        if animation_data is None or localisation_layer_url is None or not isinstance(animation_data, list):
            raise ValueError("Cannot create animation data")

        localisation = self._merge_url_and_params(localisation_layer_url,
                                                  {'th': 'd' if country == 'NL' or not dark_mode else 'n'})
        images_from_api = [self._merge_url_and_params(frame.get('uri'), {'rs': STYLE_TO_PARAM_MAP[style]})
                           for frame in animation_data if frame is not None and frame.get('uri') is not None
                           ]

        radar_animation = RadarAnimationData(
            hint=self._api_data.get('animation', {}).get('sequenceHint', {}).get(lang),
            unit=self._api_data.get('animation', {}).get('unit', {}).get(lang),
            location=localisation
        )

        sequence: List[AnimationFrameData] = list()

        current_time = datetime.now(tz)
        most_recent_frame = None

        for idx, item in enumerate(animation_data):
            frame = AnimationFrameData(
                image=images_from_api[idx],
                time=datetime.fromisoformat(item.get('time')) if item.get('time', None) is not None else None,
                value=item.get('value', 0),
                position=item.get('position', 0),
                position_lower=item.get('positionLower', 0),
                position_higher=item.get('positionHigher', 0)
            )
            sequence.append(frame)

            if most_recent_frame is None and current_time < frame['time']:
                most_recent_frame = idx - 1 if idx > 0 else idx

        radar_animation['sequence'] = sequence
        radar_animation['most_recent_image_idx'] = most_recent_frame

        return radar_animation

    def get_warnings(self, lang: str) -> List[WarningData]:
        """
        Parse the API data we currently have to build the list of warnings.

        :param lang: langage to get data for (must be 'fr', 'nl', 'de' or 'en')
        :return: unordered list of warnings
        """
        warning_data = self._api_data.get('for', {}).get('warning')
        if warning_data is None or not isinstance(warning_data, list) or len(warning_data) == 0:
            return []

        result = list()
        for data in warning_data:
            try:
                warning_id = int(data.get('warningType', {}).get('id'))
                start = datetime.fromisoformat(data.get('fromTimestamp', None))
                end = datetime.fromisoformat(data.get('toTimestamp', None))
            except (TypeError, ValueError):
                # Without this data, the warning is useless
                continue

            try:
                level = int(data.get('warningLevel'))
            except TypeError:
                level = None

            result.append(
                WarningData(
                    slug=SLUG_MAP.get(warning_id, 'unknown'),
                    id=warning_id,
                    level=level,
                    friendly_name=data.get('warningType', {}).get('name', {}).get(lang, ''),
                    text=data.get('text', {}).get(lang, ''),
                    starts_at=start,
                    ends_at=end
                )
            )

        return result if len(result) > 0 else []

    async def get_pollen(self) -> Dict[str, str | None]:
        """
        Get SVG pollen info from the API, return the pollen data dict

        :return: pollen data as dict mapping from pollen name to pollen level as a color
        :raise: IrmKmiApiError when communication with the API fails
        """
        _LOGGER.debug("Getting pollen data from API")
        svg_url = None
        for module in self._api_data.get('module', []):
            _LOGGER.debug(f"module: {module}")
            if module.get('type', None) == 'svg':
                url = module.get('data', {}).get('url', {}).get('en', '')
                if 'pollen' in url:
                    svg_url = url
                    break
        if svg_url is None:
            return PollenParser.get_default_data()

        try:
            _LOGGER.debug(f"Requesting pollen SVG at url {svg_url}")
            pollen_svg: str = await self.get_svg(svg_url)
        except IrmKmiApiError as err:
            raise err

        return PollenParser(pollen_svg).get_pollen_data()

    def get_city(self) -> str | None:
        """
        Get the city for which we currently have the forecast

        :return: city name as str or None if unavailable
        """
        return self._api_data.get('cityName', None)

    def get_country(self) -> str | None:
        """
        Get the two-letters country code for which we currently have the forecast

        :return: country code as str or None if unavailable
        """
        return self._api_data.get('country', None)

    def _get_uv_index(self) -> float | None:
        uv_index = None
        module_data = self._api_data.get('module', None)
        if not (module_data is None or not isinstance(module_data, list)):
            for module in module_data:
                if module.get('type', None) == 'uv':
                    uv_index = module.get('data', {}).get('levelValue')
        return uv_index

    def _get_now_hourly(self, tz: ZoneInfo) -> dict | None:
        now_hourly = None
        hourly_forecast_data = self._api_data.get('for', {}).get('hourly')
        now = datetime.now(tz)
        if not (hourly_forecast_data is None
                or not isinstance(hourly_forecast_data, list)
                or len(hourly_forecast_data) == 0):

            for current in hourly_forecast_data[:4]:
                if now.strftime('%H') == current['hour']:
                    now_hourly = current
                    break
        return now_hourly

    @staticmethod
    def _merge_url_and_params(url: str, params: dict) -> str:
        """Merge query string params in the URL"""
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params.update(params)
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        new_url = parsed_url._replace(query=new_query)
        return str(urllib.parse.urlunparse(new_url))

    @staticmethod
    def _next_weekday(current, weekday):
        days_ahead = weekday - current.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return current + timedelta(days_ahead)
