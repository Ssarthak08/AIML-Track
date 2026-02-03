from pydantic import BaseModel, EmailStr, computed_field # type: ignore
from typing import List, Dict

class Patient(BaseModel):
    name : str 
    email : EmailStr
    age  : int
    weight : float
    allergies : List[str]
    contact_details : Dict[str, str]



def update_patient_data(patient_details : Patient):

    print(patient_details.allergies)
    print(patient_details.email)
    print(patient_details.name)


patient_info = {'name':'sarthak','email':'abc@hdfc.com','age': 61,'weight': 22.3,'allergies': ['dust', 'pollen'], 'contact_details' : {'email':'abc@gmail.com','Phone-number' :'123456','emergency':'921688'}}

patient_1 = Patient(**patient_info)
update_patient_data(patient_1)


temp = patient_1.model_dump()
print(temp)
print(type(temp))
