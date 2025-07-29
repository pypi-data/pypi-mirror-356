import pyomo.environ as pyo
from paramclass.linker import Linker, add_linker, LinkFunc

class CrossLink:
    def __init__(self, reference):
        self._reference = reference

class PyoLinkTracer(Linker):
    pass

class PyomoLinker(Linker):
    def __call__(self, *args, **kwargs):
        if self._closed:
            return Linker(self)(*args, **kwargs)
        elif len(self._links) >= 1 and isinstance(self._links[-1], LinkFunc) and self._base in (pyo.Constraint, pyo.Objective, pyo.Expression):
            self._links[-1]._kwargs['rule'] = args[0]
        elif len(self._links) >= 1 and isinstance(self._links[-1], LinkFunc) and self._base in (pyo.Param, pyo.Var):
            self._links[-1]._kwargs['initialize'] = args[0]
        else:
            self._links.append(LinkFunc(*args, **kwargs))
        return self

add_linker(CrossLink, PyoLinkTracer)
add_linker(pyo, PyomoLinker)
for ctype in pyo.__dict__.values():
    if type(ctype) == type and issubclass(ctype, pyo.Component):
        add_linker(ctype, PyomoLinker)