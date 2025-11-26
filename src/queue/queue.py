import array
import os
from src.constants import QUEUE_MEMORY
from src.utilities.structure_tools import check_int


"""
-------------------------
------Класс очереди------
-------------------------
"""


"""--------Классы--------"""


class Queue():
    """
    Очередь
    """

    def __init__(self) -> None:
        """
        Инициализирует очередь
        :return: Ничего не возвращает
        """

        self.data = array.array("d")
        self.fromfile()


    def fromfile(self) -> None:
        """
        Извлекает очередь из файла
        :return: Ничего не возвращает
        """

        with open(QUEUE_MEMORY, "rb") as f:
            size_f = os.path.getsize(QUEUE_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)


    def tofile(self) -> None:
        """
        Записывает очередь в файл
        :return: Ничего не возвращает
        """

        with open(QUEUE_MEMORY, "wb") as f:
            self.data.tofile(f)


    def enqueue(self, x: float) -> None:
        """
        Вставляет элемент в начало очереди
        :param x: Число - новый элемент
        :return: Ничего не возвращает
        """

        self.data.insert(0, x)
        self.tofile()


    def dequeue(self) -> int | float:
        """
        Извлекает элемент из очереди, удаляя его
        :return: Число - верхний элемент очереди
        """

        if len(self.data) == 0:
            raise IndexError("Error: function \"dequeue\" cannot be applied to an empty stack")
        q = self.data.pop()
        self.tofile()
        return check_int(q)


    def front(self) -> int | float:
        """
        Извлекает элемент из стека, не удаляя его
        :return: Число - верхний элемент очереди
        """

        if len(self.data) == 0:
            raise IndexError("Error: function \"front\" cannot be applied to an empty stack")
        return check_int(self.data[-1])


    def is_empty(self) -> bool:
        """
        Проверяет, пуста ли очередь
        :return: Логический тип - пуста или нет
        """

        return not (self.data)


    def __len__(self) -> int:
        """
        Возвращает длину очереди
        :return: Число - длина очереди
        """

        return len(self.data)
