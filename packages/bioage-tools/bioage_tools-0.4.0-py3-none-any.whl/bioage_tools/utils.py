import pandas as pd
import numpy as np

DAYS_PER_YEAR = 365

def compute_age(sample_date, birthday):
    try:
        delta = pd.to_datetime(sample_date) - pd.to_datetime(birthday)
    except pd.errors.OutOfBoundsDatetime:
        return np.nan
    if type(delta) is pd.Series:
        return delta.dt.days / DAYS_PER_YEAR
    else:
        return delta.days / DAYS_PER_YEAR
