from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from models import Itinerary, TripDetails
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables.")

# Initialize FastAPI app
app = FastAPI(title="AI Itinerary Generator", version="1.0")

# Allow frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    top_p=0.9,
    google_api_key=GOOGLE_API_KEY
)

# Parser based on Pydantic model
parser = PydanticOutputParser(pydantic_object=Itinerary)

# Prompt template - FIXED
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful travel planning assistant. Create a detailed travel itinerary.
{format_instructions}"""),
    ("human", """Destination: {destination}
Dates: {startDate} to {endDate}
Travelers: {travelers}
Interests: {interests}

Provide a logical, exciting itinerary with daily plans including themes and activities.""")
])

# Route: Generate itinerary
@app.post("/generate_itinerary")
async def generate_itinerary(details: TripDetails):
    try:
        # Fill prompt with user inputs - FIXED
        messages = prompt_template.invoke({
            "destination": details.destination,
            "startDate": details.startDate,
            "endDate": details.endDate,
            "travelers": details.travelers,
            "interests": details.interests,
            "format_instructions": parser.get_format_instructions()
        })

        # Run model - FIXED
        response = llm.invoke(messages)

        # Parse structured output
        structured = parser.parse(response.content)
        return structured

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {e}")