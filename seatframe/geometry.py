"""Validated seating coordinates and a CPU perspective camera."""

from dataclasses import dataclass, fields
import json
import math
from pathlib import Path


WIDTH, HEIGHT, NEAR = 960, 540, 0.1


class SeatframeError(ValueError):
    """An input or projected view is outside the starter's supported geometry."""


def _number(value, label, positive=False):
    if type(value) not in (int, float):
        raise SeatframeError(f"{label} must be a finite number")
    try:
        value = float(value)
    except OverflowError as error:
        raise SeatframeError(f"{label} exceeds the numeric range") from error
    if not math.isfinite(value) or (positive and value <= 0):
        raise SeatframeError(f"{label} must be finite" + (" and positive" if positive else ""))
    return value


def _integer(value, label, maximum):
    if type(value) is not int or not 1 <= value <= maximum:
        raise SeatframeError(f"{label} must be an integer from 1 to {maximum}")
    return value


def _vector(value):
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise SeatframeError("A 3D vector needs exactly three finite numbers")
    return tuple(_number(item, "Vector component") for item in value)


def _dot(a, b):
    return _number(sum(x * y for x, y in zip(a, b)), "Vector product")


def _cross(a, b):
    return _vector(tuple(a[(i + 1) % 3] * b[(i + 2) % 3] - a[(i + 2) % 3] * b[(i + 1) % 3] for i in range(3)))


def _unit(vector):
    length = _number(math.hypot(*vector), "Vector length")
    if length < 1e-12:
        raise SeatframeError("Camera direction or up basis is degenerate")
    return tuple(component / length for component in vector)


@dataclass(frozen=True)
class Arena:
    id: str
    name: str
    section: int
    rows: int
    seats_per_row: int
    seat_pitch: float
    row_depth: float
    row_rise: float
    front_distance: float
    first_row_height: float
    playing_length: float
    playing_width: float

    def __post_init__(self):
        for name, maximum in (("id", 64), ("name", 120)):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip() or len(value) > maximum or not value.isprintable():
                raise SeatframeError(f"{name} must be nonempty printable text, at most {maximum} characters")
        for name, maximum in (("section", 9999), ("rows", 200), ("seats_per_row", 300)):
            _integer(getattr(self, name), name, maximum)
        for name in ("seat_pitch", "row_depth", "row_rise", "front_distance", "first_row_height", "playing_length", "playing_width"):
            object.__setattr__(self, name, _number(getattr(self, name), name, positive=True))
        if self.front_distance <= self.playing_width / 2:
            raise SeatframeError("front_distance must exceed half the playing width")


def parse_arena(value):
    expected = {field.name for field in fields(Arena)} | {"version"}
    if not isinstance(value, dict) or set(value) != expected or type(value["version"]) is not int or value["version"] != 1:
        raise SeatframeError("Arena needs exactly the version 1 geometry fields")
    return Arena(**{key: item for key, item in value.items() if key != "version"})


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SeatframeError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise SeatframeError(f"Invalid JSON constant: {value}")


def load_arena(path):
    try:
        with Path(path).open("rb") as stream:
            data = stream.read(65537)
        if len(data) > 65536:
            raise SeatframeError("Arena file exceeds 64 KiB")
        return parse_arena(json.loads(data.decode("utf-8-sig"), object_pairs_hook=_pairs, parse_constant=_constant))
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise SeatframeError(f"Cannot read arena: {error}") from error


def seat_eye(arena, row, seat, eye_height=1.15):
    _integer(row, "Row", arena.rows)
    _integer(seat, "Seat", arena.seats_per_row)
    eye_height = _number(eye_height, "Eye height", positive=True)
    return _vector(((seat - (arena.seats_per_row + 1) / 2) * arena.seat_pitch,
                    -arena.front_distance - (row - 1) * arena.row_depth,
                    arena.first_row_height + (row - 1) * arena.row_rise + eye_height))


@dataclass(frozen=True)
class Camera:
    eye: tuple
    right: tuple
    up: tuple
    forward: tuple


def look_at(eye, target=(0, 0, 0)):
    eye, target = _vector(eye), _vector(target)
    forward = _unit(_vector(tuple(target[i] - eye[i] for i in range(3))))
    right = _unit(_cross(forward, (0, 0, 1)))
    return Camera(eye, right, _unit(_cross(right, forward)), forward)


def project(point, camera, fov_degrees=60):
    fov = _number(fov_degrees, "Vertical field of view")
    if not 10 <= fov <= 120:
        raise SeatframeError("Vertical field of view must be from 10 to 120 degrees")
    point = _vector(point)
    relative = _vector(tuple(point[i] - camera.eye[i] for i in range(3)))
    depth = _dot(relative, camera.forward)
    if depth <= NEAR:
        return None
    focal = HEIGHT / (2 * math.tan(math.radians(fov) / 2))
    return (_number(WIDTH / 2 + focal * _dot(relative, camera.right) / depth, "Screen x"),
            _number(HEIGHT / 2 - focal * _dot(relative, camera.up) / depth, "Screen y"))
