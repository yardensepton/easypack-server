from typing import List

from src.models.city import City


class CityController:
    @classmethod
    def extract_cities(cls, predictions: List[dict]) -> List[City]:
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

    # @classmethod
    # def get_country_code(cls, country_name: str) -> str:
    #     country = pycountry.countries.get(name=country_name)
    #     print(country)
    #     currency_code = pycountry.currencies.get(numeric=country.numeric)
    #     print(currency_code)
    #     return currency_code.alpha_3
