# Easy Pack Server :luggage: :memo:

The EasyPack server is built with Python using the FastAPI framework, offering a secure and efficient backend for the EasyPack application.
The server handles the creation of customized packing lists by analyzing trip details, such as destination, dates, and weather conditions.

The frontend application for EasyPack is maintained in a separate repository [easypack-frontend](https://github.com/yardensepton/easypack-frontend).

## Table of Contents
* [Key Features](#key-features)
* [Installation](#installation)
* [Usage](#usage)


## Key Features	

* FastAPI Framework: Ensures high performance and scalability.
* Customizable Packing Lists: Generates lists based on destination, weather, personal preferences and the historical weather data of the user's residence.
* User Authentication: Implements OAuth2PasswordBearer for password and email authentication, including a 'forgot password' option for user convenience.
* Security System: Uses access tokens and refresh tokens to maintain secure and seamless user sessions.

Whether users are traveling to a sunny beach or a snowy mountain, EasyPack provides a tailored packing list to ensure they have everything they need.
Users can also add special items to their lists for further personalization.

The backend leverages a [MongoDB database](https://www.mongodb.com/) for robust data storage and integrates with multiple APIs
to provide comprehensive weather and location information:

* [Meteostat Python library](https://dev.meteostat.net/python/): Fetches historical weather data based on the user's residence.
* [VisualCrossingAPI](https://www.visualcrossing.com/): Supplies current and forecasted weather data for trip destinations.
* [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview): Provides autocomplete suggestions for city names and retrieves city images for profile creation or trip planning.


## Installation

#### To run it, configure environment variables in a new `.env` file:
run the following bash script. remember to fill the env variables according to your configuration.

```bash
# external API's configurations
GOOGLE_API_KEY= # TODO: insert here your google api key
WEATHER_API_KEY= # TODO: insert here your VisualCrossingAPI key

# authentication configuration
JWT_ACCESS_SECRET= # TODO: insert your access jwt access secret
JWT_REFRESH_SECRET= # TODO: insert your refresh jwt access secret
JWT_ALGORITHM= # TODO: currently using HS256, set according to your needs

# database configuration
CONNECTION_STRING_MONGO= # TODO: insert your MongoDB connection string

cat <<EOF > .env
GOOGLE_API_KEY=${GOOGLE_API_KEY}
WEATHER_API_KEY=${WEATHER_API_KEY}
JWT_ACCESS_SECRET=${JWT_ACCESS_SECRET}
JWT_REFRESH_SECRET=${JWT_REFRESH_SECRET}
JWT_ALGORITHM=${JWT_ALGORITHM}
CONNECTION_STRING_MONGO=${CONNECTION_STRING_MONGO}
EOF
```
#### To insert essential data into your database:
Use the provided script `insert_data.py` to insert critical data into your MongoDB database. This data is necessary for the functionality of EasyPack and includes:
* Clothing items categorized by temperature ranges, which the packing list generator uses to recommend appropriate clothing based on the trip's weather.
* Special items such as eyeglasses and contact lenses, which are integrated into the packing list functionality.

Run the following command to execute the script:
```
 python insert_data.py
```

## Run the backend locally
```python
...
```

## Create an image and run it locally
```bash
docker build -t <tag-name>:<version>
docker run -p 8080:8080 --env-file .env -t <tag-name>:<version>
```
