import sys
import pickle
import pandas as pd

# 1. Define DataFrame transformer function expected by sklearn Pipeline
def compute_annual_usage(df_input: pd.DataFrame) -> pd.DataFrame:
    df_out = df_input.copy()
    adjusted_age = df_out['vehicle_age'].clip(lower=1)
    df_out['annual_usage_rate'] = df_out['km_driven'] / adjusted_age
    return df_out

# 2. Attach to __main__ so pickle can resolve the serialized notebook function
sys.modules['__main__'].compute_annual_usage = compute_annual_usage

# 3. Load the model safely
with open('model/car_valuation_model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_price(input_dict: dict):
    input_df = pd.DataFrame([input_dict])
    output = model.predict(input_df)[0]
    return output
