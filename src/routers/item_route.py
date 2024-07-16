from typing import List

from fastapi import APIRouter, Query, Depends

from src.controllers.item_controller import ItemController
from src.models.calculation import Calculation
from src.models.item import Item
from src.models.item_and_calculation import ItemAndCalculation
from src.models.user_entity import UserEntity
from src.utils.authantication.current_identity_utils import get_current_access_identity

router = APIRouter(
    prefix="/items",
    tags=["ITEMS"]
)

item_controller = ItemController()


@router.get("", response_model=List[Item])
async def get(category: str = Query(None, description="category"),
              temperature: float = Query(None, description="temperature"),
              gender: str = Query(None, description="gender"),
              default: bool = Query(None, description="default"),
              identity: UserEntity = Depends(get_current_access_identity)):
    return item_controller.filter_items_by(category=category, user_trip_average_temp=temperature, user_gender=gender,
                                           default=default)


@router.get("/amount-by", response_model=List[ItemAndCalculation])
async def get_category_items_and_calculation(category: str = Query(None, description="category"),
                                             identity: UserEntity = Depends(get_current_access_identity)):
    return item_controller.get_category_items_and_calculation(category)


@router.get("/calculations", response_model=List[Calculation])
async def get_calculations(category: str = Query(None, description="category"),
                           activity: bool = Query(None, description="activity"),
                           identity: UserEntity = Depends(get_current_access_identity)):
    return item_controller.filter_calculations_by(category, activity)
