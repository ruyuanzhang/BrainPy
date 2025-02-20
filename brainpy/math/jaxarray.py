# -*- coding: utf-8 -*-


import numpy as np
from jax import numpy as jnp
from jax.tree_util import register_pytree_node

from brainpy.errors import MathError

__all__ = [
  'JaxArray',
  'ndarray',  # alias of JaxArray
  'Variable',
  'TrainVar',
  'Parameter',
]

# Ways to change values in a zero-dimensional array
# -----
# Reference: https://stackoverflow.com/questions/56954714/how-do-i-assign-to-a-zero-dimensional-numpy-array
#
#   >>> x = np.array(10)
# 1. index the original array with ellipsis or an empty tuple
#    >>> x[...] = 2
#    >>> x[()] = 2

_all_slice = slice(None, None, None)


class JaxArray(object):
  """Multiple-dimensional array for JAX backend.
  """
  __slots__ = "_value"

  def __init__(self, value):
    if isinstance(value, (list, tuple)):
      value = jnp.asarray(value)
    self._value = value

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self.update(value)

  def update(self, value):
    """Update the value of this JaxArray.
    """
    if value.shape != self._value.shape:
      raise MathError(f"The shape of the original data is {self._value.shape}, "
                      f"while we got {value.shape}.")
    if value.dtype != self._value.dtype:
      raise MathError(f"The dtype of the original data is {self._value.dtype}, "
                      f"while we got {value.dtype}.")
    self._value = value.value if isinstance(value, JaxArray) else value

  @property
  def dtype(self):
    return self._value.dtype

  @property
  def shape(self):
    return self._value.shape

  @property
  def ndim(self):
    return self._value.ndim

  @property
  def imag(self):
    return self._value.image

  @property
  def real(self):
    return JaxArray(self._value.real)

  @property
  def size(self):
    return self.value.size

  @property
  def T(self):
    return JaxArray(self.value.T)

  # ----------------------- #
  # Python inherent methods #
  # ----------------------- #

  def __repr__(self) -> str:
    lines = repr(self.value).split("\n")
    prefix = self.__class__.__name__ + "("
    lines[0] = prefix + lines[0]
    prefix = " " * len(prefix)
    for i in range(1, len(lines)):
      lines[i] = prefix + lines[i]
    lines[-1] = lines[-1] + ")"
    return "\n".join(lines)

  def __format__(self, format_spec: str) -> str:
    return format(self.value)

  def __iter__(self):
    """Solve the issue of DeviceArray.__iter__.

    Details please see JAX issues:

    - https://github.com/google/jax/issues/7713
    - https://github.com/google/jax/pull/3821
    """
    for i in range(self._value.shape[0]):
      yield self._value[i]

  def __getitem__(self, index):
    if isinstance(index, slice) and (index == _all_slice):
      return self.value
    elif isinstance(index, tuple):
      index = tuple(x.value if isinstance(x, JaxArray) else x for x in index)
    elif isinstance(index, JaxArray):
      index = index.value
    return self.value[index]

  def __setitem__(self, index, value):
    # value is JaxArray
    if isinstance(value, JaxArray):
      value = value.value

    # tuple index
    if isinstance(index, tuple):
      index = tuple(x.value if isinstance(x, JaxArray) else x for x in index)

    # JaxArray index
    elif isinstance(index, JaxArray):
      index = index.value

    # update
    self._value = self._value.at[index].set(value)

  # ---------- #
  # operations #
  # ---------- #

  def __bool__(self) -> bool:
    return bool(self._value)

  def __len__(self) -> int:
    return len(self._value)

  def __neg__(self):
    return JaxArray(self._value.__neg__())

  def __pos__(self):
    return JaxArray(self._value.__pos__())

  def __abs__(self):
    return JaxArray(self._value.__abs__())

  def __invert__(self):
    return JaxArray(self._value.__invert__())

  def __eq__(self, oc):
    return JaxArray(self._value.__eq__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ne__(self, oc):
    return JaxArray(self._value.__ne__(oc._value if isinstance(oc, JaxArray) else oc))

  def __lt__(self, oc):
    return JaxArray(self._value.__lt__(oc._value if isinstance(oc, JaxArray) else oc))

  def __le__(self, oc):
    return JaxArray(self._value.__le__(oc._value if isinstance(oc, JaxArray) else oc))

  def __gt__(self, oc):
    return JaxArray(self._value.__gt__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ge__(self, oc):
    return JaxArray(self._value.__ge__(oc._value if isinstance(oc, JaxArray) else oc))

  def __add__(self, oc):
    return JaxArray(self._value.__add__(oc._value if isinstance(oc, JaxArray) else oc))

  def __radd__(self, oc):
    return JaxArray(self._value.__radd__(oc._value if isinstance(oc, JaxArray) else oc))

  def __iadd__(self, oc):
    # a += b
    self._value += (oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __sub__(self, oc):
    return JaxArray(self._value.__sub__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rsub__(self, oc):
    return JaxArray(self._value.__rsub__(oc._value if isinstance(oc, JaxArray) else oc))

  def __isub__(self, oc):
    # a -= b
    self._value = self._value.__sub__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __mul__(self, oc):
    return JaxArray(self._value.__mul__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rmul__(self, oc):
    return JaxArray(self._value.__rmul__(oc._value if isinstance(oc, JaxArray) else oc))

  def __imul__(self, oc):
    # a *= b
    self._value = self._value.__mul__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __div__(self, oc):
    return JaxArray(self._value.__div__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rdiv__(self, oc):
    return JaxArray(self._value.__rdiv__(oc._value if isinstance(oc, JaxArray) else oc))

  def __truediv__(self, oc):
    return JaxArray(self._value.__truediv__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rtruediv__(self, oc):
    return JaxArray(self._value.__rtruediv__(oc._value if isinstance(oc, JaxArray) else oc))

  def __itruediv__(self, oc):
    # a /= b
    self._value = self._value.__truediv__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __floordiv__(self, oc):
    return JaxArray(self._value.__floordiv__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rfloordiv__(self, oc):
    return JaxArray(self._value.__rfloordiv__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ifloordiv__(self, oc):
    # a //= b
    self._value = self._value.__floordiv__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __divmod__(self, oc):
    return JaxArray(self._value.__divmod__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rdivmod__(self, oc):
    return JaxArray(self._value.__rdivmod__(oc._value if isinstance(oc, JaxArray) else oc))

  def __mod__(self, oc):
    return JaxArray(self._value.__mod__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rmod__(self, oc):
    return JaxArray(self._value.__rmod__(oc._value if isinstance(oc, JaxArray) else oc))

  def __imod__(self, oc):
    # a %= b
    self._value = self._value.__mod__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __pow__(self, oc):
    return JaxArray(self._value.__pow__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rpow__(self, oc):
    return JaxArray(self._value.__rpow__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ipow__(self, oc):
    # a **= b
    self._value = self._value ** (oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __matmul__(self, oc):
    return JaxArray(self._value.__matmul__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rmatmul__(self, oc):
    return JaxArray(self._value.__rmatmul__(oc._value if isinstance(oc, JaxArray) else oc))

  def __imatmul__(self, oc):
    # a @= b
    self._value = self._value.__matmul__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __and__(self, oc):
    return JaxArray(self._value.__and__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rand__(self, oc):
    return JaxArray(self._value.__rand__(oc._value if isinstance(oc, JaxArray) else oc))

  def __iand__(self, oc):
    # a &= b
    self._value = self._value.__and__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __or__(self, oc):
    return JaxArray(self._value.__or__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ror__(self, oc):
    return JaxArray(self._value.__ror__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ior__(self, oc):
    # a |= b
    self._value = self._value.__or__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __xor__(self, oc):
    return JaxArray(self._value.__xor__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rxor__(self, oc):
    return JaxArray(self._value.__rxor__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ixor__(self, oc):
    # a ^= b
    self._value = self._value.__xor__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __lshift__(self, oc):
    return JaxArray(self._value.__lshift__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rlshift__(self, oc):
    return JaxArray(self._value.__rlshift__(oc._value if isinstance(oc, JaxArray) else oc))

  def __ilshift__(self, oc):
    # a <<= b
    self._value = self._value.__lshift__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __rshift__(self, oc):
    return JaxArray(self._value.__rshift__(oc._value if isinstance(oc, JaxArray) else oc))

  def __rrshift__(self, oc):
    return JaxArray(self._value.__rrshift__(oc._value if isinstance(oc, JaxArray) else oc))

  def __irshift__(self, oc):
    # a >>= b
    self._value = self._value.__rshift__(oc._value if isinstance(oc, JaxArray) else oc)
    return self

  def __round__(self, ndigits=None):
    return JaxArray(self._value.__round__(ndigits))

  # ----------------------- #
  #       JAX methods       #
  # ----------------------- #

  def block_host_until_ready(self, *args):
    self._value.block_host_until_ready(*args)

  def block_until_ready(self, *args):
    self._value.block_until_ready(*args)

  # def broadcast(self, operand, sizes):
  #   """Broadcasts an array, adding new major dimensions.
  #
  #   Wraps XLA's `Broadcast
  #   <https://www.tensorflow.org/xla/operation_semantics#broadcast>`_
  #   operator.
  #
  #   Parameters
  #   ----------
  #   operand: an array
  #   sizes:
  #     A sequence of integers, giving the sizes of new major dimensions
  #     to add.
  #
  #   Returns
  #   -------
  #   ary : array
  #     An array containing the result.
  #   """
  #   raise NotImplementedError
  #
  # def client(self, *args):
  #   raise NotImplementedError
  #
  # def clone(self, *args):
  #   raise NotImplementedError
  #
  # def copy_to_device(self, *args):
  #   raise NotImplementedError
  #
  # def copy_to_host_async(self, *args):
  #   raise NotImplementedError
  #
  # def device(self, *args):
  #   raise NotImplementedError
  #
  # def device_buffer(self, *args):
  #   raise NotImplementedError

  # ----------------------- #
  #      NumPy methods      #
  # ----------------------- #

  def all(self, axis=None, keepdims=False):
    """Returns True if all elements evaluate to True."""
    r = self.value.all(axis=axis, keepdims=keepdims)
    return r if (axis is None or keepdims) else JaxArray(r)

  def any(self, axis=None, keepdims=False):
    """Returns True if any of the elements of a evaluate to True."""
    r = self.value.any(axis=axis, keepdims=keepdims)
    return r if (axis is None or keepdims) else JaxArray(r)

  def argmax(self, axis=None):
    """Return indices of the maximum values along the given axis."""
    return JaxArray(self.value.argmax(axis=axis))

  def argmin(self, axis=None):
    """Return indices of the minimum values along the given axis."""
    return JaxArray(self.value.argmin(axis=axis))

  def argpartition(self, kth, axis=-1, kind='introselect', order=None):
    """Returns the indices that would partition this array."""
    return JaxArray(self.value.argpartition(kth=kth, axis=axis, kind=kind, order=order))

  def argsort(self, axis=-1, kind=None, order=None):
    """Returns the indices that would sort this array."""
    return JaxArray(self.value.argsort(axis=axis, kind=kind, order=order))

  def astype(self, dtype, order='K', casting='unsafe', subok=True, copy=True):
    """Copy of the array, cast to a specified type.

    Parameters
    ----------
    dtype: str, dtype
      Typecode or data-type to which the array is cast.
    order : {‘C’, ‘F’, ‘A’, ‘K’}, optional
      Controls the memory layout order of the result.
      ‘C’ means C order, ‘F’ means Fortran order, ‘A’ means
      ‘F’ order if all the arrays are Fortran contiguous,
      ‘C’ order otherwise, and ‘K’ means as close to the order
      the array elements appear in memory as possible. Default is ‘K’.
    casting: {‘no’, ‘equiv’, ‘safe’, ‘same_kind’, ‘unsafe’}, optional
      Controls what kind of data casting may occur.
      Defaults to ‘unsafe’ for backwards compatibility.
      - ‘no’ means the data types should not be cast at all.
      - ‘equiv’ means only byte-order changes are allowed.
      - ‘safe’ means only casts which can preserve values are allowed.
      - ‘same_kind’ means only safe casts or casts within a kind, like float64 to float32, are allowed.
      - ‘unsafe’ means any data conversions may be done.
    subok: bool, optional
      If True, then sub-classes will be passed-through (default), otherwise
      the returned array will be forced to be a base-class array.
    copy: bool, optional
      By default, astype always returns a newly allocated array.
      If this is set to false, and the dtype, order, and subok
      requirements are satisfied, the input array is returned instead of a copy.
    """
    return JaxArray(self.value.astype(dtype=dtype, order=order, casting=casting, subok=subok, copy=copy))

  def byteswap(self, inplace=False):
    """Swap the bytes of the array elements

    Toggle between low-endian and big-endian data representation by
    returning a byteswapped array, optionally swapped in-place.
    Arrays of byte-strings are not swapped. The real and imaginary
    parts of a complex number are swapped individually."""
    return JaxArray(self.value.byteswap(inplace=inplace))

  def choose(self, choices, mode='raise'):
    """Use an index array to construct a new array from a set of choices."""
    choices = choices.value if isinstance(choices, JaxArray) else choices
    return JaxArray(self.value.choose(choices=choices, mode=mode))

  def clip(self, min=None, max=None):
    """Return an array whose values are limited to [min, max]. One of max or min must be given."""
    return JaxArray(self.value.clip(min=min, max=max))

  def compress(self, condition, axis=None):
    """Return selected slices of this array along given axis."""
    condition = condition.value if isinstance(condition, JaxArray) else condition
    return JaxArray(self.value.compress(condition=condition, axis=axis))

  def conj(self):
    """Complex-conjugate all elements."""
    return JaxArray(self.value.conj())

  def conjugate(self):
    """Return the complex conjugate, element-wise."""
    return JaxArray(self.value.conjugate())

  def copy(self):
    """Return a copy of the array."""
    return JaxArray(self.value.copy())

  def cumprod(self, axis=None, dtype=None):
    """Return the cumulative product of the elements along the given axis."""
    return JaxArray(self.value.cumprod(axis=axis, dtype=dtype))

  def cumsum(self, axis=None, dtype=None):
    """Return the cumulative sum of the elements along the given axis."""
    return JaxArray(self.value.cumsum(axis=axis, dtype=dtype))

  def diagonal(self, offset=0, axis1=0, axis2=1):
    """Return specified diagonals."""
    return JaxArray(self.value.diagonal(offset=offset, axis1=axis1, axis2=axis2))

  def dot(self, b):
    """Dot product of two arrays."""
    return JaxArray(self.value.dot(b))

  # def dump(self, file):
  #   """Dump a pickle of the array to the specified file.
  #   The array can be read back with pickle.load or numpy.load."""
  #   pass

  # def dumps(self):
  #   """Returns the pickle of the array as a string. pickle.loads
  #   or numpy.loads will convert the string back to an array."""
  #   pass

  def fill(self, value):
    """Fill the array with a scalar value."""
    self._value = jnp.ones_like(self.value) * value

  def flatten(self, order='C'):
    return JaxArray(self.value.flatten(order=order))

  # def getfield(self, dtype, offset=0):
  #   return type(self)(self.value.getfield(dtype=dtype, offset=offset))

  def item(self, *args):
    """Copy an element of an array to a standard Python scalar and return it."""
    return self.value.item(*args)

  # def itemset(self, *args):
  #   """Insert scalar into an array (scalar is cast to array’s dtype, if possible)"""
  #   self.value.itemset(*args)

  def max(self, axis=None, keepdims=False, *args, **kwargs):
    """Return the maximum along a given axis."""
    res = self.value.max(axis=axis, keepdims=keepdims, *args, **kwargs)
    return res if (axis is None or keepdims) else JaxArray(res)

  def mean(self, axis=None, dtype=None, keepdims=False, *args, **kwargs):
    """Returns the average of the array elements along given axis."""
    res = self.value.mean(axis=axis, dtype=dtype, keepdims=keepdims, *args, **kwargs)
    return res if (axis is None or keepdims) else JaxArray(res)

  def min(self, axis=None, keepdims=False, *args, **kwargs):
    """Return the minimum along a given axis."""
    res = self.value.min(axis=axis, keepdims=keepdims, *args, **kwargs)
    return res if (axis is None or keepdims) else JaxArray(res)

  def nonzero(self):
    """Return the indices of the elements that are non-zero."""
    return tuple(JaxArray(a) for a in self.value.nonzero())

  def prod(self, axis=None, dtype=None, keepdims=False, initial=1, where=True):
    """Return the product of the array elements over the given axis."""
    res = self.value.prod(axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)
    return res if (axis is None or keepdims) else JaxArray(res)

  def ptp(self, axis=None, keepdims=False):
    """Peak to peak (maximum - minimum) value along a given axis."""
    r = self.value.ptp(axis=axis, keepdims=keepdims)
    return r if (axis is None or keepdims) else JaxArray(r)

  def ravel(self, order=None):
    """Return a flattened array."""
    return JaxArray(self.value.ravel(order=order))

  def repeat(self, repeats, axis=None):
    """Repeat elements of an array."""
    return JaxArray(self.value.repeat(repeats=repeats, axis=axis))

  def reshape(self, shape, order='C'):
    """Returns an array containing the same data with a new shape."""
    return JaxArray(self.value.reshape(*shape, order=order))

  def round(self, decimals=0):
    """Return ``a`` with each element rounded to the given number of decimals."""
    return JaxArray(self.value.round(decimals=decimals))

  def searchsorted(self, v, side='left', sorter=None):
    """Find indices where elements should be inserted to maintain order.

    Find the indices into a sorted array `a` such that, if the
    corresponding elements in `v` were inserted before the indices, the
    order of `a` would be preserved.

    Assuming that `a` is sorted:

    ======  ============================
    `side`  returned index `i` satisfies
    ======  ============================
    left    ``a[i-1] < v <= a[i]``
    right   ``a[i-1] <= v < a[i]``
    ======  ============================

    Parameters
    ----------
    v : array_like
        Values to insert into `a`.
    side : {'left', 'right'}, optional
        If 'left', the index of the first suitable location found is given.
        If 'right', return the last such index.  If there is no suitable
        index, return either 0 or N (where N is the length of `a`).
    sorter : 1-D array_like, optional
        Optional array of integer indices that sort array a into ascending
        order. They are typically the result of argsort.

    Returns
    -------
    indices : array of ints
        Array of insertion points with the same shape as `v`.
    """
    v = v.value if isinstance(v, JaxArray) else v
    return JaxArray(self.value.searchsorted(v=v, side=side, sorter=sorter))

  def sort(self, axis=-1, kind=None, order=None):
    """Sort an array in-place.

    Parameters
    ----------
    axis : int, optional
        Axis along which to sort. Default is -1, which means sort along the
        last axis.
    kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
        Sorting algorithm. The default is 'quicksort'. Note that both 'stable'
        and 'mergesort' use timsort under the covers and, in general, the
        actual implementation will vary with datatype. The 'mergesort' option
        is retained for backwards compatibility.
    order : str or list of str, optional
        When `a` is an array with fields defined, this argument specifies
        which fields to compare first, second, etc.  A single field can
        be specified as a string, and not all fields need be specified,
        but unspecified fields will still be used, in the order in which
        they come up in the dtype, to break ties.
    """
    self._value = self.value.sort(axis=axis, kind=kind, order=order)

  def squeeze(self, axis=None):
    """Remove axes of length one from ``a``."""
    return JaxArray(self.value.squeeze(axis=axis))

  def std(self, axis=None, dtype=None, ddof=0, keepdims=False):
    """Compute the standard deviation along the specified axis.

    Returns the standard deviation, a measure of the spread of a distribution,
    of the array elements. The standard deviation is computed for the
    flattened array by default, otherwise over the specified axis.

    Parameters
    ----------
    axis : None or int or tuple of ints, optional
        Axis or axes along which the standard deviation is computed. The
        default is to compute the standard deviation of the flattened array.
        If this is a tuple of ints, a standard deviation is performed over
        multiple axes, instead of a single axis or all the axes as before.
    dtype : dtype, optional
        Type to use in computing the standard deviation. For arrays of
        integer type the default is float64, for arrays of float types it is
        the same as the array type.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape as the expected output but the type (of the calculated
        values) will be cast if necessary.
    ddof : int, optional
        Means Delta Degrees of Freedom.  The divisor used in calculations
        is ``N - ddof``, where ``N`` represents the number of elements.
        By default `ddof` is zero.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `std` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.
    where : array_like of bool, optional
        Elements to include in the standard deviation.

    Returns
    -------
    standard_deviation : ndarray, see dtype parameter above.
        If `out` is None, return a new array containing the standard deviation,
        otherwise return a reference to the output array.
    """
    r = self.value.std(axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims)
    return r if (axis is None or keepdims) else JaxArray(r)

  def sum(self, axis=None, dtype=None, keepdims=False, initial=0, where=True):
    """Return the sum of the array elements over the given axis."""
    res = self.value.sum(axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)
    return res if (axis is None or keepdims) else JaxArray(res)

  def swapaxes(self, axis1, axis2):
    """Return a view of the array with `axis1` and `axis2` interchanged."""
    return JaxArray(self.value.swapaxes(axis1, axis2))

  def split(self, indices_or_sections, axis=0):
    """Split an array into multiple sub-arrays as views into ``ary``.

    Parameters
    ----------
    indices_or_sections : int, 1-D array
      If `indices_or_sections` is an integer, N, the array will be divided
      into N equal arrays along `axis`.  If such a split is not possible,
      an error is raised.

      If `indices_or_sections` is a 1-D array of sorted integers, the entries
      indicate where along `axis` the array is split.  For example,
      ``[2, 3]`` would, for ``axis=0``, result in

        - ary[:2]
        - ary[2:3]
        - ary[3:]

      If an index exceeds the dimension of the array along `axis`,
      an empty sub-array is returned correspondingly.
    axis : int, optional
      The axis along which to split, default is 0.

    Returns
    -------
    sub-arrays : list of ndarrays
      A list of sub-arrays as views into `ary`.
    """
    return [JaxArray(a) for a in self.value.split(indices_or_sections, axis=axis)]

  def take(self, indices, axis=None, mode='raise'):
    """Return an array formed from the elements of a at the given indices."""
    indices = indices.value if isinstance(indices, JaxArray) else indices
    return JaxArray(self.value.take(indices=indices, axis=axis, mode=mode))

  def tobytes(self, order='C'):
    """Construct Python bytes containing the raw data bytes in the array.

    Constructs Python bytes showing a copy of the raw contents of data memory.
    The bytes object is produced in C-order by default. This behavior is
    controlled by the ``order`` parameter."""
    return JaxArray(self.value.tobytes(order=order))

  def tolist(self):
    """Return the array as an ``a.ndim``-levels deep nested list of Python scalars.

    Return a copy of the array data as a (nested) Python list.
    Data items are converted to the nearest compatible builtin Python type, via
    the `~numpy.ndarray.item` function.

    If ``a.ndim`` is 0, then since the depth of the nested list is 0, it will
    not be a list at all, but a simple Python scalar.
    """
    return self.value.tolist()

  def trace(self, offset=0, axis1=0, axis2=1, dtype=None):
    """Return the sum along diagonals of the array."""
    return JaxArray(self.value.trace(offset=offset, axis1=axis1, axis2=axis2, dtype=dtype))

  def transpose(self, *axes):
    """Returns a view of the array with axes transposed.

    For a 1-D array this has no effect, as a transposed vector is simply the
    same vector. To convert a 1-D array into a 2D column vector, an additional
    dimension must be added. `np.atleast2d(a).T` achieves this, as does
    `a[:, np.newaxis]`.
    For a 2-D array, this is a standard matrix transpose.
    For an n-D array, if axes are given, their order indicates how the
    axes are permuted (see Examples). If axes are not provided and
    ``a.shape = (i[0], i[1], ... i[n-2], i[n-1])``, then
    ``a.transpose().shape = (i[n-1], i[n-2], ... i[1], i[0])``.

    Parameters
    ----------
    axes : None, tuple of ints, or `n` ints

     * None or no argument: reverses the order of the axes.

     * tuple of ints: `i` in the `j`-th place in the tuple means `a`'s
       `i`-th axis becomes `a.transpose()`'s `j`-th axis.

     * `n` ints: same as an n-tuple of the same ints (this form is
       intended simply as a "convenience" alternative to the tuple form)

    Returns
    -------
    out : ndarray
        View of `a`, with axes suitably permuted.
    """
    return JaxArray(self.value.transpose(*axes))

  def tile(self, reps):
    """Construct an array by repeating A the number of times given by reps.

    If `reps` has length ``d``, the result will have dimension of
    ``max(d, A.ndim)``.

    If ``A.ndim < d``, `A` is promoted to be d-dimensional by prepending new
    axes. So a shape (3,) array is promoted to (1, 3) for 2-D replication,
    or shape (1, 1, 3) for 3-D replication. If this is not the desired
    behavior, promote `A` to d-dimensions manually before calling this
    function.

    If ``A.ndim > d``, `reps` is promoted to `A`.ndim by pre-pending 1's to it.
    Thus for an `A` of shape (2, 3, 4, 5), a `reps` of (2, 2) is treated as
    (1, 1, 2, 2).

    Note : Although tile may be used for broadcasting, it is strongly
    recommended to use numpy's broadcasting operations and functions.

    Parameters
    ----------
    reps : array_like
        The number of repetitions of `A` along each axis.

    Returns
    -------
    c : ndarray
        The tiled output array.
    """
    reps = reps.value if isinstance(reps, JaxArray) else reps
    return JaxArray(self.value.tile(reps))

  def var(self, axis=None, dtype=None, ddof=0, keepdims=False):
    """Returns the variance of the array elements, along given axis."""
    r = self.value.var(axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims)
    return r if (axis is None or keepdims) else JaxArray(r)

  def view(self, dtype=None, *args, **kwargs):
    """New view of array with the same data."""
    return JaxArray(self.value.view(dtype=dtype, *args, **kwargs))

  # ------------------
  # NumPy support
  # ------------------

  def numpy(self):
    """Convert to numpy.ndarray."""
    return np.asarray(self.value)

  def __array__(self):
    """Support ``numpy.array()`` and ``numpy.asarray()`` functions."""
    return np.asarray(self.value)


ndarray = JaxArray


class Variable(JaxArray):
  """The pointer to specify the dynamical variable.

  Parameters
  ----------
  value :
    Used to specify the data.
  """
  __slots__ = ()

  def __init__(self, value):
    if isinstance(value, JaxArray):
      value = value.value
    # assert jnp.ndim(value) >= 1, 'Must be an array, not scalar.'
    super(Variable, self).__init__(value)


class TrainVar(Variable):
  """The pointer to specify the trainable variable.
  """
  __slots__ = ()

  def __init__(self, value):
    if isinstance(value, JaxArray): value = value.value
    super(TrainVar, self).__init__(value)


class Parameter(Variable):
  """The pointer to specify the parameter.
  """
  __slots__ = ()

  def __init__(self, value):
    if isinstance(value, JaxArray): value = value.value
    super(Parameter, self).__init__(value)


register_pytree_node(JaxArray,
                     lambda t: ((t.value,), None),
                     lambda aux_data, flat_contents: JaxArray(*flat_contents))

register_pytree_node(Variable,
                     lambda t: ((t.value,), None),
                     lambda aux_data, flat_contents: Variable(*flat_contents))

register_pytree_node(TrainVar,
                     lambda t: ((t.value,), None),
                     lambda aux_data, flat_contents: TrainVar(*flat_contents))

register_pytree_node(Parameter,
                     lambda t: ((t.value,), None),
                     lambda aux_data, flat_contents: Parameter(*flat_contents))
