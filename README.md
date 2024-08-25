# Easy Pack Server :luggage: :memo:

The EasyPack server is built with Python using the FastAPI framework, offering a secure and efficient backend for the EasyPack application.
The server handles the creation of customized packing lists by analyzing trip details, such as destination, dates, and weather conditions.

The frontend application for EasyPack is maintained in a separate repository [easypack-frontend](https://github.com/yardensepton/easypack-frontend).

## Table of Contents
* [Key Features](#key-features)
* [Installation](#installation)
* [Run the backend locally](#Run-the-backend-locally)
* [Run the backend using Docker](#Run-the-backend-using-Docker)
* [Access the API](#access-the-api)
* [Create an Image and Run It Locally](#create-an-image-and-run-it-locally)


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
1. Open the [create_env.sh file](create_env.sh). 
2. Fill in the environment variables where "TODO" is indicated according to your configuration. 
3. If the script isn’t already executable, you need to make it executable. Open your terminal and run:
```bash
chmod +x create_env.sh
```
4. Run the script:
```
./create_env.sh
``` 

#### To insert essential data for the functionality of EasyPack into your database:
1. Open the [insert_items.sh file](insert_items.sh). 
2. Fill in your Mongo connection string where "TODO" is indicated.
3. If the script isn’t already executable, you need to make it executable. Open your terminal and run:
```bash
chmod +x insert_items.sh
```
4. Run the script:
```
./insert_items.sh
``` 


## Run the backend locally
1. Clone the EasyPack server repository:
```bash
git clone https://github.com/yardensepton/easypack-server.git
```
2. Install all required dependencies listed in the requirements.txt file:
```
pip install -r requirements.txt
```
3. Ensure you run the initialization scripts (create_env.sh and insert_items.sh) as described above.
4. Make sure your MongoDB server is running
5. Run the FastAPI server using uvicorn. Replace app with the appropriate module path for your FastAPI app:
```
 uvicorn app:app --host 0.0.0.0 --port 8080  
```
## Run the backend using Docker
1. Clone the EasyPack server repository:
```bash
git clone https://github.com/yardensepton/easypack-server.git
```
2. Ensure you run the initialization scripts (create_env.sh and insert_items.sh) as described above.
3. Pull the Docker Image.
You can pull the pre-built Docker image for EasyPack from Docker Hub. Use the following command to get the image:
```bash
docker pull yardensepton/easy-pack:<version>
```
4. After pulling the image, run the Docker container in detached mode with:
```bash
 docker run -p 8080:8080 --env-file .env -t easy-pack:<version> 
```
## Access the API
Swagger UI Documentation:
* URL: http://localhost:8080/docs
* This page provides an interactive interface where you can explore and test the API endpoints.

## Create an image and run it locally
```bash
docker build -t <tag-name>:<version>
docker run -p 8080:8080 --env-file .env -t <tag-name>:<version>
```
