import json
from datetime import datetime, time, timedelta


def cashback(data, year: datetime.year, month: datetime.month):
    ''' получение данных для анализа выгодности категории cashback '''
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    time_from = datetime(year, month, 1, 0, 0, 0)
    if 1 <= month + 1 <= 12:
        time_to = datetime(year, month + 1, 1, 0, 0, 0)
    else:
        time_to = datetime(year + 1, 1, 1, 0, 0, 0)

    spis_kat = []
    wok_kats = {}
    for i in range(0, len(data)):
        data0 = data[i]
        if data0['my_datatime_tranza'] is None or not isinstance(data0['my_datatime_tranza'], datetime):
            data0['my_datatime_tranza'] = datetime(1940, 1, 1, 0, 0, 0)

        if time_from <= data0['my_datatime_tranza'] < time_to:
            if (data0['my_category'] is None) or (data0['my_category'] == ''):
                kat_name = 'Остальное'
            else:
                kat_name = data0['my_category']

            if kat_name not in spis_kat:
                spis_kat.append(kat_name)
                wok_kats[kat_name] = 0

            # "my_kash_bak"
            if (data0['my_kash_bak'] is not None):
                wok_kats[kat_name] += float(data0['my_kash_bak'])
            else:
                if (data0['my_tranz_summa'] is None) or (data0['my_tranz_summa'] > 0):
                    amount = 0
                else:
                    amount = -1 * float(data0['my_tranz_summa']) / 100
                wok_kats[kat_name] += amount

    sorted_keys = sorted(wok_kats, key=wok_kats.get, reverse=True)
    wok_kats_s = {}

    i = 1
    for ik in sorted_keys:
        if i < 8:
            wok_kats_s[ik] = round(wok_kats[ik], 2)
        elif i == 8:
            wok_kats_s['Остальное'] = round(wok_kats[ik], 2)
        else:
            wok_kats_s['Остальное'] = round((wok_kats_s['Остальное'] + wok_kats[ik]), 2)
        i += 1

    return json.dumps(wok_kats_s)
