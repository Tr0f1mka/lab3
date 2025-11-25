import unittest
import src.math_func as math_f


class TestMathFunc(unittest.TestCase):

    def test_fact_iter(self):

        testcase = [
            [7, 5040],
            [3, 6],
            [10, 3628800],
            [1, 1],
            [0, 1],
            [-34, "Error: undefined element with index -34"]
        ]

        for i in range(len(testcase)):
            self.assertEqual(math_f.factorial(testcase[i][0]), testcase[i][1])


    def test_fact_rec(self):

        testcase = [
            [7, 5040],
            [3, 6],
            [10, 3628800],
            [1, 1],
            [0, 1],
            [-34, "Error: undefined element with index -34"]
        ]

        for i in range(10):
            math_f.factorial_recursive(i)

        for i in range(len(testcase)):
            self.assertEqual(math_f.factorial_recursive(testcase[i][0]), testcase[i][1])


    def test_fibo(self):
        testcase = [
            [20, 6765],
            [10, 55],
            [6, 8],
            [1, 1],
            [0, 0],
            [-23, "Error: undefined element with index -23"]
        ]

        for i in range(len(testcase)):
            self.assertEqual(math_f.fibo(testcase[i][0]), testcase[i][1])


    def test_fibo_rec(self):
        testcase = [
            [20, 6765],
            [10, 55],
            [6, 8],
            [1, 1],
            [0, 0],
            [-23, "Error: undefined element with index -23"]
        ]

        for i in range(20):
            math_f.fibo_recursive(i)

        for i in range(len(testcase)):
            self.assertEqual(math_f.fibo_recursive(testcase[i][0]), testcase[i][1])
