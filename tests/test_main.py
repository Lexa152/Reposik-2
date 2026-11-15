import pytest

import main
from main import user_interaction
from src.air import Aircraft


# вспомогательные моки

def sample_flights():
    return [
        {"lat": 50.0, "lon": 10.0, "alt": 9000, "vel": 800.0, "gov": "France",
         "callsign": "AFR123", "icao24": "abc123"},
        {"lat": 48.0, "lon": 2.0, "alt": 11000, "vel": 900.0, "gov": "Germany",
         "callsign": "DLH456", "icao24": "def456"},
        {"lat": 41.0, "lon": -3.0, "alt": 10000, "vel": 750.0, "gov": "Spain",
         "callsign": "IBE789", "icao24": "ghi789"},
    ]


def set_inputs(monkeypatch, answers):
    """input()"""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def patch_api(monkeypatch, flights=None):
    """все функции из src.api"""
    atlas = [
        {"name_ru": "Франция", "name_en": "France"},
        {"name_ru": "Испания", "name_en": "Spain"},
    ]
    bounds = {"юг": 41.0, "север": 52.0, "запад": -5.5, "восток": 9.5}
    flights = sample_flights() if flights is None else flights

    monkeypatch.setattr(main, "fetch_countries", lambda: atlas)
    monkeypatch.setattr(main, "get_country_bounds", lambda name: bounds)

    calls = {}

    def fake_get_flights(countries_list, lon_min, lon_max, lat_min, lat_max,
                         alt_min, alt_max):
        calls["args"] = dict(
            countries_list=list(countries_list),
            lon_min=lon_min, lon_max=lon_max,
            lat_min=lat_min, lat_max=lat_max,
            alt_min=alt_min, alt_max=alt_max,
        )
        return flights

    monkeypatch.setattr(main, "get_flights", fake_get_flights)
    monkeypatch.setattr(main, "save_to_json", lambda f, **kw: "saved.json")
    return calls


def test_full_run_happy_path(monkeypatch, capsys):
    calls = patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "5", "1000", "12000", "по скорости"])

    user_interaction()

    out = capsys.readouterr().out
    assert "К сведению принято: France" in out
    assert "Количество самолётов для вывода на экран: 5 шт." in out
    assert "Общее количество самолётов: 3 штук" in out
    assert "Топ N позиций" in out

    # в get_flights корректные границы
    a = calls["args"]
    assert a["countries_list"] == []      # "всё" — без ограничения по странам
    assert a["lat_min"] == -5.5 and a["lat_max"] == 9.5
    assert a["lon_min"] == 41.0 and a["lon_max"] == 52.0
    assert a["alt_min"] == 1000 and a["alt_max"] == 12000


def test_objects_created_in_aircraft_list(monkeypatch):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "2", "1000", "12000", "по скорости"])

    user_interaction()

    assert len(Aircraft.aircraft_list) == 2  # top_n = 2
    assert all(isinstance(a, Aircraft) for a in Aircraft.aircraft_list)


# сортировка

def test_sort_by_velocity_desc(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "3", "1000", "12000", "по скорости"])

    user_interaction()

    vels = [a.vel for a in Aircraft.aircraft_list]
    assert vels == sorted(vels, reverse=True)
    assert vels == [900.0, 800.0, 750.0]


def test_sort_by_altitude_desc(monkeypatch):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "3", "1000", "12000", "по высоте"])

    user_interaction()

    alts = [a.alt for a in Aircraft.aircraft_list]
    assert alts == sorted(alts, reverse=True)
    assert alts == [11000, 10000, 9000]


# фильтр по странам регистрации

def test_countries_filter_passed_to_get_flights(monkeypatch):
    calls = patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "Франция", "Испания", "всё",
                             "3", "1000", "12000", "по скорости"])

    user_interaction()

    assert calls["args"]["countries_list"] == ["France", "Spain"]


# некорректный ввод

def test_invalid_country_repeats_prompt(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["блабла", "Франция", "всё",
                             "3", "1000", "12000", "по скорости"])

    user_interaction()

    out = capsys.readouterr().out
    assert "такая страна - странна" in out
    assert "К сведению принято: France" in out


def test_invalid_numbers_then_valid(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, [
        "Франция", "всё",
        "-1", "abc", "3",          # top_n: отрицательное, не число, норм
        "0", "1000",               # alt_min: ноль, норм
        "500", "abc", "12000",     # alt_max: меньше нижней, не число, норм
        "по скорости",
    ])

    user_interaction()

    out = capsys.readouterr().out
    assert "Число должно быть больше нуля" in out
    assert "Ошибка: введите именно целое число" in out
    assert "Верхняя граница высот должна быть выше нижней" in out
    assert "К сведению принято: 12000" in out


def test_invalid_sort_param_repeats(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "3", "1000", "12000",
                             "по скорости ", "по скорости"])

    user_interaction()

    out = capsys.readouterr().out
    assert "К сведению принято: по скорости" in out


# выход по "стоп"

def test_stop_at_first_prompt_exits(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["стоп"])

    with pytest.raises(SystemExit):
        user_interaction()

    assert "Работа завершена" in capsys.readouterr().out


def test_stop_at_top_n_exits(monkeypatch, capsys):
    patch_api(monkeypatch)
    set_inputs(monkeypatch, ["Франция", "всё", "стоп"])

    with pytest.raises(SystemExit):
        user_interaction()

    out = capsys.readouterr().out
    assert "К сведению принято: France" in out  # дошли до третьего шага
    assert "Работа завершена" in out


# пустой результат

def test_empty_flights(monkeypatch, capsys):
    patch_api(monkeypatch, flights=[])
    set_inputs(monkeypatch, ["Франция", "всё", "5", "1000", "12000", "по скорости"])

    user_interaction()

    out = capsys.readouterr().out
    assert "Общее количество самолётов: 0 штук" in out
