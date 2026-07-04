# Rising Waters — A Machine Learning Approach to Flood Prediction

An end-to-end machine learning internship project that predicts flood risk from rainfall and
weather readings, and serves live predictions through a Flask web app. This repository contains
the full project lifecycle — from ideation to deployment and demonstration — organized by phase.

---

## 📌 Problem Statement

Flood-prone regions often lack a quick, localized way to assess flood risk from current rainfall
and weather conditions, which leads to delayed warnings and reactive rather than preventive
responses. Two customer perspectives shaped the project:

- **A resident in a flood-prone area** wants to know in advance whether their area is at risk
  this monsoon, but the local weather report gives no personalized flood-risk information.
- **A local disaster management official** needs to issue timely warnings, but manually
  analyzing rainfall trends is slow and often inaccurate.

**Objective:** accurately predict the likelihood of flooding in a given region by applying
machine learning to rainfall and weather data, enabling faster, more informed decisions for both
residents and disaster-response authorities.

---

## 🗂️ Repository Structure

This project follows an 8-phase internship workflow, with each phase in its own folder:

```
rising waters/
├── 1. Brainstorming & Ideation/          Empathy map, problem statements, idea prioritization
├── 2. Requirement Analysis/              Customer journey map, DFD, solution requirements, tech stack
├── 3. Project Design Phase/               Problem-solution fit, proposed solution, architecture
├── 4. Project Planning Phase/             Sprint/task planning
├── 5. Project Development Phase/          ⭐ the actual code — notebook, model, Flask app
├── 6. Project Testing/                    Performance testing report
├── 7. Project Documentation/              Executable files & sample documentation
└── 8. Project Demonstration/              Demo planning, features, scalability, team involvement
```

The **`5. Project Development Phase/`** folder is where the working system lives — that's the
part you'd actually run. Its own README has full setup instructions, but the short version:

```bash
cd "5. Project Development Phase"
pip install -r requirements.txt
jupyter notebook notebook/Flood_Prediction_Analysis.ipynb   # explore the data & retrain
cd app && pip install -r requirements.txt && python app.py  # run the web app
```

---

## 🧠 Approach

Rising Waters trains and compares four classification models on historical rainfall and weather
data, then deploys the strongest performer behind a simple web interface:

| Model                        | Test Accuracy    |
| ---------------------------- | ---------------- |
| Decision Tree                | 95.65%           |
| Random Forest                | 95.65%           |
| K-Nearest Neighbors          | 86.96%           |
| **XGBoost (deployed)** | **95.65%** |

With only 115 labelled records, several models tie on accuracy for this particular split —
XGBoost is chosen for deployment since boosted ensembles tend to generalize better than a single
Decision Tree on unseen data.

**Data used:**

- `rainfall in india 1901-2015.xlsx` — 115 years of monthly/seasonal rainfall across 36 Indian
  subdivisions, used for exploratory analysis and trend visualization.
- `flood dataset.xlsx` — 115 labelled records (temperature, humidity, cloud cover, seasonal
  rainfall totals, and a binary flood outcome) — the ground-truth data the models are trained
  and evaluated on.

---

## 🛠️ Technology Stack

| Layer        | Technology                                              | Why                                                                               |
| ------------ | ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Frontend     | HTML5, CSS3, Jinja2 (Flask templates)                   | Server-rendered pages keep a form-driven tool simple, with no separate build step |
| Backend      | Python, Flask                                           | Lightweight, integrates directly with the scikit-learn/XGBoost ecosystem          |
| Data storage | Static files (Excel + joblib model bundle)              | No live database needed for a small, static training set                          |
| Deployment   | Docker, IBM Cloud Code Engine, Cloud Foundry buildpacks | Consistent containerized environment, with buildpack fallback for other PaaS      |

---

## 🚀 Key Features

- Machine learning flood prediction model, with four algorithms trained and compared
  (Decision Tree, Random Forest, KNN, XGBoost)
- Publicly accessible prediction form — no login required
- Instant flood / no-flood result page with predicted probability and recommended next steps
- Fully reproducible notebook: re-run all cells to retrain the model from scratch
- Three deployment paths included out of the box: Docker, Cloud Foundry, and generic
  buildpack PaaS (Procfile)

---

## 📄 Documentation

Every phase above includes its corresponding artifact PDF (empathy maps, DFDs, architecture
diagrams, sprint plans, testing reports, and demo materials) as submitted for internship
evaluation. See `7. Project Documentation/` for the consolidated write-up and a list of
executable files.

---

## 👥 Use Cases

- **Resident in a flood-prone area** — checks personal flood risk ahead of the monsoon.
- **Disaster-relief coordinator** — gets a fast, data-driven second opinion before issuing warnings.
- **Government analyst** — uses historical rainfall trends alongside live predictions for
  regional planning.
