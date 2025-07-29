from types import EllipsisType
from typing import Any, Generic, TypeAlias, overload
from typing_extensions import Buffer, TypeVar

import numpy as np
import optype as op
import optype.numpy as onp
import optype.numpy.compat as npc

from ._base import _spbase
from ._typing import Numeric

_ScalarT = TypeVar("_ScalarT", bound=Numeric)
_ScalarT_co = TypeVar("_ScalarT_co", bound=Numeric, default=Any, covariant=True)
_ShapeT_co = TypeVar("_ShapeT_co", bound=onp.AtLeast1D, default=onp.AtLeast0D[Any], covariant=True)

_Self1DT = TypeVar("_Self1DT", bound=IndexMixin[Any, _1D])
_Self2DT = TypeVar("_Self2DT", bound=IndexMixin[Any, _2D])

_ToInt: TypeAlias = str | op.CanInt | op.CanIndex | op.CanTrunc | Buffer
_ToFloat: TypeAlias = str | op.CanFloat | op.CanIndex | Buffer
_ToComplex: TypeAlias = str | op.CanComplex | op.CanFloat | op.CanIndex | complex

_1D: TypeAlias = tuple[int]  # noqa: PYI042
_2D: TypeAlias = tuple[int, int]  # noqa: PYI042

_ToIndex1D: TypeAlias = op.CanIndex | tuple[op.CanIndex]
_ToIndex2D: TypeAlias = tuple[op.CanIndex, op.CanIndex]

_ToSlice1D: TypeAlias = slice | EllipsisType | onp.ToJustInt2D | onp.ToBool1D
_ToSlice2D: TypeAlias = (
    slice
    | EllipsisType
    | tuple[_ToIndex1D | _ToSlice1D, _ToSlice1D]
    | tuple[_ToSlice1D, _ToSlice1D | _ToIndex1D]
    | onp.ToBool2D
    | list[bool]
    | list[np.bool_]
    | list[int]
    | _spbase[np.bool_, _2D]
)

###

INT_TYPES: tuple[type[int], type[np.integer[Any]]] = ...

class IndexMixin(Generic[_ScalarT_co, _ShapeT_co]):
    @overload
    def __getitem__(self: IndexMixin[Any, _1D], ix: op.CanIndex, /) -> _ScalarT_co: ...
    @overload
    def __getitem__(self: IndexMixin[Any, _2D], ix: _ToIndex2D, /) -> _ScalarT_co: ...
    @overload
    def __getitem__(self: _Self1DT, ixs: _ToSlice1D, /) -> _Self1DT: ...
    @overload
    def __getitem__(self: _Self2DT, ixs: _ToSlice2D, /) -> _Self2DT: ...

    #
    @overload
    def __setitem__(self: IndexMixin[_ScalarT, _1D], ix: op.CanIndex | _ToSlice1D, x: _ScalarT, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[_ScalarT], ix: _ToIndex2D | _ToSlice2D, x: _ScalarT, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.integer, _1D], ix: _ToIndex1D, x: _ToInt, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.integer], ix: _ToIndex2D, x: _ToInt, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.floating, _1D], ix: _ToIndex1D, x: _ToFloat, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.floating], ix: _ToIndex2D, x: _ToFloat, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.complexfloating, _1D], ix: _ToIndex1D, x: _ToComplex, /) -> None: ...
    @overload
    def __setitem__(self: IndexMixin[npc.complexfloating], ix: _ToIndex2D, x: _ToComplex, /) -> None: ...
    @overload
    def __setitem__(self, ix: _ToIndex1D | _ToSlice1D | _ToIndex2D | _ToSlice2D, x: object, /) -> None: ...
