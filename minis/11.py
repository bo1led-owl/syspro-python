from typing import Iterable, List, Any, Generator
import copy
import unittest


def take(iter: Iterable, n: int) -> List[Any]:
    res = []
    for i, e in enumerate(iter):
        if i >= n:
            break
        res.append(e)
    return res


def cycle(iter: Iterable) -> Iterable:
    # this is a very strange function because
    # the following code does **not** work if `chain` is a generator because
    # there's no way to copy a generator
    # (even python's own implementation of `cycle` just presaves the values):
    #     a = chain([1, 2], [3, 4])
    #     print(take(cycle(a), 7))

    while True:
        iter_copy = copy.deepcopy(iter)
        yield from iter_copy


def chain(*iters) -> Iterable:
    for iter in iters:
        yield from iter


class TestSuite(unittest.TestCase):
    def testCycle(self):
        self.assertEqual(
            [1, 2, 3, 1, 2, 3, 1, 2],
            take(cycle(range(1, 4)), 8)
        )

    def testChain(self):
        it1 = range(1, 4)
        it2 = [4, 5, 6]
        self.assertEqual(
            [1, 2, 3, 4, 5, 6],
            list(chain(it1, it2))
        )


if __name__ == "__main__":
    unittest.main()
