import unittest

from masslos.distance import Distance


class TestDistances(unittest.TestCase):
    def setUp(self):
        self.distance = Distance()

    def test_metric(self):
        self.assertEqual(self.distance.convert(1, "m", "dm"), 10)
        self.assertEqual(self.distance.convert(0, "m", "dm"), 0)
        self.assertEqual(self.distance.convert(-5, "m", "dm"), -50)

    def test_imperial(self):
        self.assertAlmostEqual(self.distance.convert(1, "FEET", "INCH"), 12)

    def test_non_value(self):
        self.assertIsNone(self.distance.convert("foo", "m", "cm"))

    def test_key_tolerance(self):
        self.assertIsNotNone(self.distance.convert(1, "m", "dm"))
        self.assertIsNotNone(self.distance.convert(1, "m", "DM"))
        self.assertIsNotNone(self.distance.convert(1, "M", "dm"))
        self.assertIsNotNone(self.distance.convert(1, "M", "DM"))
        self.assertIsNotNone(self.distance.convert(1, "m", "dM"))
        self.assertIsNotNone(self.distance.convert(1, "m", "Dm"))
        self.assertIsNotNone(self.distance.convert(1, "Light Year", "Km"))

    def test_key_unknwon(self):
        self.assertIsNone(self.distance.convert(1, "foo", "m"))
        self.assertIsNone(self.distance.convert(1, "m", "foo"))
        self.assertIsNone(self.distance.convert(1, "foo", "foo"))


if __name__ == "__main__":
    unittest.main()
