import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from src.air import Aircraft

DATA_DIR = Path(__file__).parent / "data"

def fetch_countries() -> list[dict]:
    """Возвращает список стран. Если кэш есть — читает его,
    иначе скачивает данные, сохраняет в data/countries.json и возвращает."""

    DATA_URLS = [
        "https://raw.githubusercontent.com/mledoze/countries/master/countries.json",
        "https://cdn.jsdelivr.net/npm/world-countries@master/countries.json",
    ]
    CACHE_FILE = DATA_DIR / "countries.json"
    if CACHE_FILE.exists():
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)

    response = None
    for url in DATA_URLS:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            response = r
            break
        except requests.RequestException:
            continue

    if response is None:
        raise RuntimeError("скачать список стран не удалось")

    countries = response.json()

    rows = []
    for country in countries:
        name_en = country.get("name", {}).get("common", "")
        name_ru = country.get("translations", {}).get("rus", {}).get("common", "")
        if name_en:
            rows.append({
                "name_ru": name_ru if name_ru else "nu",
                "name_en": name_en if name_en else "nu",
            })

    rows.sort(key=lambda x: x["name_ru"])

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    return rows


def get_country_bounds(country_name: str) -> dict:
    """
    координаты крайних точек страны по её названию.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": country_name,
        "format": "json",
        "limit": 1,
        "countrycodes": ""
    }
    headers = {"User-Agent": "flights-by-lon-alt/1.0"}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"Страна «{country_name}» не найдена")
    else:
        bbox = data[0]["boundingbox"]
        return {
            "юг": float(bbox[0]),
            "север": float(bbox[1]),
            "запад": float(bbox[2]),
            "восток": float(bbox[3]),
        }


def get_flights(
    countries_list: Optional[List[str]] = None,
    lon_min: Optional[float] = None,
    lon_max: Optional[float] = None,
    lat_min: Optional[float] = None,
    lat_max: Optional[float] = None,
    alt_min: Optional[int] = None,
    alt_max: Optional[int] = None
) -> List[Dict]:
    """
    Возвращает самолёты в заданной зоне и диапазоне высот.
    Если границы не заданы (None), ограничение по этому параметру не применяется.
    """
    URL = "https://opensky-network.org/api/states/all"
    FIELDS = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude",
        "squawk", "spi", "position_source"
    ]

    params = {}
    # Добавляем только те границы, которые реально заданы
    if lon_min is not None:
        params["lomin"] = lon_min
    if lon_max is not None:
        params["lomax"] = lon_max
    if lat_min is not None:
        params["lamin"] = lat_min
    if lat_max is not None:
        params["lamax"] = lat_max

    headers = {
        "User-Agent": "my-flight-tracker/1.0 (contact@example.com)"  # обязательно уникальный
    }

    r = requests.get(URL, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()

    states = data.get("states") or []

    aircraft_list = []
    result = []

    for s in states:
        flight = dict(zip(FIELDS, s))

        lon = flight.get("longitude")
        lat = flight.get("latitude")
        alt = flight.get("geo_altitude")
        gov = flight.get("origin_country")
        vel = flight.get("velocity")

        # Пропускаем, если нет координат или высоты
        if lon is None or lat is None or alt is None:
            continue

        # Фильтрация по долготе
        if lon_min is not None and lon < lon_min:
            continue
        if lon_max is not None and lon > lon_max:
            continue

        # Фильтрация по широте
        if lat_min is not None and lat < lat_min:
            continue
        if lat_max is not None and lat > lat_max:
            continue

        # Фильтрация по высоте
        if alt_min is not None and alt < alt_min:
            continue
        if alt_max is not None and alt > alt_max:
            continue

        # Опционально: фильтрация по странам
        if countries_list and gov not in countries_list:
            continue

        result.append({
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "vel": vel,
            "gov": gov,
            "callsign": flight.get("callsign"),
            "icao24": flight.get("icao24")
        })

    return result


def save_to_json(flights: list[dict], data_dir: str = DATA_DIR) -> str:
    """
    данные в один файл flights_latest.json
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, "flights_latest.json")

    payload = {
        "count": len(flights),
        "flights": flights,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return filepath
