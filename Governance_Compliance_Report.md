# Healthcare Governance & Compliance Report

**Project:** Hospital Operations & Revenue Risk Intelligence Platform
**Phase:** 6 — Monitoring, Drift Detection, and Governance
**Version:** 2.0 (October 2026) — revised to separate what is implemented in this repository from what is planned.

> **Scope note:** this is a design document for an academic prototype. Each section is marked **✅ Implemented**, **🟡 Partial** or **📋 Planned**. Monitoring and validation work explored elsewhere during the capstone is not included in this repository.

---

## 1. System Overview

The system consists of two models served through a FastAPI prototype (`api/app.py`):

1. **Risk model:** classifies hospital visits as Low, Medium or High risk.
2. **Claim model:** predicts insurance claim outcome as Paid, Pending or Rejected.

Both are scikit-learn pipelines trained on historical records using a time-ordered train/test split.

## 2. Assumptions

- Input data uses the same categories as the training data:
  - **Departments:** Cardiology, ER, General, ICU, Neurology, Orthopedics
  - **Visit types:** ER, ICU, OPD
  - **Cities:** Bangalore, Chennai, Delhi, Hyderabad, Mumbai, Pune
  - **Insurers:** CareOne, HealthPlus, MediCareX, SecureLife
- The models may not generalise to other locations, insurers or hospitals.
- Financial fields (billed amount, approved amount, payment days) are recorded accurately. Phase 1–2 analysis found this is not fully true: some fields are missing and some dates are inconsistent.

## 3. Known Limitations

- **Claim model target leakage:** it uses `approved_amount` and `payment_days`, which are only known after a claim is decided, so its reported accuracy overstates real-world performance.
- **Risk model performance:** it does not beat a majority-class baseline and detects almost no high-risk visits.
- **Temporal leakage:** some engineered features are computed over the full dataset, including future records.
- **Unknown categories:** new categories (for example, a new department) are ignored by the encoder rather than flagged, so predictions for them may be silently unreliable.
- **Missing values:** the claim model's pipeline imputes missing values; the risk model's pipeline has no imputation step.
- **Fairness:** subgroup metrics are reported, but no fairness claims can be made given the limitations above.

## 4. Monitoring & Data Validation

| Control | Description | Status |
|---|---|---|
| Schema & type validation | Pydantic checks every request has the required fields and correct types; invalid requests return HTTP 422 | ✅ Implemented |
| Range & category checks | Reject out-of-range values (e.g. negative age) and unknown categories | 📋 Planned |
| Prediction logging | Each prediction prints a UTC timestamp, the predicted class and an MD5 hash of the inputs to the console | 🟡 Partial: console only, not persisted |
| Persistent audit log | Store predictions with model version in a durable, access-controlled log | 📋 Planned |
| Feature drift | Compare live input distributions with the **training data** (not the same dataset) using KS tests | 📋 Planned (explored in capstone; not in repo) |
| Prediction drift | Track the predicted class distribution over time against the test-set distribution | 📋 Planned |
| Model versioning | Record training date, data range, features and library versions for each model | 📋 Planned |

**Note on input hashing:** an MD5 hash of the inputs is useful for spotting duplicate requests, but it is **not anonymisation**. Inputs such as age, gender and city have few possible values, so the hash can be reversed by trying all combinations. A production system should use a salted hash or a random request ID and avoid logging patient attributes entirely.

## 5. Retraining Strategy (Planned)

- **Scheduled:** retrain quarterly.
- **Triggered:** retrain early if feature or prediction drift exceeds an agreed threshold. A human reviews and approves the retraining; it is not fully automatic.
- **Validation gate:** a new model is deployed only if it beats both the current model and a majority-class baseline on a recent, time-ordered hold-out set, with subgroup metrics reviewed.
- **Leakage check:** confirm every feature is available at prediction time before retraining.

## 6. Security

| Control | Status |
|---|---|
| Authentication / API keys | 📋 Planned: **the current API has none** |
| HTTPS / TLS | 📋 Planned |
| Network restriction (firewall / IP allow-list) | 📋 Planned |
| No secrets in code or repository | ✅ Implemented: checked before publication |
| No patient data in repository | ✅ Implemented: source data and trained models are not committed |
| Safe model loading | 🟡 Models are loaded with `joblib` (pickle), which can execute code; load only model files you generated yourself |

## 7. Data Protection & Compliance

This prototype **does not claim compliance** with any regulation. A real deployment handling patient data would need to consider:

- **UK GDPR / Data Protection Act 2018:** health data is *special category data*, which requires a lawful basis and an Article 9 condition, data minimisation, a Data Protection Impact Assessment (DPIA), and defined retention periods.
- **NHS Data Security and Protection Toolkit**, if deployed with NHS organisations.
- **HIPAA**, only if deployed in the United States.

## 8. Recommendations

1. Retrain the claim model without post-decision features before any further use.
2. Implement authentication, HTTPS and a persistent audit log before the API handles real data.
3. Replace raw-input MD5 hashing with random request IDs or salted hashes, and log no patient attributes.
4. Add range and unknown-category validation that rejects or flags bad inputs instead of silently ignoring them.
5. Review model outputs with operational and clinical staff before any decision-making use.
