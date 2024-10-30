import functools

# tests runner is in `./minis/test7.sh`
# expected test result is in `./minis/7.expected`


def deprecated(f=None, *, since=None, will_be_removed=None):
    if f is None:
        return functools.partial(deprecated,
                                 since=since,
                                 will_be_removed=will_be_removed)

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            since_msg = f" since version {since}" if since else ""
            removed_in_msg = ""
            if will_be_removed:
                removed_in_msg = f"version {will_be_removed}"
            else:
                removed_in_msg = "future versions"

            msg = (f"Function `{f.__name__}` is deprecated{since_msg}. "
                   f"It will be removed in {removed_in_msg}.")

            print(msg)
            return f(*args, **kwargs)

        return wrapper
    return decorator(f)


@deprecated(since="1.0.1", will_be_removed="1.1.0")
def foo(a, b, **kwargs):
    """Foo"""
    print(f"I'm foo! I got {a}, {b} and {kwargs}")


@deprecated(since="1.0.1")
def bar(*args):
    """Bar"""
    print(f"I'm bar! I summed my args: {sum(args)}!")


@deprecated(will_be_removed="1.1.0")
def baz(arg=None):
    """Baz"""
    print(f"I'm baz! I have a kwarg: {arg}")


@deprecated
def fuzz():
    """Fuzz"""
    print("I'm fuzz!")


assert foo.__doc__ == "Foo"
assert bar.__doc__ == "Bar"
assert baz.__doc__ == "Baz"
assert fuzz.__doc__ == "Fuzz"

foo(1, 2, c=42)
bar(1, 2, 3, 4)
baz(arg="MESSAGE")
fuzz()
