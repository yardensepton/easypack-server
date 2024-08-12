from pymongo import MongoClient

from config import CONNECTION_STRING_MONGO
from config import MONGO_DB_NAME

client = MongoClient(CONNECTION_STRING_MONGO)
db = client[MONGO_DB_NAME]

items_collection = db['ITEMS']
calculation_collection = db['CALCULATIONS']

# Data to be inserted into the ITEMS and CALCULATIONS collections
items = [
    {
        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "hat",
        "temp_max": 999,
        "temp_min": 20
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "sunglasses",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "day bag",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "gloves",
        "temp_max": 10,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "top layer",
        "gender": "all",
        "name": "jacket",
        "temp_max": 19,
        "temp_min": 10
    },
    {

        "default": True,
        "category": "important",
        "gender": "all",
        "name": "passport",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "finance",
        "gender": "all",
        "name": "local currency",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "plasters and bandages",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "formal_event",
        "gender": "male",
        "name": "tie",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "shoes",
        "gender": "all",
        "name": "sneakers",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "female",
        "name": "jewellery",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "scarf",
        "temp_max": 15,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "top layer",
        "gender": "all",
        "name": "coat",
        "temp_max": 9,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "mid layer",
        "gender": "all",
        "name": "fleece",
        "temp_max": 15,
        "temp_min": 11
    },
    {

        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "headphones",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "lip balm",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "bag for laundry",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "warm hat",
        "temp_max": 10,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "backpack",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "work",
        "gender": "all",
        "name": "computer",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "phone",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "finance",
        "gender": "all",
        "name": "credit card",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "travel sickness tablets",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "prescription medications",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "hand sanitiser",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "formal_event",
        "gender": "male",
        "name": "suit jacket",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "rain clothes",
        "gender": "all",
        "name": "water-resistant coat",
        "temp_max": 15,
        "temp_min": 5
    },
    {

        "default": False,
        "category": "skirts",
        "gender": "female",
        "name": "sundress",
        "temp_max": 35,
        "temp_min": 20
    },
    {

        "default": False,
        "category": "shirts",
        "gender": "all",
        "name": "tank top",
        "temp_max": 999,
        "temp_min": 29
    },
    {

        "default": False,
        "category": "shoes",
        "gender": "all",
        "name": "flip flops",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "shoes",
        "gender": "all",
        "name": "sandals",
        "temp_max": 999,
        "temp_min": 20
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "wallet",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "belt",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "eyeglasses",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "car",
        "gender": "all",
        "name": "driver's licence",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "important",
        "gender": "all",
        "name": "travel insurance",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "charger",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "travel adapters",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "power bank",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "antihistamines",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "indigestion tablets",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "formal_event",
        "gender": "female",
        "name": "formal dress",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": False,
        "category": "formal_event",
        "gender": "female",
        "name": "heels",
        "temp_max": 999,
        "temp_min": -999
    },
    {

        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "sunscreen",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "pants",
        "gender": "all",
        "name": "long pants",
        "temp_max": 24,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "pants",
        "gender": "all",
        "name": "short pants",
        "temp_max": 999,
        "temp_min": 25
    },
    {
        "default": False,
        "category": "rain clothes",
        "gender": "all",
        "name": "umbrella",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "shirts",
        "gender": "all",
        "name": "long-sleeved shirt",
        "temp_max": 22,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "underwear",
        "gender": "all",
        "name": "socks",
        "temp_max": 999,
        "temp_min": 10
    },
    {
        "default": False,
        "category": "shoes",
        "gender": "all",
        "name": "going out shoes",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "sports",
        "gender": "female",
        "name": "sports bra",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "swimming",
        "gender": "all",
        "name": "swimsuit",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "female",
        "name": "hair products",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "travel sized shampoo",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "tissues",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "underwear",
        "gender": "all",
        "name": "underwear",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "bottles and formula",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby toys",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby monitor",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "sun hat",
        "temp_max": 30,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby winter coat",
        "temp_max": 19,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "sleepwear",
        "gender": "all",
        "name": "warm pajamas",
        "temp_max": 15,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "swimming",
        "gender": "female",
        "name": "beach cover-up",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "wet wipes",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "tweezers",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "personal hygiene",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "female",
        "name": "feminine products",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "underwear",
        "gender": "all",
        "name": "thick socks",
        "temp_max": 10,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby carrier or stroller",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "changing pad",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "shoes",
        "gender": "all",
        "name": "boots",
        "temp_max": 10,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "running shoes",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "sleepwear",
        "gender": "all",
        "name": "pajamas",
        "temp_max": 999,
        "temp_min": 16
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "deodorant",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "female",
        "name": "makeup",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "toothbrush",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "dental floss",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "underwear",
        "gender": "female",
        "name": "bra",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby wipes",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "pacifiers",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby sunscreen",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "portable crib",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "lightweight baby clothes",
        "temp_max": 30,
        "temp_min": 20
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby thermal wear",
        "temp_max": 10,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "gym long pants",
        "temp_max": 22,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "perfume",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "travel sized conditioner",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "scissors",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "razor",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "all",
        "name": "toothpaste",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "diapers",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby food",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby blanket",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby sandals",
        "temp_max": 30,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "trip_with_a_baby",
        "gender": "all",
        "name": "baby sweater",
        "temp_max": 20,
        "temp_min": 10
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "male",
        "name": "shaving products",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "electronics",
        "gender": "all",
        "name": "esim or local simcard",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "first aid kit",
        "gender": "all",
        "name": "mosquito repellents",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "work",
        "gender": "all",
        "name": "work suit",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "work",
        "gender": "all",
        "name": "computer charger",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "contact lenses",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "female",
        "name": "hair straightener",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "female",
        "name": "hair dryer",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "female",
        "name": "curling iron",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "allergy pills",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "earplugs ",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "camera ",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "books ",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "female",
        "name": "birth control",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "toiletries",
        "gender": "female",
        "name": "hair brush",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "swimming",
        "gender": "all",
        "name": "beach bag",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "special items",
        "gender": "all",
        "name": "blindfold",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "thermal",
        "gender": "all",
        "name": "thermal shirt",
        "temp_max": 0,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "thermal",
        "gender": "all",
        "name": "thermal pants",
        "temp_max": 0,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "mid layer",
        "gender": "all",
        "name": "hoodie",
        "temp_max": 20,
        "temp_min": 16
    },
    {
        "default": False,
        "category": "shirts",
        "gender": "all",
        "name": "short-sleeved shirt",
        "temp_max": 29,
        "temp_min": 23
    },
    {
        "default": False,
        "category": "mid layer",
        "gender": "all",
        "name": "sweater",
        "temp_max": 10,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "important",
        "gender": "all",
        "name": "house keys",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": True,
        "category": "accessories",
        "gender": "all",
        "name": "ear muffs",
        "temp_max": 0,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "gym short pants",
        "temp_max": 999,
        "temp_min": 22
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "gym long-sleeved shirt",
        "temp_max": 15,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "gym short-sleeved shirt",
        "temp_max": 999,
        "temp_min": 15
    },
    {
        "default": False,
        "category": "sports",
        "gender": "all",
        "name": "extra socks",
        "temp_max": 999,
        "temp_min": -999
    },
    {
        "default": False,
        "category": "swimming",
        "gender": "all",
        "name": "extra set of clothes",
        "temp_max": 999,
        "temp_min": -999
    }
]

