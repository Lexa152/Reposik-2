import requests
from decimal import InvalidOperation


def torg_news(www_torg, torg_list):
    """ Стоимость акций """
    r_torg = requests.get(www_torg)
    data_torg = r_torg.json()

    # Создаем словарь: тикер -> краткое название
    securities_map = {}
    for row in data_torg["securities"]["data"]:
        if row[0] in torg_list: # torg_list - список акций их словаря настроек
            secid = row[0]
            shortname = row[2]
            securities_map[secid] = shortname

    # Собираем пары: название цена
    result = []
    for row in data_torg["marketdata"]["data"]:
        secid = row[0]          # SECID
        last_price = str(row[12])     # LAST (текущая цена)
        if secid in securities_map:
            name = securities_map[secid]
            result.append({"name": name, "ticker": secid, "price": round(float(last_price), 2)})

    return result


def money(https_wrappers, my_wrappers):
    """ Получает курсы валют и возвращает словарьwww_money, money_list """
    try:
        resp = requests.get(https_wrappers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

    except (requests.RequestException, ValueError, Exception):
        return None

    rates = {}
    valutes = data.get("Valute", {})

    for v in valutes.values():
        char_code = v.get("CharCode")
        if char_code in my_wrappers: # ("USD", "EUR"):
            try:
                rates[char_code] = float(str(v["Value"]))
            except (TypeError, ValueError, InvalidOperation):
                continue
    return rates
