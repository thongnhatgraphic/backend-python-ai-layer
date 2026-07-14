import random
import numpy as np
import pandas as pd


def generate_random_indices(
    vl_from: int, vl_to: int, size: int, seed: int | None = None
):
    rng = np.random.default_rng(seed)
    list_value = rng.integers(vl_from, vl_to, size)

    return list_value


def generate_random_rows(
    vl_from: int, vl_to: int, amount: int, seed: int | None = None
):
    rng = random.Random(seed)

    return rng.sample(range(vl_from, vl_to), amount)


def generate_random_cells(
    num_rows: int,
    columns: list[str],
    amount: int,
    seed: int | None = None,
):
    num_columns = len(columns)

    random_index_list = generate_random_rows(0, num_rows, amount, seed)
    list_name_collumn = generate_random_indices(0, num_columns, amount, seed)

    cells: list[tuple[int, str]] = []

    for row, column in zip(random_index_list, list_name_collumn):
        cells.append((row, column))

    return cells
    # return [
    #     (row, columns[col_idx])
    #     for row, col_idx in zip(random_index_list, list_name_collumn)
    # ]


def validate_columns(df: pd.DataFrame, columns: list[str]):
    if not columns:
        raise ValueError("columns must not be empty")
    if len(columns) != len(set(columns)):
        raise ValueError("columns must be unique")

    invalid_columns = set(columns) - set(df.columns)
    if invalid_columns:
        raise ValueError(f"Columns not found in dataframe: {sorted(invalid_columns)}")


def validate_percent(percent: float, percent_rule: float):
    if percent <= 0 or percent > percent_rule:
        raise ValueError(f"'percent' must be in the range (0, {percent_rule}].")
