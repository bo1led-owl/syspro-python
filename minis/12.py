import unittest


def coroutine(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        next(res)
        return res
    return wrapper


@coroutine
def adder(start):
    res = start
    while True:
        res += yield res


class TestSuite(unittest.TestCase):
    def testCoro(self):
        add = adder(0)
        self.assertEqual(1, add.send(1))
        self.assertEqual(3, add.send(2))
        self.assertEqual(6, add.send(3))
        self.assertEqual(10, add.send(4))


if __name__ == "__main__":
    unittest.main()
