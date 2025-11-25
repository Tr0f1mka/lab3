import unittest
from src.utilities.check_list import scan_type, check_list


class TestCheckList(unittest.TestCase):

    def test_scan_type_with_float(self):

        self.assertEqual(scan_type("12.4"), float)
        self.assertEqual(scan_type("-12.4"), float)
        self.assertEqual(scan_type("+12.4"), float)
        self.assertEqual(scan_type("12.0"), float)
        self.assertEqual(scan_type("0.0"), float)


    def test_scan_type_with_int(self):

        self.assertEqual(scan_type("12"), int)
        self.assertEqual(scan_type("+12"), int)
        self.assertEqual(scan_type("-12"), int)
        self.assertEqual(scan_type("0"), int)


    def test_scan_type_with_str(self):

        self.assertEqual(scan_type("abc"), str)
        self.assertEqual(scan_type("123a54"), str)
        self.assertEqual(scan_type("123.a4"), str)
        self.assertEqual(scan_type("-234a"), str)
        self.assertEqual(scan_type("23-e5"), str)
        self.assertEqual(scan_type("+23+34"), str)
        self.assertEqual(scan_type("+*"), str)
        self.assertEqual(scan_type("-45/5"), str)
        self.assertEqual(scan_type("12..3"), str)



    def test_check_list_int(self):

        self.assertEqual(check_list(["234", "-235", "000", "+76", "1"]), [234, -235, 0, 76, 1])
        self.assertEqual(check_list(["4", "-5", "9", "7", "1"]), [4, -5, 9, 7, 1])
        self.assertEqual(check_list(["234", "+5", "0", "8"]), [234, 5, 0, 8])


    def test_check_list_float(self):

        self.assertEqual(check_list(["234.0", "-235.56", "0.1", "+76.67", "1.6"]), [234.0, -235.56, 0.1, +76.67, 1.6])
        self.assertEqual(check_list(["4.89", "-5.5", "9", "7.100", "1.0000"]), [4.89, -5.5, 9.0, 7.1, 1.0])
        self.assertEqual(check_list(["234", "+5", "0.6", "8"]), [234.0, 5.0, 0.6, 8.0])


    def test_check_list_str(self):

        self.assertEqual(check_list(["ikm", "rt", "gfd", "+e", "s"]), ["ikm", "rt", "gfd", "+e", "s"])
        self.assertEqual(check_list(["4.56", "-5.7", "9a", "7.9", "1.43"]), ["4.56", "-5.7", "9a", "7.9", "1.43"])
        self.assertEqual(check_list(["234", "+5", "qwe", "+"]), ["234", "+5", "qwe", "+"])


    def test_check_list_empty(self):

        self.assertEqual(check_list([]), [])
