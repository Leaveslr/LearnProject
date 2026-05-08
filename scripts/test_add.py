import unittest
from add import add


class TestAdd(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_floats(self):
        self.assertAlmostEqual(add(1.1, 2.2), 3.3, places=7)

    def test_add_negative(self):
        self.assertEqual(add(-5, 3), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
