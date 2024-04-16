from src.services.item_service import ItemService


class ItemController:

    def __init__(self):
        self.itemService = ItemService()

    def get_all_items_by_category(self, category: str):
        return self.itemService.get_all_items_by_category(category)

    def get_all_items_by_season(self, season: str):
        return self.itemService.get_all_items_by_season(season)

    def get_all_items(self):
        return self.itemService.get_all_items()


    def get_all_items_by_category_and_season(self, category: str, season: str):
        return self.itemService.get_all_items_by_category_and_season(category, season)


    def get_category_items_and_calculation(self, category: str):
        return self.itemService.get_category_items_and_calculation(category)
