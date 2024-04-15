class PackingListNotFoundError(Exception):
    def __init__(self, packing_list_id):
        super().__init__(f"Packing list '{packing_list_id}' not found")