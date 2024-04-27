class TripNotFoundError(Exception):
    def __init__(self, trip_id):
        super().__init__(f"Trip '{trip_id}' not found")