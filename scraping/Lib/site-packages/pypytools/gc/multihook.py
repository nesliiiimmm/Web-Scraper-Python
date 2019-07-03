"""
Improve PyPy's GC hooks and make it possible to have multiple callbacks
"""
from pypytools import IS_PYPY
import gc
import types

class GcHooks(object):
    """
    Main entry point to use multiple GC hooks. Make a subclass, override the
    desided handlers and call enable() and disable() appropriately.
    """

    on_gc_minor = None
    on_gc_collect_step = None
    on_gc_collect = None

    def enable(self):
        return MultiHook.get().add(self)

    def disable(self):
        return MultiHook.get().remove(self)


class MultiHook(object):
    """
    This is the actual class which is installed as GC hooks. It is not meant
    to be used directly, but to be manipulates by GcHooks()
    """

    # MultiHook is supposed to be a singleton (apart from tests). Use
    # MultiHook.get() to access it
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __new__(cls):
        # some magic to make MultiHook not crashing on CPython. If we don't
        # have gc.hook, MultiHook() returns an instance of FakeMultiHook
        self = object.__new__(cls)
        if not hasattr(gc, 'hooks'):
            self.__class__ = FakeMultiHook
        return self

    def __init__(self):
        self.hooks = [] # list of GcHooks instances
        self._update_callbacks()

    def add(self, gchooks):
        self.hooks.append(gchooks)
        self._update_callbacks()
        return True

    def remove(self, gchooks):
        self.hooks.remove(gchooks)
        self._update_callbacks()
        return True

    def _check_other_hooks(self):
        # Safety check to avoid disabling other hooks by mistake: the only
        # permitted hooks are the ones installed by us, i.e. bound methods of
        # "self". If we find extraneous hooks, complain
        def check(m):
            return (m is None or
                    (isinstance(m, types.MethodType) and m.__self__ is self))

        if not (check(gc.hooks.on_gc_minor) and
                check(gc.hooks.on_gc_collect_step) and
                check(gc.hooks.on_gc_collect)):
            raise ValueError("It seems other GC hooks are already installed. "
                             "Consider to use multihook everywhere.")

    def _update_callbacks(self):
        self._check_other_hooks()
        self.minor_callbacks = []
        self.collect_step_callbacks = []
        self.collect_callbacks = []
        for h in self.hooks:
            cb = getattr(h, 'on_gc_minor', None)
            if cb:
                self.minor_callbacks.append(cb)

            cb = getattr(h, 'on_gc_collect_step', None)
            if cb:
                self.collect_step_callbacks.append(cb)

            cb = getattr(h, 'on_gc_collect', None)
            if cb:
                self.collect_callbacks.append(cb)

        if self.minor_callbacks:
            gc.hooks.on_gc_minor = self.on_gc_minor

        if self.collect_step_callbacks:
            gc.hooks.on_gc_collect_step = self.on_gc_collect_step

        if self.collect_callbacks:
            gc.hooks.on_gc_collect = self.on_gc_collect
    
    def on_gc_minor(self, stats):
        for cb in self.minor_callbacks:
            cb(stats)

    def on_gc_collect_step(self, stats):
        for cb in self.collect_step_callbacks:
            cb(stats)

    def on_gc_collect(self, stats):
        for cb in self.collect_callbacks:
            cb(stats)


class FakeMultiHook(object):
    """
    This is the fake class which is used on CPython. See MultiHook.__new__
    """

    def is_working(self):
        return False
    
    def add(self, gchooks):
        return False

    def remove(self, gchooks):
        return False
