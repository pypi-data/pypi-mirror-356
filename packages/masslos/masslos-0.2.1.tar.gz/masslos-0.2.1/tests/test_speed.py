import unittest

from masslos.speed import Speed


class TestSpeed(unittest.TestCase):
    def setUp(self):
        self.speed = Speed()

    def test_in_ms(self):
        self.assertAlmostEqual(self.speed.in_ms(36, "km/h"), 10.0, places=2)
        self.assertAlmostEqual(self.speed.in_ms(1, "mph", 5), 0.44704, places=5)
        self.assertAlmostEqual(self.speed.in_ms(1, "fps", 4), 0.3048, places=4)
        self.assertAlmostEqual(self.speed.in_ms(1, "knot", 5), 0.5144444, places=5)
        self.assertAlmostEqual(self.speed.in_ms(1, "mach"), 343, places=0)
        self.assertAlmostEqual(self.speed.in_ms(1, "c"), 299792458, places=0)

    def test_in_kmh(self):
        self.assertAlmostEqual(self.speed.in_kmh(10, "m/s"), 36.0, places=2)
        self.assertAlmostEqual(self.speed.in_kmh(1, "mph", 5), 1.609344, places=5)
        self.assertAlmostEqual(self.speed.in_kmh(1, "fps", 5), 1.09728, places=5)
        self.assertAlmostEqual(self.speed.in_kmh(1, "knot", 5), 1.852, places=5)
        self.assertAlmostEqual(self.speed.in_kmh(1, "mach"), 1234.8, places=1)
        self.assertAlmostEqual(self.speed.in_kmh(1, "c"), 1079252762.5, places=1)

    def test_in_mph(self):
        self.assertAlmostEqual(self.speed.in_mph(10, "m/s", 4), 22.3694, places=4)
        self.assertAlmostEqual(self.speed.in_mph(36, "km/h", 4), 22.3694, places=4)
        self.assertAlmostEqual(self.speed.in_mph(1, "fps", 5), 0.681818, places=5)
        self.assertAlmostEqual(self.speed.in_mph(1, "knot", 5), 1.150779, places=5)
        self.assertAlmostEqual(self.speed.in_mph(1, "mach"), 767.269, places=2)
        self.assertAlmostEqual(self.speed.in_mph(1, "c"), 670616629, places=0)

    def test_in_fps(self):
        self.assertAlmostEqual(self.speed.in_fps(1, "m/s", 5), 3.28084, places=5)
        self.assertAlmostEqual(self.speed.in_fps(36, "km/h", 4), 32.8084, places=4)
        self.assertAlmostEqual(self.speed.in_fps(1, "mph", 5), 1.46667, places=5)
        self.assertAlmostEqual(self.speed.in_fps(1, "knot", 5), 1.68781, places=5)
        self.assertAlmostEqual(self.speed.in_fps(1, "mach"), 1125.33, places=2)
        self.assertAlmostEqual(self.speed.in_fps(1, "c"), 983571056, places=0)

    def test_in_knot(self):
        self.assertAlmostEqual(self.speed.in_knot(1, "m/s", 5), 1.94384, places=5)
        self.assertAlmostEqual(self.speed.in_knot(36, "km/h", 4), 19.4384, places=4)
        self.assertAlmostEqual(self.speed.in_knot(1, "mph", 5), 0.868976, places=5)
        self.assertAlmostEqual(self.speed.in_knot(1, "fps", 5), 0.592484, places=5)
        self.assertAlmostEqual(self.speed.in_knot(1, "mach", 2), 666.739, places=2)
        self.assertAlmostEqual(self.speed.in_knot(1, "c"), 582749969, places=0)

    def test_in_mach(self):
        self.assertAlmostEqual(self.speed.in_mach(343, "m/s", 5), 1.0, places=5)
        self.assertAlmostEqual(self.speed.in_mach(1234.8, "km/h"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_mach(767.269, "mph"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_mach(1125.33, "fps"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_mach(667.748, "knot"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_mach(1, "c"), 874030, places=0)

    def test_in_c(self):
        self.assertAlmostEqual(self.speed.in_c(299792458, "m/s", 5), 1.0, places=5)
        self.assertAlmostEqual(self.speed.in_c(1079252762.5, "km/h"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_c(670616629, "mph"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_c(983571056, "fps"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_c(582749918, "knot"), 1.0, places=2)
        self.assertAlmostEqual(self.speed.in_c(874030, "mach"), 1.0, places=2)


if __name__ == "__main__":
    unittest.main()
