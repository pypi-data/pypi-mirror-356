"""
This module provides a TypeDescriptor class that allows introspection of Python classes,
including their methods, decorators, and type hints. It supports caching for performance
"""
from __future__ import annotations

import inspect
from inspect import signature, getmembers
import threading
from typing import Callable, get_type_hints, Type, Dict, Optional
from weakref import WeakKeyDictionary


class DecoratorDescriptor:
    """
    A DecoratorDescriptor covers the decorator - a callable - and the passed arguments
    """
    __slots__ = [
        "decorator",
        "args"
    ]

    def __init__(self, decorator: Callable, *args):
        self.decorator = decorator
        self.args = args

    def __str__(self):
        return f"@{self.decorator.__name__}({','.join(self.args)})"

class Decorators:
    """
    Utility class that caches decorators ( Python does not have a feature for this )
    """
    @classmethod
    def add(cls, func, decorator: Callable, *args):
        decorators = getattr(func, '__decorators__', None)
        if decorators is None:
            setattr(func, '__decorators__', [DecoratorDescriptor(decorator, *args)])
        else:
            decorators.append(DecoratorDescriptor(decorator, *args))

    @classmethod
    def has_decorator(cls, func, callable: Callable) -> bool:
        return any(decorator.decorator is callable for decorator in Decorators.get(func))

    @classmethod
    def get(cls, func) -> list[DecoratorDescriptor]:
        return getattr(func, '__decorators__', [])

class TypeDescriptor:
    """
    This class provides a way to introspect Python classes, their methods, decorators, and type hints.
    """
    # inner class

    class MethodDescriptor:
        """
        This class represents a method of a class, including its decorators, parameter types, and return type.
        """
        # constructor

        def __init__(self, cls, method: Callable):
            self.clazz = cls
            self.method = method
            self.decorators: list[DecoratorDescriptor] = Decorators.get(method)
            self.param_types : list[Type] = []

            type_hints = get_type_hints(method)
            sig = signature(method)

            for name, _ in sig.parameters.items():
                if name != 'self':
                    self.param_types.append(type_hints.get(name, object))

            self.return_type = type_hints.get('return', None)

        # public

        def get_name(self) -> str:
            """
            return the method name
            :return: the method name
            """
            return self.method.__name__

        def get_doc(self, default = "") -> str:
            """
            return the method docstring
            :param default: the default if no docstring is found
            :return:  the docstring
            """
            return self.method.__doc__ or default

        def is_async(self) -> bool:
            """
            return true if the method is asynchronous
            :return: async flag
            """
            return inspect.iscoroutinefunction(self.method)

        def get_decorator(self, decorator: Callable) -> Optional[DecoratorDescriptor]:
            """
            return the DecoratorDescriptor - if any - associated with the passed Callable
            :param decorator:
            :return:  the DecoratorDescriptor or None
            """
            for dec in self.decorators:
                if dec.decorator is decorator:
                    return dec

            return None

        def has_decorator(self, decorator: Callable) -> bool:
            """
            return True if the method is decorated with the decorator
            :param decorator: the decorator callable
            :return:  True if the method is decorated with the decorator
            """
            for dec in self.decorators:
                if dec.decorator is decorator:
                    return True

            return False

        def __str__(self):
            return f"Method({self.method.__name__})"

    # class properties

    _cache = WeakKeyDictionary()
    _lock = threading.RLock()

    # class methods

    @classmethod
    def for_type(cls, clazz: Type) -> TypeDescriptor:
        """
        Returns a TypeDescriptor for the given class, using a cache to avoid redundant introspection.
        """
        descriptor = cls._cache.get(clazz)
        if descriptor is None:
            with cls._lock:
                descriptor = cls._cache.get(clazz)
                if descriptor is None:
                    descriptor = TypeDescriptor(clazz)
                    cls._cache[clazz] = descriptor

        return descriptor

    # constructor

    def __init__(self, cls):
        self.cls = cls
        self.decorators = Decorators.get(cls)
        self.methods: Dict[str, TypeDescriptor.MethodDescriptor] = {}
        self.local_methods: Dict[str, TypeDescriptor.MethodDescriptor] = {}

        # check superclasses

        self.super_types = [TypeDescriptor.for_type(x) for x in cls.__bases__ if not x is object]

        for super_type in self.super_types:
            self.methods = self.methods | super_type.methods

        # methods

        for name, member in self._get_local_members(cls):
            method = TypeDescriptor.MethodDescriptor(cls, member)
            self.local_methods[name] = method
            self.methods[name] = method

    # internal

    def _get_local_members(self, cls):
        return [
            (name, value)
            for name, value in getmembers(cls, predicate=inspect.isfunction)
            if name in cls.__dict__
        ]

    # public

    def get_decorator(self, decorator: Callable) -> Optional[DecoratorDescriptor]:
        """
        Returns the first decorator of the given type, or None if not found.
        """
        for dec in self.decorators:
            if dec.decorator is decorator:
                return dec

        return None

    def has_decorator(self, decorator: Callable) -> bool:
        """
        Checks if the class has a decorator of the given type."""
        for dec in self.decorators:
            if dec.decorator is decorator:
                return True

        return False

    def get_methods(self, local = False) ->  list[TypeDescriptor.MethodDescriptor]:
        """
        Returns a list of MethodDescriptor objects for the class.
        If local is True, only returns methods defined in the class itself, otherwise includes inherited methods.
        """
        if local:
            return list(self.local_methods.values())
        else:
            return list(self.methods.values())

    def get_method(self, name: str, local = False) -> Optional[TypeDescriptor.MethodDescriptor]:
        """
        Returns a MethodDescriptor for the method with the given name.
        If local is True, only searches for methods defined in the class itself, otherwise includes inherited methods.
        """
        if local:
            return self.local_methods.get(name, None)
        else:
            return self.methods.get(name, None)
