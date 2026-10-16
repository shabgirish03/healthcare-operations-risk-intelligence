# Healthcare Operations & Revenue Risk Intelligence Platform

An end-to-end healthcare analytics and machine learning capstone project focused on operational insights, visit risk classification, insurance claim outcomes, and responsible model evaluation.

## Project Overview

Healthcare organisations generate operational and billing data that can help identify patterns in service utilisation, revenue realisation, and insurance claim outcomes.

This project explores how SQL analytics, exploratory data analysis, and machine learning can support data-informed operational decision-making. It develops two classification workflows: one for visit risk and another for insurance claim outcomes.

The project also explores model evaluation, feature importance, subgroup analysis, API deployment, monitoring, and AI governance.

## Project Objectives

- Analyse healthcare operational and billing data using SQL.
- Assess data quality, missing values, and outliers.
- Explore patterns in patient visits, length of stay, billing, and claims.
- Develop classification models for visit risk and claim outcomes.
- Evaluate model performance using classification metrics and business-focused measures.
- Explore model explainability, subgroup evaluation, and responsible AI practices.
- Develop a foundation for API-based model serving and monitoring.

## Project Workflow

### Phase 1 — SQL Analytics
Explore operational and billing data using SQL to identify patterns and generate business-relevant insights.

### Phase 2 — Exploratory Data Analysis
Investigate distributions, missing values, outliers, and data quality to understand the dataset and prepare it for modelling.

### Phase 3 — Model Development
Develop classification workflows for:
- **Visit Risk Classification:** Predict visit risk categories.
- **Claim Outcome Classification:** Predict insurance claim outcomes, including paid, pending, and rejected categories.

Compare baseline and advanced modelling approaches using an appropriate train/test split.

### Phase 4 — Model Evaluation
Evaluate model performance using confusion matrices, precision, recall, and F1 scores. Explore feature importance, business-focused recall measures, subgroup performance, and model limitations.

### Deployment and Monitoring
The wider capstone work includes a FastAPI application, Docker-based deployment components, input validation, drift-monitoring experiments, prediction logging, and governance documentation.

## Technology Stack

- **Languages:** Python, SQL
- **Data Analysis:** Pandas, NumPy
- **Visualisation:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Development Environment:** Google Colab, Jupyter Notebook
- **API and Deployment:** FastAPI, Docker
- **Monitoring and Governance:** Data validation, drift analysis, model documentation, responsible AI considerations

## Repository Structure

```text
healthcare-operations-risk-intelligence/
├── notebooks/
│   ├── Phase1_SQL.ipynb
│   ├── Phase2_EDA.ipynb
│   ├── Phase3_Modeling.ipynb
│   └── Phase4_Evaluation.ipynb
└── README.md
```

Additional deployment code and documentation may be added as the portfolio version is finalised.

## Responsible Use and Limitations

This project was developed as an academic capstone using data supplied for the project. The original source datasets are not included in this repository.

Model outputs are experimental and depend on the dataset, feature engineering, and evaluation methodology. They should not be interpreted as clinical advice or used to make real-world patient-care decisions without appropriate validation, oversight, and governance.

The project explores fairness and monitoring considerations but does not establish that the models are production-ready or free from bias.

## Project Context

Developed as part of a healthcare analytics and machine learning capstone, bringing together data analysis, predictive modelling, model evaluation, and deployment concepts in one project.
