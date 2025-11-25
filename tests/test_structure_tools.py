import unittest
from src.utilities.structure_tools import check_int


class TestStructureTools(unittest.TestCase):

    def test_check_int_int(self):
        testcase = 1.0
        result = check_int(testcase)
        self.assertEqual(testcase, result)
        self.assertEqual(type(result), int)

    def test_check_int_float(self):
        testcase = 1.1
        result = check_int(testcase)
        self.assertEqual(testcase, result)
        self.assertEqual(type(result), float)
