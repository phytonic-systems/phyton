import np
from math import *
from inspect import getmro as inspect
from phyton.constants.unit import rad

def check(obj, cls):
    return cls in inspect(type(obj))

def isnumeric(val):
    if type(val) in [np.generic, int, float, complex]: return True
    try: return bool(set(inspect(type(val))) & set([np.generic, int, float, complex]))
    except: return False

def _mag(*args):
    return sum([i**2 for i in args]) ** 0.5

def convert(value):
    if type(value) == SpatialVector or type(value) == _Scalar: return value
    elif isnumeric(value): return _Scalar(value)

class _Scalar(float): pass


class SpatialVector:
    def __init__(self, x = 0, y = 0, z = 0):
        """if column:
            super().__init__(self, [[x], [y], [z]], dtype=float)
        else:
            super().__init__(self, [x, y, z], dtype=float)

        self.column = column
        self.row = not row """

        self.x = convert(x)
        self.y = convert(y)
        self.z = convert(z)
        self.vec = (self.x, self.y, self.z)

    def dot(self, other):
        if check(other, SpatialVector):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else: return self * other

    def cross(self, other):
        if check(other, SpatialVector):
            return SpatialVector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        else: return self * other

    def angleFrom(self, other):
        if check(other, SpatialVector):
            return rad(acos(self.dot(other) / (self.mag *  other.mag)))

    @property
    def mag(self):
        return _mag(*self.vec)

    @property
    def unitVector(self):
        return self / self.mag

    def __repr__(self):
        return f"SpatialVector({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if check(other, SpatialVector):
            return SpatialVector(self.x + other.x, self.y + other.y, self.z + other.z)
        else: return self

    def __radd__(self, other):
        if check(other, SpatialVector):
            return SpatialVector(self.x + other.x , self.y + other.y , self.z + other.z)
        else: return self

    def __sub__(self, other):
        if check(other, SpatialVector):
            return SpatialVector(self.x - other.x , self.y - other.y , self.z - other.z)
        else: return self

    def __rsub__(self, other):
        if check(other, SpatialVector):
            return SpatialVector(other.x - self.x , other.y - self.y , other.z - self.z)
        else: return self

    def __truediv__(self, other):
        if check(other, SpatialVector):
            if other.x != 0 and other.y != 0 and other.z != 0:
                if self.x / other.x == self.y / other.y == self.z / other.z: return self.x / other.x
                else: return SpatialVector(self.x / other.mag, self.y / other.mag, self.z / other.mag)

            else: return SpatialVector(self.x / other.mag, self.y / other.mag, self.z / other.mag)

        else:
            other = convert(other)
            return SpatialVector(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other):
        if check(other, SpatialVector):
            return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self == other
