from typing import Any, Optional
from functools import reduce
import unittest


def flatten(items: list, depth: Optional[int] = None) -> list:
    if not isinstance(items, list):
        return [items]

    if depth == 0:
        return items

    next_depth = depth - 1 if depth else None
    return reduce(
        lambda a, b: a + flatten(b, depth=next_depth),
        items,
        []
    )


class TestSuite(unittest.TestCase):
    def testNoDepth(self):
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]]),
            [1, 2, 3, 4, 5, 6]
        )

    def testZeroDepth(self):
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]], depth=0),
            [1, [2, 3], [4, [5, [6]]]]
        )

    def testInsufficientDepth(self):
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]], depth=1),
            [1, 2, 3, 4, [5, [6]]]
        )
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]], depth=2),
            [1, 2, 3, 4, 5, [6]]
        )

    def testIdealDepth(self):
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]], depth=3),
            [1, 2, 3, 4, 5, 6]
        )

    def testExceedingDepth(self):
        self.assertEqual(
            flatten([1, [2, 3], [4, [5, [6]]]], depth=4),
            [1, 2, 3, 4, 5, 6]
        )

    def testFlat(self):
        self.assertEqual(
            flatten([1, 2, 3, 4, 5, 6]),
            [1, 2, 3, 4, 5, 6]
        )
        self.assertEqual(
            flatten([1, 2, 3, 4, 5, 6], depth=42),
            [1, 2, 3, 4, 5, 6]
        )

    def testCollectionsInside(self):
        self.assertEqual(
            flatten([[{1, 2}, {3, 4}], {5}]),
            [{1, 2}, {3, 4}, {5}]
        )


if __name__ == "__main__":
    unittest.main()
