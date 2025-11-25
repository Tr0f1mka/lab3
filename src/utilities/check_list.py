from re import fullmatch
from src.constants import FLOAT_PATT, INT_PATT


def scan_type(a: str) -> type[float] | type[int] | type[str]:
    """
    Определяет тип переменной
    :param a: Строка - определяемая переменная
    :return: Тип - тип
    """

    if fullmatch(FLOAT_PATT, a):
        return float
    if fullmatch(INT_PATT, a):
        return int
    return str


# The POWER of types: str > float > int


def check_list(x: list[str])  -> list[int | float | str]:
    """
    Проверяет тип элементов списка и приводит их к единому виду
    :param x: Список строк, которые нужно проверить и преобразовать
    :return: Преобразованный список строк или чисел
    """

    if not x:
        return []
    list_type = scan_type(x[0])
    for i in x[1:]:
        if list_type is int:
            list_type = scan_type(i)
        elif list_type is float:
            if scan_type(i) is str:
                list_type = str
        else:
            list_type = str
            break
    return [list_type(i) for i in x]
