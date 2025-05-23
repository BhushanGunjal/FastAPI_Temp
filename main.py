from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()


class Patient(BaseModel):
    id      : Annotated[str, Field(..., title='Patient ID',description='ID of the patient', example='P001')]
    name    : Annotated[str, Field(..., title='Patient Name', description='Name of the patient', example='John Doe')]
    city    : Annotated[str, Field(..., title='Patient City', description='City of the patient', example='New York')]
    age     : Annotated[int, Field(..., gt=0, lt=120, title='Patient Age', description='Age of the patient', example=30)]
    gender  : Annotated[str, Literal['male','female','other'], Field(..., title='Gender', description='Gender of the patient', example='female')]
    height  : Annotated[float, Field(..., gt=0, title='Height', description='Height of the patient in cm', example=1.75)]
    weight  : Annotated[float, Field(..., gt=0, title='Weight', description='Weight of the patient in kg', example=70)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / ((self.height ) ** 2)
        return round(bmi, 2)   

    @computed_field
    @property
    def verify(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def load_data():
    # Load data from the database or any other source
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    # Save data to the database or any other source
    with open("patients.json", "w") as file:
        json.dump(data, file, indent=4)


@app.get("/")
def hello():
    return {"message": "PATIENT MANAGEMENT SYSTEM!"}

@app.get("/about")
def about():
    return {"message": "FULL SYSTEM FOR PATIENT MANAGEMENT!"}

@app.get("/view")
def get_patients():
    # Load data from the database or any other source
    data = load_data()
    return data

@app.get("/search/{patient_id}")
def search_patient(patient_id: str = Path(..., title='Patient ID', description='ID of the patient', example='P001')):

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')




@app.get("/sort")
def sort_patients(sort_by: str = Query(..., title='Sort By', description='Field to sort by', example='name'), order: str = Query('asc', title='Order By', description='Order of sorting', example='asc')):

    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data




@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient ID already exists')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})
    
