import sys
import gc
from contextlib import contextmanager
from pypytools import IS_PYPY
from pypytools.gc.multihook import GcHooks

KB = 1024.0
MB = KB * KB

class CustomGc(GcHooks):    
    """
    GC with custom logic which is triggered by hooks. Override on_gc_minor to
    implement your custom logic
    """

    def __init__(self):
        self._isenabled = False

    def isenabled(self):
        return self._isenabled

    def enable(self):
        if self._isenabled:
            return
        self._isenabled = True
        if super(CustomGc, self).enable():
            gc.disable()

    def disable(self):
        if not self._isenabled:
            return
        if super(CustomGc, self).disable():
            gc.enable()
        self._isenabled = False



class DefaultGc(CustomGc):
    """
    Custom GC which mimimcs the default logic of incminimark
    """

    MAJOR_COLLECT = 1.82      # same as PYPY_GC_MAJOR_COLLECT
    MIN_THRESHOLD = 4*8 * MB  # same as PYPY_GC_MIN
    MAX_GROWTH = 1.4          # same as PYPY_GC_GROWTH

    def __init__(self):
        super(DefaultGc, self).__init__()
        self.major_in_progress = False
        self.threshold = 0
        self.update_threshold(0)
        self.nogc_count = 0

    def update_threshold(self, mem):
        self.threshold = max(self.MIN_THRESHOLD,
                             min(mem * self.MAJOR_COLLECT,
                                 self.threshold * self.MAX_GROWTH))

    @contextmanager
    def nogc(self):
        self.nogc_count += 1
        yield self
        self.nogc_count -= 1

    def on_gc_minor(self, stats):
        if self.nogc_count > 0:
            return

        # run the hook inside a nogc() section to avoid calling it
        # recursively. Else, it happens the following:
        #   1. a minor collection occurs, and we enter on_gc_minor
        #   2. we reached the threshold and start a major
        #   3. we call gc.collect_step
        #   4. internally, pypy does ANOTHER minor collection
        #   5. we enter AGAIN this hook
        #   6. we are major_in_progress, so we call another gc.collect_step
        #   7. and so on, until we finish the whole collection in one run :-(
        with self.nogc():
            if self.major_in_progress:
                step_stats = gc.collect_step()
                if step_stats.major_is_done:
                    self.major_in_progress = False
                    self.update_threshold(stats.total_memory_used)

            elif stats.total_memory_used > self.threshold:
                self.major_in_progress = True
                gc.collect_step()
