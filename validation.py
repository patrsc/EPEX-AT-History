"""Data validation."""
from pydantic import BaseModel
from typing import Literal


class DataObject(BaseModel):
    start_timestamp: int
    end_timestamp: int
    marketprice: float
    unit: Literal["Eur/MWh"]


class ResponseData(BaseModel):
    object: Literal["list"]
    data: list[DataObject]
    url: Literal["/at/v1/marketdata"]


def validate(data, start_time: int, end_time: int):
    d = ResponseData.model_validate(data)
    assert len(d.data) >= 23, "data contains less than 23 hours"
    assert d.data[0].start_timestamp == start_time, "data does not start with start time"
    assert d.data[-1].end_timestamp == end_time, "data does not end with end time"
