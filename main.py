from datetime import datetime

from src.input_data import readln_setting, readln_xlsx, filter_by_state, sort_by_date, sort_by_number
from src.views import torg_news, money
from src.times import time_and_range
from src.services import cashback
from src.reports import spending_by_category

# читаю настройки из файла настроек:
setting = readln_setting()
file_xlsx = setting['file_name'] # txt
https_moneys = setting['currencies_from'] # txt js
https_wrappers = setting['fantiki_from'] # txt json
my_currencies = setting['user_currencies'] # ["USD", "EUR"]
my_wrappers = setting['user_stocks'] # ["ABRD", "AFLT", "BRZL", "DIOD", "DOMRF"]


def main_data_viewer(current_datetime: datetime | None = None):
    ''' Формирование итогового словаря по задаче Главная из категории Веб '''
    if current_datetime is None:
        current_datetime = datetime.now()

    time_from = datetime(current_datetime.year, current_datetime.month, 1, 0, 0, 0)
    if 1 <= current_datetime.month + 1 <= 12:
        time_to = datetime(current_datetime.year, current_datetime.month + 1, 1, 0, 0, 0)
    else:
        time_to = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0)

    wok0 = readln_xlsx(file_xlsx, time_from, time_to)
    wok0 = filter_by_state(wok0, state="OK")
    wok0 = sort_by_date(wok0, reverse=True)
    wok0 = sort_by_number(wok0, 'my_tranz_summa', reverse=False)

    spis_top_tranz = []
    spis_card_nums = []
    card_nums_and_amount = {}
    card_nums_and_kashbk = {}
    for i in range(0, len(wok0)):
        wok_i = wok0[i]
        time_print = wok_i['my_datatime_tranza'].strftime("%d.%m.%Y")
        stat_print = wok_i['my_oknotok']
        kat_name = wok_i['my_category']
        kard_num = str(wok_i['my_number_card'])
        if len(kard_num) > 4:
            kard_num = kard_num[-4:]
        amount = wok_i['my_tranz_summa']
        if (amount is None) or (amount > 0):
            amount = 0
        else:
            amount = -1 * amount
        kashbk = wok_i['my_kash_bak']
        if kashbk is None:
            kashbk = amount / 100
        # zad 3
        if i <= 4:
            spis_top_tranz.append({'date': str(time_print), 'amount': round(amount, 2), 'category': str(kat_name), 'description': str(wok_i['my_info'])})
        # zad 2
        if kard_num not in spis_card_nums:
            spis_card_nums.append(kard_num)
            card_nums_and_amount[kard_num] = amount
            card_nums_and_kashbk[kard_num] = kashbk
        else:
            card_nums_and_amount[kard_num] = card_nums_and_amount[kard_num] + amount
            card_nums_and_kashbk[kard_num] = card_nums_and_kashbk[kard_num] + kashbk

    spis_card_alldata = []
    for i in spis_card_nums:
        spis_card_alldata.append({'last_digits': i, 'total_spent': round(card_nums_and_amount[i], 2), 'cashback': round(card_nums_and_kashbk[i], 2)})

    currency_rates = []
    money0 = money(https_moneys, my_currencies)
    for i in my_currencies:
        currency_rates.append({"currency": i, "rate": money0[i]})

    stock_prices = []
    stock0 = torg_news(https_wrappers, my_wrappers)
    for i in stock0:
        stock_prices.append({'stock': i['ticker'], 'price': i['price']})

    main_data_wok = {}
    main_data_wok['greeting'] = time_and_range(current_datetime)
    main_data_wok['cards'] = spis_card_alldata
    main_data_wok['top_transactions'] = spis_top_tranz
    main_data_wok['currency_rates'] = currency_rates
    main_data_wok['stock_prices'] = stock_prices

    return main_data_wok
