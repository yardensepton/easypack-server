from typing import List, Dict, Any

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers.item_controller import ItemController
from src.entity.item import Item
from src.entity.item_boundary import ItemBoundary
from src.exceptions.calculation_not_found_error import CalculationNotFoundError
from src.exceptions.item_not_found_error import ItemNotFoundError

router = APIRouter(
    prefix="/items",
    tags=["ITEMS"]
)

item_controller = ItemController()


@router.get("/", response_model=List[Item])
async def get(category: str = Query(None, description="category"),
        season: str = Query(None, description="season"),
              gender: str = Query(None, description="gender")
              ):
    try:
        return item_controller.filter_items_by(category, season, gender)
        # if category is not None and season is not None and gender is not None:
        #     return item_controller.get_all_items_by_category_season_and_gender(category, season,gender)
        # if category is not None and season is not None and gender is not None:
        #     return item_controller.get_all_items_by_category_season_and_gender(category, season, gender)
        # elif category is not None:
        #     return item_controller.get_all_items_by_category(category)
        # elif season is not None:
        #     return item_controller.get_all_items_by_season(season)
        # elif gender is not None:
        #     return item_controller.get_all_items_by_gender(gender)
        # else:
        #     return item_controller.get_all_items()

    except ItemNotFoundError as inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(inf))


@router.get("/amount-by", response_model=List[ItemBoundary])
async def get_category_items_and_calculation(category: str = Query(..., description="category")):
    try:
        return item_controller.get_category_items_and_calculation(category)
    except ItemNotFoundError as inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(inf))
    except CalculationNotFoundError as cnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(cnf))
