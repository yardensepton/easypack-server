#!/bin/bash

# Configuration
CONNECTION_STRING_MONGO=# TODO: insert here your mongo connection string here
MONGO_DB_NAME="EasyPack"
ITEMS_MONGO_COLLECTION="ITEMS"
CALCULATIONS_COLLECTION_NAME="CALCULATIONS"

# Define a function to insert data into MongoDB
insert_data() {
  mongo "$CONNECTION_STRING_MONGO/$MONGO_DB_NAME" --quiet --eval "
    db.$ITEMS_MONGO_COLLECTION.insertMany([
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"hat\", \"temp_max\": 999, \"temp_min\": 20},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"sunglasses\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"day bag\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"gloves\", \"temp_max\": 10, \"temp_min\": -999},
      {\"default\": false, \"category\": \"top layer\", \"gender\": \"all\", \"name\": \"jacket\", \"temp_max\": 19, \"temp_min\": 10},
      {\"default\": true, \"category\": \"important\", \"gender\": \"all\", \"name\": \"passport\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"finance\", \"gender\": \"all\", \"name\": \"local currency\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"plasters and bandages\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"formal_event\", \"gender\": \"male\", \"name\": \"tie\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"shoes\", \"gender\": \"all\", \"name\": \"sneakers\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"female\", \"name\": \"jewellery\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"scarf\", \"temp_max\": 15, \"temp_min\": -999},
      {\"default\": false, \"category\": \"top layer\", \"gender\": \"all\", \"name\": \"coat\", \"temp_max\": 9, \"temp_min\": -999},
      {\"default\": false, \"category\": \"mid layer\", \"gender\": \"all\", \"name\": \"fleece\", \"temp_max\": 15, \"temp_min\": 11},
      {\"default\": true, \"category\": \"electronics\", \"gender\": \"all\", \"name\": \"headphones\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"lip balm\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"bag for laundry\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"warm hat\", \"temp_max\": 10, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"backpack\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"work\", \"gender\": \"all\", \"name\": \"computer\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"electronics\", \"gender\": \"all\", \"name\": \"phone\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"finance\", \"gender\": \"all\", \"name\": \"credit card\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"travel sickness tablets\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"prescription medications\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"hand sanitiser\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"formal_event\", \"gender\": \"male\", \"name\": \"suit jacket\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"rain clothes\", \"gender\": \"all\", \"name\": \"water-resistant coat\", \"temp_max\": 15, \"temp_min\": 5},
      {\"default\": false, \"category\": \"skirts\", \"gender\": \"female\", \"name\": \"sundress\", \"temp_max\": 35, \"temp_min\": 20},
      {\"default\": false, \"category\": \"shirts\", \"gender\": \"all\", \"name\": \"tank top\", \"temp_max\": 999, \"temp_min\": 29},
      {\"default\": false, \"category\": \"shoes\", \"gender\": \"all\", \"name\": \"flip flops\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"shoes\", \"gender\": \"all\", \"name\": \"sandals\", \"temp_max\": 999, \"temp_min\": 20},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"wallet\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"accessories\", \"gender\": \"all\", \"name\": \"belt\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"special items\", \"gender\": \"all\", \"name\": \"eyeglasses\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"car\", \"gender\": \"all\", \"name\": \"driver\\'s licence\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"important\", \"gender\": \"all\", \"name\": \"travel insurance\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"electronics\", \"gender\": \"all\", \"name\": \"charger\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"electronics\", \"gender\": \"all\", \"name\": \"travel adapters\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"electronics\", \"gender\": \"all\", \"name\": \"power bank\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"antihistamines\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"first aid kit\", \"gender\": \"all\", \"name\": \"indigestion tablets\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"formal_event\", \"gender\": \"female\", \"name\": \"formal dress\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"formal_event\", \"gender\": \"female\", \"name\": \"heels\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"sunscreen\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"pants\", \"gender\": \"all\", \"name\": \"long pants\", \"temp_max\": 24, \"temp_min\": -999},
      {\"default\": false, \"category\": \"pants\", \"gender\": \"all\", \"name\": \"short pants\", \"temp_max\": 999, \"temp_min\": 25},
      {\"default\": false, \"category\": \"rain clothes\", \"gender\": \"all\", \"name\": \"umbrella\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": false, \"category\": \"rain clothes\", \"gender\": \"all\", \"name\": \"waterproof trousers\", \"temp_max\": 15, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"toothbrush\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"toothpaste\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"deodorant\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"shampoo\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"conditioner\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"soap\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"comb\", \"temp_max\": 999, \"temp_min\": -999},
      {\"default\": true, \"category\": \"toiletries\", \"gender\": \"all\", \"name\": \"tissues\", \"temp_max\": 999, \"temp_min\": -999}
    ])
  "
mongo "$CONNECTION_STRING_MONGO/$MONGO_DB_NAME" --quiet --eval "
  db.$CALCULATIONS_COLLECTION_NAME.insertMany([
    {\"activity\": false, \"category\": \"top layer\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"work\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"shirts\", \"amount_per_day\": 0.75},
    {\"activity\": false, \"category\": \"electronics\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"first aid kit\", \"amount_per_day\": 999},
    {\"activity\": true, \"category\": \"formal_event\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"rain clothes\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"sleepwear\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"toiletries\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"accessories\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"others\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"pants\", \"amount_per_day\": 0.5},
    {\"activity\": false, \"category\": \"underwear\", \"amount_per_day\": 1},
    {\"activity\": true, \"category\": \"swimming\", \"amount_per_day\": 999},
    {\"activity\": true, \"category\": \"trip_with_a_baby\", \"amount_per_day\": 999},
    {\"activity\": true, \"category\": \"car\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"important\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"finance\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"shoes\", \"amount_per_day\": 999},
    {\"activity\": true, \"category\": \"sports\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"skirts\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"special items\", \"amount_per_day\": 999},
    {\"activity\": false, \"category\": \"mid layer\", \"amount_per_day\": 0.1},
    {\"activity\": false, \"category\": \"thermal\", \"amount_per_day\": 999}
  ])
"
}

# Execute the function
insert_data
