from pydantic import BaseModel, Field, EmailStr, field_validator # type: ignore
from typing import List,Dict,Optional

class Patient(BaseModel):
    name : str = Field(min_length=1)
    email : EmailStr
    age  : int
    weight : float
    allergies : List[str]
    contact_details : Dict[str, str]

    @field_validator('email')  # jisper bhi constraints laganey hai use field validator on it 
    @classmethod                       # always
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com']
        #abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid Domain name')
        return value   
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()          # always gives name in uppercase 


def update_patient_data(patient_details : Patient):

    print(patient_details.allergies)
    print(patient_details.email)
    print(patient_details.name)


patient_info = {'name':'sarthak','email':'abc@hdfc.com','age': 54,'weight': 22.3,'allergies': ['dust', 'pollen'], 'contact_details' : {'email':'abc@gmail.com','Phone-number' :'123456'}}

patient_1 = Patient(**patient_info)
update_patient_data(patient_1)