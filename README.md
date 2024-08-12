# Easy Pack :luggage:	:flight_departure:	

EasyPack is a smart packing list generator designed to simplify your travel preparations.
By analyzing your trip's destination, dates, and expected weather conditions, EasyPack creates a customized packing list tailored to your personal preferences and temperature comfort zones.
Whether you're heading to a sunny beach or a snowy mountain, EasyPack ensures you won't forget any essentials.
Plus, you can personalize your list further by adding special items.


The backend uses a [MongoDB database](https://www.mongodb.com/) and integrates with the [Meteostat Python library](https://dev.meteostat.net/python/) to fetch historical weather data for the user's residence and the [VisualCrossingAPI](https://www.visualcrossing.com/) to provide current and forecasted weather data for the trip's destination

## Quickstart

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




Then, use the following `docker` command in order to run the backend:

```bash
docker build -t <tag-name>:<version>
docker run -p 8080:8080 --env-file .env -t <tag-name>:<version>
```
