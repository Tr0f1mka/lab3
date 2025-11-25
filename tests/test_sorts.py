import unittest
from src.utilities.check_list import check_list
import src.sorts as sorts


class TestSorts(unittest.TestCase):

    def test_bubble_sort(self):

        expect = [
            ["qwe", "qwr", "qwr", "t", "tg", "wer"],
            [-324, 0, 7, 34, 123],
            [-23.0, 3.45, 56.4, 56.7, 234.0],
            ['45', '56.1', 'aq'],
            []
        ]

        testcase = [
            ["qwe", "tg", "qwr", "t", "wer", "qwr"],
            ["123", "-324", "34", "0", "7"],
            ["56.7", "56.4", "-23.0", "234", "3.45"],
            ["aq", "56.1", "45"],
            []
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.bubble_sort(testcase[i]), expect[i])


    def test_quick_sort(self):

        expect = [
            ["qwe", "qwr", "qwr", "t", "tg", "wer"],
            [-324, 0, 7, 34, 123],
            [-23.0, 3.45, 56.4, 56.7, 234.0],
            ['45', '56.1', 'aq'],
            []
        ]

        testcase = [
            ["qwe", "tg", "qwr", "t", "wer", "qwr"],
            ["123", "-324", "34", "0", "7"],
            ["56.7", "56.4", "-23.0", "234", "3.45"],
            ["aq", "56.1", "45"],
            []
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.quick_sort(check_list(testcase[i])), expect[i])


    def test_counting_sort(self):

        expect = [
            [45, 45, 234, 567, 5443],
            [-567, -45, 45, 234, 5443],
            [0, 45, 45, 234, 567],
            []
        ]

        testcase = [
            [45, 567, 5443, 234, 45],
            [45, -567, 5443, 234, -45],
            [45, 567, 0, 234, 45],
            []
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.counting_sort(testcase[i]), expect[i])


    def test_radix_sort(self):

        expect = [
            ["3", "10", "16", "726", "765"],
            ["3", "d0", "e6", "7b5", "a26"],
            ["0", "101", "110", "1001", "11001"],
            []
        ]

        testcase = [
            [["10", "765", "3", "16", "726"]],
            [["d0", "7b5", "3", "e6", "a26"], 16],
            [["1001", "110", "101", "0", "11001"], 2],
            [[]]
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.radix_sort(*testcase[i]), expect[i])

        with self.assertRaises(ValueError) as e:
            sorts.radix_sort(["34.5", "5", "23", "45"])
            self.assertEqual(e, "Error: radix sort does not work with real numbers.")


    def test_bucket_sort(self):

        expect = [
            [45, 45, 234, 567, 5443],
            [-567, -45, 45, 234, 5443],
            [0, 45.34, 45.56, 234.987, 567],
            [0, 0, 0, 0, 0],
            []
        ]

        testcase = [
            [[45, 567, 5443, 234, 45]],
            [[45, -567, 5443, 234, -45], 3],
            [[45.34, 567, 0, 234.987, 45.56]],
            [[0, 0, 0, 0, 0], 20],
            [[]]
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.bucket_sort(*testcase[i]), expect[i])




    def test_build_tree(self):

        testcase = [
            [["qwe", "tg", "qwr", "t", "wer", "qwr"], 6, 1],
            [[-324, 123, 34, 0, 7], 5, 0],
            [[56.7, 56.4, -23.0, 234.0, 3.45], 5, 1],
            [[], 0, 0]
        ]

        expect = [
            ["qwe", "wer", "qwr", "t", "tg", "qwr"],
            [123, 7, 34, 0, -324],
            [56.7, 234.0, -23.0, 56.4, 3.45],
            []
        ]

        for i in range(len(testcase)):
            sorts.build_tree(*testcase[i])
            self.assertEqual(testcase[i][0], expect[i])


    def test_heap_sort(self):

        expect = [
            ["qwe", "qwr", "qwr", "t", "tg", "wer"],
            [-324, 0, 7, 34, 123],
            [-23.0, 3.45, 56.4, 56.7, 234.0],
            ['45', '56.1', 'aq'],
            []
        ]

        testcase = [
            ["qwe", "tg", "qwr", "t", "wer", "qwr"],
            ["123", "-324", "34", "0", "7"],
            ["56.7", "56.4", "-23.0", "234", "3.45"],
            ["aq", "56.1", "45"],
            []
        ]

        for i in range(len(testcase)):
            self.assertEqual(sorts.heap_sort(testcase[i]), expect[i])
