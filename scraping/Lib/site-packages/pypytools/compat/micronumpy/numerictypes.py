import pypytools
assert pypytools.IS_PYPY
from _numpypy.multiarray import dtype

_types = ['bool_', 'int8', 'uint8', 'int16', 'uint16', 'int32',
          'uint32', 'int64', 'uint64', 'float16', 'float32',
          'float64', 'complex64', 'complex128', 'object']

for _typename in _types:
    globals()[_typename] = dtype(_typename).type
