from datetime import datetime

from freezegun import freeze_time

from tests.conftest import get_api_with_data


@freeze_time(datetime.fromisoformat('2024-01-12T07:10:00+00:00'))
async def test_warning_data() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    result = api.get_warnings(lang='en')

    assert isinstance(result, list)
    assert len(result) == 2

    first = result[0]
    assert first.get('starts_at').replace(tzinfo=None) < datetime.now()
    assert first.get('ends_at').replace(tzinfo=None) > datetime.now()

    assert first.get('slug') == 'fog'
    assert first.get('friendly_name') == 'Fog'
    assert first.get('id') == 7
    assert first.get('level') == 1

async def test_warning_heat() -> None:
    api = get_api_with_data("antwerp_with_heat_warning.json")

    result = api.get_warnings(lang='en')

    assert isinstance(result, list)
    assert len(result) == 1

    first = result[0]

    assert first.get('slug') == 'heat'
    assert first.get('friendly_name') == 'Heat'
    assert first.get('id') == 10
    assert first.get('level') == 1