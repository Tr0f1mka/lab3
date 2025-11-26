import array
import os
from src.constants import STACK_MEMORY
from src.utilities.structure_tools import check_int


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

    def __init__(self) -> None:
        """
        Инициализирует стек
        :return: Ничего не возвращает
        """

        self.data = array.array("d")
        self.fromfile()


    def fromfile(self) -> None:
        """
        Извлекает стек из файла
        :return: Ничего не возвращает
        """

        with open(STACK_MEMORY, "rb") as f:
            size_f = os.path.getsize(STACK_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)


    def tofile(self) -> None:
        """
        Записывает стек в файл
        :return: Ничего не возвращает
        """

        with open(STACK_MEMORY, "wb") as f:
            self.data.tofile(f)


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
        self.tofile()


    def pop(self) -> int | float:
        """
        Извлекает элемент из стека, удаляя его
        :return: Число - верхний элемент стека
        """

        if len(self.data) == 0:
            raise IndexError("Error: function \"pop\" cannot be applied to an empty stack")
        self.data.pop()
        q = self.data.pop()
        self.tofile()
        return check_int(q)


    def peek(self) -> int | float:
        """
        Извлекает элемент из стека, не удаляя его
        :return: Число - верхний элемент стека
        """

        if len(self.data) == 0:
            raise IndexError("Error: function \"peek\" cannot be applied to an empty stack")
        return check_int(self.data[-2])


    def is_empty(self) -> bool:
        """
        Проверяет, пуст ли стек
        :return: Логический тип - пуст или нет
        """

        return not (self.data)


    def __len__(self) -> int:
        """
        Возвращает длину стека
        :return: Число - длина стека
        """

        return len(self.data) // 2


    def min(self) -> int | float:
        """
        Возвращает минимум стека
        :return: Число - минимум стека
        """

        if len(self.data) == 0:
            raise IndexError("Error: function \"min\" cannot be applied to an empty stack")
        return check_int(self.data[-1])
