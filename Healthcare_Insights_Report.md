# Healthcare Operations & Revenue Risk Intelligence Platform — Insights Report

**Project:** Hospital Analytics Capstone Project
**Prepared by:** Shabari Girish
**Version:** 2.0 (October 2026) — revised so that every figure matches the notebook outputs in this repository. Version 1.0 (February 2026) contained placeholder figures and has been withdrawn.

---

## 1. Executive Summary

Hospitals face operational inefficiencies and revenue leakage from insurance claim rejections. This project builds an analytics and machine learning pipeline (SQL analytics, exploratory analysis, two classification models, and a FastAPI prototype) to explore whether operational and billing data can support those decisions.

**What the analysis found:**

- Operational metrics (visit volume, length of stay, share of high-risk visits) are **very similar across all six departments and six cities**. The data shows no department standing out as a clear priority.
- Around **15% of claims are rejected** and only **~74% of billed value is approved**, so revenue leakage is the most material business signal in the data.
- The **visit-risk model does not outperform a simple baseline**, so it is not suitable for staffing or clinical decisions.
- The **claim-outcome model scores highly (89–93% accuracy), but this is inflated by target leakage** (see Section 5). Its true predictive ability at the time a claim is submitted has not yet been measured.

No business-impact or cost-saving figures are claimed, because the models do not yet support them.

## 2. Business Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| BR-01 | Monitor department visit volume | High | ✅ Delivered: SQL queries (Phase 1) |
| BR-02 | Identify high-risk visits | High | ⚠️ Model built, but does not beat baseline |
| BR-03 | Predict claim outcomes | High | ⚠️ Model built; must be retrained without post-decision features |
| BR-04 | Provide audit trail and governance | Medium | 🟡 Partial: console prediction logs only (see Governance report) |
| BR-05 | Enable API integration | Medium | ✅ Prototype: FastAPI endpoints `/predict/risk` and `/predict/claim` |

## 3. System Architecture & Data Flow

```
CSV files (patients, visits, billing)
        ↓
SQLite analytics layer (Phase 1) ──→ operational & financial KPIs
        ↓
pandas feature engineering (Phases 2–3)
        ↓
Risk model + Claim model (scikit-learn pipelines)
        ↓
FastAPI service (api/) ── Docker
```

**Data:** 25,000 visits, ~5,000 patients and 25,000 billing records. Six departments (Cardiology, ER, General, ICU, Neurology, Orthopedics), three visit types (ER, ICU, OPD), six cities and four insurers.

**SQL layer:** relational schema with primary/foreign keys and constraints; indexed on `visit_date`, `department`, `insurance_provider`, `claim_status`, `patient_id` and `visit_id`.

**Engineered features:** visit frequency per patient, average length of stay per patient, provider rejection rate, days since registration, visit month and weekday.

**Models:** Logistic Regression (baseline) and Random Forest for each task. Time-ordered 80/20 train/test split.

## 4. Key Operational & Financial Insights (Phase 1)

### Operational metrics

| Metric | Finding |
|---|---|
| Visits by department | 4,064 (ICU) to 4,228 (General), so near-uniform |
| Average length of stay | 19.4–19.7 hours in every department |
| High-risk visits by department | 19.0% (Cardiology) to 20.8% (ICU) |
| Average visits per patient by city | 4.95 (Delhi) to 5.12 (Pune) |
| High-risk visits per doctor | 34 to 71 across 101 doctors |

**Interpretation:** the differences between departments and cities are 1–2 percentage points and were not tested for statistical significance. On this data they are not strong enough to justify reallocating resources.

### Financial metrics

| Metric | Finding |
|---|---|
| Total billed by insurer | 126.3M to 134.6M (MediCareX highest); currency not specified in the source data |
| Claim rejection rate by insurer | 14.9% (CareOne) to 15.7% (SecureLife) |
| Average payment delay | ~13 days for every insurer |
| Revenue realisation (approved ÷ billed) | 0.74 in five departments, 0.75 in ICU |
| Claims billed > 10,000 with zero or missing approval | **4,289** |

**Interpretation:** roughly a quarter of billed value is not realised, and 4,289 high-value claims have no approved amount. These claims are the clearest candidates for a revenue-recovery review.

### Data integrity

- No visits without a billing record, no bills without a visit, and no duplicate patient IDs.
- 790 claims have a missing `payment_days` value, most of them marked **Paid**, which points to a recording gap rather than unpaid claims.
- Some records have billing or registration dates that are inconsistent with the visit date (for example, a bill dated before the visit). This affects date-based features.

## 5. Model Performance

Test set: the most recent 20% of records (5,000), ordered by date.

| Model | Accuracy | Key recall | Assessment |
|---|---|---|---|
| Risk: Logistic Regression | 0.50 | High-risk: 0.00 | Predicts "Low" for every visit |
| Risk: Random Forest | 0.47 | High-risk: 0.01 | Below the majority-class baseline (~0.50) |
| Claim: Logistic Regression | 0.93 | Rejected: 0.94 | Inflated by leakage |
| Claim: Random Forest | 0.89 | Rejected: 0.96 | Inflated by leakage |

**Why the claim results are not trustworthy yet:** the claim models use `approved_amount` and `payment_days`, which are only known after a claim has been decided. `approved_amount` alone accounts for ~55% of Random Forest feature importance and has the largest Logistic Regression coefficient. The models are largely reading the outcome back from its consequences.

**Why the risk model fails:** high-risk rates are almost identical across departments, and the strongest features (length of stay, days since registration, age) carry little signal for `risk_score` in this dataset.

**Subgroup performance (descriptive only):** claim Random Forest accuracy ranges from 0.87 to 0.91 across insurers and cities. The risk model scores 0.47 for both genders. Because the risk model is near baseline and the claim model is leaky, these figures cannot support fairness conclusions.

## 6. Deployment

- FastAPI service with `/health`, `/predict/risk` and `/predict/claim` endpoints and Pydantic input validation.
- A Dockerfile is provided. The trained `.pkl` model files must be generated by the Phase 3 notebook before building the image.
- This is a **prototype**. It has no authentication, no HTTPS and no persistent audit log, and must not be used with real patient data. See the Governance report and the deployment runbook.

## 7. Governance Framework (NIST AI RMF)

The NIST AI Risk Management Framework has four functions. This table shows how they apply to this project and what is in place today.

| Function | Application in this project | Current status |
|---|---|---|
| **Govern** | Documented assumptions, limitations and responsible-use statement; model documentation | Documented in README and these reports |
| **Map** | Identified operational risks (missed high-risk visits), financial risks (claim rejection, revenue leakage) and data-quality risks (missing values, date inconsistencies) | Done |
| **Measure** | Precision, recall, F1, confusion matrices, feature importance, subgroup metrics; leakage identified through feature-importance review | Done for current models |
| **Manage** | Input validation, drift monitoring, retraining strategy, access control | Partial: type validation only; the rest is planned |

## 8. Recommendations

1. **Do not deploy either model in their current form.** Retrain the claim model using only features available at submission time, and rebuild the risk model or reconsider whether `risk_score` is predictable from these features.
2. **Prioritise revenue recovery.** Review the 4,289 high-value claims with no approved amount, and investigate why ~26% of billed value is not realised.
3. **Fix data-quality issues first:** missing `payment_days` on paid claims and inconsistent dates.
4. **Compute features from prior history only** to remove temporal leakage, and compare every model against a majority-class baseline.
5. **Add authentication, HTTPS and a persistent, privacy-preserving audit log** before the API handles any real data.
