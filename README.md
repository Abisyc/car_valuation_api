# 🚗 Car Market Value Predictor

A production-ready, end-to-end Machine Learning application that estimates used car market values in India. The system features a **Scikit-Learn** inference pipeline, a **FastAPI** REST backend with strict **Pydantic** request/response schemas, and an interactive **Streamlit** frontend with dynamic cascading dropdowns—all containerized using **Docker**.

---

## 🌟 Features

- **Machine Learning Pipeline:** Predicts vehicle resale price in INR (₹) using vehicle age, mileage, engine displacement, max power, and brand metrics.
- **FastAPI REST Backend:** Built with strict input validation (`CarInput`) and typed output models (`PredictionResponse`), providing automatic Swagger/OpenAPI documentation.
- **Dynamic Streamlit Frontend:** Features dynamic dropdown filtering where car models automatically update based on the selected brand.
- **Single-Dockerfile Architecture:** Containerized setup built from a single lightweight Docker context.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Pickle |
| **Backend Framework** | FastAPI, Uvicorn, Pydantic |
| **Frontend Framework** | Streamlit, Requests |
| **Containerization** | Docker |

---

## 📁 Project Directory Structure

```text
.
├── main.py              # FastAPI server & /predict route definition
├── frontend.py         # Streamlit web UI & API client
├── model.pkl           # Serialized Scikit-Learn model pipeline
├── requirements.txt    # Project dependencies
├── Dockerfile          # Single image container build definition
└── Dataset             # Cardekho dataset
```

---

## 🚀 Running with Docker

### 1. Build the Docker Image

Run the following command in the project root:

```bash
docker build -t car-price-predictor .
```

### 2. Run the FastAPI Backend Container

```bash
docker run -d \
  --name car-backend \
  -p 8000:8000 \
  car-price-predictor \
  uvicorn app:app --host 0.0.0.0 --port 8000
```

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### 3. Run the Streamlit Frontend Container

```bash
docker run -d \
  --name car-frontend \
  -p 8501:8501 \
  -e API_URL=[http://host.docker.internal:8000/predict](http://host.docker.internal:8000/predict) \
  car-price-predictor \
  streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
```

- **Web App UI:** `http://localhost:8501`

> **Note for Linux users:** If `host.docker.internal` is not resolved by default, append `--add-host=host.docker.internal:host-gateway` to the frontend `docker run` command.

---

## 💻 Local Setup (Without Docker)

### 1. Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
uvicorn app:app --reload --port 8000
```

### 3. Start the Streamlit Application (In a second terminal)

```bash
streamlit run frontend.py
```

---

## 🔌 API Reference

### Predict Car Price

- **URL:** `/predict`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`

#### Request Body (`CarInput`)

```json
{
  "brand": "Honda",
  "model": "City",
  "vehicle_age": 4,
  "km_driven": 35000,
  "seller_type": "Dealer",
  "fuel_type": "Petrol",
  "transmission_type": "Automatic",
  "mileage": 18.0,
  "engine": 1498.0,
  "max_power": 119.0,
  "seats": 5
}
```

#### Response (`PredictionResponse` - `200 OK`)

```json
{
  "predicted_price_inr": 949050.0,
  "status": "success"
}
```

#### cURL Command

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "brand": "Honda",
  "model": "City",
  "vehicle_age": 4,
  "km_driven": 35000,
  "seller_type": "Dealer",
  "fuel_type": "Petrol",
  "transmission_type": "Automatic",
  "mileage": 18.0,
  "engine": 1498.0,
  "max_power": 119.0,
  "seats": 5
}'
```

---

## 📄 Container Configuration Reference

### `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `.dockerignore`

```text
__pycache__/
*.pyc
*.pyo
*.pyd
.git
.gitignore
venv/
.env
```
