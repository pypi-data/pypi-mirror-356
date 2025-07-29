import os
import sys
import datetime
import pytz

import pandas as pd


def _make_timestamp(r: pd.Series, field_name_root) -> pd.Timestamp:
    """Take a TAQ row and convert to more Pythonic time information"""
    row_time = r[field_name_root]
    if isinstance(row_time, pd.Timedelta):
        t = r.date + row_time
    else:
        try:
            t = datetime.datetime.combine(r.date, row_time)
        except TypeError as te:
            print(
                f"Unable to form a datetime from a {r.date.__class__} equal to {r.date} and a '{field_name_root}' of class {row_time.__class__} equal to {row_time}"
            )
            raise te
    loc_t = pd.to_datetime(t).tz_localize(pytz.timezone("America/New_York"))
    pdt = loc_t + pd.Timedelta(r[f"{field_name_root}_ns"], unit="ns")
    return pdt


# Chattiness control for when we look at db tables
# From:  https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
class HidePrinting:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
