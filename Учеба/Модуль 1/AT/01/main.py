import unittest


def modulo(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    return a % b


class TestModuloFunction(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(modulo(10, 3), 1)

    def test_negative_dividend(self):
        self.assertEqual(modulo(-10, 3), 2)

    def test_negative_divisor(self):
        self.assertEqual(modulo(10, -3), -2)

    def test_zero_dividend(self):
        self.assertEqual(modulo(0, 5), 0)

    def test_division_by_one(self):
        self.assertEqual(modulo(25, 1), 0)

    def test_division_by_self(self):
        self.assertEqual(modulo(7, 7), 0)

    def test_large_numbers(self):
        self.assertEqual(modulo(1000001, 97), 36)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            modulo(10, 0)

if __name__ == "__main__":
    unittest.main()
