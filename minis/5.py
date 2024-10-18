import unittest
import inspect


def specialize(func, *applied_args, **applied_kwargs):
    def wrapper(*args, **kwargs):
        return func(*applied_args, *args, **applied_kwargs, **kwargs)

    args_names = inspect.getfullargspec(func).args
    if len(applied_args) >= len(args_names):
        raise TypeError(f"Too many arguments passed to {func.__name__}")

    formatted_args = ""
    formatted_kwargs = ""
    for i, v in enumerate(applied_args):
        formatted_args += '_' + f"{args_names[i]}_{v}"
    for k, v in applied_kwargs.items():
        formatted_kwargs += '_' + f"{k}_{v}"

    wrapper.__name__ = f"partial_{func.__name__}" + \
        formatted_args +\
        formatted_kwargs

    formatted_args = ""
    formatted_kwargs = ""
    for i, v in enumerate(applied_args):
        formatted_args += ' ' + f"{args_names[i]}={v}"
    for k, v in applied_kwargs.items():
        formatted_kwargs += ' ' + f"{k}={v}"

    wrapper.__doc__ = func.__doc__
    if wrapper.__doc__ is not None and (applied_args or applied_kwargs):
        trailing_dot = '.' if not func.__doc__.endswith('.') else ''
        wrapper.__doc__ += trailing_dot +\
            " Specialized with" + formatted_args + formatted_kwargs
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
            "Foo. Does something"
            return (a + b + c) / d

        partial_foo = specialize(foo, 1, c=3)

        self.assertEqual(partial_foo.__name__, "partial_foo_a_1_c_3")
        self.assertEqual(partial_foo.__doc__,
                         "Foo. Does something. Specialized with a=1 c=3")

        self.assertEqual(partial_foo(2), 1.5)
        self.assertEqual(partial_foo(2, d=2), 3)

    def testTooManyArgs(self):
        def sum(a, b):
            return a + b

        got_exception = False
        try:
            partial_sum = specialize(sum, 1, 2, 3)
        except TypeError:
            got_exception = True

        self.assertTrue(
            got_exception,
            "Expected to get a `TypeError` for too many args"
        )

    def testNewKwarg(self):
        def sum(a, b):
            return a + b

        partial_sum = specialize(sum, c=4)
        got_exception = False
        try:
            partial_sum(1, 2)
        except TypeError:
            got_exception = True

        self.assertTrue(
            got_exception,
            "Expected to get a `TypeError` for wrong kwarg"
        )


if __name__ == "__main__":
    unittest.main()
