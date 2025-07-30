import unittest

from masslos.unit import Unit


class TestUnit(unittest.TestCase):
    def setUp(self):
        # Example unit dictionary for testing
        self.unit_dict = {
            "kg": 1.0,
            "g": 1000.0,
            "lb": 2.20462,
        }
        self.unit = Unit(self.unit_dict)

    def test_convert_same_unit(self):
        self.assertEqual(self.unit.convert(1, "kg", "kg"), 1.0)

    def test_convert_kg_to_g(self):
        self.assertEqual(
            self.unit.convert(1, "kg", "g"),
            0.0,
        )  # 1/1000 = 0.001, rounded to 2 digits

    def test_convert_g_to_kg(self):
        self.assertEqual(self.unit.convert(1000, "g", "kg"), 1000000.0)

    def test_convert_kg_to_lb(self):
        result = self.unit.convert(1, "kg", "lb")
        self.assertIsInstance(result, float)

    def test_convert_invalid_unit(self):
        self.assertIsNone(self.unit.convert(1, "kg", "oz"))

    def test_convert_invalid_value(self):
        self.assertIsNone(self.unit.convert("abc", "kg", "g"))

    def test_list_units(self):
        units = self.unit.list_units()
        self.assertIn("kg", units)
        self.assertIn("g", units)
        self.assertIn("lb", units)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
