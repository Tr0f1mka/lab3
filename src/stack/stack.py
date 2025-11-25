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


class Stack:
    def __init__(self) -> None:
        self.data = array.array("d")
        self.fromfile()


    def fromfile(self) -> None:
        with open(STACK_MEMORY, "rb") as f:
            size_f = os.path.getsize(STACK_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)


    def tofile(self) -> None:
        with open(STACK_MEMORY, "wb") as f:
            self.data.tofile(f)


    def push(self, x: float) -> None:
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
        self.data.pop()
        q = self.data.pop()
        self.tofile()
        return check_int(q)


    def peek(self) -> int | float:
        return check_int(self.data[-2])


    def is_empty(self) -> bool:
        return not (bool(self.data))


    def __len__(self) -> int:
        return len(self.data) // 2


    def min(self) -> int | float:
        return check_int(self.data[-1])
