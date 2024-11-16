def singleton(c):
    c_new = c.__new__
    c_init = c.__init__

    def new(c, *args, **kwargs):
        if c.obj is None:
            c.obj = c_new(c)
            c_init(c.obj, *args, **kwargs)
        return c.obj

    # init should do nothing now, because
    # singleton's initialization is handled in `new`
    def init(self, *args, **kwargs):
        pass

    c.obj = None
    c.__new__ = new
    c.__init__ = init
    return c


@singleton
class Foo:
    def __init__(self, x):
        self.x = x


@singleton
class Bar:
    pass


f1 = Foo(1)
f2 = Foo(2)
b1 = Bar()
b2 = Bar()

assert id(f1) == id(f2)
assert f1.x == f2.x
assert f1.x == 1
assert id(b1) == id(b2)
assert id(f1) != id(b1)
