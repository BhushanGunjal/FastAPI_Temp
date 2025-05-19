from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()


def load_data():
    # Load data from the database or any other source
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

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
    for patient in data:
        if patient["patient_id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., title='Sort By', description='Field to sort by', example='name'), order: str = Query('asc', title='Order By', description='Order of sorting', example='asc')):

    
    valid_fields = ['age','gender']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid sort field. Select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Select from asc or desc')
    
    data = load_data()
    sorted_data = sorted(data, key=lambda x: x["age"], reverse=False)
    return sorted_data



