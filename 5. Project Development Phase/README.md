# Rising Waters: A Machine Learning Approach to Flood Prediction

An end-to-end flood early-warning system: rainfall/weather data → exploratory analysis →
four trained classifiers → a saved deployment model → an interactive Flask web app.

```
Rising Waters/
├── README.md                    ← you are here
├── requirements.txt              top-level dependency list (for the notebook + app)
├── Dockerfile                    container build for IBM Cloud Code Engine / any Docker host
├── Procfile                      buildpack-style deployment (Cloud Foundry / Heroku-style PaaS)
├── manifest.yml                  IBM Cloud Foundry deployment manifest
│
├── data/
│   ├── rainfall in india 1901-2015.xlsx     historical rainfall, 36 subdivisions, 1901-2015
│   └── flood dataset.xlsx                   115 labelled weather/rainfall records + flood target
│
├── notebook/
│   └── Flood_Prediction_Analysis.ipynb      full pipeline: EDA → preprocessing → modeling → save
│
├── model/
│   └── floods.save                          trained model + StandardScaler, bundled with joblib
│
└── app/
    ├── app.py                                Flask application
    ├── requirements.txt
    ├── templates/
    │   ├── base.html
    │   ├── home.html                         Home Page
    │   ├── predict.html                      Prediction Input Page
    │   ├── flood_result.html                 Flood Chance Result Page
    │   └── no_flood_result.html              No Flood Chance Result Page
    └── static/css/style.css
```

## 1. What's in the data

**`rainfall in india 1901-2015.xlsx`** — monthly and seasonal rainfall totals for 36 Indian
subdivisions across 115 years (4,116 rows). Used in the notebook for the broad exploratory
analysis: national distribution, monthly seasonality, year-over-year trend, and a
subdivision-by-subdivision comparison.

**`flood dataset.xlsx`** — 115 records with temperature, humidity, cloud cover, and seasonal
rainfall totals (`ANNUAL`, `Jan-Feb`, `Mar-May`, `Jun-Sep`, `Oct-Dec`, `avgjune`, `sub`), plus a
binary `flood` label. This is the dataset the four classifiers are actually trained and
evaluated on, since it's the one with ground-truth outcomes. Both datasets share the same
seasonal rainfall column definitions, which is what ties them together in the notebook's
analysis.

## 2. Running the notebook

```bash
pip install -r requirements.txt
jupyter notebook notebook/Flood_Prediction_Analysis.ipynb
```

The notebook is already fully executed — you'll see the real charts, confusion matrices, and
accuracy numbers from this exact dataset if you just open it. Re-run all cells (`Kernel → Restart & Run All`)
any time you want to regenerate everything from scratch; it will overwrite `model/floods.save`
with a freshly trained model.

**About XGBoost:** the notebook tries `import xgboost` first. If it isn't installed, it
automatically falls back to scikit-learn's `GradientBoostingClassifier` (same kind of
boosted-tree algorithm, very similar API) so the notebook still runs end-to-end. Run
`pip install xgboost` beforehand for the full experience — most Anaconda setups with internet
access can install it with no issues.

### Results on this dataset

| Model                                       | Test Accuracy    |
| ------------------------------------------- | ---------------- |
| Decision Tree                               | 95.65%           |
| Random Forest                               | 95.65%           |
| K-Nearest Neighbors                         | 86.96%           |
| **XGBoost (selected for deployment)** | **95.65%** |

With only 115 labelled records, several models land on the same accuracy on this particular
train/test split — when that happens, the notebook prefers the boosted-ensemble model for
deployment since it tends to generalize better than a single Decision Tree on unseen data.
*(Run the notebook with real XGBoost installed for the precise numbers it produces in your
environment — small datasets like this one are sensitive to library versions and random seeds.)*

## 3. Running the web app locally

```bash
cd app
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. The four pages:

- **Home** (`/`) — project overview, model accuracy, the three usage scenarios (meteorologist,
  disaster-relief coordinator, government analyst), and how a prediction is made.
- **Prediction Console** (`/predict`) — enter the ten weather/rainfall readings.
- **Flood Chance result** — shown automatically when the model predicts a flood; includes the
  predicted probability and recommended next steps.
- **No Flood Chance result** — shown automatically when the model predicts no flood.

The app loads `model/floods.save` once at startup, so retraining in the notebook and
restarting the app is all that's needed to deploy an updated model.

## 4. Deploying to IBM Cloud

Three ready-made options are included — pick whichever matches your IBM Cloud setup:

**Option A — Code Engine (containers), using the included `Dockerfile`:**

```bash
docker build -t rising-waters .
ibmcloud cr login                                  # or your own registry
docker tag rising-waters <your-registry>/rising-waters
docker push <your-registry>/rising-waters
ibmcloud ce application create --name rising-waters --image <your-registry>/rising-waters --port 5000
```

**Option B — Cloud Foundry (buildpacks), using the included `manifest.yml`:**

```bash
ibmcloud login
ibmcloud target --cf
ibmcloud cf push
```

**Option C — Any other buildpack-based PaaS**, using the included `Procfile` the same way you
would for Heroku-style platforms.

In every case, make sure the `model/` folder is deployed alongside `app/` (the app loads
`../model/floods.save` relative to `app.py`) — the Dockerfile and manifest already handle this.

## 5. Retraining with new data

Drop an updated `flood dataset.xlsx` into `data/`, re-run the notebook, and a new
`model/floods.save` will be written automatically — no code changes needed in the Flask app,
since it always loads whatever's in that file (including the feature list, so the prediction
form would need new fields added in `app/app.py` → `FIELD_META` / `FIELD_GROUPS` only if you
change which columns the model uses).
