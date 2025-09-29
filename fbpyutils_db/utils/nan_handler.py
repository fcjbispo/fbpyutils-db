import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Any

def deal_with_nans(x: Any) -> Any:
    """
    Convert NaN, None, empty strings, and NaT to None; return other values unchanged.

    Handles pandas NaN, numpy NaN, empty str, and datetime NaT.

    Args:
        x: Input value of any type.

    Returns:
        Any: None for null-like values, else original x.

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> deal_with_nans(np.nan)
        None
        >>> deal_with_nans(pd.NaT)
        None
        >>> deal_with_nans('value')
        'value'
        # Returns None for NaN/NaT/None/empty, else input.
    """
    if pd.isna(x) or x is None or (isinstance(x, str) and not x):
        return None
    elif isinstance(x, (float, np.float64)) and np.isnan(x):
        return None
    elif isinstance(x, (datetime, pd.Timestamp)) and pd.isna(x):
        return None
    elif isinstance(x, date) and pd.isna(pd.Timestamp(x)):
        return None
    return x
