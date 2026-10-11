import unittest
from replay import replay


class FIFORepostingTests(unittest.TestCase):
    def test_before_edit(self):
        result = replay(60)
        self.assertEqual(result.jan15_issue_value, 4000.0)
        self.assertEqual(result.jan21_milk_consumption_value, 5800.0)
        self.assertEqual(result.powder_unit_cost, 580.0)
        self.assertEqual(result.jan25_powder_issue_value, 5800.0)
        self.assertEqual(result.remaining_milk_qty, 20.0)
        self.assertEqual(result.remaining_milk_value, 1200.0)

    def test_after_edit_reposts_dependent_manufacturing_and_issue(self):
        result = replay(80)
        self.assertEqual(result.jan15_issue_value, 4000.0)
        self.assertEqual(result.jan21_milk_consumption_value, 6800.0)
        self.assertEqual(result.powder_unit_cost, 680.0)
        self.assertEqual(result.jan25_powder_issue_value, 6800.0)
        self.assertEqual(result.remaining_milk_qty, 20.0)
        self.assertEqual(result.remaining_milk_value, 1200.0)

    def test_edit_changes_downstream_cost_by_1000(self):
        before = replay(60)
        after = replay(80)
        self.assertEqual(
            after.jan21_milk_consumption_value - before.jan21_milk_consumption_value,
            1000.0,
        )

    def test_insufficient_stock_raises(self):
        from fifo import FIFOStock

        stock = FIFOStock()
        stock.receive(2, 10)

        with self.assertRaises(ValueError):
            stock.issue(3)


if __name__ == "__main__":
    unittest.main()
