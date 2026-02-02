from pydantic import BaseModel, Field # type: ignore
from pydantic import BaseModel,EmailStr, # type: ignore
from typing import List,Dict,Optional

class Patient(BaseModel):
    name : str = Field(min_length=1)
    email : EmailStr
    age  : int
    weight : float
    allergies : List[str]
    contact_details : Dict[str, str]

def update_patient_data(patient_details : Patient):

    print(patient_details.allergies)
    print(patient_details.email)


patient_info = {'name':'sarthak','email':'abc@gmail.com','age': 54,'weight': 22.3,'allergies': ['dust', 'pollen'], 'contact_details' : {'email':'abc@gmail.com','Phone-number' :'123456'}}

patient_1 = Patient(**patient_info)
update_patient_data(patient_1)