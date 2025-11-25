"""------Библиотеки------"""

import array
import random
import time
import os
import src.constants as cons
import shutil as poshutil
from src.utilities.card_wrap import wrap

"""
------------------
-----Блекджек-----
------------------
"""

class BlackJack():

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

        # self.data.append(10000)
        # self.data.append(25)
        # self.data.append(now)
        # self.data.append(1)

        # self.tofile()
        self.fromfile()
        # print(self.data)
        # self.data.pop()
        self.balance = self.data[0]
        if now - self.data[2] > 0:
            if self.balance < 500:
                self.balance = 500
                self.data[0] = self.balance
            self.data[2] = now
            self.tofile()


    def user_input(self, message: str) -> str:
        a = input(message)
        self.clear_table(2)
        return a

    def print_hand(self, player_hand: list[int], player_cnt: int, dealer_hand: list[int], dealer_cnt: int):
        clen = poshutil.get_terminal_size()[0]
        cnt = clen//2-3*(len(player_hand)-1)-13
        # print(type(clen))
        print(f"{player_cnt:<{3*(len(player_hand)-1)+7}}PLAYER{" "*cnt}{dealer_cnt:<{3*(len(dealer_hand)-1)+7}}DEALER")

        for i in range(2):
            print(*[wrap(x, i)[:32] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(player_hand[-1], i), end=" "*cnt)
            print(*[wrap(x, i)[:32] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(dealer_hand[-1], i))

        print(*[wrap(x, 2)[:32 if x%2 == 0 else 62] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
        print(wrap(player_hand[-1], 2), end=" "*cnt)
        print(*[wrap(x, 2)[:32 if x%2 == 0 else 62] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
        print(wrap(dealer_hand[-1], 2))

        for i in range(3, cons.H_DECK):
            print(*[wrap(x, i)[:32] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(player_hand[-1], i), end=" "*cnt)
            print(*[wrap(x, i)[:32] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(dealer_hand[-1], i))

    @staticmethod
    def clear_table(cnt=11):
        for i in range(cnt):
            print("\033[2K\033[A", end="")
            # time.sleep(0.6)
        print("\r")

    @staticmethod
    def counting(a: list[int]) -> int:
        cnt = 0
        aces = 0
        for i in a:
            if i%13 == 12:
                cnt += 11
                aces += 1
            elif 8 <= i%13 <= 11:
                cnt += 10
            else:
                cnt += 2+i%13
        while cnt > 21 and aces > 0:
            cnt -= 10
            aces -= 1
        return cnt


    def moves_player(self):
        # self.player_hand = [12, 11]
        # self.player_cnt = 21
        message = "Your move: "

        print("┌───────────┐   ┌───────────┐")
        print("│  BALANCE  │   │    BET    │")
        print(f"│{self.balance:^11}│   │{self.bet:^11}│")
        print("└───────────┘   └───────────┘")
        self.print_hand(self.player_hand, self.player_cnt, [self.dealer_hand[0], 52], self.dealer_cnt)

        while (self.player_cnt != 21 and (cin := self.user_input(message)) != "pass"):
            # time.sleep(2)
            # self.clear_table(1)
            if cin == "more":
                self.player_hand.append(self.local_deck.pop())
                self.player_cnt = self.counting(self.player_hand)
                self.clear_table()
                self.print_hand(self.player_hand, self.player_cnt, [self.dealer_hand[0], 52], self.dealer_cnt)
                if self.player_cnt > 21:
                    # print("Перебор")
                    break
                message = "Your move: "
            elif cin == "double":
                if len(self.player_hand) > 2:
                    message = "Double must be first. Your move: "
                    continue
                if self.balance - self.bet < 0:
                    message = "Don't enough money. Your move: "
                    continue
                self.balance -= self.bet
                self.bet *= 2
                # self.player_hand.append(self.local_deck.pop())
                self.player_hand.append(8)
                self.player_cnt = self.counting(self.player_hand)

                self.clear_table(13)
                print(f"│{self.balance:^11}│   │{self.bet:^11}│")
                print("└───────────┘   └───────────┘")
                self.print_hand(self.player_hand, self.player_cnt, [self.dealer_hand[0], 52], self.dealer_cnt)

                if self.player_cnt > 21:
                    # print("Перебор")
                    ...
                break
            else:
                message = "Unknoun action. Your move: "
        else:
            ...
            # print("Завершено")
        # print("azaza")
        # if self.player_cnt == 21 and len(self.player_hand) == 2:
        #     print()
        # self.clear_table(2)
        # time.sleep(5)


    def moves_dealer(self):
        # self.dealer_cnt = 11
        # self.dealer_hand = [11, 12]
        while self.dealer_cnt < 17:
            self.dealer_cnt = self.counting(self.dealer_hand)
            self.clear_table()
            self.print_hand(self.player_hand, self.player_cnt, self.dealer_hand, self.dealer_cnt)
            self.dealer_hand.append(self.local_deck.pop())
            # time.sleep(1)


    def analise_result(self):
        if self.dealer_cnt > 21:
            self.balance += self.bet*2
            print(f"Перебор диллера. Ваш выигрыш: {self.bet*2}")
            self.balance += self.bet*2
        elif self.player_cnt == 21 and len(self.player_hand) == 2:
            if self.dealer_cnt == 21 and len(self.dealer_hand) == 3:
                print("Ничья. Ваша ставка возвращена.")
                self.balance += self.bet
            else:
                print(f"Блекджек! Ваш выигрыш: {int(self.bet*2.5)}")
                self.balance += int(self.bet*2.5)
        elif self.dealer_cnt == 21 and len(self.dealer_hand) == 3:
            print("Поражение")
        elif self.player_cnt > self.dealer_cnt:
            print(f"Победа. Ваш выигрыш: {self.bet*2}")
            self.balance += self.bet*2
        elif self.player_cnt < self.dealer_cnt:
            print("Поражение")
        else:
            print("Ничья. Ваша ставка возвращена.")
            self.balance += self.bet


    def game(self, a: int):

        if not 25 <= a <= 500:
            print("Wrong bet")
            return

        self.bet = a

        if self.balance - self.bet >= 0:
            self.balance -= self.bet
            self.user_input("Press ENTER ")

            self.local_deck = [x for x in range(52)]
            random.shuffle(self.local_deck)

            self.player_hand = [self.local_deck.pop(), self.local_deck.pop()]
            self.player_cnt = self.counting(self.player_hand)
            self.dealer_hand = [self.local_deck.pop(), self.local_deck.pop()]
            self.dealer_cnt = self.counting([self.dealer_hand[0]])

            self.moves_player()
            if self.player_cnt > 21:
                print("Перебор игрока")
                self.data[0] = self.balance
                self.tofile()
                return
            self.moves_dealer()
            self.analise_result()
            self.data[0] = self.balance
            self.tofile()
        else:
            print("Come back tomorrow")


# blackjack = BlackJack()

# blackjack.game(150)
