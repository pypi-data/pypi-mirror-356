# /mapper/isc_catalog.py
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

COLS = [
    "time_str",
    "latitude",
    "longitude",
    "smajax",
    "sminax",
    "strike",
    "epic_q",
    "depth_km",
    "depth_unc",
    "depth_q",
    "mw",
    "mw_unc",
    "mw_q",
    "mw_src",
    "moment",
    "moment_fac",
    "mo_auth",
    "mpp",
    "mpr",
    "mrr",
    "mrt",
    "mtp",
    "mtt",
    "str1",
    "dip1",
    "rake1",
    "str2",
    "dip2",
    "rake2",
    "mech_type",
    "eventid",
]


def load_isc(path: str | Path) -> pd.DataFrame:
    """
    Parse an ISC‑GEM main catalogue (v11.0) file into a minimal unified
    dataframe required by EventMap: time, latitude, longitude, depth_km,
    magnitude, mag_type, event_id.
    """
    df = (
        pd.read_csv(
            path,
            comment="#",
            names=COLS,
            sep=r"\s*,\s*",  # comma *with* optional whitespace, python engine
            engine="python",
            na_values=["", " "],
            dtype={"eventid": "Int64"},
        )
        .assign(
            time=lambda d: pd.to_datetime(d["time_str"], utc=True),
            mag_type="Mw",
        )
        .rename(
            columns={
                "latitude": "latitude",
                "longitude": "longitude",
                "depth_km": "depth_km",
                "mw": "mag",
                "eventid": "event_id",
            }
        )[["time", "latitude", "longitude", "depth_km", "mag", "mag_type", "event_id"]]
    )
    return df
