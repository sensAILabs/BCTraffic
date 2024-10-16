import base64
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from starlette.responses import HTMLResponse

from dependency_injection import SessionDep, create_db_and_tables
from entities import ExperimentCreate, Experiment, ExperimentRowCreate, ExperimentRow, CounterType

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
    print(temp[0])
    return templates.TemplateResponse(
        name="dashboard.html",
        context={"request": request, "page_title": "Dashboard", "experiments": temp},
    )


@app.get("/experiment/new", response_class=HTMLResponse)
def read_root(request: Request, session: SessionDep):
    statement = select(Experiment)
    results = session.exec(statement)
    temp = results.fetchall()
    print(temp[0])
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


@app.get("/experiment/{experiment_id}", response_model=Experiment)
def read_item(session: SessionDep, experiment_id: int, request: Request):
    statement = select(Experiment).where(Experiment.id == experiment_id)
    res = session.exec(statement)
    exp = res.first()
    return templates.TemplateResponse(
        name="new_row.html",
        context={"request": request, "page_title": "New Experiment", "experiment": exp, "counters": CounterType.list()},
    )


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
        wind_speed=row.wind_speed,
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
