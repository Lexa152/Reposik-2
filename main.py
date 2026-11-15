from src.air import Aircraft
from src.api import fetch_countries
from src.api import get_country_bounds
from src.api import get_flights
from src.api import save_to_json


def user_interaction():
    atlas = fetch_countries() # загрузка списка стран для запроса
    country = 'nu'
    country_en = 'nu'
    sort_param = 'по скорости'
    air_list = []
    sorted_air_list = []

    print('Привет пользователь!'
          '\nСейчас я покажу список самолётов, пролетающих над выбранной страной! (если это интересно ...)'
          '\nДля этого придётся пройти небольшое анкетирование ...'
          '\n   === короткий мануал ==='
          '\n1) вводи по-русски, затем жми enter;'
          '\n2) ввод данных пофиг с какой буквы (заглавная/строчная);'
          '\n3) для завершения работы с программой вводи слово "стоп"'
          '\n   === Начало анкетирования ===')

    while (country_en == 'nu'):
        user_input = input('Введите название страны, самолёты над которой интересуют: ')
        if user_input == 'стоп':
            print(f'Работа завершена по вашей просьбе')
            exit()
        for i in atlas:
            if i['name_ru'].lower() == user_input.lower():
                country_en = i['name_en']
                country = i['name_en']
        if country_en == 'nu':
            print('такая страна - странна (в базе не числится), вводите снова')
    print(f"К сведению принято: {country_en}")
    geo_bounds = get_country_bounds(country_en)
    print(f'Границы выбранной страны: {geo_bounds}')

    # список для фильтрации по стране регистрации борта
    print('Предлагается ввести страны, в которых зарегистрированы интересующие самолёты'
          '\n   - для окончания ввода стран введите "всё"'
          '\n   - если введёте "всё" сразу, то ограничения по странам регистрации не будет')
    countries_list = []
    country_en = 'nu'
    while (country_en == 'nu'):
        country_en = 'nu'
        user_input = input('Введите название: ')
        if user_input == 'стоп':
            print(f'Работа завершена')
            exit()
        if user_input == 'всё':
            print(f'Ввод списка стран окончен')
            break
        for i in atlas:
            if i['name_ru'].lower() == user_input.lower():
                countries_list.append(i['name_en'])
                country_en = i['name_en']
                print(f'в список внесена страна {country_en}')
        if country_en == 'nu':
            print('такая страна - странна (в базе не числится), вводите снова')
        else:
            country_en = 'nu'

    # top_n
    while True:
        user_input = input('Введите количество самолетов для вывода на экране: ')
        if user_input == 'стоп':
            print(f'Работа завершена по вашей просьбе')
            exit()
        try:
            top_n = int(user_input)
            if top_n <= 0:
                print('Число должно быть больше нуля. Вводите снова')
                continue
            break
        except ValueError:
            print('Ошибка: введите именно целое число (например, 12345). пробуйте снова')
    print(f'К сведению принято: {top_n}')

    # altitude_min
    while True:
        user_input = input('Введи нижнюю границу диапазона высот полёта (значение в метрах): ')
        if user_input == 'стоп':
            print(f'Работа завершена')
            exit()
        try:
            altitude_min = int(user_input)
            if altitude_min <= 0:
                print('Число должно быть больше нуля. пробуйте снова')
                continue
            break
        except ValueError:
            print('Ошибка: введите именно целое число (например, 12345). пробуйте снова')
    print(f'К сведению принято: {altitude_min}')

    # altitude_max
    while True:
        user_input = input('Введите верхнюю границу диапазона высот полёта (значение в метрах): ')
        if user_input == 'стоп':
            print(f'Работа завершена')
            exit()
        try:
            altitude_max = int(user_input)
            if altitude_max <= 0:
                print('Число должно быть больше нуля. пробуйте снова')
                continue
            if altitude_max <= altitude_min:
                print('Верхняя граница высот должна быть выше нижней границы,'
                      '\n т.е. введите бОльшее число. пробуйте снова')
                continue
            break
        except ValueError:
            print('Ошибка: введи именно целое число (например, 12345). пробуй снова')
    print(f'К сведению принято: {altitude_max}')

    # сортировка по скорости или по высоте?
    print('Укажите, по какому параметру отсортировать список самолётов:\n'
          '"по скорости" или "по высоте" (вводите точно как в кавычках).')

    while True:
        user_input = input('Выбранный параметр: ').strip()
        if user_input == 'стоп':
            print('Работа завершена')
            exit()

        if user_input not in ['по скорости', 'по высоте']:
            print('Необходимо напечатать "по скорости" или "по высоте". Попробуйте снова.')
            continue

        sort_param = user_input
        break

    print(f'К сведению принято: {sort_param}')

    print('Итого, данные для поиска:')
    print(f"     Страна, чьё пространство интересует, (на нерусском): {country}")
    print(f"     Диапазон высот, в пределах которого интересующие самолёты: {altitude_min}-{altitude_max} метров")
    print(f"     Количество самолётов для вывода на экран: {top_n} шт.")
    print(f"     Сортировка списка самолётов будет произведена {sort_param} ")
    print('В выборку попадут самолёты следующих государств:')
    if len(countries_list) == 0:
        print('     все обнаруженные')
    else:
        for i in countries_list:
            print(f'     {i} ')

    print('Результаты поиска:')

    air_list = get_flights(countries_list,
                           geo_bounds['юг'],
                           geo_bounds['север'],
                           geo_bounds['запад'],
                           geo_bounds['восток'],
                           altitude_min,
                           altitude_max)

    if len(air_list) > 0:
        if sort_param == 'по скорости':
            air_list = sorted(air_list, key=lambda x: x["vel"], reverse=True)
        if sort_param == 'по высоте':
            air_list = sorted(air_list, key=lambda x: x["alt"], reverse=True)

    Aircraft.search_aircraft(air_list, top_n)
    print(f'Общее количество самолётов: {len(air_list)} штук')
    save_to_json(air_list)
    print(f'Список "Топ N позиций":')
    for i in Aircraft.aircraft_list:
        print(i)

if __name__ == "__main__":
    user_interaction()
