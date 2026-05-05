from __future__ import annotations

import sys
import csv
import math
from dataclasses import dataclass
from typing import *

sys.setrecursionlimit(10_000)


EXPECTED_HEADER = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]


@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]


@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node] = None


def parse_float(text: str) -> Optional[float]:
    if text == "":
        return None
    return float(text)


def parse_row(fields: list[str]) -> Row:
    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=parse_float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=parse_float(fields[3]),
        energy_co2_emissions=parse_float(fields[4]),
        energy_co2_emissions_per_capita=parse_float(fields[5]),
        total_co2_emissions_excluding_lucf=parse_float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=parse_float(fields[7]),
    )


def build_list(rows: list[list[str]], index: int = 0) -> Optional[Node]:
    if index >= len(rows):
        return None

    return Node(parse_row(rows[index]), build_list(rows, index + 1))


def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        if header != EXPECTED_HEADER:
            raise ValueError("unexpected first line: got: {}".format(header))

        rows = list(reader)

    return build_list(rows)


def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0

    return 1 + listlen(data.next)


def get_field(row: Row, field_name: str) -> Union[str, int, float, None]:
    if field_name == "country":
        return row.country
    if field_name == "year":
        return row.year
    if field_name == "electricity_and_heat_co2_emissions":
        return row.electricity_and_heat_co2_emissions
    if field_name == "electricity_and_heat_co2_emissions_per_capita":
        return row.electricity_and_heat_co2_emissions_per_capita
    if field_name == "energy_co2_emissions":
        return row.energy_co2_emissions
    if field_name == "energy_co2_emissions_per_capita":
        return row.energy_co2_emissions_per_capita
    if field_name == "total_co2_emissions_excluding_lucf":
        return row.total_co2_emissions_excluding_lucf
    if field_name == "total_co2_emissions_excluding_lucf_per_capita":
        return row.total_co2_emissions_excluding_lucf_per_capita

    raise ValueError("Invalid field name")


def matches(
    row: Row,
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> bool:
    field_value = get_field(row, field_name)

    if field_value is None:
        return False

    if field_name == "country" and comparison != "equal":
        raise ValueError("Only equal comparison is allowed for country")

    if comparison == "equal":
        return field_value == value
    if comparison == "less_than":
        return field_value < value
    if comparison == "greater_than":
        return field_value > value

    raise ValueError("Invalid comparison")


def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:
    if data is None:
        return None

    filtered_rest = filter_rows(data.next, field_name, comparison, value)

    if matches(data.value, field_name, comparison, value):
        return Node(data.value, filtered_rest)

    return filtered_rest