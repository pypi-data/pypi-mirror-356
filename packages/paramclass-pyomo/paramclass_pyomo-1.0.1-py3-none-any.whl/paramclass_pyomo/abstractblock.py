from paramclass_pyomo.proxycomponent import ProxyComponent
from paramclass_pyomo.linker import CrossLink

from paramclass.base import ParamClass, UNDEFINED

from typing import Any, Generic, TypeVar
from types import FunctionType, MethodType
from pyomo.core.base.block import IndexedBlock, Block

import pyomo.environ as pyo

INDEXED_BLOCK_ATTR = object

TAbstractBlock = TypeVar('TAbstractBlock', bound='AbstractBlock')

class UnsupportedModelType(Exception):
    pass

class UnsupportedBlockType(Exception):
    pass

class AbstractBlock(ParamClass, Generic[TAbstractBlock]):
    def build(self, model):
        if isinstance(model, pyo.Block):
            self._model = model
        else:
            raise UnsupportedModelType(f"{type(model)}")
        self._name = None
        self.__finalize__(target=None)
    
    def __setup__(self, *args, **kwargs):
        allfuncs = set((k for k in dir(type(self)) if isinstance(getattr(type(self), k, None), FunctionType)))
        self._functions = allfuncs.difference(_pyo_protected)
        self._initializing = True
        self._autobuild = False
        self._args = args
    
    def __finalize__(self, target=None):
        if self._name == None:
            self._block = self._model
        else:
            self._block = pyo.Block(*self._args)
            target.__set_proxy__(self._name, self._block)
        
        self_type = type(self)
        block = self._block
        for func_name in self._functions:
            if isinstance(block, IndexedBlock):
                for i in block:
                    self._idx = i
                    method = MethodType(getattr(self_type, func_name), block[i])
                    setattr(block[i], func_name, method)
                del self._idx
            else:
                method = MethodType(getattr(self_type, func_name), block)
                setattr(block, func_name, method)
        self.__build__()
        
        self._initializing = False
    
    def __build_param__(self, key):
        val = self._overrides.get(key, UNDEFINED)
        if isinstance(block := self._block, IndexedBlock):
            for i in block:
                self._idx = i
                setval = val
                if setval is UNDEFINED:
                    setval = getattr(type(self), key).__execute__(self)
                if type(setval) is CrossLink:
                    setval = setval._reference[i]
                self.__set_proxy__(key, setval)
            del self._idx
        else:
            setval = val
            if setval is UNDEFINED:
                setval = getattr(type(self), key).__execute__(self)
            self.__set_proxy__(key, setval)
    
    def __set_proxy__(self, key: str, val: Any) -> None:
        block = self._block
        setval = val
        if isinstance(setval, AbstractBlock):
            if setval._initializing:
                setval._name = key
                setval._model = self._block
                setval.__finalize__(target=self)
            return
        if isinstance(setval, pyo.Component):
            if setval.parent_block() is not None:
                setval = ProxyComponent(setval)
        if isinstance(block, IndexedBlock):
            setattr(block[self._idx], key, setval)
        elif isinstance(block, Block):
            setattr(block, key, setval)
        else:
            raise UnsupportedBlockType(f"{type(block)}")
    
    def __get_proxy__(self, name: str) -> Any:
        if isinstance(self._block, IndexedBlock):
            return self._block[self._idx].__getattribute__(name)
        elif isinstance(self._block, Block):
            return self._block.__getattribute__(name)
        else:
            raise UnsupportedBlockType(f"{type(self._block)}")
    
    def __del_proxy__(self, __name: str) -> None:
        if isinstance(self._block, IndexedBlock):
            for i in self._block:
                delattr(self._block[i], __name)
        elif isinstance(self._block, Block):
            delattr(self._block, __name)
        else:
            raise UnsupportedBlockType(f"{type(self._block)}")
    
    def __setattr__(self, key, val):
        if key not in _pyo_protected:
            self.__set_proxy__(key, val)
        else:
            super().__setattr__(key, val)

    def __getattribute__(self, name):
        if name not in _pyo_protected:
            return self.__get_proxy__(name)
        else:
            return super().__getattribute__(name)
    
    def __delattr__(self, __name: str) -> None:
        if __name not in _pyo_protected:
            self.__del_proxy__(__name)
        else:
            super().__delattr__(__name)
    
    def __getitem__(self, index) -> TAbstractBlock:
        if isinstance(self._block, IndexedBlock):
            return self._block[index]
        else:
            raise UnsupportedBlockType(f"{type(self._block)}")
    
_instance_protected = set(('_pyo_protected', '_block', '_idx', '_initializing', '_name', '_autobuild', '_overrides', '_functions', '_args', '_model'))
_class_protected = set((k for k in dir(AbstractBlock)))
_pyo_protected = _instance_protected | _class_protected

