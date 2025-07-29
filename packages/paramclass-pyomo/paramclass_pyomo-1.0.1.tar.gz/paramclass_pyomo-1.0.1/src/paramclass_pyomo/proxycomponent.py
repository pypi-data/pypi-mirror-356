import pyomo.environ as pyo

class ProxyComponent():
    __protected__ = [
        '__protected__',
        '__component__',
    ]
    def __init__(self, component:pyo.Component) -> None:
        self.__component__ = component
    def __getattr__(self, name):
        if name in self.__protected__: return super().__getattribute__(name)
        else: return getattr(self.__component__, name)
    def __setattr__(self, name, value):
        if name in self.__protected__: super().__setattr__(name, value)
        else: setattr(self.__component__, name, value)
    def __delattr__(self, name):
        if name in self.__protected__: super().__delattr__(name)
        else: delattr(self.__component__, name)
    def __len__(self): return len(self.__component__)
    def __getitem__(self, index): return self.__component__[index]
    def __setitem__(self, index, value): self.__component__[index] = value
    def __delitem__(self, index): del self.__component__[index]
    def __iter__(self): return iter(self.__component__)
    def __contains__(self, item): return item in self.__component__
    def __call__(self, *args, **kwargs): return self.__component__(*args, **kwargs)
    def __eq__(self, other): return self.__component__ == other
    def __lt__(self, other): return self.__component__ < other
    def __le__(self, other): return self.__component__ <= other
    def __gt__(self, other): return self.__component__ > other
    def __ge__(self, other): return self.__component__ >= other
    def __ne__(self, other): return self.__component__ != other
    def __hash__(self): return hash(self.__component__)
    def __bool__(self): return bool(self.__component__)
    def __str__(self): return str(self.__component__)
    def __repr__(self): return f'ProxyComponent {repr(self.__component__)}'
    def __format__(self, format_spec): return format(self.__component__, format_spec)
    def __enter__(self): return self.__component__.__enter__()
    def __exit__(self, exc_type, exc_value, traceback): return self.__component__.__exit__(exc_type, exc_value, traceback)
    def __neg__(self): return -self.__component__
    def __add__(self, other): return self.__component__ + other
    def __radd__(self, other): return other + self.__component__
    def __sub__(self, other): return self.__component__ - other
    def __rsub__(self, other): return other - self.__component__
    def __mul__(self, other): return self.__component__ * other
    def __rmul__(self, other): return other * self.__component__
    def __truediv__(self, other): return self.__component__ / other
    def __rtruediv__(self, other): return other / self.__component__
    def __floordiv__(self, other): return self.__component__ // other
    def __rfloordiv__(self, other): return other // self.__component__
    def __mod__(self, other): return self.__component__ % other
    def __rmod__(self, other): return other % self.__component__
    def __pow__(self, other): return self.__component__ ** other
    def __rpow__(self, other): return other ** self.__component__
    def __divmod__(self, other): return divmod(self.__component__, other)
    def __rdivmod__(self, other): return divmod(other, self.__component__)
    def __lshift__(self, other): return self.__component__ << other
    def __rlshift__(self, other): return other << self.__component__
    def __rshift__(self, other): return self.__component__ >> other
    def __rrshift__(self, other): return other >> self.__component__
    def __and__(self, other): return self.__component__ & other
    def __rand__(self, other): return other & self.__component__    
    def __xor__(self, other): return self.__component__ ^ other
    def __rxor__(self, other): return other ^ self.__component__
    def __or__(self, other): return self.__component__ | other
    def __ror__(self, other): return other | self.__component__
    def __iadd__(self, other): self.__component__ += other; return self
    def __isub__(self, other): self.__component__ -= other; return self
    def __imul__(self, other): self.__component__ *= other; return self
    def __itruediv__(self, other): self.__component__ /= other; return self
    def __ifloordiv__(self, other): self.__component__ //= other; return self
    def __imod__(self, other): self.__component__ %= other; return self
    def __ipow__(self, other): self.__component__ **= other; return self
    def __ilshift__(self, other): self.__component__ <<= other; return self
    def __irshift__(self, other): self.__component__ >>= other; return self
    def __iand__(self, other): self.__component__ &= other; return self
    def __ixor__(self, other): self.__component__ ^= other; return self
    def __ior__(self, other): self.__component__ |= other; return self
