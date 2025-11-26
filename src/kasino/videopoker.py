"""------Библиотеки------"""

import array
import random
import time
import os
import src.constants as cons
from src.utilities.card_wrap import wrap
from src.sorts import counting_sort

"""
------------------
----Видеопокер----
------------------
"""

class VideoPoker():
    """
    Видепокер
    """

    def __init__(self) -> None:
        """
        Инициализирует объект
        :return: Ничего не возвращает
        """

        self.data = array.array("Q")
        self.fromfile()
        self.init_params()


    def init_params(self) -> None:
        """
        Инициализирует параметры balance и bet, а также начисляет бонус за вход при малом балансе
        :return: Ничего не возвращает
        """

        self.balance = self.data[0]
        self.bet = self.data[3]

        now = int(time.time() / 60 / 60 / 24)          # Обработка бонуса за вход
        if now - self.data[2] > 0:
            if self.balance < 500:
                self.balance = 500
                self.data[0] = self.balance
                print("Daily Entry Bonus: Your balance: 500")
            self.data[2] = now
            self.tofile()


    def fromfile(self) -> None:
        """
        Извлекает данные из файла
        :return: Ничего не возвращает
        """

        with open(cons.KASINO_MEMORY, "rb") as f:
            size_f = os.path.getsize(cons.KASINO_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)


    def tofile(self) -> None:
        """
        Записывает данные в файл
        :return: Ничего не возвращает
        """

        with open(cons.KASINO_MEMORY, "wb") as f:
            self.data.tofile(f)


    @staticmethod
    def print_hand(hand: list[int]) -> None:
        """
        Отрисовка текущей ситуации на столе
        :param hand: Список чисел - рука игрока
        :return: Ничего не возвращает
        """

        for i in range(cons.H_DECK):
            for j in hand:
                print(f"{wrap(j, i)}   ", end="")
            print(f"           {wrap(52, i)}")


    @staticmethod
    def clear_table(cnt: int = 11) -> None:
        """
        Очистка стола
        :param cnt: Число - количество удаляемых строк
        :return: Ничего не возвращает
        """

        for i in range(cnt):
            print("\033[2K\033[A", end="")
        print("\r")


    def input_hold(self, mess="Hold: ") -> list[int]:
        """
        Ввод удерживаемых карт
        :param mess: Строка - сообщение для пользователя
        :return: Список чисел - заменяемые карты или ничего
        """

        # self.clear_table(2)
        try:
            a = list(map(int, input(mess).split()))
            self.clear_table(1)
            rev = [1, 2, 3, 4, 5]
            for i in a:
                rev.remove(i)
            return rev

        except ValueError:
            self.clear_table(2)
            return self.input_hold("Wrong input. Hold: ")


    def check_flush_royal(self, suit: list[int], rank: list[int]) -> bool:
        """
        Проверяет флеш-рояль
        :param suit: Список чисел - масти руки
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return self.check_street_flush(suit, rank) and rank[0] == 8


    def check_street_flush(self, suit: list[int], rank:list[int]) -> bool:
        """
        Проверяет стрит-флеш
        :param suit: Список чисел - масти руки
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return self.check_flush(suit) and self.check_street(rank)


    @staticmethod
    def check_kara(rank: list[int]) -> bool:
        """
        Проверяет каре
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return rank.count(rank[2]) == 4


    @staticmethod
    def check_full_house(rank: list[int]) -> bool:
        """
        Проверяет фулл-хаус
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        if rank.count(rank[2]) == 3:
            return (rank.count(rank[0]) == 2) or (rank.count(rank[-1]) == 2)
        return False


    @staticmethod
    def check_flush(suit: list[int]) -> bool:
        """
        Проверяет флеш
        :param suit: Список чисел - масти руки
        :return: Логический тип - результат проверки
        """

        return suit.count(suit[0]) == 5


    @staticmethod
    def check_street(rank: list[int]) -> bool:
        """
        Проверяет стрит
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        q = set(rank)
        if len(q) == 5:
            if rank[-1] - rank[0] == 4:
                return True
            if rank[-1] == 12 and rank[-2] - rank[0] == 3:
                return True
        return False


    @staticmethod
    def check_set(rank: list[int]) -> bool:
        """
        Проверяет сет
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return rank.count(rank[2]) == 3


    @staticmethod
    def check_2_pairs(rank: list[int]) -> bool:
        """
        Проверяет 2 пары
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return rank.count(rank[1]) == 2 and rank.count(rank[-2]) == 2


    @staticmethod
    def check_pair_tens_and_more(rank: list[int]) -> bool:
        """
        Проверяет пару 10 и старше
        :param rank: Список чисел - ранги руки
        :return: Логический тип - результат проверки
        """

        return (rank.count(rank[1]) == 2 and rank[1] >= 8) or (rank.count(rank[-2]) == 2 and rank[-2] >= 8)


    def analise_result(self) -> None:
        """
        Вычисляет выигрыш
        :return: Ничего не возвращает
        """

        rank = counting_sort([x%13 for x in self.hand])  # Отсортированный список рангов карт
        suit = [x%4 for x in self.hand]                  # Список мастей

        if self.check_flush_royal(suit, rank):
            print(f"JACKPOT! You win: {25*cons.PAYOUT_TABLE[0][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[0][self.bet-1]

        elif self.check_street_flush(suit, rank):
            print(f"Street flush! You win: {25*cons.PAYOUT_TABLE[1][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[1][self.bet-1]

        elif self.check_kara(rank):
            print(f"Kara! You win: {25*cons.PAYOUT_TABLE[2][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[2][self.bet-1]

        elif self.check_full_house(rank):
            print(f"Full house! You win: {25*cons.PAYOUT_TABLE[3][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[3][self.bet-1]

        elif self.check_flush(suit):
            print(f"Flush! You win: {25*cons.PAYOUT_TABLE[4][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[4][self.bet-1]

        elif self.check_street(rank):
            print(f"Street! You win: {25*cons.PAYOUT_TABLE[5][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[5][self.bet-1]

        elif self.check_set(rank):
            print(f"Set! You win: {25*cons.PAYOUT_TABLE[6][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[6][self.bet-1]

        elif self.check_2_pairs(rank):
            print(f"2 pairs! You win: {25*cons.PAYOUT_TABLE[7][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[7][self.bet-1]

        elif self.check_pair_tens_and_more(rank):
            print(f"Pair! You win: {25*cons.PAYOUT_TABLE[8][self.bet-1]} GC")
            self.balance += 25*cons.PAYOUT_TABLE[8][self.bet-1]

        else:
            print("You lose")


    def cheat(self) -> None:
        """
        Заменяет баланс игрока на 10000 GC
        :return: Ничего не возвращает
        """

        self.data[0] = 500
        self.tofile()


    def game(self) -> None:
        """
        Основная игровая функция
        :return: Ничего не возвращает
        """

        if self.balance - 25*self.bet >= 0:

            self.balance -= 25*self.bet

            print("┌───────────┐   ┌───────────┐")      # Отрисовка окон баланса и ставки
            print("│  BALANCE  │   │    BET    │")
            print(f"│{self.balance:^11}│   │{25*self.bet:^11}│")
            print("└───────────┘   └───────────┘")

            self.print_hand([52]*5)      # Вывод 5 рубашек
            input("Press ENTER ")
            self.clear_table()

            local_deck = [i for i in range(52)]   # Создание колоды и руки
            random.shuffle(local_deck)
            self.hand = [local_deck.pop() for i in range(5)]

            self.print_hand(self.hand)
            a = self.input_hold()

            for i in a:                  # Замена неудерживаемых карт
                self.hand[i-1] = local_deck.pop()

            self.clear_table()
            self.print_hand(self.hand)

            self.analise_result()

            self.data[0] = self.balance  # Запись результата
            self.tofile()

        else:
            print("Come back tomorrow!")


    def poker_bet(self, a: int) -> None:
        """
        Меняет множитель ставки
        :return: Ничего не возвращает
        """

        if 1 <= a <= 5:
            self.data[3] = a
            self.tofile()

        else:
            print("Wrong bet")
