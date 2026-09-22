import streamlit as st
import requests

# Define the API endpoint URL from your FastAPI app
API_URL = "http://127.0.0.1:8000/predict"

# Streamlit UI for input fields
st.title("Car Market Value Predictor")
st.write("Enter the vehicle specifications below to get an estimated market price.")

# 1. Complete mapping of Brands to their specific Models from your dataset
BRAND_MODEL_MAP = {
    "Maruti": ["Alto", "Wagon R", "Swift", "Ciaz", "Baleno", "Swift Dzire", "Ignis", "Vitara", "Celerio", "Ertiga", "Eeco", "Dzire VXI", "XL6", "S-Presso", "Dzire LXI", "Dzire ZXI"],
    "Hyundai": ["Grand", "i20", "i10", "Venue", "Verna", "Creta", "Santro", "Elantra", "Aura", "Tucson"],
    "Ford": ["Ecosport", "Aspire", "Figo", "Endeavour", "Freestyle"],
    "Renault": ["Duster", "KWID", "Triber"],
    "Mini": ["Cooper"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GL-Class", "S-Class", "CLS", "GLS", "C"],
    "Toyota": ["Innova", "Fortuner", "Camry", "Yaris", "Glanza"],
    "Volkswagen": ["Vento", "Polo"],
    "Honda": ["City", "CR-V", "Amaze", "Jazz", "Civic", "WR-V"],
    "Mahindra": ["Bolero", "XUV500", "KUV100", "Scorpio", "Marazzo", "KUV", "Thar", "Hexa", "XUV300", "Alturas"],
    "Datsun": ["RediGO", "GO", "redi-GO"],
    "Tata": ["Tiago", "Tigor", "Safari", "Hexa", "Nexon", "Harrier", "Altroz"],
    "Kia": ["Seltos", "Carnival"],
    "BMW": ["5", "3", "Z4", "6", "X5", "X1", "7", "X3", "X4"],
    "Audi": ["A4", "A6", "Q7", "A8"],
    "Land Rover": ["Rover"],
    "Jaguar": ["XF", "F-PACE", "XE"],
    "MG": ["Hector"],
    "Isuzu": ["D-Max", "MUX"],
    "ISUZU": ["D-Max", "MUX"],
    "Porsche": ["Cayenne", "Macan", "Panamera"],
    "Skoda": ["Rapid", "Superb", "Octavia"],
    "Volvo": ["S90", "XC", "XC90", "XC60"],
    "Lexus": ["ES", "NX", "RX"],
    "Jeep": ["Wrangler", "Compass"],
    "Maserati": ["Ghibli", "Quattroporte"],
    "Bentley": ["Continental"],
    "Ferrari": ["GTC4Lusso"],
    "Nissan": ["Kicks", "X-Trail"],
    "Mercedes-AMG": ["C"],
    "Rolls-Royce": ["Ghost"],
    "Force": ["Gurkha"]
}

# --- DYNAMIC CATEGORICAL FEATURES ---
col1, col2 = st.columns(2)

with col1:
    # 2. User selects the Brand first
    brand = st.selectbox("Brand", list(BRAND_MODEL_MAP.keys()))
    
with col2:
    # 3. Model dropdown dynamically updates based on the selected Brand
    available_models = BRAND_MODEL_MAP.get(brand, [])
    model_name = st.selectbox("Model", available_models)

# --- OTHER CATEGORICAL FEATURES ---
col3, col4, col5 = st.columns(3)

with col3:
    seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
with col4:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
with col5:
    transmission_type = st.selectbox("Transmission Type", ["Manual", "Automatic"])

# --- NUMERICAL FEATURES ---
st.write("### Vehicle Specifications")
col6, col7 = st.columns(2)

with col6:
    vehicle_age = st.number_input("Vehicle Age (years)", min_value=0, max_value=30, value=5)
    mileage = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=100.0, value=20.0)
    max_power = st.number_input("Max Power (BHP)", min_value=0.0, max_value=1000.0, value=80.0)

with col7:
    km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=1000000, value=50000)
    engine = st.number_input("Engine Capacity (CC)", min_value=500, max_value=6000, value=1200)
    seats = st.number_input("Number of Seats", min_value=2, max_value=14, value=5)

st.write("---")

# --- PREDICTION LOGIC ---
if st.button("Predict Market Value", use_container_width=True):
    # Prepare the JSON payload exactly how FastAPI expects it
    input_data = {
        "brand": brand,
        "model": model_name,
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "seller_type": seller_type,
        "fuel_type": fuel_type,
        "transmission_type": transmission_type,
        "mileage": mileage,
        "engine": engine,
        "max_power": max_power,
        "seats": seats
    }
    
    # Ping the FastAPI server
    try:
        response = requests.post(API_URL, json=input_data)
        
        if response.status_code == 200:
            prediction = response.json()
            # Note: Ensure "predicted_price_inr" matches the exact key returned by your FastAPI backend
            predicted_price = prediction.get("predicted_price_inr", 0) 
            
            # Display result
            st.success(f"### Estimated Market Price: ₹ {predicted_price:,.2f}")
            
        else:
            st.error(f"Server Error ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Connection Failed. Is the FastAPI backend running in terminal 1? (uvicorn main:app --reload)")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")