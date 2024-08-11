# Easy Pack :luggage:	:airplane:	

EasyPack is a smart packing list generator designed to simplify your travel preparations.
By analyzing your trip's destination, dates, and expected weather conditions, EasyPack creates a customized packing list tailored to your personal preferences and temperature comfort zones.
Whether you're heading to a sunny beach or a snowy mountain, EasyPack ensures you won't forget any essentials.
Plus, you can personalize your list further by adding special items.

## Quickstart

The backend uses `Mongo database`, TODO: add more. 

#### To run it, configure environment variables in a new `.env` file:
run the following bash script. remember to fill the env variables according to your configuration.

```bash
# external API's configurations
GOOGLE_API_KEY= # TODO: insert here your google api key
WEATHER_API_KEY= # TODO: insert here your weather api key

# authentication configuration
JWT_ACCESS_SECRET= # TODO: insert your access jwt access secret
JWT_REFRESH_SECRET= # TODO: fill
JWT_ALGORITHM= # TODO: fill

# database configuration
CONNECTION_STRING_MONGO= # TODO: fill

cat <<EOF > .env
GOOGLE_API_KEY=${GOOGLE_API_KEY}
WEATHER_API_KEY=${WEATHER_API_KEY}
JWT_ACCESS_SECRET=${JWT_ACCESS_SECRET}
JWT_REFRESH_SECRET=${JWT_REFRESH_SECRET}
JWT_ALGORITHM=${JWT_ALGORITHM}
CONNECTION_STRING_MONGO=${CONNECTION_STRING_MONGO}
EOF
```

Then, use the following `docker` command in order to run the backend:

```bash
docker build -t <tag-name>:<version>
docker run -p 8080:8080 --env-file .env -t <tag-name>:<version>
```
