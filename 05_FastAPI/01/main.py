from fastapi import FastAPI, Path, HTTPException, Query
from typing import Annotated, field, Literal
from pydantic import BaseModel, computed_field
import json

app = FastAPI()
 
class Patient(BaseModel):

    id: Annotated[str, field(...,description="The unique identifier for the patient")]
    name: Annotated[str, field(...,description="The full name of the patient")]
    city : Annotated[str, field(...,description="The city where the patient resides")]
    age: Annotated[int, field(...,description="The age of the patient")]
    gender: Annotated[Literal['male', 'female', 'other'], field(..., description="The gender of the patient")]
    height: Annotated[float, field(...,description="The height of the patient in meters")]
    weight: Annotated[float, field(...,description="The weight of the patient in kilograms")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = (self.weight/self.height**2),

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
    
@app.get('/sort')
def sort_patients(sort_by :str = Query(..., description="The field to sort patients by (e.g., age, bmi)"), order : str = Query("asc", description="The order to sort patients by (e.g., asc, desc)")):
    valid_fields = ['age', 'bmi', 'weight', 'height']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: asc, desc")
    data = load_data()
    sorted_patients = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=(order == 'desc'))
    return {patient_id: patient_info for patient_id, patient_info in sorted_patients}
    
    # query parameters are used to filter the patients based on specific criteria. For example, you can filter patients
    # path parameters are used to retrieve specific patient information based on their unique ID. and are in the urls itself 
    #  query parameters are after ? 