import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/exchange-rate",
    tags=["MONEY"]
)


def load_env() -> str:
    load_dotenv()
    exchange_rate_api = os.getenv("EXCHANGE_RATE_API")
    return exchange_rate_api


@router.get("")
async def exchange_rate():
    exchange_api = load_env()
    base = "ILS"
    target = "USD"

    url = f"https://v6.exchangerate-api.com/v6/{exchange_api}/pair/{base}/{target}/10"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data

            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch city exchange rate")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
