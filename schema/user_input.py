from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated

class CarInput(BaseModel):
    # A car model with all the features required for prediction.
    brand: Annotated[str, Field(..., description='Brand of the car')]
    model: Annotated[str, Field(..., description='Model of the car')]
    vehicle_age: Annotated[int, Field(..., ge=0, description='Age of the car in years')]
    km_driven: Annotated[int, Field(..., ge=0, description='Total kilometers driven')]
    seller_type: Annotated[Literal['Individual', 'Dealer', 'Trustmark Dealer'], Field(..., description='Type of seller')]
    fuel_type: Annotated[Literal['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'], Field(..., description='Fuel type')]
    transmission_type: Annotated[Literal['Manual', 'Automatic'], Field(..., description='Transmission type')]
    mileage: Annotated[float, Field(..., gt=0, description='Fuel efficiency in kmpl')]
    engine: Annotated[float, Field(..., gt=0, description='Engine displacement in CC')]
    max_power: Annotated[float, Field(..., gt=0, description='BHP rating')]
    seats: Annotated[int, Field(..., ge=2, le=14, description='Number of passenger seats')]
    
    #calc field
    @computed_field
    @property
    def annual_usage_rate(self) -> float:
        adjusted_age = max(self.vehicle_age, 1)
        return round(self.km_driven / adjusted_age, 2)
    #handle the case of lowercase or uppercase
    @field_validator('brand')
    @classmethod
    def validate_brand(cls, v):
        v = v.strip().title()
        return v