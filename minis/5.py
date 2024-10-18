import unittest


def specialize(func, *applied_args, **applied_kwargs):
    def wrapper(*args, **kwargs):
        return func(*applied_args, *args, **applied_kwargs, **kwargs)
    return wrapper


class Tests(unittest.TestCase):
    def testArgs(self):
        def multiply(x, y):
            return x * y

        double = specialize(multiply, 2)
        self.assertEqual(double(10), 20)
        self.assertEqual(double(y=15), 30)

    def testKwargs(self):
        def sum(x, y):
            return x + y

        plus_one = specialize(sum, y=1)
        self.assertEqual(plus_one(10), 11)
        self.assertEqual(plus_one(x=4), 5)
        self.assertEqual(plus_one(x=-42), -41)

    def testDefaults(self):
        def floatEq(x, y, eps=1e-5):
            return abs(x - y) < eps

        close_to_zero = specialize(floatEq, y=0)
        self.assertFalse(close_to_zero(1))
        self.assertFalse(close_to_zero(-4))
        self.assertTrue(close_to_zero(0))
        self.assertTrue(close_to_zero(2, eps=5.0))

    def testEverything(self):
        def foo(a, b, c, d=4):
            return (a + b + c) / d

        partial_foo = specialize(foo, 1, c=3)
        self.assertEqual(partial_foo(2), 1.5)
        self.assertEqual(partial_foo(2, d=2), 3)


if __name__ == "__main__":
    unittest.main()
