from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import datetime
import hashlib

app = FastAPI(title="Hospital Models API")

# Load models
risk_model = joblib.load("risk_model.pkl")
claim_rf_model = joblib.load("claim_rf_model.pkl")  # advanced claim model

# Input schemas
class RiskInput(BaseModel):
    age: int
    gender: str
    chronic_flag: int
    city: str
    department: str
    visit_type: str
    length_of_stay_hours: float
    visit_frequency: float
    avg_length_of_stay: float
    provider_rejection_rate: float
    days_since_registration: int
    visit_month: int
    visit_weekday: int

class ClaimInput(BaseModel):
    age: int
    gender: str
    chronic_flag: int
    city: str
    department: str
    visit_type: str
    length_of_stay_hours: float
    billed_amount: float
    approved_amount: float
    payment_days: float
    visit_frequency: float
    avg_length_of_stay: float
    provider_rejection_rate: float
    days_since_registration: int
    visit_month: int
    visit_weekday: int

@app.get("/health")
def health_check():
    return {"status": "OK", "timestamp": datetime.datetime.utcnow().isoformat()}

@app.post("/predict/risk")
def predict_risk(input_data: RiskInput):
    features = [[
        input_data.age, input_data.gender, input_data.chronic_flag, input_data.city,
        input_data.department, input_data.visit_type, input_data.length_of_stay_hours,
        input_data.visit_frequency, input_data.avg_length_of_stay,
        input_data.provider_rejection_rate, input_data.days_since_registration,
        input_data.visit_month, input_data.visit_weekday
    ]]
    prediction = risk_model.predict(features)[0]
    input_hash = hashlib.md5(str(features).encode()).hexdigest()
    print(f"[{datetime.datetime.utcnow()}] Risk Prediction: {prediction}, hash: {input_hash}")
    return {"risk_score": prediction, "timestamp": datetime.datetime.utcnow().isoformat()}

@app.post("/predict/claim")
def predict_claim(input_data: ClaimInput):
    features = [[
        input_data.age, input_data.gender, input_data.chronic_flag, input_data.city,
        input_data.department, input_data.visit_type, input_data.length_of_stay_hours,
        input_data.billed_amount, input_data.approved_amount, input_data.payment_days,
        input_data.visit_frequency, input_data.avg_length_of_stay,
        input_data.provider_rejection_rate, input_data.days_since_registration,
        input_data.visit_month, input_data.visit_weekday
    ]]
    prediction = claim_rf_model.predict(features)[0]
    input_hash = hashlib.md5(str(features).encode()).hexdigest()
    print(f"[{datetime.datetime.utcnow()}] Claim Prediction: {prediction}, hash: {input_hash}")
    return {"claim_status": prediction, "timestamp": datetime.datetime.utcnow().isoformat()}
