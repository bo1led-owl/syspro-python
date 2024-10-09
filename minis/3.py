import unittest


def parseWierdMatrix(raw: str) -> [[float]]:
    def parseRow(raw_row: str) -> [float]:
        return list(map(int, raw_row.split()))

    return list(map(parseRow, raw.split('|')))


class TestSuite(unittest.TestCase):
    def test(self):
        data = "1 3 2 | 2 1 3"
        self.assertEqual(
            [[1, 3, 2], [2, 1, 3]],
            parseWierdMatrix(data),
            f"input: {data}"
        )


if __name__ == "__main__":
    unittest.main()
