from typing import TypedDict, NotRequired
import pandas as pd


class MeasurementGroupRecord(TypedDict):
    id: str
    latitude: float
    longitude: float
    start_date: NotRequired[pd.Timestamp]
    end_date: NotRequired[pd.Timestamp]
    distance_km: NotRequired[float]
    freq: NotRequired[str]