calculations = [
    {

        "activity": False,
        "category": "top layer",
        "amount_per_day": 999
    },
    {

        "activity": False,
        "category": "work",
        "amount_per_day": 999
    },
    {

        "activity": False,
        "category": "shirts",
        "amount_per_day": 0.75
    },
    {

        "activity": False,
        "category": "electronics",
        "amount_per_day": 999
    },
    {

        "activity": False,
        "category": "first aid kit",
        "amount_per_day": 999
    },
    {
        "activity": True,
        "category": "formal_event",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "rain clothes",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "sleepwear",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "toiletries",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "accessories",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "others",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "pants",
        "amount_per_day": 0.5
    },
    {
        "activity": False,
        "category": "underwear",
        "amount_per_day": 1
    },
    {
        "activity": True,
        "category": "swimming",
        "amount_per_day": 999
    },
    {
        "activity": True,
        "category": "trip_with_a_baby",
        "amount_per_day": 999
    },
    {
        "activity": True,
        "category": "car",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "important",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "finance",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "shoes",
        "amount_per_day": 999
    },
    {
        "activity": True,
        "category": "sports",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "skirts",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "special items",
        "amount_per_day": 999
    },
    {
        "activity": False,
        "category": "mid layer",
        "amount_per_day": 0.1
    },
    {
        "activity": False,
        "category": "thermal",
        "amount_per_day": 999
    }
]

# Insert data into the collections
items_result = items_collection.insert_many(items)
calc_result = calculation_collection.insert_many(calculations)

# Print out the inserted IDs
print("Inserted items IDs:", items_result.inserted_ids)
print("Inserted calc IDs:", calc_result.inserted_ids)
