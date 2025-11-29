from logging import config, getLogger
from src.config import LOGGING_CONFIG


config.dictConfig(LOGGING_CONFIG)
logger = getLogger(__name__)


def check_data_base(func) -> None:
    """
    Декоратор для логов инициализации классов
    :param func: Функция - метод класса
    :return: Ничего не возвращает
    """

    def wrapper(self, *args, **kwargs) -> None:
        """
        Функция-обертка
        :param self: Ссылка на экземпляр класса
        :param args: Массив аргументов оборачиваемой функции
        :param kwargs: Словарь аргументов оборачиваемой функции
        :return: Ничего не возвращает
        """

        try:
            # print('azaza', func.__name__, type(self).__name__)
            func(self, *args, **kwargs)
            logger.info(f"Load data of {type(self).__name__}: SUCCES")
        except FileNotFoundError:
            del self.__dict__
        return None
    return wrapper         #type: ignore


def structure_data_log(func) -> int | float | str | None:
    """
    Декоратор для логов структур данных
    :param func: Функция - метод класса
    :return: Число или ничего - результат работы метода, строка - сообщение об ошибке
    """

    def wrapper(self, *args, **kwargs) -> int | float | str | None:
        """
        Функция-обертка
        :param self: Ссылка на экземпляр класса
        :param args: Массив аргументов оборачиваемой функции
        :param kwargs: Словарь аргументов оборачиваемой функции
        :return: Число или ничего - результат работы метода, строка - сообщение об ошибке
        """

        logger.info(f"[CALL] {func.__name__}{self, args, kwargs}")
        try:
            res = func(self, *args, **kwargs)
            logger.info(f"RESULT: SUCCES with data of {type(self).__name__}: {list(self.data)}")
            return res
        except (FileNotFoundError, IndexError) as e:
            logger.error(str(e))
            return str(e)
        except AttributeError:
            logger.error(f"Error: data base of {type(self).__name__} undefined")
            return f"Error: data base of {type(self).__name__} undefined"
    return wrapper               #type: ignore


def kasik_log(func) -> None:
    """
    Декоратор для логов казино
    :param func: Функция - метод класса
    :return: Ничего не возвращает
    """

    def wrapper(self, *args, **kwargs) -> None:
        """
        Функция-обертка
        :param self: Ссылка на экземпляр класса
        :param args: Массив аргументов оборачиваемой функции
        :param kwargs: Словарь аргументов оборачиваемой функции
        :return: Ничего не возвращает
        """

        logger.info(f"[CALL] {func.__name__}{self, args, kwargs}")
        last = self.balance
        func(self, *args, **kwargs)
        logger.info(f"RESULT: SUCCES. Win: {self.balance-last}. Kasino data: {list(self.data)}")
        return None
    return wrapper                 #type: ignore


def create_log(func):


    def wrapper(*args, **kwargs) -> str | list:
        logger.info(f"[CALL] {func.__name__}{args, kwargs}")
        try:
            res = func(*args, **kwargs)
            logger.info("RESULT: SUCCES")
            return res
        except ValueError as e:
            logger.error(str(e))
            return str(e)
    return wrapper
