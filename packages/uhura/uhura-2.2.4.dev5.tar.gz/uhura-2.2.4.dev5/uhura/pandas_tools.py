from collections import defaultdict
from typing import Any

import pandas as pd

from uhura.comparison import Comparer


def compare_data(data1: Any, data2: Any):
    assert type(data1) is type(data2), f"Data types do not match: {type(data1)} vs {type(data2)}"
    datatype = type(data1)
    if datatype not in COMPARISON_LOOKUP:
        assert data1 == data2, "Observed != Expected"
    else:
        COMPARISON_LOOKUP[datatype](data1, data2)


class PandasComparer(Comparer):
    def base_compare(self, actual, expected):
        return compare_data(actual, expected)


COMPARISON_LOOKUP = {
    pd.DataFrame: pd.testing.assert_frame_equal,
    pd.Series: pd.testing.assert_series_equal,
}

pandas_comparator = defaultdict(PandasComparer)
