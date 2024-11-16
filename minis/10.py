def singleton(c):
    c_new = c.__new__

    def new(c):
        if c.obj is None:
            c.obj = c_new(c)
        return c.obj

    c.obj = None
    c.__new__ = new
    return c


@singleton
class Foo:
    pass


@singleton
class Bar:
    pass


f1 = Foo()
f2 = Foo()
b1 = Bar()
b2 = Bar()

assert id(f1) == id(f2)
assert id(b1) == id(b2)
assert id(f1) != id(b1)
