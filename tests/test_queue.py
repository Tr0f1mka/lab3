import unittest
from unittest.mock import patch
from array import array
from src.queue.queue import Queue


class TestQueue(unittest.TestCase):

    @patch("src.queue.queue.Queue.fromfile")
    @patch("src.queue.queue.Queue.tofile")
    def test_enqueue(self, mock_tofile, mock_fromfile):

        test = Queue()
        test.data = array('d', [3, -2, 5.4])
        expect = array('d', [3, -2, 5.4, -3])
        test.enqueue(-3)
        self.assertEqual(test.data, expect)

        test.data = array('d', [3, -2, 5.4])
        expect = array('d', [3, -2, 5.4, -3.6])
        test.enqueue(-3.6)
        self.assertEqual(test.data, expect)


    @patch("src.queue.queue.Queue.fromfile")
    @patch("src.queue.queue.Queue.tofile")
    def test_dequeue(self, mock_tofile, mock_fromfile):

        test = Queue()
        test.data = array('d', [-3.6, 3, -2, 5.4])
        self.assertEqual(test.dequeue(), -3.6)
        self.assertEqual(len(test.data), 3)

        test.data = array('d', [36, 3, -2, 5, 654])
        self.assertEqual(test.dequeue(), 36)
        self.assertEqual(len(test.data), 4)

        test.data = array('d')
        self.assertEqual(test.dequeue(), "Error: function \"dequeue\" cannot be applied to an empty stack")


    @patch("src.queue.queue.Queue.fromfile")
    @patch("src.queue.queue.Queue.tofile")
    def test_front(self, mock_tofile, mock_fromfile):

        test = Queue()
        test.data = array('d', [-3.6, 3, -2, 5.4])
        self.assertEqual(test.front(), -3.6)
        self.assertEqual(len(test.data), 4)

        test.data = array('d', [36, 3, -2, 5, 654])
        self.assertEqual(test.front(), 36)
        self.assertEqual(len(test.data), 5)

        test.data = array('d', [])
        self.assertEqual(test.front(), "Error: function \"front\" cannot be applied to an empty stack")


    @patch("src.queue.queue.Queue.fromfile")
    @patch("src.queue.queue.Queue.tofile")
    def test_is_empty(self, mock_tofile, mock_fromfile):

        test = Queue()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertFalse(test.is_empty())

        test.data = array('d', [])
        self.assertTrue(test.is_empty())


    @patch("src.queue.queue.Queue.fromfile")
    @patch("src.queue.queue.Queue.tofile")
    def test_len(self, mock_tofile, mock_fromfile):

        test = Queue()
        test.data = array('d', [3, 3, -2, -2, 5.4, -2])
        self.assertEqual(len(test), 6)

        test.data = array('d', [3, 3, -2, -3.6, -3.6])
        self.assertEqual(len(test), 5)

        test.data = array('d', [])
        self.assertEqual(len(test), 0)