# Healthcare Operations & Revenue Risk Intelligence Platform

An end-to-end healthcare analytics and machine learning capstone project covering SQL analytics, exploratory data analysis, two classification models, model evaluation, and a FastAPI/Docker deployment prototype — with an honest look at where the models fall short.

## Project Overview

Healthcare organisations generate operational and billing data that can help identify patterns in service utilisation, revenue realisation, and insurance claim outcomes.

This project explores how SQL analytics, exploratory data analysis, and machine learning can support data-informed operational decision-making. It develops two classification workflows: one for visit risk and another for insurance claim outcomes. The project also explores model evaluation, feature importance, subgroup analysis, API deployment, and AI governance.

**Dataset:** 25,000 visits, ~5,000 patients, and 25,000 billing records across three related tables (patients, visits, billing).

## Project Workflow

| Phase | Notebook | What it does |
|---|---|---|
| 1 — SQL Analytics | `notebooks/Phase1_SQL.ipynb` | SQLite schema with primary/foreign keys and constraints, indexing strategy, operational and financial KPIs, referential-integrity checks |
| 2 — EDA | `notebooks/Phase2_EDA.ipynb` | Missing-value analysis, distributions, IQR outlier detection |
| 3 — Modelling | `notebooks/Phase3_Modeling.ipynb` | Feature engineering; Logistic Regression baseline vs Random Forest for both tasks; time-ordered 80/20 split; class weighting for the claim model |
| 4 — Evaluation | `notebooks/Phase4_Evaluation.ipynb` | Confusion matrices, precision/recall/F1, business-focused recall, feature importance, subgroup performance by gender, insurer and city |
| Deployment | `api/` | FastAPI prediction service, Dockerfile, deployment runbook |

> Notebook outputs for Phases 1–2 have been cleared. Phases 3–4 retain aggregate results only (no individual records).

## Key Results

**SQL analytics (Phase 1)**
- Visit volume, average length of stay (~19.5h) and high-risk share (19–21%) are very similar across all six departments.
- Revenue realisation (approved ÷ billed) is ~0.74 across departments; claim rejection rates range from 14.9% to 15.7% across insurers.
- 4,289 claims billed above 10,000 had a zero or missing approved amount, a potential revenue-leakage signal.
- No orphan visits or billing records, and no duplicate patient IDs.

**Models (time-ordered test set, 5,000 records)**

| Task | Model | Accuracy | Key recall |
|---|---|---|---|
| Visit risk (Low/Medium/High) | Logistic Regression | 0.50 | High: 0.00 |
| Visit risk | Random Forest | 0.47 | High: 0.01 |
| Claim outcome (Paid/Pending/Rejected) | Logistic Regression (balanced) | 0.93 | Rejected: 0.94 |
| Claim outcome | Random Forest (balanced) | 0.89 | Rejected: 0.96 |

## Known Limitations — read before interpreting the results

These were identified in a post-project review and are documented deliberately:

1. **Claim model target leakage.** The claim model uses `approved_amount` and `payment_days`, which are only known *after* a claim is decided. `approved_amount` alone accounts for ~55% of Random Forest feature importance. The high claim accuracy therefore does **not** reflect real predictive ability; a deployable model must use only information available at billing time.
2. **Risk model does not beat a naive baseline.** Always predicting "Low" would score ~0.50 accuracy. The Random Forest scores 0.47 and detects almost no High-risk visits, suggesting `risk_score` is weakly related to the available features.
3. **Temporal leakage in engineered features.** `visit_frequency`, `avg_length_of_stay` and `provider_rejection_rate` are computed over the full dataset, including the test period. They should be computed from prior/training data only.
4. **`chronic_flag` is silently dropped** by the preprocessing pipeline because it is not listed in either feature group.
5. **Data quality.** Some records have billing or registration dates inconsistent with the visit date, which affects date-based features and the time-ordered split.
6. **Subgroup analysis is descriptive only.** Per-group metrics are reported, but no fairness conclusions can be drawn, particularly for a near-baseline risk model.
7. **The API is a demo.** It has no authentication and should not be exposed publicly or used with real patient data (see the security section of the runbook).

**Planned fixes:** remove post-decision features, compute features from prior history only, add majority-class baselines, fix the `chronic_flag` bug, pin library versions, and add authentication to the API.

## How to Run

The source data is not included (see below), so the notebooks will run only if you supply `patients.csv`, `visits.csv` and `billing.csv` with the same schema.

1. Run the notebooks in order: Phase 1 → 2 → 3 → 4. They were developed in Google Colab and use `files.upload()` to load the CSVs.
2. Phase 3 creates `model_table.csv`, `risk_model.pkl`, `claim_lr_model.pkl` and `claim_rf_model.pkl`, which Phase 4 and the API need.
3. To run the API, copy `risk_model.pkl` and `claim_rf_model.pkl` into `api/`, then follow [`api/Deployment_runbook.md`](api/Deployment_runbook.md):

```bash
cd api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Trained model files are not committed: they are regenerated by Phase 3, and pickle files should only be loaded from trusted sources.

## Technology Stack

- **Languages:** Python, SQL
- **Data analysis:** pandas, NumPy, SQLite
- **Visualisation:** Matplotlib, Seaborn
- **Machine learning:** scikit-learn
- **API and deployment:** FastAPI, Pydantic, Docker
- **Environment:** Google Colab, Jupyter

## Repository Structure

```
healthcare-operations-risk-intelligence/
├── README.md
├── notebooks/
│   ├── Phase1_SQL.ipynb
│   ├── Phase2_EDA.ipynb
│   ├── Phase3_Modeling.ipynb
│   └── Phase4_Evaluation.ipynb
├── api/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Deployment_runbook.md
└── docs/
    ├── Data Quality Report.pdf
    ├── Healthcare_Insights_Report.md
    └── Governance_Compliance_Report.md
```

## Responsible Use and Data

This project was developed as an academic capstone using data supplied for the project. The original source datasets are not included in this repository.

Model outputs are experimental and depend on the dataset, feature engineering, and evaluation methodology. They should not be interpreted as clinical advice or used to make real-world patient-care decisions without appropriate validation, oversight, and governance.

The project explores fairness and monitoring considerations but does not establish that the models are production-ready or free from bias.

## Project Context

Developed as part of a healthcare analytics and machine learning capstone, bringing together data analysis, predictive modelling, model evaluation, and deployment concepts in one project.
