import base64
import json
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlmodel import select
from starlette.responses import HTMLResponse

from dependency_injection import SessionDep, create_db_and_tables
from entities import ExperimentCreate, Experiment, ExperimentRow, CounterType, ExperimentRowBase, CongestionLevel

TEMPLATES_AUTO_RELOAD = True
app = FastAPI()

create_db_and_tables()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, session: SessionDep):
    statement = select(Experiment)
    results = session.exec(statement)
    temp = results.fetchall()
    return templates.TemplateResponse(
        name="dashboard.html",
        context={"request": request, "page_title": "Dashboard", "experiments": temp},
    )


@app.get("/experiment/new", response_class=HTMLResponse)
def read_root(request: Request, session: SessionDep):
    statement = select(Experiment)
    results = session.exec(statement)
    temp = results.fetchall()
    return templates.TemplateResponse(
        name="dashboard.html", context={"request": request, "page_tsitle": "Dashboard", "experiments": temp},
    )


class Config:
    arbitrary_types_allowed = True


@app.post("/experiment/", response_model=Experiment)
def read_item(session: SessionDep, experiment: ExperimentCreate):
    new_experiment = Experiment(
        experiment_name=experiment.experiment_name,
        creator_name=experiment.creator_name,
        create_at=datetime.now(),
        update_at=datetime.now(),
        sampling_rate=experiment.sampling_rate,
        sender_type=experiment.sender_type,
        comment=experiment.comment,
    )
    session.add(new_experiment)
    session.commit()
    session.refresh(new_experiment)
    return new_experiment


@app.get("/experiment/{experiment_id}", response_model=Experiment)
def read_item(session: SessionDep, experiment_id: int, request: Request):
    statement = select(Experiment).where(Experiment.id == experiment_id)
    res = session.exec(statement)
    exp = res.first()
    return templates.TemplateResponse(
        name="new_row.html",
        context={"request": request, "page_title": "New Experiment", "experiment": exp,
                 "congestion_levels": CongestionLevel.list(), "counters": CounterType.list()},
    )


from pydantic import BaseModel


class Item(BaseModel):
    row_json: str = None
    file: UploadFile = File(None)


class Duration(BaseModel):
    date: str
    duration_second: int


@app.get("/experiments/all_duration")
def date_duration(session: SessionDep, request: Request):
    date_keys = {}

    sql = select(ExperimentRow.start_time, ExperimentRow.end_time)
    results = session.exec(sql).fetchall()

    for re in results:
        temp1 = re[0]
        temp2 = re[1]
        temp3 = temp2 - temp1
        key = "{}-{}-{}".format(temp1.date().year, temp1.date().month, temp1.date().day)
        if key in date_keys:
            date_keys[key] += temp3.total_seconds()
        else:
            date_keys[key] = temp3.total_seconds()

    return date_keys


@app.post("/experiments/{experiment_id}/rows/", response_model=ExperimentRow)
async def create_experiment_row(session: SessionDep,
                                experiment_id: int,
                                row_json: str = None,
                                file: UploadFile = File(...),
                                ):
    print(file)
    print("-------------------")
    row = json.loads(row_json)
    print(row)
    print(row.keys())

    new_row = ExperimentRow(
        experiment_id=experiment_id,
        latitude=row["latitude"],
        longitude=row["longitude"],
        counters=row["counters"],
        allowed_speed=row["allowed_speed"],
        current_speed=row["current_speed"],
        temperature=row["temperature"],
        humidity=row["humidity"],
        wind_speed=row["wind_speed"],
        start_time=datetime.fromtimestamp(row["start_time"] / 1000),
        end_time=datetime.fromtimestamp(row["end_time"] / 1000),
        congestion_level=row["congestion_level"],
    )

    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    base_addr = "/home/aryan/PycharmProjects/audioBC"
    file_addr = "/static/sound/experiment_id:{}-row:{}.wav".format(experiment_id, new_row.id)
    st = datetime.now()
    with open(base_addr + file_addr, "wb") as f:
        f.write(file.file.read())
        f.close()

    new_row.record = file_addr

    session.add(new_row)
    session.commit()
    session.refresh(new_row)

    print(st, datetime.now())
    return new_row
