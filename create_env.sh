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