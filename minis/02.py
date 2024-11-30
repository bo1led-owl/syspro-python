import unittest


def myZip(lhs: list, rhs: list) -> [tuple]:
    min_len = min(len(lhs), len(rhs))
    return [(lhs[i], rhs[i]) for i in range(min_len)]


class TestSuite(unittest.TestCase):
    def testBasic(self):
        tests = [
            ([1, 2, 3], [4, 5, 6]),
            (['a', 2, 3.0], ['4', [], ()]),
            ([], []),
        ]
        for lhs, rhs in tests:
            self.assertEqual(myZip(lhs, rhs), list(zip(lhs, rhs)),
                             f'lhs = {lhs}, rhs = {rhs}')
            self.assertEqual(myZip(rhs, lhs), list(zip(rhs, lhs)),
                             f'lhs = {rhs}, rhs = {lhs}')

    def testDifferentLength(self):
        tests = [
            ([1, 2, 3], [4, 5]),
            ([1, 2, 3], [4]),
            ([1, 2, 3], []),
            ([4, 5], [1, 2, 3]),
            ([4], [1, 2, 3]),
            ([], [1, 2, 3]),
        ]
        for lhs, rhs in tests:
            self.assertEqual(myZip(lhs, rhs), list(zip(lhs, rhs)),
                             f'lhs = {lhs}, rhs = {rhs}')
            self.assertEqual(myZip(rhs, lhs), list(zip(rhs, lhs)),
                             f'lhs = {rhs}, rhs = {lhs}')


if __name__ == "__main__":
    unittest.main()
