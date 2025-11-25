import unittest
from unittest.mock import patch
from random import seed
from src.kasino.blackjack import BlackJack


class TestBlackJack(unittest.TestCase):

    @patch("src.kasino.blackjack.BlackJack.fromfile")
    @patch("src.kasino.blackjack.BlackJack.tofile")
    @patch("src.kasino.blackjack.BlackJack.init_params")
    def test_counting(self, mock_init, mock_tofile, mock_fromfile):

        test = BlackJack()

        testcase = [
            [[34, 3], 15],
            [[0, 13, 26, 1, 39, 14, 12, 27, 40], 21],
            [[51, 38], 12],
            [[38, 36], 21]
        ]

        for i in testcase:
            self.assertEqual(test.counting(i[0]), i[1])


    @patch("src.kasino.blackjack.BlackJack.fromfile")
    @patch("src.kasino.blackjack.BlackJack.tofile")
    @patch("src.kasino.blackjack.BlackJack.init_params")
    @patch("src.kasino.blackjack.BlackJack.user_input")
    @patch("src.kasino.blackjack.BlackJack.print_hand")
    @patch("src.kasino.blackjack.BlackJack.clear_table")
    def test_init_game(self, mock_clear, mock_cout, mock_cin, mock_init, mock_tofile, mock_fromfile):

        test = BlackJack()

        test.balance = 500      # Инициализация нужных параметров
        test.bet = 50

        test.init_game()

        self.assertEqual(len(test.local_deck), 48)
        self.assertEqual(len(test.player_hand), 2)
        self.assertEqual(len(test.dealer_hand), 2)


    @patch("src.kasino.blackjack.BlackJack.fromfile")
    @patch("src.kasino.blackjack.BlackJack.tofile")
    @patch("src.kasino.blackjack.BlackJack.init_params")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_more(self, mock_cout, mock_cin, mock_init, mock_tofile, mock_fromfile):

        seed(10)
        test = BlackJack()

        test.balance = 500        # Инициализация нужных параметров
        test.bet = 50
        test.init_game()
        balance_before = test.balance
        bet_before = test.bet
        player_hand_before = [x for x in test.player_hand]
        player_cnt_before = test.player_cnt
        dealer_hand_before = [x for x in test.dealer_hand]
        dealer_cnt_before = test.dealer_cnt

        test.more()

        self.assertEqual(test.balance, balance_before)
        self.assertEqual(test.bet, bet_before)
        self.assertEqual(len(test.player_hand), 3)
        self.assertEqual(len(test.dealer_hand), 2)
        self.assertEqual(test.player_hand[:2], player_hand_before)
        self.assertEqual(test.dealer_hand, dealer_hand_before)
        self.assertNotEqual(test.player_cnt, player_cnt_before)
        self.assertEqual(test.dealer_cnt, dealer_cnt_before)


    @patch("src.kasino.blackjack.BlackJack.fromfile")
    @patch("src.kasino.blackjack.BlackJack.tofile")
    @patch("src.kasino.blackjack.BlackJack.init_params")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_double(self, mock_cout, mock_cin, mock_init, mock_tofile, mock_fromfile):

        seed(10)
        test = BlackJack()

        test.balance = 500        # Инициализация нужных параметров
        test.bet = 50
        test.init_game()
        balance_before = test.balance
        bet_before = test.bet
        player_hand_before = [x for x in test.player_hand]
        player_cnt_before = test.player_cnt
        dealer_hand_before = [x for x in test.dealer_hand]
        dealer_cnt_before = test.dealer_cnt

        test.double()

        self.assertEqual(test.balance, balance_before-bet_before)
        self.assertEqual(test.bet, bet_before*2)
        self.assertEqual(len(test.player_hand), 3)
        self.assertEqual(len(test.dealer_hand), 2)
        self.assertEqual(test.player_hand[:2], player_hand_before)
        self.assertEqual(test.dealer_hand, dealer_hand_before)
        self.assertNotEqual(test.player_cnt, player_cnt_before)
        self.assertEqual(test.dealer_cnt, dealer_cnt_before)
