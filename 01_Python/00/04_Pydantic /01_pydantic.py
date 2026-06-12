# pydantic is used to eliminate type validation. expected input format = expected input's format 
from pydantic import BaseModel, Field # type: ignore
from typing import List,Dict,Optional

class Patient(BaseModel):
    name: str = Field(max_length=50)
    age: int
    weight : float = Field(gt=0)
    married : Optional[bool] = None
    allergies : List[str]
    contact_details : Dict[str, str]

def insert_patient_data(patient : Patient):   # () type validation, param --> str, hoker ayegi
    print(patient.age)
    print(patient.name)
    print(patient.allergies)

patient_info = {'name': 'sarthak', 'age': 30, 'weight' : 56.5, 'married' : True, 'allergies': ['dust', 'pollen'], 'contact_details': {'email':'abc@gmail.com','Phone-number' :'123456'}}


patient_1 = Patient(**patient_info)
insert_patient_data(patient_1)