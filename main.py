from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_price
from schema.user_input import CarInput
from schema.prediction_response import PredictionResponse

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Welcome to the Car Valuation API"} 
@app.get("/health")
def health():
    return {"status": "OK"} 
@app.post('/predict',response_model=PredictionResponse)
def predict_endpoint(data: CarInput):
    input_dict = {
        'brand': data.brand,
        'model': data.model,
        'vehicle_age': data.vehicle_age,
        'km_driven': data.km_driven,
        'seller_type': data.seller_type,
        'fuel_type': data.fuel_type,
        'transmission_type': data.transmission_type,
        'mileage': data.mileage,
        'engine': data.engine,
        'max_power': data.max_power,
        'seats': data.seats
    }
    prediction = predict_price(input_dict)
    return JSONResponse(status_code=200, content={'predicted_price_inr': round(prediction, 2)})
