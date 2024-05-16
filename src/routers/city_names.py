from typing import List

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import os

router = APIRouter(
    prefix="/cities",
    tags=["CITY NAMES"]
)


@router.get("/city-autocomplete/")
async def city_autocomplete(prefix: str) -> List[str]:
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json"

    params = {
        "input": prefix,
        "types": "(cities)",
        "key": google_api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "predictions" in data:
                    filtered_predictions = []

                    # Prioritize and filter predictions based on type "locality"
                    for prediction in data["predictions"]:
                        if "types" in prediction and "locality" in prediction["types"]:
                            filtered_predictions.append(prediction["description"])

                    return filtered_predictions

            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch city predictions")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
