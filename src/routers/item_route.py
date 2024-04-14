from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Query

from src.controllers.item_controller import ItemController
from src.entity.item import Item

router = APIRouter(
    prefix="/items",
    tags=["ITEMS"]
)

item_controller = ItemController()


@router.get("/", response_model=List[Item])
def get(category: str = Query(None, description="category"),
        season: str = Query(None, description="season")):
    if category is not None and season is not None:
        return item_controller.get_all_items_by_category_and_season(category, season)
    elif category is not None:
        return item_controller.get_all_items_by_category(category)
    elif season is not None:
        return item_controller.get_all_items_by_season(season)
    else:
        return item_controller.get_all_items()



@router.get("/amount-by", response_model=Dict[str, Any])
def get_category_items_and_calculation(category: str = Query(..., description="category")):
    return item_controller.get_category_items_and_calculation(category)
