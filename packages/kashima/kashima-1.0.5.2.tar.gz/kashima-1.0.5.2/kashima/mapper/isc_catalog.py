"""
ISC‑GEM (version 11.0) catalogue loader
======================================

Produces a dataframe with the *same* columns used by the USGS helper so
that EventMap, legend.csv, and tooltips work seamlessly.

Unified schema
--------------
time | latitude | longitude | depth | mag | mag_type | place | event_id | source
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from .utils import stream_read_csv_bbox

# ---------------------------------------------------------------------
# Fixed column list for the raw v11.0 CSV (do not change order)
# ---------------------------------------------------------------------
COLS = [
    "time_str",
    "latitude",
    "longitude",
    "smajax",
    "sminax",
    "strike",
    "epi_q",
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


# ---------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------
def load_isc(
    path: str | Path,
    bbox: tuple[float, float, float, float] | None = None,
) -> pd.DataFrame:
    """
    Parameters
    ----------
    path : str or Path
        Path to the ISC‑GEM main catalogue CSV.
    bbox : (min_lon, max_lon, min_lat, max_lat), optional
        Bounding box to pre‑filter rows while streaming.

    Returns
    -------
    pd.DataFrame
        Columns: time, latitude, longitude, depth,
                 mag, mag_type, place, event_id, source
    """
    usecols = ["time_str", "latitude", "longitude", "depth_km", "mw", "eventid"]
    dtypes = {
        "latitude": "float64",
        "longitude": "float64",
        "depth_km": "float32",
        "mw": "float32",
        "eventid": "string",
    }

    df = stream_read_csv_bbox(
        path,
        bbox=bbox,
        lat_col="latitude",
        lon_col="longitude",
        chunksize=50_000,
        dtype_map=dtypes,
        sep=r"\s*,\s*",  # comma + optional spaces
        engine="python",
        comment="#",  # skip header lines
        names=COLS,
        usecols=usecols,
        parse_dates={"time": ["time_str"]},  # <-- correct column
        keep_date_col=False,
    )

    # Rename + add missing columns to align with USGS schema
    df = df.rename(
        columns={
            "depth_km": "depth",
            "mw": "mag",
            "eventid": "event_id",
        }
    ).assign(
        mag_type="Mw",
        place=pd.NA,  # ISC has no 'place' field
        source="ISC-GEM",
    )[
        [
            "time",
            "latitude",
            "longitude",
            "depth",
            "mag",
            "mag_type",
            "place",
            "event_id",
            "source",
        ]
    ]

    return df
