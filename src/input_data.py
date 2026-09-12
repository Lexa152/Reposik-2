from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
from typing import Any, Dict, List
import json, re


def readln_setting():
    ''' чтение данных setting '''
    file_path = Path(__file__).parent.parent / 'user_settings.json'
    data_file = {}
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data_file = json.load(f)
            return data_file
    except FileNotFoundError:
        print("Файл user_settings.json не найден.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка: файл user_settings.json содержит невалидный JSON.")
        return {}


def readln_xlsx(file_name, time_from: datetime | None = None, time_to: datetime | None = None):
    ''' чтение excel файла '''
    file_path = Path(__file__).parent.parent / r'data/' / file_name

    if time_from is None:
        time_from = datetime(1941, 6, 22, 4, 0, 0)
    if time_to is None:
        time_to = datetime.now()

    try:
        wb = load_workbook(file_path, data_only=True) # Открываем файл
        sheet = wb.active # Получаем активный лист
        # чтение данных
        my_data_tranz = []
        default_dt = datetime(1940, 6, 22, 4, 0, 0)
        for i in range (2, sheet.max_row):
            my_datatime_tranza = default_dt

            cell = sheet.cell(row=i, column=1)
            value = cell.value
            if value is None:
                my_datatime_tranza = default_dt
            elif isinstance(value, datetime):
                my_datatime_tranza = value
            else:
                try:
                    my_datatime_tranza = datetime.strptime(str(value), '%d.%m.%Y %H:%M:%S')
                except ValueError:
                    my_datatime_tranza = default_dt

            cell = sheet.cell(row=i, column=2)
            value = cell.value
            if value is None:
                my_data_pay = default_dt
            elif isinstance(value, datetime):
                my_data_pay = value
            else:
                try:
                    my_data_pay = datetime.strptime(str(value), '%d.%m.%Y %H:%M:%S')
                except ValueError:
                    my_data_pay = default_dt

            # my_datatime_tranza 1
            # my_data_pay 2
            my_number_card =       sheet.cell(row=i, column=3 ).value  if sheet.cell(row=i, column=3 ).value is not None else None
            my_oknotok     =       sheet.cell(row=i, column=4 ).value  if sheet.cell(row=i, column=4 ).value is not None else None
            my_tranz_summa = float(sheet.cell(row=i, column=5 ).value) if sheet.cell(row=i, column=5 ).value is not None else None #123
            my_pay_summa   = float(sheet.cell(row=i, column=7 ).value) if sheet.cell(row=i, column=7 ).value is not None else None #123
            my_val_tranz   =       sheet.cell(row=i, column=6 ).value  if sheet.cell(row=i, column=6 ).value is not None else None
            my_val_pay     =       sheet.cell(row=i, column=8 ).value  if sheet.cell(row=i, column=8 ).value is not None else None
            my_kash_bak    = float(sheet.cell(row=i, column=9 ).value) if sheet.cell(row=i, column=9 ).value is not None else None #123
            my_category    =       sheet.cell(row=i, column=10).value  if sheet.cell(row=i, column=10).value is not None else None
            my_mcc         = float(sheet.cell(row=i, column=11).value) if sheet.cell(row=i, column=11).value is not None else None #123
            my_info        =       sheet.cell(row=i, column=12).value  if sheet.cell(row=i, column=12).value is not None else None
            my_bonus       = float(sheet.cell(row=i, column=13).value) if sheet.cell(row=i, column=13).value is not None else None #123

            new_item = {"my_datatime_tranza": my_datatime_tranza,
                        "my_data_pay" :       my_data_pay,
                        "my_number_card" :    my_number_card,
                        "my_oknotok" :        my_oknotok,
                        "my_tranz_summa":     my_tranz_summa,
                        "my_pay_summa":       my_pay_summa,
                        "my_val_tranz":       my_val_tranz,
                        "my_val_pay":         my_val_pay,
                        "my_kash_bak":        my_kash_bak,
                        "my_category":        my_category,
                        "my_mcc":             my_mcc,
                        "my_info":            my_info,
                        "my_bonus":           my_bonus}

            if time_from <= my_datatime_tranza < time_to:
                my_data_tranz.append(new_item)
        # чтение данных
        return my_data_tranz

    except FileNotFoundError:
        return f"Файл не найден по пути: {file_path} "
    except Exception as e:
        return f"Произошла ошибка: {str(e)} "


def filter_by_state(data, state="OK"):
    """
    Фильтр по статусу транзакции
    """
    if not isinstance(data, (list, tuple)):
        return []

    result = []
    for item in data:
        # Пропускаем всё, что не словарь
        if not isinstance(item, dict):
            continue

        # Проверяем наличие ключа и совпадение значения
        if "my_oknotok" in item and item["my_oknotok"] == state:
            result.append(item)

    return result


def sort_by_date(data, reverse=True):
    """
    Сортировка данных по дате туда-сюда
    """
    def parse_date(item):
        if not isinstance(item, dict):
            return datetime.min

        # Проверяем наличие ключа "date"
        if "my_datatime_tranza" not in item:
            return datetime.min

        raw = str(item["my_datatime_tranza"])

        if not isinstance(raw, str):
            return datetime.min

        try:
            return datetime.fromisoformat(raw)
        except (ValueError, TypeError):
            return datetime.min

    # Защита от передачи не-итерируемого объекта (None, число и т.п.)
    if not isinstance(data, (list, tuple)):
        return []

    return sorted(data, key=parse_date, reverse=reverse)


def sort_by_number(data, key_name: str, reverse: bool = True) -> List[Any]:
    ''' сортировка данных по номеру '''
    if not isinstance(data, (list, tuple)):
        return []

    def key_func(item):
        if not isinstance(item, dict) or key_name not in item:
            return float("-inf")
        try:
            return float(item[key_name])
        except Exception:
            return float("-inf")

    return sorted(data, key=key_func, reverse=reverse)
