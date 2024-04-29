from typing import List

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers.item_controller import ItemController
from src.entity.item import Item
from src.entity.item_boundary import ItemBoundary

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
    # try:
    items = item_controller.filter_items_by(category, season, gender)
    if len(items) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found matching the filters.")
    return items


@router.get("/amount-by", response_model=List[ItemBoundary])
async def get_category_items_and_calculation(category: str = Query(..., description="category")):
    return item_controller.get_category_items_and_calculation(category)
