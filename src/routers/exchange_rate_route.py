import httpx
from fastapi import APIRouter, HTTPException

from config import EXCHANGE_RATE_API

router = APIRouter(
    prefix="/exchange-rate",
    tags=["MONEY"]
)


@router.get("")
async def exchange_rate():
    base = "ILS"
    target = "USD"

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API}/pair/{base}/{target}/10"

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
