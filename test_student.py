import unittest
from proj2 import *


class TestParseRow(unittest.TestCase):
    def test_parse_row_basic(self):
        fields = ["USA", "2020", "1.5", "", "3.0", "", "10.0", ""]
        row = parse_row(fields)

        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 2020)
        self.assertEqual(row.electricity_and_heat_co2_emissions, 1.5)
        self.assertIsNone(row.electricity_and_heat_co2_emissions_per_capita)


class TestListLen(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(listlen(None), 0)

    def test_multiple_nodes(self):
        data = Node(
            Row("A", 2020, 1.0, None, None, None, None, None),
            Node(Row("B", 2021, 2.0, None, None, None, None, None))
        )
        self.assertEqual(listlen(data), 2)


class TestFilterRows(unittest.TestCase):
    def test_filter_equal_country(self):
        data = Node(
            Row("USA", 2020, 1.0, None, None, None, None, None),
            Node(Row("Canada", 2020, 2.0, None, None, None, None, None))
        )

        result = filter_rows(data, "country", "equal", "USA")

        self.assertEqual(listlen(result), 1)
        self.assertEqual(result.value.country, "USA")


    def test_filter_greater_than(self):
        data = Node(
            Row("USA", 2020, 5.0, None, None, None, None, None),
            Node(Row("Canada", 2020, 2.0, None, None, None, None, None))
        )

        result = filter_rows(
            data,
            "electricity_and_heat_co2_emissions",
            "greater_than",
            3.0
        )

        self.assertEqual(listlen(result), 1)
        self.assertEqual(result.value.country, "USA")


    def test_filter_skips_none(self):
        data = Node(
            Row("USA", 2020, None, None, None, None, None, None),
            Node(Row("Canada", 2020, 2.0, None, None, None, None, None))
        )

        result = filter_rows(
            data,
            "electricity_and_heat_co2_emissions",
            "greater_than",
            1.0
        )

        self.assertEqual(listlen(result), 1)
        self.assertEqual(result.value.country, "Canada")


if __name__ == "__main__":
    unittest.main()
