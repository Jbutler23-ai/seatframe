from copy import deepcopy
from math import radians, tan
import unittest

from seatframe.geometry import HEIGHT, WIDTH, SeatframeError, look_at, parse_arena, project, seat_eye


def synthetic_arena():
    return {
        "version": 1, "id": "synthetic-bank", "name": "Fictional test seating bank", "section": 101,
        "rows": 8, "seats_per_row": 16, "seat_pitch": 0.52, "row_depth": 0.85, "row_rise": 0.4,
        "front_distance": 18.0, "first_row_height": 1.2, "playing_length": 28.0, "playing_width": 15.0,
    }


class GeometryTests(unittest.TestCase):
    def assert_vector_close(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for component, reference in zip(actual, expected):
            self.assertAlmostEqual(component, reference, places=11)

    def test_seat_coordinates_match_centered_spacing_and_documented_row_offsets(self):
        source = synthetic_arena()
        original = deepcopy(source)
        arena = parse_arena(source)
        self.assert_vector_close(seat_eye(arena, 4, 8), (-0.26, -20.55, 3.55))
        self.assert_vector_close(seat_eye(arena, 4, 9), (0.26, -20.55, 3.55))
        self.assertEqual(source, original)

    def test_row_and_eye_height_changes_move_only_the_expected_axes(self):
        arena = parse_arena(synthetic_arena())
        first = seat_eye(arena, 4, 8)
        next_row = seat_eye(arena, 5, 8)
        taller = seat_eye(arena, 4, 8, eye_height=1.65)
        self.assert_vector_close(tuple(after - before for before, after in zip(first, next_row)),
                                 (0.0, -0.85, 0.4))
        self.assert_vector_close(tuple(after - before for before, after in zip(first, taller)),
                                 (0.0, 0.0, 0.5))

    def test_optical_center_symmetry_and_perspective_distance_match_pinhole_geometry(self):
        camera = look_at((0.0, -10.0, 0.0), target=(0.0, 0.0, 0.0))
        focal_length = HEIGHT / (2 * tan(radians(60) / 2))
        self.assert_vector_close(project((0.0, 0.0, 0.0), camera), (WIDTH / 2, HEIGHT / 2))
        left = project((-2.0, 0.0, 0.0), camera)
        right = project((2.0, 0.0, 0.0), camera)
        farther = project((2.0, 10.0, 0.0), camera)
        self.assert_vector_close(left, (WIDTH / 2 - focal_length * 2 / 10, HEIGHT / 2))
        self.assert_vector_close(right, (WIDTH / 2 + focal_length * 2 / 10, HEIGHT / 2))
        self.assertAlmostEqual(farther[0] - WIDTH / 2, (right[0] - WIDTH / 2) / 2, places=11)
        self.assert_vector_close(project((0.0, 0.0, 2.0), camera),
                                 (WIDTH / 2, HEIGHT / 2 - focal_length * 2 / 10))

    def test_camera_basis_handles_rotation_and_translation_without_mirroring(self):
        baseline = project((2.0, 0.0, 1.0), look_at((0.0, -10.0, 0.0)))
        rotated = project((0.0, 2.0, 1.0), look_at((10.0, 0.0, 0.0)))
        shifted = project((5.0, -4.0, 3.0), look_at((3.0, -14.0, 2.0), target=(3.0, -4.0, 2.0)))
        self.assert_vector_close(rotated, baseline)
        self.assert_vector_close(shifted, baseline)

    def test_near_plane_and_degenerate_camera_cases_are_explicit(self):
        camera = look_at((0.0, 0.0, 0.0), target=(0.0, 1.0, 0.0))
        for point in ((0.0, -1.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.1, 0.0)):
            with self.subTest(point=point):
                self.assertIsNone(project(point, camera))
        self.assert_vector_close(project((0.0, 0.11, 0.0), camera), (WIDTH / 2, HEIGHT / 2))
        for eye, target in (((1, 2, 3), (1, 2, 3)), ((0, 0, 10), (0, 0, 0))):
            with self.subTest(eye=eye, target=target):
                with self.assertRaises(SeatframeError):
                    look_at(eye, target=target)

    def test_invalid_dimensions_selectors_and_nonfinite_projection_are_rejected(self):
        for field, value in (("rows", True), ("seat_pitch", 0), ("row_rise", float("nan")),
                             ("front_distance", 7.5), ("version", True)):
            with self.subTest(field=field, value=value):
                data = synthetic_arena()
                data[field] = value
                with self.assertRaises(SeatframeError):
                    parse_arena(data)
        arena = parse_arena(synthetic_arena())
        for row, seat in ((0, 1), (9, 1), (1, 0), (1, 17), (True, 1)):
            with self.subTest(row=row, seat=seat):
                with self.assertRaises(SeatframeError):
                    seat_eye(arena, row, seat)
        camera = look_at((0, -10, 0))
        with self.assertRaises(SeatframeError):
            project((float("inf"), 0, 0), camera)
        with self.assertRaises(SeatframeError):
            project((0, 0, 0), camera, fov_degrees=float("nan"))


if __name__ == "__main__":
    unittest.main()
