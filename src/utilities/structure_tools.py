from re import fullmatch
from src.constants import INT_PATT


def check_int(x: float) -> int | float:
    """
    Функция, определяющая тип числа
    :param x: Вещественное число, которое нужно проверить
    :return: Целое или вещественное число - результат проверки
    """

    if fullmatch(INT_PATT, str(x)):
        return int(x)
    return x
