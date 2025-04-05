

from fastapi import APIRouter # type: ignore
from typing import List
from app.models import UserInfo, Scheme
from app.gemini import get_recommendations
import json
from pathlib import Path

router = APIRouter()

# Load static schemes from JSON
def load_schemes():
    path = Path(__file__).parent / "schemes.json"
    with open(path) as f:
        return json.load(f)

@router.post("/recommend", tags=["Recommendations"])
async def recommend_schemes(user: UserInfo):
    user_dict = user.dict()
    schemes = load_schemes()

    # Call Gemini to get recommendation text
    gemini_response = await get_recommendations(user_dict, schemes)

    # Return the raw Gemini text (or format if you want)
    return {"recommendation": gemini_response}
