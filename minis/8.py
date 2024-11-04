from typing import List, Any
from textwrap import dedent
import functools
import unittest


def calculateColumnWidths(table: List[List[Any]]) -> List[int]:
    def getColumn(col_index: int, table: List[List[Any]]) -> List[Any]:
        return map(lambda row: row[col_index], table)

    def getColumnWidth(column: List[Any]) -> int:
        def getFormattedLength(x: Any) -> int:
            return len(str(x))
        return max(map(getFormattedLength, column))

    column_getter = functools.partial(getColumn, table=table)

    columns_count = len(table[0])
    columns = map(column_getter, range(columns_count))
    return list(map(getColumnWidth, columns))


def formatRow(row: List, column_widths: List[int]) -> str:
    formatted_columns = map(
        lambda item, width: f" {item:<{width}} ",
        row,
        column_widths,
    )
    return '|' + '|'.join(formatted_columns) + '|'


def makeSeparatorLine(column_widths: List[int]) -> str:
    column_widths_sum = sum(column_widths)
    spaces_count = 2 * len(column_widths)
    separator_bar_count = len(column_widths) - 1
    dash_count = column_widths_sum + spaces_count + separator_bar_count
    return f"|{'-' * dash_count}|"


def formatBenchmarkTable(
    row_titles: List[str],
    column_titles: List[str],
    data: List[List[Any]]
) -> str:
    assert len(data) > 0

    # assert that the table is peferctly rectangular
    assert all(map(lambda row: len(row) == len(data[0]), data))
    assert len(column_titles) == len(data[0])
    assert len(row_titles) == len(data)

    table = [["Benchmark", *column_titles]]
    table += list(map(lambda title, row: [title, *row], row_titles, data))

    column_widths = calculateColumnWidths(table)

    formatter = functools.partial(formatRow, column_widths=column_widths)
    formatted_rows = list(map(formatter, table))
    formatted_rows.insert(1, makeSeparatorLine(column_widths))
    return '\n'.join(formatted_rows)


class TestSuite(unittest.TestCase):
    def testBasic(self):
        actual = formatBenchmarkTable(
            ["best case", "worst case"],
            ["quick sort", "merge sort", "bubble sort"],
            [
                [1.23, 1.56, 2.0],
                [3.3, 2.9, 3.9],
            ]
        )
        expected = dedent("""\
                | Benchmark  | quick sort | merge sort | bubble sort |
                |----------------------------------------------------|
                | best case  | 1.23       | 1.56       | 2.0         |
                | worst case | 3.3        | 2.9        | 3.9         |""")
        self.assertEqual(actual, expected)

    def testDifferentData(self):
        actual = formatBenchmarkTable(
            ["best case", "worst case"],
            ["quick sort", "merge sort", "bubble sort"],
            [
                [1.23, 1.56, 2],
                [3.3, "2.9", 3.9],
            ]
        )
        expected = dedent("""\
                | Benchmark  | quick sort | merge sort | bubble sort |
                |----------------------------------------------------|
                | best case  | 1.23       | 1.56       | 2           |
                | worst case | 3.3        | 2.9        | 3.9         |""")
        self.assertEqual(actual, expected)

    def testWideColumns(self):
        actual = formatBenchmarkTable(
            ["best case", "the very worst case"],
            ["quick sort", "bubble sort"],
            [
                ["not that much", 2],
                [3.3, "very long time"],
            ],
        )

        expected = dedent("""\
                | Benchmark           | quick sort    | bubble sort    |
                |------------------------------------------------------|
                | best case           | not that much | 2              |
                | the very worst case | 3.3           | very long time |""")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
