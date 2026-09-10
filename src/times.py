from datetime import datetime, time


def time_and_range(current_datetime):
    ''' формирование приветствия в соответствии с заданием '''
    current_time = current_datetime.time()
    # Временные интервалы
    morning_start = time(6, 0, 0)
    morning_end = time(11, 59, 59)

    afternoon_start = time(12, 0, 0)
    afternoon_end = time(17, 59, 59)

    evening_start = time(18, 0, 0)
    evening_end = time(22, 59, 59)

    night_start = time(23, 0, 0)
    night_end = time(23, 59, 59)

    midnight_start = time(0, 0, 0)
    midnight_end = time(5, 59, 59)

    # Вычисляю в каком интервале текущее время
    if current_time is not None:
        if morning_start <= current_time <= morning_end:
            return 'Доброе утро'
        elif afternoon_start <= current_time <= afternoon_end:
            return 'Добрый день'
        elif evening_start <= current_time <= evening_end:
            return 'Добрый вечер'
        elif night_start <= current_time <= night_end or midnight_start <= current_time <= midnight_end:
            return 'Доброй ночи'
        else:
            return 'Доброго времени суток'
    else:
        return 'ошибка данных'
