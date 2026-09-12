from datetime import datetime
from typing import Optional
import json
from functools import wraps


def save_last_result(filename: str = "last_spending_result.json"):
    """ Сохраняет последний результат функции в JSON-файл """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result
        return wrapper
    return decorator


@save_last_result("last_spending_result.json")
def spending_by_category(data: [], category: str, report_date: Optional[str] = None) -> {}:
    ''' подсчёт сумм затрат по категориям за 3 месяца от даты '''
    if report_date is None:
        report_date_d = datetime.now()
    else:
        report_date_d = None
        try:
            report_date_d = datetime.strptime(report_date, "%Y-%m-%d")
        except ValueError as e:
            pass
        try:
            report_date_d = datetime.strptime(report_date, "%d-%m-%Y")
        except ValueError as e:
            pass

    if (int(report_date_d.month) - 2) < 1:
        datatime11 = datetime(report_date_d.year - 1, (int(report_date_d.month) - 2 + 12), 1, 0, 0, 0)
    else:
        datatime11 = datetime(report_date_d.year - 0, (int(report_date_d.month) - 2 +  0), 1, 0, 0, 0)

    if (int(report_date_d.month) - 1) < 1:
        datatime21 = datetime(report_date_d.year - 1, (int(report_date_d.month) - 1 + 12), 1, 0, 0, 0)
    else:
        datatime21 = datetime(report_date_d.year - 0, (int(report_date_d.month) - 1 +  0), 1, 0, 0, 0)

    datatime31 = datetime(report_date_d.year - 0, (int(report_date_d.month) - 0 +  0), 1, 0, 0, 0)

    if (int(report_date_d.month) + 1) > 12:
        datatime32 = datetime(report_date_d.year + 1, 1, 1, 0, 0, 0)
    else:
        datatime32 = datetime(report_date_d.year + 0, (int(report_date_d.month) + 1), 1, 0, 0, 0)

    datatime22 = datetime(report_date_d.year, int(report_date_d.month), 1, 0, 0, 0)

    if (int(report_date_d.month) - 1) < 1:
        datatime12 = datetime(report_date_d.year - 1, (int(report_date_d.month) - 1 + 12), 1, 0, 0, 0)
    else:
        datatime12 = datetime(report_date_d.year - 0, (int(report_date_d.month) - 1 + 0), 1, 0, 0, 0)

    wok_month = {}
    wok_month[datatime11.strftime("%Y-%m")] = 0
    wok_month[datatime21.strftime("%Y-%m")] = 0
    wok_month[datatime31.strftime("%Y-%m")] = 0
    wok_month['Всего'] = 0

    for i in range(0, len(data)):
        data0 = data[i]
        if (data0['my_category'] == category):
            if data0['my_datatime_tranza'] is None or not isinstance(data0['my_datatime_tranza'], datetime):
                data0['my_datatime_tranza'] = datetime(1940, 1, 1, 0, 0, 0)

            if (datatime11 <= data0['my_datatime_tranza'] < datatime12):
                if (data0['my_tranz_summa'] is None) or (data0['my_tranz_summa'] > 0):
                    amount = 0
                else:
                    amount = -1 * data0['my_tranz_summa']
                wok_month[datatime11.strftime("%Y-%m")] += amount
            elif (datatime21 <= data0['my_datatime_tranza'] < datatime22):
                if (data0['my_tranz_summa'] is None) or (data0['my_tranz_summa'] > 0):
                    amount = 0
                else:
                    amount = -1 * data0['my_tranz_summa']
                wok_month[datatime21.strftime("%Y-%m")] += amount
            elif (datatime31 <= data0['my_datatime_tranza'] < datatime32):
                if (data0['my_tranz_summa'] is None) or (data0['my_tranz_summa'] > 0):
                    amount = 0
                else:
                    amount = -1 * data0['my_tranz_summa']
                wok_month[datatime31.strftime("%Y-%m")] += amount

    wok_month[datatime11.strftime("%Y-%m")] = round(wok_month[datatime11.strftime("%Y-%m")], 2)
    wok_month[datatime21.strftime("%Y-%m")] = round(wok_month[datatime21.strftime("%Y-%m")], 2)
    wok_month[datatime31.strftime("%Y-%m")] = round(wok_month[datatime31.strftime("%Y-%m")], 2)
    wok_month['Всего'] = round(wok_month[datatime11.strftime("%Y-%m")] + wok_month[datatime21.strftime("%Y-%m")] + wok_month[datatime31.strftime("%Y-%m")], 2)

    return wok_month
