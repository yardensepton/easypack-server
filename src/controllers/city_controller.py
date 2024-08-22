from typing import List

from src.models.city import City


class CityController:
    @classmethod
    def extract_cities(cls, predictions: List[dict]) -> List[City]:
        """
              Extracts cities from a list of prediction dictionaries.

              Args:
                  predictions (List[dict]): A list of prediction dictionaries containing location data.

              Returns:
                  List[City]: A list of City objects extracted from the predictions.
              """
        cities = []
        for prediction in predictions:
            if "types" in prediction and "locality" in prediction["types"]:
                if "description" in prediction and "place_id" in prediction:
                    text = prediction["description"]
                    arr = text.split(",")
                    city_name = arr[0]
                    country_name = arr[len(arr) - 1].strip(" ")
                    place_id = prediction["place_id"]
                    cities.append(City(text=text, city_name=city_name, place_id=place_id, country_name=country_name))
        return cities
