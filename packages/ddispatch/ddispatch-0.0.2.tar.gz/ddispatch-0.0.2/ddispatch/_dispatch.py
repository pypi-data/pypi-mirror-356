import inspect

from functools import singledispatch
from typing import overload, TYPE_CHECKING


if TYPE_CHECKING:
    dispatch = overload
else:

    def dispatch(f):
        """Decorator for creating generic functions.

        dispatch uses the type annotation of the first parameter to determine
        the type that the function should be dispatched on. Currently, the type
        annotation must be a single type, rather than a union of types.

        Examples
        --------

        ```{python}
        from ddispatch import dispatch

        @dispatch
        def my_func(x: int) -> int:
            return x + 1
        
        @dispatch
        def my_func(x: str) -> str:
            return x * 3
        
        my_func(1)    # returns 2
        my_func("a")  # returns "aaa"
        ```
        """
        crnt = inspect.currentframe()
        outer = crnt.f_back

        if f.__name__ not in outer.f_locals:
            # no generic function found, so create a new one
            generic = singledispatch(f)
            generic._is_singledispatch = True

            # overwrite the behavior of defaulting to the initial
            # function, then register it explicitly so its first argument
            # type is used.
            generic.register(object, _raise_not_implemented)
            generic.register(f)
            return generic
        else:
            generic = outer.f_locals[f.__name__]
            if not getattr(generic, "_is_singledispatch"):
                raise ValueError(
                    f"Function {f.__name__} does not appear to be a generic function"
                )

            generic.register(f)

            if generic.__doc__ is None and f.__doc__ is not None:
                generic.__doc__ = f.__doc__

            return generic


def _raise_not_implemented(dispatch_on):
    raise TypeError(f"No dispatch implementation for type: {type(dispatch_on)}")
