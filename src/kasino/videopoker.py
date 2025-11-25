"""------Библиотеки------"""

import array
import random
import time
import os
import src.constants as cons
from src.utilities.card_wrap import wrap
from src.sorts import quick_sort

"""
------------------
----Видеопокер----
------------------
"""

class VideoPoker():

    def fromfile(self) -> None:
        with open(cons.KASINO_MEMORY, "rb") as f:
            size_f = os.path.getsize(cons.KASINO_MEMORY)
            cnt_elems = size_f // 8
            self.data.fromfile(f, cnt_elems)

    def tofile(self) -> None:
        with open(cons.KASINO_MEMORY, "wb") as f:
            self.data.tofile(f)

    def __init__(self) -> None:

        self.data = array.array("Q")
        now = int(time.time() / 60 / 60 / 24)

        self.fromfile()
        self.balance = self.data[0]
        self.bet = self.data[3]
        if now - self.data[2] > 0:
            if self.balance < 500:
                self.balance = 500
                self.data[0] = self.balance
            self.data[2] = now
            self.tofile()

    def print_hand(self, hand: list[int]):
        for i in range(cons.H_DECK):
            for j in hand:
                print(f"{wrap(j, i)}   ", end="")
            print(f"           {wrap(52, i)}")

    def clear_table(self):
        for i in range(10):
            print(f"\033[A{" "*120}\033[A")

    def input_hold(self, mess = "Hold: "):
        print(f"\033[A{" "*120}\033[A")
        try:
            a = list(map(int, input(mess).split()))
            print(a)
            rev = [1, 2, 3, 4, 5]
            for i in a:
                if (1 <= i <= 5) and (i in rev):
                    rev.remove(i)
                else:
                    print(f"\033[A{" "*120}\033[A")
                    raise ValueError
            print(f"\033[A{" "*120}\033[A"*2)
            return rev
        except ValueError:
            # print(f"\033[A{" "*120}\033[A")
            return self.input_hold("Wrong input. Retry hold: ")


    def check_flush_royal(self, suit: list[int], rank: list[int]):
        return self.check_street_flush(suit, rank) and rank[0] == 8

    def check_street_flush(self, suit: list[int], rank:list[int]):
        return self.check_flush(suit) and self.check_street(rank)

    def check_kara(self, rank: list[int]):
        return rank.count(rank[2]) == 4

    def check_full_house(self, rank: list[int]):
        if rank.count(rank[2]) == 3:
            return (rank.count(rank[0]) == 2) or (rank.count(rank[-1]) == 2)
        return False

    def check_flush(self, suit: list[int]):
        return suit.count(suit[0]) == 5

    def check_street(self, rank:list[int]):
        q = set(rank)
        if len(q) == 5:
            if rank[-1] - rank[0] == 4:
                return True
            if rank[-1] == 12 and rank[-2] - rank[0] == 3:
                return True
        return False

    def check_set(self, rank: list[int]):
        return rank.count(rank[2]) == 3

    def check_2_pairs(self, rank: list[int]):
        return rank.count(rank[1]) == 2 and rank.count(rank[-2]) == 2

    def check_pair_tens_and_more(self, rank: list[int]):
        return (rank.count(rank[1]) == 2 and rank[1] >= 8) or (rank.count(rank[-2]) == 2 and rank[-2] >= 8)

    def analise_result(self):
        rank = quick_sort([x%13 for x in self.hand])
        suit = [x%4 for x in self.hand]

        if self.check_flush_royal(suit, rank):
            print(f"JACKPOT! You win: {25*cons.PAYOUT_TABLE[0][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[0][self.bet-1]
        elif self.check_street_flush(suit, rank):
            print(f"Street flush! You win: {25*cons.PAYOUT_TABLE[1][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[1][self.bet-1]
        elif self.check_kara(rank):
            print(f"Kara! You win: {25*cons.PAYOUT_TABLE[2][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[2][self.bet-1]
        elif self.check_full_house(rank):
            print(f"Full house! You win: {25*cons.PAYOUT_TABLE[3][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[3][self.bet-1]
        elif self.check_flush(suit):
            print(f"Flush! You win: {25*cons.PAYOUT_TABLE[4][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[4][self.bet-1]
        elif self.check_street(rank):
            print(f"Street! You win: {25*cons.PAYOUT_TABLE[5][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[5][self.bet-1]
        elif self.check_set(rank):
            print(f"Set! You win: {25*cons.PAYOUT_TABLE[6][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[6][self.bet-1]
        elif self.check_2_pairs(rank):
            print(f"2 pairs! You win: {25*cons.PAYOUT_TABLE[7][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[7][self.bet-1]
        elif self.check_pair_tens_and_more(rank):
            print(f"Pair! You win: {25*cons.PAYOUT_TABLE[8][self.bet-1]}")
            self.balance += 25*cons.PAYOUT_TABLE[8][self.bet-1]
        else:
            print("you lose")

    def cheat(self):
        self.data[0] = 10000
        self.tofile()

    def game(self):
        if self.balance - 25*self.bet >= 0:
            self.balance -= 25*self.bet
            print("┌───────────┐   ┌───────────┐")
            print("│  BALANCE  │   │    BET    │")
            print(f"│{self.balance:^11}│   │{25*self.bet:^11}│")
            print("└───────────┘   └───────────┘")
            for i in range(cons.H_DECK):
                print(f"{wrap(52, i)}   "*5, end="")
                print(f"           {wrap(52, i)}")
            input("Press ENTER ")
            self.clear_table()

            local_deck = [i for i in range(52)]
            random.shuffle(local_deck)
            self.hand = [local_deck.pop() for i in range(5)]
            # print(self.hand)

            self.print_hand(self.hand)
            print()
            a = self.input_hold()
            for i in a:
                self.hand[i-1] = local_deck.pop()

            print()
            self.clear_table()
            self.print_hand(self.hand)
            self.analise_result()
            self.data[0] = self.balance
            self.tofile()
        else:
            print("Come back tomorrow!")


    def poker_bet(self, a: int):
        if 1 <= a <= 5:
            self.data[3] = a
            self.tofile()
        else:
            print("Wrong bet")

# videopoker = VideoPoker()
# videopoker.print_hand([23, 51, 13, 34, 0])
# videopoker.print_hand([34, 23, 0, 1, 5])
# time.sleep(3)
# videopoker.clear_table()
# time.sleep(2)
# videopoker.print_hand([34, 23, 0, 1, 5])
# time.sleep(3)
# videopoker.clear_table()
# videopoker.game()
# print(videopoker.check_flush_royal([3, 3, 3, 3, 3], [8, 9, 10, 11, 12]))
# videopoker.hand = [35, 17, 6, 38, 37]
# print(videopoker.analise_result())
