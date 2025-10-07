Here’s a simple top-level `README.md` you can drop into the **parent folder** that contains both the dashboard app and the model package.

```markdown
# Black Carbon Project — Monorepo

This repository holds two parts of the Black Carbon (BC) project:

- **dashboard/** – FastAPI-based data collection dashboard (ingest + quick views)
- **model/** – XGBoost-based modeling workflow (data prep, training, inference)

> See each subfolder’s README for details.

---

## Repository Layout

```

.
├── dashboard/        # FastAPI app, Dockerfile, docker-compose, templates/static
│   └── README.md
├── model/            # Data, notebook, trained model (xgboost_model.pkl), requirements
│   └── README.md
└── README.md         # (this file)

````

---

## Quick Start

### 1) Run the Dashboard (Docker)
```bash
cd dashboard
docker compose up --build
# Open http://localhost:8000 (API docs at /docs)
````

### 2) Use the Model (Local)

```bash
cd model
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip -r requirements.txt
# Optional: start Jupyter to explore the notebook
jupyter lab  # open process_and_train.ipynb
```

**Inference (example):**

```python
# inside model/
import pandas as pd, pickle
df = pd.read_csv("shifted_datasets/corr_shift/3921.csv")
with open("xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

feature_cols = [  # adjust to match training features
    "car_line1","car_line1_stop","car_line2","car_line2_stop","car_line3","car_line3_stop",
    "truck_line1","truck_line1_stop","truck_line2","truck_line2_stop","truck_line3","truck_line3_stop",
    "summed","traffic",
    "history_temperature","history_wind_speed","history_humidity",
    "forecast_temperature","forecast_wind_speed","forecast_humidity",
]
df["BC_post_pred"] = model.predict(df[feature_cols])
df[["Time","BC","BC post","BC_post_pred"]].head()
```

---

## Development Notes

* Keep data schemas (feature names/order) in sync between `model/` and any ingestion/export logic in `dashboard/`.
* For production deployments, consider:

  * Postgres (instead of SQLite) for the dashboard
  * Authentication and CORS restrictions
  * Versioned model artifacts + a `model_card.md`

---

## License

TBD