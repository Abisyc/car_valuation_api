from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    predicted_price_inr: float = Field(
        ..., 
        description="Predicted market price of the vehicle in Indian Rupees (INR)",
        example=949050.0,
    )
    status: str = Field(
        default="success",
        description="API execution status",
        example="success",
    )