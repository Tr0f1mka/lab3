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
    def __init__(self) -> None:
        self.data = array.array("d")
        self.fromfile()


    def fromfile(self) -> None:
        with open(QUEUE_MEMORY, "rb") as f:
            size_f = os.path.getsize(QUEUE_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)


    def tofile(self) -> None:
        with open(QUEUE_MEMORY, "wb") as f:
            self.data.tofile(f)


    def enqueue(self, x: float) -> None:
        self.data.insert(0, x)
        self.tofile()


    def dequeue(self) -> int | float:
        q = self.data.pop()
        self.tofile()
        return check_int(q)


    def front(self) -> int | float:
        return check_int(self.data[-1])


    def is_empty(self) -> bool:
        return not (bool(self.data))


    def __len__(self) -> int:
        return len(self.data)
