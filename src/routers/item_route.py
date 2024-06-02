from typing import List

from fastapi import APIRouter, Query

from src.controllers.item_controller import ItemController
from src.models.item import Item
from src.models.item_and_calculation import ItemAndCalculation

router = APIRouter(
    prefix="/items",
    tags=["ITEMS"]
)

item_controller = ItemController()


@router.get("", response_model=List[Item])
async def get(category: str = Query(None, description="category"),
              season: str = Query(None, description="season"),
              gender: str = Query(None, description="gender")
              ):
    return item_controller.filter_items_by(category, season, gender)


@router.get("/amount-by", response_model=List[ItemAndCalculation])
async def get_category_items_and_calculation(category: str = Query(..., description="category")):
    return item_controller.get_category_items_and_calculation(category)
