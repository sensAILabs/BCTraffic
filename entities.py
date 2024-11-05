import json
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, constr
from pydantic_core.core_schema import DatetimeSchema
from sqlmodel import Field, SQLModel, Relationship, Column, JSON, DATETIME


class SenderType(str, Enum):
    PC = "pc"
    PHONE = "phone"
    HARDWARE = "hardware"


class CounterType(str, Enum):
    # GASOLINE = "gasoline"
    # DIESEL = "diesel"
    # HYBRID = "hybrid"
    CAR = "car"
    STREET_CAR = "street_car"
    TRUCK = "truck"
    BUS = "bus"
    SMALL_TRUCK = "small_truck"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, CounterType))


class Counter(BaseModel):
    counter_type: CounterType
    count: int


class ExperimentBase(SQLModel):
    experiment_name: str
    creator_name: str
    sampling_rate: int
    comment: Optional[str] = None
    sender_type: SenderType


class Experiment(ExperimentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: datetime
    update_at: datetime
    rows: List["ExperimentRow"] = Relationship(back_populates="experiment")


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentRowBase(SQLModel):
    latitude: float
    longitude: float
    allowed_speed: int
    current_speed: int
    temperature: int
    humidity: int
    wind_speed: int
    start_time: datetime
    end_time: datetime
    counters: list[Counter] | str = Field(sa_column=Column(JSON))

    def serialize_counters(self):
        if isinstance(self.counters, list) and all(isinstance(c, Counter) for c in self.counters):
            return json.dumps([c.model_dump() for c in self.counters])
        return self.counters

    @classmethod
    def get_counters(self, **kwargs: Any):
        print(json.loads(self.counters))
        # if 'counters' in kwargs and isinstance(kwargs['counters'], str):
        #     # Convert the JSON string back to a list of Counter instances
        #     counters_data = json.loads(kwargs['counters'])
        #     kwargs['counters'] = [Counter(**counter) for counter in counters_data]
        # return cls(**kwargs)


class ExperimentRow(ExperimentRowBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: int = Field(foreign_key="experiment.id")
    experiment: "Experiment" = Relationship(back_populates="rows")
    record: str | None


class RecordedObject(SQLModel):
    object_name: str
    storage_address: str
    start_time: datetime
    end_time: datetime
