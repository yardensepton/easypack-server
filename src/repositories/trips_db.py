from src.models.trip_entity import TripEntity
from src.repositories.db_handler import DBHandler


class TripsDB(DBHandler):
    def init(self, data: dict) -> TripEntity:
        return TripEntity(**data)

    # async def watch(self, pipeline):
    #     self.collection.watch(pipeline)

    # def watch(self):
    #     print("in watch")
    #     change_stream = self.collection.watch([{
    #         '$match': {
    #             'operationType': {'$in': ['insert']}
    #         }
    #     }])
    #
    #     for change in change_stream:
    #         print(dumps(change))
    #         print('')
