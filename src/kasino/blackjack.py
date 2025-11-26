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
    """
    Блекджек
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
        Инициализирует параметр balance, а также начисляет бонус за вход при малом балансе
        :return: Ничего не возвращает
        """

        self.balance = self.data[0]

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


    def user_input(self, message: str) -> str:
        """
        Пользовательский ввод, который сразу очищается
        :param message: Сообщение для пользователя
        :return: Строка - ответ пользователя
        """

        a = input(message)
        self.clear_table(2)
        return a.strip()


    @staticmethod
    def print_hand(player_hand: list[int], player_cnt: int, dealer_hand: list[int], dealer_cnt: int) -> None:
        """
        Отрисовка текущей ситуации на столе
        :param player_hand: Список чисел - рука игрока
        :param player_cnt: Число - счёт игрока
        :param dealer_hand: Список чисел - рука дилера
        :param dealer_cnt: Число - счёт дилера
        :return: Ничего не возвращает
        """

        clen = poshutil.get_terminal_size()[0]               # Ширина консоли
        space_player = 3*(len(player_hand)-1)+13             # Ширина руки игрока
        space_dealer = 3*(len(dealer_hand)-1)+13             # Ширина руки дилера
        space = clen//2-space_player                         # Расчёт интервала между руками игрока и дилера

        print(f"{player_cnt:<{space_player-6}}PLAYER{" "*space}{dealer_cnt:<{space_dealer-6}}DEALER")      # Вывод силы рук

        # Вывод первых двух строк карт
        for i in range(2):
            print(*[wrap(x, i)[:32] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(player_hand[-1], i), end=" "*space)
            print(*[wrap(x, i)[:32] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(dealer_hand[-1], i))

        # Третья строка имеет разные длины из-за разницы в цветах масти, обрабатывается отдельно
        print(*[wrap(x, 2)[:32 if x%2 == 0 else 62] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
        print(wrap(player_hand[-1], 2), end=" "*space)
        print(*[wrap(x, 2)[:32 if x%2 == 0 else 62] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
        print(wrap(dealer_hand[-1], 2))

        # Вывод оставшихся строк карт
        for i in range(3, cons.H_DECK):
            print(*[wrap(x, i)[:32] for x in player_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(player_hand[-1], i), end=" "*space)
            print(*[wrap(x, i)[:32] for x in dealer_hand[:-1]], cons.Color.RESET, sep="", end="")
            print(wrap(dealer_hand[-1], i))


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


    @staticmethod
    def counting(a: list[int]) -> int:
        """
        Подсчёт силы руки
        :param a: Список строк - рука, которую нужно посчитать
        :return: Число - подсчитанная рука
        """

        cnt = 0        # Сила руки
        aces = 0       # Количество тузов

        for i in a:
            if i%13 == 12:             # Тузы прибавляют по 11 и увеличивают свой счётчик
                cnt += 11
                aces += 1
            elif 8 <= i%13 <= 11:      # Картинки и 10 прибавляют по 10
                cnt += 10
            else:                      # Остальное - столько, сколько на карте
                cnt += 2+i%13

        while cnt > 21 and aces > 0:   # Если сила больше 21 и есть тузы - уменьшаем силу до допустимой/пока есть тузы
            cnt -= 10
            aces -= 1

        return cnt


    def init_game(self) -> None:
        """
        Инициализация переменных игры
        :return: Ничего не возвращает
        """

        self.balance -= self.bet
        self.user_input("Press ENTER ")

        # Создание колоды
        self.local_deck = [x for x in range(52)]
        random.shuffle(self.local_deck)

        # Создание руки игрока и расчёт её силы
        self.player_hand = [self.local_deck.pop(), self.local_deck.pop()]
        self.player_cnt = self.counting(self.player_hand)

        # Создание руки дилера, её сила в этот момент равна силе первой карты
        self.dealer_hand = [self.local_deck.pop(), self.local_deck.pop()]
        self.dealer_cnt = self.counting([self.dealer_hand[0]])


    def more(self) -> None:
        """
        Добавляет карту в руку игрока
        :return: Ничего не возвращает
        """

        self.player_hand.append(self.local_deck.pop())       # Изменение руки игрока
        self.player_cnt = self.counting(self.player_hand)

        self.clear_table()                          # Перерисовка руки игрока
        self.print_hand(self.player_hand, self.player_cnt, [self.dealer_hand[0], 52], self.dealer_cnt)


    def double(self) -> None:
        """
        Добавляет карту в руку игрока, удваивая ставку
        :return: Ничего не возвращает
        """

        self.balance -= self.bet                    # Изменение баланса и руки игрока
        self.bet *= 2
        self.player_hand.append(self.local_deck.pop())
        self.player_cnt = self.counting(self.player_hand)

        self.clear_table(13)                        # Перерисовка баланса и ставки
        print(f"│{self.balance:^11}│   │{self.bet:^11}│")
        print("└───────────┘   └───────────┘")
        self.print_hand(self.player_hand, self.player_cnt, [self.dealer_hand[0], 52], self.dealer_cnt)


    def moves_player(self) -> None:
        """
        Ходы игрока
        :return: Ничего не возвращает
        """

        message = "Your move: "

        print("┌───────────┐   ┌───────────┐")             # Отрисовка окон баланса и ставки
        print("│  BALANCE  │   │    BET    │")
        print(f"│{self.balance:^11}│   │{self.bet:^11}│")
        print("└───────────┘   └───────────┘")

        # Отрисовка стола
        self.print_hand(self.player_hand,
                        self.player_cnt,
                        [self.dealer_hand[0], 52],      # У дилера верхняя карта должна быть перевёрнута
                        self.dealer_cnt)

        # Цикл ходов игрока(если не собрался блекджек)
        while (self.player_cnt != 21 and (cin := self.user_input(message)) != "pass"):

            # Взятие карты
            if cin == "more":
                self.more()
                if self.player_cnt > 21:
                    break
                message = "Your move: "

            # Удвоение ставки и взятие единственной карты
            elif cin == "double":

                if len(self.player_hand) > 2:                 # Удвоить можно лишь раз
                    message = "Double must be first. Your move: "
                    continue

                if self.balance - self.bet < 0:               # Нельзя удвоить при недостатке средств
                    message = "Don't enough money. Your move: "
                    continue

                self.double()
                break

            # Остальное - неизвестные команды
            else:
                message = "Unknoun action. Your move: "


    def moves_dealer(self) -> None:
        """
        Ходы дилера
        :return: Ничего не возвращает
        """

        # Дилер добирает до 17 очков
        while self.dealer_cnt < 17:

            time.sleep(1)
            self.dealer_cnt = self.counting(self.dealer_hand)

            self.clear_table()      # Перерисовка стола
            self.print_hand(self.player_hand, self.player_cnt, self.dealer_hand, self.dealer_cnt)

            self.dealer_hand.append(self.local_deck.pop())     # Добавление карты в руку дилера
            # time.sleep(1)


    def analise_result(self) -> None:
        """
        Анализ результата игры и расчёт выплат
        :return: Ничего не возвращает
        """

        # Блекджек игрока - победа игрока(ставка*2.5) либо ничья(ставка*1)
        if self.player_cnt == 21 and len(self.player_hand) == 2:
            if self.dealer_cnt == 21 and len(self.dealer_hand) == 3:
                print("Ничья. Ваша ставка возвращена.")
                self.balance += self.bet
            else:
                print(f"Блекджек! Ваш выигрыш: {int(self.bet*2.5)} GC")
                self.balance += int(self.bet*2.5)

        # Перебор дилера - победа игрока(ставка*2)
        elif self.dealer_cnt > 21:
            print(f"Перебор диллера. Ваш выигрыш: {self.bet*2} GC")
            self.balance += self.bet*2

        # Блекджек дилера - поражение игрока
        elif self.dealer_cnt == 21 and len(self.dealer_hand) == 3:
            print("Поражение")

        # Счёт игрока выше дилера - победа игрока(ставка*2)
        elif self.player_cnt > self.dealer_cnt:
            print(f"Победа. Ваш выигрыш: {self.bet*2} GC")
            self.balance += self.bet*2

        # Счёт игрока ниже дилера - поражение игрока
        elif self.player_cnt < self.dealer_cnt:
            print("Поражение")

        # Счёт равный - ничья(ставка*1)
        else:
            print("Ничья. Ваша ставка возвращена.")
            self.balance += self.bet


    def game(self, a: int) -> None:
        """
        Основная игровая функция
        :param a: Число - ставка игрока
        :return: Ничего не возвращает
        """

        if not 25 <= a <= 500:      # Ставка должна быть между 25 и 500
            print("Wrong bet")
            return

        self.bet = a

        if self.balance - self.bet >= 0:      # Проверка на платёжеспособность игрока

            self.init_game()

            self.moves_player()

            if self.player_cnt > 21:          # Проверка на перебор игрока
                print("Перебор игрока")
                self.data[0] = self.balance
                self.tofile()
                return

            self.moves_dealer()
            self.analise_result()

            self.data[0] = self.balance       # Обновляем баланс в массиве данных и записываем в файл
            self.tofile()
        else:
            print("Come back tomorrow")
