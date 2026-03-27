from pydantic import BaseModel, Field
from typing import List, Optional

class Activity(BaseModel):
    time: str = Field(..., description="Time or time range for the activity, e.g., '9:00 AM'")
    description: str = Field(..., description="Description of the activity")
    location: Optional[str] = Field(None, description="Place or area for the activity")
    details: Optional[str] = Field(None, description="Extra details like booking info or tips")

class DayPlan(BaseModel):
    day: int = Field(..., description="Day number (1, 2, 3, ...)")
    date: str = Field(..., description="Date of the day plan")
    theme: str = Field(..., description="Theme of the day, e.g., 'Cultural Exploration'")
    activities: List[Activity] = Field(..., description="List of activities for the day")

class Itinerary(BaseModel):
    destination: str = Field(..., description="Destination city and country")
    startDate: str = Field(..., description="Start date of the trip")
    endDate: str = Field(..., description="End date of the trip")
    summary: str = Field(..., description="Brief summary of the trip")
    dailyPlans: List[DayPlan] = Field(..., description="Day-by-day travel plans")

class TripDetails(BaseModel):
    destination: str
    startDate: str
    endDate: str
    travelers: str
    interests: str
