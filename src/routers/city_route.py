from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_pagination import Params, Page, paginate

from config import GOOGLE_API_KEY
from src.controllers.city_controller import CityController
from src.models.city import City

router = APIRouter(
    prefix="/cities",
    tags=["CITIES"]
)

city_controller = CityController()


@router.get("/city-autocomplete/{prefix}")
async def city_autocomplete(prefix: str, pagination_params: Params = Depends()) -> Page[City]:
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json"

    params = {
        "input": prefix,
        "types": "(cities)",
        "key": GOOGLE_API_KEY,
        "language": "en"
    }
    headers = {
        "Accept-Charset": "utf-8"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "predictions" in data:
                    return paginate(city_controller.extract_cities(data["predictions"]), pagination_params)

            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch city predictions")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/photo_reference/{place_id}")
async def get_city_photo_reference(place_id: str) -> Optional[str]:
    url = f"https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "placeid": place_id,
        "key": GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            data = response.json()

            # Check if photos exist in data
            if "result" in data and "photos" in data["result"]:
                # Return the photo reference of the first photo
                first_photo_reference = data["result"]["photos"][0]["photo_reference"]
                return first_photo_reference

            # If no photo reference found, return None
            return None

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Google API: {e}")

    except (IndexError, KeyError):
        raise HTTPException(status_code=404, detail="No photo reference found")


@router.get("/picture/{place_id}")
async def city_picture(place_id: str) -> str:
    photo_reference = await get_city_photo_reference(place_id)

    if photo_reference is None:
        raise HTTPException(status_code=404, detail="No photo reference found")

    url = f"https://maps.googleapis.com/maps/api/place/photo"
    params = {
        "maxwidth": 400,
        "photo_reference": photo_reference,
        "key": GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return str(response.url).strip('"')  # Returns the URL of the photo

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/lat-lon/{city_text}")
async def get_lat_lon(city_text: str) -> dict:
    if not city_text:
        raise HTTPException(status_code=404, detail="No city given")

    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city_text,
        "key": GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response_data = response.json()

            # Extract latitude and longitude
            if response_data["status"] == "OK" and response_data["results"]:
                location = response_data["results"][0]["geometry"]["location"]
                lat = location["lat"]
                lon = location["lng"]
                return {"lat": lat, "lon": lon}
            else:
                raise HTTPException(status_code=404, detail="Location not found")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected response structure: {str(e)}")
