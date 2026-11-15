import unittest
from jp_cost_estimator import costing


class TestCosting(unittest.TestCase):
    def test_tax_excluded(self):
        ex, tax, incl = costing.material_line(10, 1000, "tax_excluded")
        self.assertEqual(ex, 10000.0)
        self.assertEqual(tax, 1000.0)
        self.assertEqual(incl, 11000.0)

    def test_tax_included_reverse(self):
        ex, tax, incl = costing.material_line(1, 1100, "tax_included")
        self.assertAlmostEqual(ex, 1000.0, places=2)

    def test_labor(self):
        self.assertEqual(costing.labor_line(20000, 8), 20000.0)


if __name__ == "__main__":
    unittest.main()
