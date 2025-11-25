import src.constants as cons

def wrap(a: int, i: int) -> str:
    """
    Окрашивает часть карты карты
    :param a: Индекс карты из списка текстур карт(52 - рубашка)
    :param i: Индекс строки карты
    :return: Окрашенная строка карты
    """

    if a == 52:
        return f"{cons.Color.WHITE}{cons.Color.BLACK}{cons.SHIRT[i]}{cons.Color.RESET}"
    else:
        return f"{cons.Color.WHITE}{cons.Color.BLACK}{cons.DECK[a][i]}{cons.Color.RESET}"
