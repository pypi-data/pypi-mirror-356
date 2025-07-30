import unittest

from masslos.weight import Weight


class TestWeightConversion(unittest.TestCase):
    def setUp(self):
        self.weight = Weight()

    def test_convert_weight_kg_to_g(self):
        self.assertEqual(self.weight.convert(1, "kg", "g"), 1000)

    def test_convert_weight_g_to_kg(self):
        self.assertEqual(self.weight.convert(1000, "g", "kg"), 1)

    def test_convert_weight_lb_to_kg(self):
        self.assertAlmostEqual(self.weight.convert(2.20462, "lbs", "kg"), 1, places=3)

    def test_convert_weight_kg_to_lb(self):
        self.assertAlmostEqual(
            self.weight.convert(1, "kg", "lbs", 5),
            2.20462,
            places=3,
        )

    def test_convert_weight_oz_to_g(self):
        self.assertAlmostEqual(self.weight.convert(1, "oz", "g"), 28.34952, places=3)

    def test_convert_weight_tonne_to_kg(self):
        self.assertEqual(self.weight.convert(1, "t", "kg"), 1000)

    def test_convert_weight_invalid_unit(self):
        self.assertIsNone(self.weight.convert(1, "foo", "kg"))

    def test_convert_weight_invalid_value(self):
        self.assertIsNone(self.weight.convert("abc", "kg", "g"))

    def test_in_pound(self):
        self.assertAlmostEqual(self.weight.in_pound(1, "kg", 5), 2.20462, places=3)

    def test_in_ounce(self):
        self.assertAlmostEqual(self.weight.in_ounce(1, "kg", 5), 35.27396, places=3)

    def test_in_gram(self):
        self.assertEqual(self.weight.in_gram(1, "kg"), 1000)

    def test_in_kilogram(self):
        self.assertEqual(self.weight.in_kilogram(1000, "g"), 1)

    def test_in_tonne(self):
        self.assertEqual(self.weight.in_tonne(1000, "kg"), 1)

    def test_case_insensitivity_and_spaces(self):
        self.assertEqual(self.weight.convert(1, " KiloGram ", " g "), 1000)


if __name__ == "__main__":
    unittest.main()
