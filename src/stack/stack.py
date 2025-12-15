import array
import os
from src.constants import STACK_MEMORY
from src.utilities.structure_tools import check_int
from src.utilities.logger import structure_data_log, check_data_base


"""
-------------------------
-------Класс стека-------
-------------------------
"""


"""--------Классы--------"""


class Stack():
    """
    Стек
    """

    @check_data_base                 #type: ignore
    def __init__(self) -> None:
        """
        Инициализирует стек
        :return: Ничего не возвращает
        """

        self.data = self.fromfile()


    @staticmethod
    def fromfile() -> array.array:
        """
        Извлекает стек из файла
        :return: Ничего не возвращает
        """

        data = array.array("d")
        with open(STACK_MEMORY, "rb") as f:
            size_f = os.path.getsize(STACK_MEMORY)
            cnt_elems = size_f // 8
            data.fromfile(f, cnt_elems)
        return data


    def tofile(self) -> None:
        """
        Записывает стек в файл
        :return: Ничего не возвращает
        """

        with open(STACK_MEMORY, "wb") as f:
            self.data.tofile(f)


    @structure_data_log
    def push(self, x: float) -> None:
        """
        Вставляет элемент в конец стека
        :param x: Число - новый элемент
        :return: Ничего не возвращает
        """

        self.data.append(x)
        if len(self.data) == 1:
            self.data.append(x)
        else:
            if self.data[-2] < self.data[-1]:
                self.data.append(self.data[-2])
            else:
                self.data.append(x)


    @structure_data_log
    def pop(self) -> int | float:
        """
        Извлекает элемент из стека, удаляя его
        :return: Число - верхний элемент стека
        """

        if not self.data:
            raise IndexError("Error: function \"pop\" cannot be applied to an empty stack")
        self.data.pop()
        q = self.data.pop()
        return check_int(q)


    @structure_data_log
    def peek(self) -> int | float:
        """
        Извлекает элемент из стека, не удаляя его
        :return: Число - верхний элемент стека
        """

        if not self.data:
            raise IndexError("Error: function \"peek\" cannot be applied to an empty stack")
        return check_int(self.data[-2])


    @structure_data_log
    def is_empty(self) -> bool:
        """
        Проверяет, пуст ли стек
        :return: Логический тип - пуст или нет
        """

        return not (self.data)


    @structure_data_log
    def __len__(self) -> int:
        """
        Возвращает длину стека
        :return: Число - длина стека
        """

        return len(self.data) // 2


    @structure_data_log
    def min(self) -> int | float:
        """
        Возвращает минимум стека
        :return: Число - минимум стека
        """

        if not self.data:
            raise IndexError("Error: function \"min\" cannot be applied to an empty stack")
        return check_int(self.data[-1])
