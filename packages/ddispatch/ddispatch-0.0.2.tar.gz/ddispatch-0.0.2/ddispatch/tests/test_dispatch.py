import pytest

from ddispatch import dispatch


@dispatch
def f_out(x: str) -> int:
    return int(x)


def create_generic():
    @dispatch
    def f_inner(x: int) -> int:
        return x + 1

    @dispatch
    def f_inner(x: str) -> int:
        return int(x) + 1

    return f_inner


@dispatch
def f_out(x: int) -> str:
    return str(x)


def test_basic():
    assert f_out(1) == "1"
    assert f_out("1") == 1


def test_inner():
    f = create_generic()
    assert f(1) == 2
    assert f("1") == 2


def test_inner_new_registration():
    f = create_generic()

    @dispatch
    def f(x: bool) -> str:
        return "a bool"

    assert f(1) == 2
    assert f(True) == "a bool"


def test_dispatch_default():
    @dispatch
    def f(x: object):
        return x

    f(1)


def test_dispatch_no_default():
    @dispatch
    def f(x: int):
        return x

    f(1)

    with pytest.raises(TypeError) as exc_info:
        f("a")


def test_dispatch_on_abc():
    from abc import ABC

    class Base(ABC): ...

    Base.register(int)

    @dispatch
    def f(x: Base):
        return x

    f(1)

    with pytest.raises(TypeError) as exc_info:
        f("a")


def test_dispatch_uses_final_docstring():
    @dispatch
    def f(x: int) -> int:
        return x + 1

    @dispatch
    def f(x: str) -> str:
        """This is the final docstring."""
        return x * 2

    assert f.__doc__ == "This is the final docstring."