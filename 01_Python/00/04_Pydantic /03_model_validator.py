# model validtors are used when we need to apply conditions on 2 or more fields and they are interconnected connections

from pydantic import BaseModel, EmailStr, model_validator # type: ignore
from typing import List, Dict

class Patient(BaseModel):
    name : str 
    email : EmailStr
    age  : int
    weight : float
    allergies : List[str]
    contact_details : Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 should have an emergency contact')
        return model

def update_patient_data(patient_details : Patient):

    print(patient_details.allergies)
    print(patient_details.email)
    print(patient_details.name)


patient_info = {'name':'sarthak','email':'abc@hdfc.com','age': 61,'weight': 22.3,'allergies': ['dust', 'pollen'], 'contact_details' : {'email':'abc@gmail.com','Phone-number' :'123456','emergency':'921688'}}

patient_1 = Patient(**patient_info)
update_patient_data(patient_1)