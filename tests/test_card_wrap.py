import unittest
from src.utilities.card_wrap import wrap


class TestWrap(unittest.TestCase):

    def test_wrap_shirt(self):

        expect = [
            "\033[01;48;05;15m\033[01;38;05;232m┌───────────┐\033[0m",
            "\033[01;48;05;15m\033[01;38;05;232m│░░░░░░░░░░░│\033[0m",
            "\033[01;48;05;15m\033[01;38;05;232m└───────────┘\033[0m"
            ]

        testcase = [0, 5, 8]

        for i in range(len(testcase)):
            self.assertEqual(wrap(52, testcase[i]), expect[i])


    def test_wrap_card(self):

        expect = [
            "\033[01;48;05;15m\033[01;38;05;232m│♠ ┌─────┐  │\033[0m",
            "\033[01;48;05;15m\033[01;38;05;232m│  │ \033[01;38;05;196m♦\033[01;38;05;232m \033[01;38;05;196m♦\033[01;38;05;232m │  │\033[0m",
            "\033[01;48;05;15m\033[01;38;05;232m│          9│\033[0m"
        ]

        testcase = [
            [0, 2],
            [3, 3],
            [7, 7]
        ]

        for i in range(len(testcase)):
            self.assertEqual(wrap(*testcase[i]), expect[i])
