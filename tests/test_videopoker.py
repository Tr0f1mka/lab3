import unittest
from unittest.mock import patch
from src.kasino.videopoker import VideoPoker

# Тесты чеков комбинаций
class TestVideoPoker(unittest.TestCase):

    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_flush_royal(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[[1, 1, 1, 1, 1], [8, 9, 10, 11, 12]], True],
            [[[1, 1, 1, 2, 1], [8, 9, 10, 11, 12]], False],
            [[[3, 3, 3, 3, 3], [7, 8, 9,  10, 11]], False]
        ]

        for i in testcase:
            self.assertEqual(test.check_flush_royal(*i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_street_flush(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[[1, 1, 1, 1, 1], [8, 9, 10, 11, 12]], True],
            [[[1, 1, 1, 2, 1], [8, 9, 10, 11, 12]], False],
            [[[3, 3, 3, 3, 3], [7, 8, 9,  10, 11]], True],
            [[[0, 0, 0, 0, 0], [1, 3, 4,  5,  6]], False],
            [[[2, 2, 2, 2, 2], [0, 1, 2,  3,  12]], True]
        ]

        for i in testcase:
            self.assertEqual(test.check_street_flush(*i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_kara(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[1, 1, 1, 1, 1], False],
            [[1, 1, 1, 1, 2], True],
            [[2, 3, 3, 3, 7], False]
        ]

        for i in testcase:
            self.assertEqual(test.check_kara(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_full_house(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[1, 1, 1, 1, 1], False],
            [[1, 1, 1, 2, 2], True],
            [[3, 3, 12, 12, 12], True]
        ]

        for i in testcase:
            self.assertEqual(test.check_full_house(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_flush(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[1, 1, 1, 1, 1], True],
            [[1, 1, 1, 1, 2], False],
            [[2, 3, 2, 3, 3], False]
        ]

        for i in testcase:
            self.assertEqual(test.check_flush(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_street(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[2, 3, 4, 5, 6], True],
            [[0, 1, 2, 3, 12], True],
            [[2, 3, 3, 3, 7], False]
        ]

        for i in testcase:
            self.assertEqual(test.check_street(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_set(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[2, 2, 2, 3, 6], True],
            [[1, 1, 1, 1, 2], False],
            [[2, 3, 3, 3, 7], True]
        ]

        for i in testcase:
            self.assertEqual(test.check_set(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_2_pairs(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[1, 1, 2, 3, 3], True],
            [[5, 5, 8, 8, 12], True],
            [[2, 3, 3, 3, 7], False]
        ]

        for i in testcase:
            self.assertEqual(test.check_2_pairs(i[0]), i[1])


    @patch("src.kasino.videopoker.VideoPoker.fromfile")
    @patch("src.kasino.videopoker.VideoPoker.tofile")
    @patch("src.kasino.videopoker.VideoPoker.init_params")
    def test_pair_tens_and_more(self, mock_init, mock_tofile, mock_fromfile):

        test = VideoPoker()

        testcase = [
            [[1, 1, 2, 3, 4], False],
            [[5, 6, 8, 8, 12], True],
            [[2, 10, 10, 11, 12], True]
        ]

        for i in testcase:
            self.assertEqual(test.check_pair_tens_and_more(i[0]), i[1])
