import pypytools
assert pypytools.IS_PYPY
from _numpypy.multiarray import *
from _numpypy.umath import *

from math import e, pi
PZERO = float('0.0')
NZERO = float('-0.0')
PINF = float('inf')
NINF = float('-inf')
NAN = float('nan')
euler_gamma = 0.577215664901532860606512090082402431 # from npy_math.h
Inf = inf = infty = Infinity = PINF
nan = NaN = NAN

def asarray(a, dtype=None, order=None):
    return array(a, dtype, copy=False, order=order)

def asanyarray(a, dtype=None, order=None):
    if isinstance(a, ndarray):
        return a
    return asarray(a, dtype, order)

def array_equal(a1, a2):
    try:
        a1, a2 = asarray(a1), asarray(a2)
    except:
        return False
    if a1.shape != a2.shape:
        return False
    return bool(asarray(a1 == a2).all())

def not_equal(a, b):
    return asarray(a) != b

def subtract(a, b):
    return asarray(a) - b

# generate wrappers for ndarray's methods
def make_wrappers():
    from pypytools.codegen import Code
    code = Code()
    names = ['all', 'any', 'argmax', 'argmin', 'argsort', 'choose', 'clip',
             'copy', 'cumprod', 'cumsum', 'diagonal', 'max', 'min',
             'nonzero', 'prod', 'ptp', 'put', 'ravel', 'repeat', 'reshape',
             'round', 'squeeze', 'sum', 'swapaxes', 'transpose']
    #
    for name in names:
        ns = code.new_scope(name=name)
        with code.def_(name, ['myarray'], '*args', '**kwargs'):
            ns.w('return myarray.{name}(*args, **kwargs)')
    #
    code.compile()
    gbl = globals()
    for name in names:
        gbl[name] = code[name]

make_wrappers()
del make_wrappers
