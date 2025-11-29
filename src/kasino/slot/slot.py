"""------Библиотеки------"""

import array
import random
import time
from pygame import mixer     #type: ignore
import webbrowser
import os
import src.constants as cons
from src.utilities.logger import check_data_base, create_log, kasik_log


print("\033[2K\033[A\033[2K\033[A\033[2K\033[A")

"""
------------------
-------Слот-------
------------------
"""


class Slot:
    """
    Слот
    """

    @check_data_base                 #type: ignore
    def __init__(self) -> None:
        """
        Инициализирует объект
        :return: Ничего не возвращает
        """

        self.sound_init()
        self.data = array.array("Q")
        self.fromfile()
        self.init_params()


    def sound_init(self) -> None:
        """
        Инициализирует звуки
        :return: Ничего не возвращает
        """

        mixer.init()
        self.start_spin = mixer.Sound("src/kasino/slot/sounds/start_spin.ogg")
        self.spin_sound = mixer.Sound("src/kasino/slot/sounds/spin.ogg")
        self.music_spin = mixer.Sound("src/kasino/slot/sounds/music_spin.ogg")
        self.jackpot = mixer.Sound("src/kasino/slot/sounds/jackpot.ogg")
        self.mega_win = mixer.Sound("src/kasino/slot/sounds/mega_win.ogg")
        self.win = mixer.Sound("src/kasino/slot/sounds/win.ogg")
        self.lose = mixer.Sound("src/kasino/slot/sounds/lose.ogg")


    def init_params(self) -> None:
        """
        Инициализирует параметры
        :return: Ничего не возвращает
        """

        self.balance = self.data[0]
        self.bet = self.data[1]

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


    def print_slot(self, a: str, b: str, c: str, balance: int, bet: int) -> None:
        """
        Отрисовка слота
        :return: Ничего не возвращает
        """

        print("╔═══════════════════════╗")  # ╔═══════════════════════╗
        print("║  $$$ LUDOMAN 777 $$$  ║")  # ║  $$$ LUDOMAN 777 $$$  ║
        print("╠═══════╦═══════╦═══════╣")  # ╠═══════╦═══════╦═══════╣
        print("║ ╔═══╗ ║ ╔═══╗ ║ ╔═══╗ ║")  # ║ ╔═══╗ ║ ╔═══╗ ║ ╔═══╗ ║
        print(f"║ ║{a} ║ ║ ║{b} ║ ║ ║{c} ║ ║")  # ║ ║ a ║ ║ ║ b ║ ║ ║ c ║ ║
        print("║ ╚═══╝ ║ ╚═══╝ ║ ╚═══╝ ║")  # ║ ╚═══╝ ║ ╚═══╝ ║ ╚═══╝ ║
        print("╠═══════╩═══════╩═══════╣")  # ╠═══════╩═══════╩═══════╣
        print(f"║  BALANCE: {balance:<11} ║")  # ║  BALANCE: 500         ║
        print(f"║  BET: {bet:<8} [SPIN] ║")  # ║  BET: 10       [SPIN] ║
        print("╚═══════════════════════╝")  # ╚═══════════════════════╝


    def color_print(self, message: str) -> None:
        """
        Делает цветной вывод сообщений
        :return: Ничего не возвращает
        """

        for i in message:
            print(f"\033[01;{random.randint(31, 34)}m{i}", end="")
        print("\033[0m")


    def clear_slot(self) -> None:
        """
        Очищает экран
        :return: Ничего не возвращает
        """

        for i in range(10):
            print("\033[A\033[A")


    def analise_result(self, a: int, b: int, c: int) -> None:
        """
        Анализирует комбинацию и вычисляет выигрыш
        :param a: Число - номер элемента в барабане
        :param b: Число - номер элемента в барабане
        :param c: Число - номер элемента в барабане
        :return: Ничего не возвращает
        """

        symb_a = cons.BARABAN1[a]
        symb_b = cons.BARABAN2[b]
        symb_c = cons.BARABAN3[c]

        if symb_a == symb_b == symb_c:                # Комбинации на 3 символа
            self.balance += self.bet * cons.MULT_3_SYMB[symb_a]

            if symb_a == "💎":
                self.color_print(
                    f"Jackpot! Your prize: {self.bet * cons.MULT_3_SYMB[symb_a]} GC"
                )
                self.jackpot.play()
                time.sleep(5)

            elif symb_a == "💰":
                print(f"Mega win! Your prize: {self.bet * cons.MULT_3_SYMB[symb_a]} GC")
                self.mega_win.play()
                time.sleep(4)

            else:
                print(f"You win! Your prize: {self.bet * cons.MULT_3_SYMB[symb_a]} GC")
                self.win.play()
                time.sleep(2)

        elif symb_a == symb_b or symb_a == symb_c:              # Комбинации на 2 символа

            if symb_a in cons.MULT_2_SYMB:
                self.balance += self.bet * cons.MULT_2_SYMB[symb_a]
                print(f"So good! Your prize: {self.bet * cons.MULT_2_SYMB[symb_a]} GC")
                self.win.play()
                time.sleep(2)

            else:
                print("You need dodep!")
                self.lose.play()
                time.sleep(0.5)

        elif symb_b == symb_c:                                  # Комбинации на 2 символа

            if symb_b in cons.MULT_2_SYMB:
                self.balance += self.bet * cons.MULT_2_SYMB[symb_b]
                print(f"So good! Your prize: {self.bet * cons.MULT_2_SYMB[symb_a]}")
                self.win.play()
                time.sleep(2)

            else:
                print("You need dodep!")
                self.lose.play()
                time.sleep(0.5)

        else:                                      # Секретная комбинация: алмаз, мешок, звезда
            cnt = sum(1 for i in [symb_a, symb_b, symb_c] if i in ("💎", "💰", "⭐"))

            if cnt == 3:
                self.balance += self.bet * 30
                print(f"Not bad, not bad!  Your prize: {self.bet * 30}")
                self.win.play()
                time.sleep(2)
                webbrowser.open("https://yandex.ru/video/preview/7548887151231436014")

            else:                                   # Иначе - проигрыш
                print("You need dodep!")
                self.lose.play()
                time.sleep(0.5)


    @kasik_log
    def spin(self) -> None:
        """
        Основная игровая функция
        :return: Ничего не возвращает
        """

        if self.balance - self.bet > 0:

            self.balance -= self.bet

            # Начальные настройки:
            r = random.randint(70, 100)               # Количество итераций
            a = random.randint(0, cons.LEN_BARABAN)   # Стартовое положение 1 барабана
            b = random.randint(0, cons.LEN_BARABAN)   # Стартовое положение 2 барабана
            c = random.randint(0, cons.LEN_BARABAN)   # Стартовое положение 3 барабана
            d = 0.02                                  # Стартовая задержка

            self.start_spin.play()
            time.sleep(1.25)
            self.music_spin.play()

            print("\n" * 9)         # Отступ для корректной работы

            for i in range(r):

                self.spin_sound.play()
                self.clear_slot()

                self.print_slot(
                    cons.BARABAN1[a % cons.LEN_BARABAN],
                    cons.BARABAN2[b % cons.LEN_BARABAN],
                    cons.BARABAN3[c % cons.LEN_BARABAN],
                    self.balance,
                    self.bet,
                )

                if a <= int(r / 7 * 5):        # Постепенно останавливаем барабаны
                    a += 1
                if b <= int(r / 9 * 8):
                    b += 1
                c += 1

                time.sleep(d)                  # Задержка(постепенно увеличивается)
                d += 0.002

            self.music_spin.stop()

            self.analise_result(               # Анализируем итог
                a % cons.LEN_BARABAN,
                b % cons.LEN_BARABAN,
                (c - 1) % cons.LEN_BARABAN
            )

            self.data[0] = self.balance        # Запись результата в файл
            self.tofile()

        else:
            print("Your balance is empty. Come back tomorrow!")


    @create_log
    def change_bet(self, a: int) -> None:
        """
        Меняет ставку
        :return: Ничего не возвращает
        """

        a -= 1
        if 0 <= a <= 2:
            self.bet = [10, 25, 50][a]

            self.data[1] = self.bet
            self.tofile()

            print(f"Bet set: {self.bet}")

        else:
            print("Wrong bet")
