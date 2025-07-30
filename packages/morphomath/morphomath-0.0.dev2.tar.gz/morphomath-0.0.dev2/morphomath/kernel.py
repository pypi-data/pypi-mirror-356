#!/usr/bin/env python3

"""Kernel representation."""

import typing

import numpy as np


class Kernel:
    """A binary morphological kernel.

    Attributes
    ----------
    tensor : np.ndarray[np.uint8, ...]
        The binary kernel as a readonly ndarray.
    points : set[tuple[int, ...]]
        The points in the kernel, relative to and arbitrary reference.
    points_array : np.ndarray[np.int64, np.int64]
        The 2d numpy array of the individuals, sorted in lexicographic order.
        The origin is set at the first point.
        By convention, the shape is (nbr_points, dim).
    dim : int
        The dimension of the kernel, 2 for images, 3 for video...
    """

    def __init__(self, kernel: np.ndarray | list):
        """Initialise the kernel.

        Parameters
        ----------
        kernel : arraylike
            The kernel tensor. All non zero values become 1.
        """
        self._tensor: np.ndarray[np.uint8, ...] = np.asarray(kernel).astype(np.uint8, copy=False)
        self._points: set[tuple[int, ...]] = None
        self._points_array: np.ndarray[np.int64, np.int64] = None

    def anchors(self, other: typing.Self) -> tuple[int, ...]:
        """Yield all the positions where other can fit into self.

        Examples
        --------
        >>> from morphomath.kernel import Kernel
        >>> ref = Kernel([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        >>> list(ref.anchors(Kernel([[1, 1]])))
        [(0, 0), (0, 1), (2, 0), (2, 1)]
        >>>
        """
        def _is_in(self_points: list[list[int]], other_points: list[list[int]]) -> bool:
            if not other_points:
                return True
            for i in range(len(self_points)-len(other_points)+1):
                if other_points[0] == self_points[i]:
                    return _is_in(self_points[i+1:], other_points[1:])
            return False

        for i in range(len(self.points_array)-len(other.points_array)+1):
            shift = self.points_array[i] - other.points_array[0]
            if _is_in(self.points_array[i+1:].tolist(), (other.points_array[1:] + shift).tolist()):
                yield tuple(shift.tolist())

    @property
    def dim(self) -> int:
        """Return the dimension of the kernel."""
        return self.points_array.shape[1]

    @classmethod
    def _from_points(cls, points: set[tuple[int, ...]]) -> typing.Self:
        """Construct a new kernel from the points."""
        kernel = cls.__new__(cls)
        kernel._tensor = None
        kernel._points = points
        kernel._points_array = None
        return kernel

    @property
    def tensor(self) -> np.ndarray[np.uint8, ...]:
        """Return the binary kernel as a readonly ndarray."""
        if self._tensor is None:
            # tensor from points
            shape = [max(d) - min(d) + 1 for d in zip(*self._points)]
            self._tensor = np.zeros(shape, np.uint8)
            mini = [min(d) for d in zip(*self._points)]
            points = [[c-m for c, m in zip(p, mini)] for p in self._points]
            self._tensor[*zip(*points)] = 1
            self._tensor.flags.writeable = False
        return self._tensor

    @property
    def points(self) -> set[tuple[int, ...]]:
        """Return the points of the kernel."""
        if self._points is None:
            self._points = set(zip(*(d.tolist() for d in np.nonzero(self._tensor))))
        return self._points

    @property
    def points_array(self) -> np.ndarray[np.int64, np.int64]:
        """Return the array of the sorted points anchorded at origin."""
        if self._points_array is None:
            self._points_array = np.asarray(sorted(self.points), dtype=np.int64)
            self._points_array -= self._points_array[0, :]  # set anchor
            self._points_array.flags.writeable = False
        return self._points_array

    def __contains__(self, other: typing.Self) -> bool:
        """Test if other is in self.

        Examples
        --------
        >>> from morphomath.kernel import Kernel
        >>> Kernel([[1, 0], [0, 1]]) in Kernel([[0, 0, 1], [0, 1, 1], [1, 0, 1]])
        True
        >>> Kernel([[1, 0], [1, 1]]) in Kernel([[0, 0, 1], [0, 1, 1], [1, 0, 1]])
        False
        >>>
        """
        try:
            next(iter(self.anchors(other)))
        except StopIteration:
            return False
        return True

    def __hash__(self) -> int:
        """Return the hash of the kernel."""
        return hash(self.points_array.tobytes())

    def __eq__(self, other: typing.Self) -> bool:
        """For hash table colision."""
        return np.array_equal(self.points_array, other.points_array)

    def __repr__(self) -> str:
        """Return a representation of the kernel."""
        return f"{self.__class__.__name__}({self.tensor.tolist()})"
