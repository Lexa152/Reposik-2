import pytest
import json
import os
import requests
from src import api


class FakeResponse:
    """мок ответа requests"""
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._payload


def make_country(name_en="France", name_ru="Франция"):
    return {
        "name": {"common": name_en},
        "translations": {"rus": {"common": name_ru}},
    }


def make_state(lon=10.0, lat=50.0, alt=9000, vel=800.0, gov="France"):
    return [
        "abc123",          # icao24
        "AFR123",          # callsign
        gov,               # origin_country
        1700000000,        # time_position
        1700000100,        # last_contact
        lon, lat,
        8500.0,            # baro_altitude
        False,             # on_ground
        vel,               # velocity
        90.0,              # true_track
        0.0,               # vertical_rate
        None,              # sensors
        alt,               # geo_altitude
        "1234",            # squawk
        False,             # spi
        0,                 # position_source
    ]


def test_fetch_countries_reads_cache(tmp_path, monkeypatch):
    cache = tmp_path / "countries.json"
    rows = [{"name_ru": "Тест", "name_en": "Test"}]
    cache.write_text(json.dumps(rows), encoding="utf-8")

    monkeypatch.setattr(api, "DATA_DIR", tmp_path)

    def fail_get(*args, **kwargs):
        raise AssertionError("requests.get не должен вызываться при наличии кэша")
    monkeypatch.setattr(api.requests, "get", fail_get)

    assert api.fetch_countries() == rows


def test_fetch_countries_downloads_and_saves(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "DATA_DIR", tmp_path)

    def fake_get(url, **kwargs):
        return FakeResponse([make_country("Spain", "Испания"),
                             make_country("France", "Франция")])
    monkeypatch.setattr(api.requests, "get", fake_get)

    rows = api.fetch_countries()

    assert rows == [
        {"name_ru": "Испания", "name_en": "Spain"},
        {"name_ru": "Франция", "name_en": "France"},
    ]  # отсортированы по name_ru
    assert (tmp_path / "countries.json").exists()  # кэш записан


def test_fetch_countries_raises_when_all_urls_fail(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "DATA_DIR", tmp_path)

    def fake_get(url, **kwargs):
        raise requests.ConnectionError("нет сети")
    monkeypatch.setattr(api.requests, "get", fake_get)

    with pytest.raises(RuntimeError):
        api.fetch_countries()


# get_country_bounds

def test_get_country_bounds_parses_bbox(monkeypatch):
    data = [{"boundingbox": ["41.0", "52.0", "-5.5", "9.5"]}]
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse(data))

    bounds = api.get_country_bounds("Франция")

    assert bounds == {"юг": 41.0, "север": 52.0, "запад": -5.5, "восток": 9.5}
    assert all(isinstance(v, float) for v in bounds.values())


def test_get_country_bounds_empty_result_raises(monkeypatch):
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse([]))

    with pytest.raises(ValueError, match="не найдена"):
        api.get_country_bounds("НесуществующаяСтрана")


def test_get_country_bounds_http_error(monkeypatch):
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse([], status_code=400))

    with pytest.raises(requests.HTTPError):
        api.get_country_bounds("Франция")


# get_flights

def test_get_flights_filters_by_bounds_and_altitude(monkeypatch):
    states = [
        make_state(lon=10.0, lat=50.0, alt=9000),    # внутри
        make_state(lon=100.0, lat=50.0, alt=9000),   # вне по долготе
        make_state(lon=10.0, lat=5.0, alt=9000),     # вне по широте
        make_state(lon=10.0, lat=50.0, alt=30000),   # вне по высоте
        make_state(lon=None, lat=50.0, alt=9000),    # нет координат
    ]
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse({"states": states}))

    flights = api.get_flights(lon_min=0, lon_max=20,
                              lat_min=40, lat_max=60,
                              alt_min=1000, alt_max=20000)

    assert len(flights) == 1
    f = flights[0]
    assert f["lon"] == 10.0
    assert f["lat"] == 50.0
    assert f["alt"] == 9000
    assert f["gov"] == "France"
    assert f["callsign"] == "AFR123"


def test_get_flights_no_bounds_returns_all_with_data(monkeypatch):
    states = [make_state(), make_state(lon=0, lat=0, alt=0)]
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse({"states": states}))

    flights = api.get_flights()

    assert len(flights) == 2
    # параметры запроса должны быть пустыми, если границы не заданы
    captured = {}
    def capture(url, params=None, **kw):
        captured["params"] = params
        return FakeResponse({"states": states})
    monkeypatch.setattr(api.requests, "get", capture)
    api.get_flights()
    assert captured["params"] == {}


def test_get_flights_country_filter(monkeypatch):
    states = [
        make_state(gov="France"),
        make_state(gov="Spain"),
    ]
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse({"states": states}))

    flights = api.get_flights(countries_list=["Spain"])
    assert [f["gov"] for f in flights] == ["Spain"]


def test_get_flights_empty_states(monkeypatch):
    monkeypatch.setattr(api.requests, "get",
                        lambda *a, **kw: FakeResponse({"states": None}))

    assert api.get_flights() == []


# save_to_json

def test_save_to_json_writes_file(tmp_path):
    flights = [{"lat": 50.0, "lon": 10.0, "alt": 9000,
                "vel": 800.0, "gov": "France"}]

    filepath = api.save_to_json(flights, data_dir=str(tmp_path))

    assert os.path.exists(filepath)
    with open(filepath, encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["count"] == 1
    assert payload["flights"] == flights


def test_save_to_json_empty_list(tmp_path):
    filepath = api.save_to_json([], data_dir=str(tmp_path))

    with open(filepath, encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["count"] == 0
    assert payload["flights"] == []