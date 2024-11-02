from typing import List
from textwrap import dedent
import unittest


def getFormattedLength(x) -> int:
    return len(str(x))


def formatRow(row: List, column_widths: List[int]) -> str:
    result = '|'
    for column_index, item in enumerate(row):
        column_len = column_widths[column_index]
        result += f" {item:<{column_len}} |"
    return result


def makeSeparatorLine(column_widths: List[int]) -> str:
    column_widths_sum = sum(column_widths)
    spaces_count = 2 * len(column_widths)
    separator_bar_count = len(column_widths) - 1
    dash_count = column_widths_sum + spaces_count + separator_bar_count
    return f"|{'-' * dash_count}|"


def formatBenchmarkTable(
    row_titles: List[str],
    column_titles: List[str],
    data: List[List]
) -> str:
    table = [["Benchmark", *column_titles]]
    for i, row in enumerate(data):
        table.append([row_titles[i], *row])

    column_widths = []
    for column_index in range(max(map(len, table))):
        column = [row[column_index] for row in table]
        cur_width = max(map(getFormattedLength, column))
        column_widths.append(cur_width)

    formatted_table = list(
        map(lambda row: formatRow(row, column_widths), table)
    )
    formatted_table.insert(1, makeSeparatorLine(column_widths))
    return '\n'.join(formatted_table)


class TestSuite(unittest.TestCase):
    def testBasic(self):
        actual = formatBenchmarkTable(["best case", "worst case"],
                                      ["quick sort", "merge sort",
                                       "bubble sort"],
                                      [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]])
        expected = dedent("""\
                | Benchmark  | quick sort | merge sort | bubble sort |
                |----------------------------------------------------|
                | best case  | 1.23       | 1.56       | 2.0         |
                | worst case | 3.3        | 2.9        | 3.9         |""")
        self.assertEqual(actual, expected)

    def testDifferentData(self):
        actual = formatBenchmarkTable(["best case", "worst case"],
                                      ["quick sort", "merge sort",
                                       "bubble sort"],
                                      [[1.23, 1.56, 2], [3.3, "2.9", 3.9]])
        expected = dedent("""\
                | Benchmark  | quick sort | merge sort | bubble sort |
                |----------------------------------------------------|
                | best case  | 1.23       | 1.56       | 2           |
                | worst case | 3.3        | 2.9        | 3.9         |""")
        self.assertEqual(actual, expected)

    def testWideColumns(self):
        actual = formatBenchmarkTable(["best case", "the very worst case"],
                                      ["quick sort", "bubble sort"],
                                      [["not that much", 2],
                                       [3.3, "very long time"],
                                       ])

        expected = dedent("""\
                | Benchmark           | quick sort    | bubble sort    |
                |------------------------------------------------------|
                | best case           | not that much | 2              |
                | the very worst case | 3.3           | very long time |""")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
