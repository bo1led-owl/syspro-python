import unittest


def parseWierdMatrix(raw: str) -> [[float]]:
    def parseRow(raw_row: str) -> [float]:
        return list(map(float, raw_row.split()))

    return list(map(parseRow, raw.split('|')))


class TestSuite(unittest.TestCase):
    def testBasic(self):
        data = "1 3 2 | 2 1 3"
        self.assertEqual(
            [[1, 3, 2], [2, 1, 3]],
            parseWierdMatrix(data),
            f"input: {data}"
        )

    def testManyRows(self):
        data = "1|2|3|4|5|6|7|8"
        self.assertEqual(
            [[1], [2], [3], [4], [5], [6], [7], [8]],
            parseWierdMatrix(data),
            f"input: {data}"
        )

    def testTooMuchWhitespace(self):
        data = "  1  \t\n \r 3   2  \r\n|\t  \t2  \t\r\v 1   3 "
        self.assertEqual(
            [[1, 3, 2], [2, 1, 3]],
            parseWierdMatrix(data),
            f"input: {data}"
        )


if __name__ == "__main__":
    unittest.main()
