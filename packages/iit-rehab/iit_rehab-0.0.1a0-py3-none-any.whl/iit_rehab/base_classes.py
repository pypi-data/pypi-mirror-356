"""Common base classes."""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from iit_rehab.definitions import LOG_FILE_EXT


@dataclass
class VectorXYZ:
    """XYZ Vector."""

    x: np.ndarray = field(default_factory=lambda: np.array([]))
    y: np.ndarray = field(default_factory=lambda: np.array([]))
    z: np.ndarray = field(default_factory=lambda: np.array([]))

    def __getitem__(self, index: int | slice) -> np.ndarray:
        """Return stacked XYZ components as a 2D array, or select one component.

        :param index: Index or slice for accessing stacked vector components.
                      0 = x, 1 = y, 2 = z; or a slice like 0:2
        :return: Stacked NumPy array of shape (3, N) or (K, N).
        :raises IndexError: If index is out of bounds.
        """
        stacked = np.stack([self.x, self.y, self.z], axis=1)
        return stacked[index].T

    def __len__(self) -> int:
        """Return the number of elements in the vector."""
        return len(self.x)


@dataclass
class Quaternion:
    """Quaternion."""

    w: np.ndarray = field(default_factory=lambda: np.array([]))
    x: np.ndarray = field(default_factory=lambda: np.array([]))
    y: np.ndarray = field(default_factory=lambda: np.array([]))
    z: np.ndarray = field(default_factory=lambda: np.array([]))

    def __getitem__(self, index: int | slice) -> np.ndarray:
        """Return stacked XYZ components as a 2D array, or select one component.

        :param index: Index or slice for accessing stacked vector components.
                      0 = x, 1 = y, 2 = z; or a slice like 0:2
        :return: Stacked NumPy array of shape (3, N) or (K, N).
        :raises IndexError: If index is out of bounds.
        """
        stacked = np.stack([self.w, self.x, self.y, self.z], axis=1)
        return stacked[index].T


@dataclass
class AngleXYZ:
    """XYZ Angle Vector."""

    x_deg: np.ndarray = field(default_factory=lambda: np.array([]))
    y_deg: np.ndarray = field(default_factory=lambda: np.array([]))
    z_deg: np.ndarray = field(default_factory=lambda: np.array([]))

    def __getitem__(self, index: int | slice) -> np.ndarray:
        """Return stacked XYZ components as a 2D array, or select one component.

        :param index: Index or slice for accessing stacked vector components.
                      0 = x, 1 = y, 2 = z; or a slice like 0:2
        :return: Stacked NumPy array of shape (3, N) or (K, N).
        :raises IndexError: If index is out of bounds.
        """
        stacked = np.stack([self.x_deg, self.y_deg, self.z_deg], axis=1)
        return stacked[index].T

    def __len__(self) -> int:
        """Return the number of elements in the vector."""
        return len(self.x_deg)


class SensorFile:
    """Represent a sensor category with left and right side access."""

    def __init__(self, category: str, base_path: Path) -> None:
        self.left = base_path / f"{category}_left{LOG_FILE_EXT}"
        self.right = base_path / f"{category}_right{LOG_FILE_EXT}"


@dataclass
class Limb:
    """Represent a side of the body."""

    time: np.ndarray
    accel: VectorXYZ
    gyro: VectorXYZ
    quat: Quaternion


@dataclass
class Joint:
    """Represent a side of the body."""

    time: np.ndarray
    angles: AngleXYZ


@dataclass
class Body:
    """Represent a body."""

    pelvis: Limb
    upper_leg: Limb
    lower_leg: Limb
    foot: Limb
    hip: Joint
    knee: Joint
    ankle: Joint


@dataclass
class LeftRight:
    """Represent a body."""

    left: Body
    right: Body
