from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management API"} 

@app.get('/about')
def about():
    return {"message": "This is a simple API for managing patient data. You can retrieve patient information, add new patients, and update existing records."}   

@app.get('/view')  # this endpoint will return the list of patients in the JSON file
def view_patients():
    return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")