import unittest


def convertToPositive(n: int) -> int:
    if n >= 0:
        return n

    i = 1
    while i <= -n:
        i <<= 1

    # now `i` is a power of 2 and `i > |n|`
    return i - abs(n)  # this is equivalent to removing the signed bit from `n`


def countBits(n: int) -> int:
    result = int(n < 0)
    n = convertToPositive(n)
    while n != 0:
        # `n &= (n - 1)` removes the rightmost set bit of `n`
        # I couldn't find the source of that trick, but on the internet
        # it is called Brian Kernighan's algorithm
        n &= (n - 1)
        result += 1
    return result


class TestSuite(unittest.TestCase):
    def test_positives(self):
        tests = [
            (0, 0),     # 0
            (1, 1),     # 1
            (4, 1),     # 100
            (6, 2),     # 110
            (7, 3),     # 111
            (10, 2),    # 1001
        ]
        for n, correct in tests:
            self.assertEqual(correct, countBits(n), f'input: {n}')

    def test_negatives(self):
        tests = [
            (-1, 2),    # 11        (-2 + 1)
            (-123, 3),  # 10000101  (-128 + 5)
            (-128, 2),  # 110000000 (-256 + 128)
        ]
        for n, correct in tests:
            self.assertEqual(correct, countBits(n), f'input: {n}')


if __name__ == "__main__":
    unittest.main()
