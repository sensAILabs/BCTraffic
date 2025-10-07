# Black Carbon Model — Traffic & Weather Feature Set (XGBoost)

This repository contains data, a training notebook, and an exported model to predict **post-processed Black Carbon (BC post)** concentrations using traffic-derived features (vehicle counts by lane/type) and meteorological features (historical & forecast). The core model is an **XGBoost regressor** trained on feature-shifted datasets to capture temporal alignment between traffic signals and BC response.

> Quick start: jump to [Inference](#inference) to load `xgboost_model.pkl` and run predictions on the provided CSVs.

---

## Repository Structure

```
.
├── __init__.py
├── requirements.txt              # Reproducible environment
├── process_and_train.ipynb       # End-to-end data prep + training + evaluation
├── xgboost_model.pkl             # Trained XGBoostRegressor
├── bc_ona_df.csv                 # Base dataset (traffic + meteo + BC)
├── shifted_datasets/             # Feature-shifted training tables
│   ├── corr_shift/               # Correlation-based temporal shift
│   │   ├── 3921.csv
│   │   ├── 3922.csv
│   │   └── ... (plus *_aug.csv augmentations)
│   └── fft_shift/                # Frequency-domain aligned shift
│       ├── 3921.csv
│       ├── 3922.csv
│       └── ... (plus *_aug.csv augmentations)
├── corr_matrix.pdf               # Feature correlation visualization
└── bc_post_histogram.pdf         # Target distribution visualization
```

---

## Data Overview

### Base Table (`bc_ona_df.csv`)
Representative columns (trimmed):
- `Time`: Timestamp (string/ISO or numeric epoch depending on source)
- `BC`: Raw black carbon concentration
- `BC post`: Post-processed/cleaned BC target
- `LDPV_1`, `LDPV_2`, `LDPV_3`: Light-duty passenger vehicle counts by lane
- `HDV_1`, `HDV_2`, `HDV_3`: Heavy-duty vehicle counts by lane
- `StopLDPV_*`, `StopHDV_*`: Stopped/idle counts by lane
- `his_temp`, `his_wind`, `his_humid`: Historical meteorology
- `dataset_number`: Scenario/segment identifier

### Shifted Datasets (`shifted_datasets/*/*.csv`)
Each CSV contains **aligned features** so that predictors (traffic, meteo) better match the **lagged response** in BC. Two methods are supplied:
- **corr_shift/**: temporal offsets chosen via correlation analysis
- **fft_shift/**: alignment using frequency-domain signals

Representative columns (from `corr_shift/3921.csv`):
- `Time`, `BC`, `BC post`
- `car_line1/2/3`, `car_line*_stop`, `truck_line*`, `truck_line*_stop`, `summed`, `traffic`
- `history_temperature/wind_speed/humidity`
- `forecast_temperature/wind_speed/humidity`

> Tip: prefer the shifted datasets for training; the base table is useful for exploration.

---

## Environment Setup

We recommend a Python 3.10+ environment.

```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` pins versions for: `pandas`, `numpy`, `xgboost`, `scikit-learn`, plotting (matplotlib/plotly), geospatial/tiling utilities used in exploration, and Jupyter.

---

## Training

Open the notebook and run all cells:

```bash
jupyter lab
# then open: process_and_train.ipynb
```

The notebook covers:
1. **Load data** from `bc_ona_df.csv` or a subset of `shifted_datasets`.
2. **EDA** (see `corr_matrix.pdf`, `bc_post_histogram.pdf` for quick references).
3. **Feature engineering**: lane-level counts, stopped vehicles, total traffic, meteorology merges.
4. **Temporal alignment** using either correlation-based or FFT-based shifting.
5. **Train** an XGBoost regressor on `BC post`.
6. **Evaluate** using held-out splits (RMSE/MAE/R²) and partial diagnostics.
7. **Export** the trained model as `xgboost_model.pkl`.

> If you train a new model, be sure to **save** a new pickle and record the feature order used during fit.

---

## Inference

You can use the provided model to predict `BC post` for any CSV with the **same feature schema and ordering** used at training time. Below is a minimal example loading a shifted dataset and producing predictions.

```python
import pandas as pd
import pickle

# 1) Load a feature table (example: one of the corr_shift CSVs)
df = pd.read_csv("shifted_datasets/corr_shift/3921.csv")

# 2) Select the features your model expects (example subset below)
feature_cols = [
    # Vehicle features (adapt to match your training set)
    "car_line1","car_line1_stop","car_line2","car_line2_stop","car_line3","car_line3_stop",
    "truck_line1","truck_line1_stop","truck_line2","truck_line2_stop","truck_line3","truck_line3_stop",
    "summed","traffic",
    # Meteo features
    "history_temperature","history_wind_speed","history_humidity",
    "forecast_temperature","forecast_wind_speed","forecast_humidity",
]

X = df[feature_cols]

# 3) Load the trained model
with open("xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

# 4) Predict BC post
y_pred = model.predict(X)

# 5) Attach to DataFrame and save
df["BC_post_pred"] = y_pred
df[["Time","BC","BC post","BC_post_pred"]].to_csv("predictions.csv", index=False)
print("Saved predictions.csv")
```

### Feature Compatibility
- Ensure that the **column names and order** in `feature_cols` exactly match what the model was trained on.
- If you add or remove features, retrain the model and export a new pickle.

---

## Evaluation Artifacts

- **`corr_matrix.pdf`** — pairwise correlations to identify redundant or highly informative features.
- **`bc_post_histogram.pdf`** — target distribution; useful to check class/scale balance and for choosing error metrics.

> These files provide a snapshot; for rigorous evaluation, re-run the notebook on your splits and record metrics (MAE/RMSE/R²) and plots (residuals, learning curves, feature importance).

---

## Tips & Best Practices

- **Temporal Leakage**: When crafting shifts, avoid leaking future information into the present timestep.
- **Scaling**: Tree-based models (like XGBoost) don’t require standardization, but be consistent with NA handling.
- **Cross-Validation**: Prefer **time-series-aware** splits (e.g., expanding window) if data is temporally ordered.
- **Feature Importance**: Use `model.get_booster().get_score()` or SHAP for interpretable insights.
- **Augmentations**: The `*_aug.csv` files may include engineered variants; track which ones are used per experiment.

---

## Reproducing Results

1. Choose a family of shifted datasets (`corr_shift` or `fft_shift`).
2. Define your **feature list** explicitly in the notebook.
3. Split data into train/validation/test with a time-aware strategy.
4. Train XGBoost with documented hyperparameters.
5. Export `xgboost_model.pkl` and save the **feature list and preprocessing steps** alongside the model.

Consider saving a `model_card.md` with:
- Data sources and timespan
- Preprocessing pipeline summary
- Evaluation metrics by split
- Known limitations & assumptions

---

## License

Add a `LICENSE` file (e.g., MIT/Apache-2.0). If data files have separate terms, document them here.

---

## Acknowledgments

Thanks to contributors collecting BC data and providing traffic & meteorological signals that enable this modeling effort.
