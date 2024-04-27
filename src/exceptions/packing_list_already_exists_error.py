class PackingListAlreadyExistsError(Exception):
    def __init__(self, trip_id: str):
        super().__init__(f"Trip '{trip_id}' already has a packing list")