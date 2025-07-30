import unittest

from masslos import distance


class TestDistances(unittest.TestCase):
    def test_metric(self):
        self.assertEqual(distance.convert_distance(1, "m", "dm"), 10)
        self.assertEqual(distance.convert_distance(0, "m", "dm"), 0)
        self.assertEqual(distance.convert_distance(-5, "m", "dm"), -50)

    def test_imperial(self):
        self.assertAlmostEqual(distance.convert_distance(1, "FEET", "INCH"), 12)

    def test_non_value(self):
        self.assertIsNone(distance.convert_distance("foo", "m", "cm"))

    def test_key_tolerance(self):
        self.assertIsNotNone(distance.convert_distance(1, "m", "dm"))
        self.assertIsNotNone(distance.convert_distance(1, "m", "DM"))
        self.assertIsNotNone(distance.convert_distance(1, "M", "dm"))
        self.assertIsNotNone(distance.convert_distance(1, "M", "DM"))
        self.assertIsNotNone(distance.convert_distance(1, "m", "dM"))
        self.assertIsNotNone(distance.convert_distance(1, "m", "Dm"))
        self.assertIsNotNone(distance.convert_distance(1, "Light Year", "Km"))

    def test_key_unknwon(self):
        self.assertIsNone(distance.convert_distance(1, "foo", "m"))
        self.assertIsNone(distance.convert_distance(1, "m", "foo"))
        self.assertIsNone(distance.convert_distance(1, "foo", "foo"))


if __name__ == "__main__":
    unittest.main()
