import base64
import json
import os
from datetime import datetime
from itertools import count
from typing import Union, Annotated

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.testing import rowset
from sqlmodel import Session

from dependency_injection import SessionDep, create_db_and_tables
from entities import ExperimentCreate, Experiment, ExperimentRowCreate, ExperimentRow, Counter, CounterType

app = FastAPI()


# create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/experiment/", response_model=Experiment)
def read_item(session: SessionDep, experiment: ExperimentCreate):
    new_experiment = Experiment(
        experiment_name=experiment.experiment_name,
        creator_name=experiment.creator_name,
        create_at=datetime.utcnow(),
        update_at=datetime.utcnow(),
        sampling_rate=experiment.sampling_rate,
        sender_type=experiment.sender_type,
        comment=experiment.comment,
    )
    session.add(new_experiment)
    session.commit()
    session.refresh(new_experiment)
    return new_experiment


@app.post("/experiments/{experiment_id}/rows/", response_model=ExperimentRow)
def create_experiment_row(
        experiment_id: int,
        row: ExperimentRowCreate,
        session: SessionDep):
    new_row = ExperimentRow(
        experiment_id=experiment_id,
        latitude=row.latitude,
        longitude=row.longitude,
        counters=row.serialize_counters(),
        allowed_speed=row.allowed_speed,
        current_speed=row.current_speed,
        temperature=row.temperature,
        humidity=row.humidity,
        start_time=row.start_time,
        end_time=row.end_time,
    )
    try:
        if row.record_file.startswith("data:audio/mpeg;base64,"):
            audio_data = base64.b64decode(row.record_file.split(",")[1])
        elif row.record_file.startswith("data:audio/wav;base64,"):
            audio_data = base64.b64decode(row.record_file.split(",")[1])
        else:
            raise HTTPException(status_code=400, detail="Invalid audio format. Must be MP3 or WAV.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Base64 input.")

    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    file_addr = "./{}/{}.mp3".format(experiment_id, new_row.id)
    with open(file_addr, "wb") as f:
        f.write(audio_data)
    new_row.record = file_addr

    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    return new_row

    #
    #
    # # print("Here")
    # #
    # #
    # # ter = Counter()
    # # ter.count = 2
    # # print("Here1")
    # # ter.counter_type = CounterType.TRUCK
    # # print("Here3")
    # #
    # # print(json.dump(ter, indent=4))
    # print("Her4")
    # new_row = ExperimentRow(
    #
    # )
    # session.add(new_row)
    # await session.commit()
    # await session.refresh(new_row)
    # return new_row
