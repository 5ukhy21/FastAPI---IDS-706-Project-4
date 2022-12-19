## Import libraries
import sqlite3
import csv
import fastapi
from fastapi import FastAPI
import uvicorn
import pandas as pd
import json


## Create FastAPI get command
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "3 Star Michelin Restaurants. These are the top restaurants in the world."}

## Establish connection
connection = sqlite3.connect("michelin_star_restaurants.db")
drop = "DROP TABLE IF EXISTS michelin_star_restaurants"
restaurants_table = "CREATE TABLE michelin_star_restaurants (name string primary key, year int, latitude float, longitude float, city VARCHAR, region VARCHAR, zipCode VARCHAR, cuisine VARCHAR, price VARCHAR, url VARCHAR)"

## Execute on the connection
cursor = connection.cursor()
cursor.execute(drop)
cursor.execute(restaurants_table)

## Insert into table
insert = "INSERT INTO michelin_star_restaurants(name,year,latitude,longitude,city,region,zipCode,cuisine,price,url) VALUES (?,?,?,?,?,?,?,?,?,?)"

## Open the csv files
one_star_file = open("/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 706.01.F22/Week 13/FastAPI---IDS-706-Project-4/one-star-michelin-restaurants.csv")
two_star_file = open("/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 706.01.F22/Week 13/FastAPI---IDS-706-Project-4/two-stars-michelin-restaurants.csv")
three_star_file = open("/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 706.01.F22/Week 13/FastAPI---IDS-706-Project-4/three-stars-michelin-restaurants.csv")

## Read the contents of each of the csv files
one_star_restaurants = csv.reader(one_star_file)
two_star_restaurants = csv.reader(two_star_file)
three_star_restaurants = csv.reader(three_star_file)

## Skip the first row for all csv files
#next(one_star_restaurants)
next(two_star_restaurants)
next(three_star_restaurants)

## Create a list of restaurants
list_of_restaurants = []

##for restaurant in one_star_restaurants:
    ##list_of_restaurants.append(restaurant)

##for restaurant in two_star_restaurants:
    ##list_of_restaurants.append(restaurant)

for restaurant in three_star_restaurants:
    list_of_restaurants.append(restaurant)

#print(seq_of_parameters)

for i in list_of_restaurants:
    cursor.execute(insert,i)

connection.commit()

## Query Database

print(f"Below are the list of all Michelin Star restaurants:")
all_restaurants = """SELECT * FROM michelin_star_restaurants;"""

restaurants = []
for i in cursor.execute(all_restaurants):
    restaurants.append(i)

#convert restaurants from list to string
restaurants = str(restaurants)
restaurants = restaurants.replace("[","")
restaurants = restaurants.replace("]","")
restaurants = restaurants.replace("'","")

@app.get("/all_restaurants")
async def root():
    return {"These are all the Michelin star restaurants in the world": restaurants}

print(f"Find all restaurants that serve Contemporary cuisine")
contemporary_restaurants = """SELECT * FROM michelin_star_restaurants WHERE cuisine = 'Contemporary';"""

contemporary = []
for i in cursor.execute(contemporary_restaurants):
    contemporary.append(i)

#convert restaurants from list to string
contemporary = str(contemporary)
contemporary = contemporary.replace("[","")
contemporary = contemporary.replace("]","")
contemporary = contemporary.replace("'","")

@app.get("/contemporary_restaurants")
async def root():
    return {"These are all the Michelin star restaurants in the world that serve Contemporary cuisine": restaurants}

print(f"Find restaurants that serve French cuisine in the United Kingdom")
uk_french_restaurants = """SELECT * FROM michelin_star_restaurants WHERE cuisine = 'French' AND region = 'United Kingdom';"""

uk_french = []
for i in cursor.execute(uk_french_restaurants):
    uk_french.append(i)

#convert restaurants from list to string
uk_french = str(uk_french)
uk_french = uk_french.replace("[","")
uk_french = uk_french.replace("]","")
uk_french = uk_french.replace("'","")


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")