import unittest
from unittest.mock import patch
from array import array
from src.stack.stack import Stack


class TestStack(unittest.TestCase):

    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_push(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        expect = array('d', [3, 3, -2, -2, 5.4, -2, -3, -3])
        test.push(-3)
        self.assertEqual(test.data, expect)

        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        expect = array('d', [3, 3, -2, -2, 5.4, -2, -3.6, -3.6])
        test.push(-3.6)
        self.assertEqual(test.data, expect)


    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_pop(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertEqual(test.pop(), 5.4)
        self.assertEqual(len(test.data), 4)

        test.data = array('d', [3, 3, -2, -2, 5.4, -2, -3.6, -3.6])
        self.assertEqual(test.pop(), -3.6)
        self.assertEqual(len(test.data), 6)

        test.data = array('d', [])
        with self.assertRaises(IndexError) as e:
            test.pop()
            self.assertEqual(e, "Error: function \"pop\" cannot be applied to an empty stack")


    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_peek(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertEqual(test.peek(), 5.4)
        self.assertEqual(len(test.data), 6)

        test.data = array('d', [3, 3, -2, -2, 5.4, -2, -3.6, -3.6])
        self.assertEqual(test.peek(), -3.6)
        self.assertEqual(len(test.data), 8)

        test.data = array('d', [])
        with self.assertRaises(IndexError) as e:
            test.pop()
            self.assertEqual(e, "Error: function \"peek\" cannot be applied to an empty stack")


    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_is_empty(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertFalse(test.is_empty())

        test.data = array('d', [])
        self.assertTrue(test.is_empty())


    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_len(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertEqual(len(test), 3)

        test.data = array('d', [3, 3, -2, -2, 5.4, -2, -3.6, -3.6])
        self.assertEqual(len(test), 4)

        test.data = array('d', [])
        self.assertEqual(len(test), 0)


    @patch("src.stack.stack.Stack.fromfile")
    @patch("src.stack.stack.Stack.tofile")
    def test_min(self, mock_tofile, mock_fromfile):

        test = Stack()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertEqual(test.min(), -2)

        test.data = array('d', [3, 3, -2, -2, 5.4, -2, -3.6, -3.6])
        self.assertEqual(test.min(), -3.6)

        test.data = array('d', [])
        with self.assertRaises(IndexError) as e:
            test.pop()
            self.assertEqual(e, "Error: function \"min\" cannot be applied to an empty stack")
