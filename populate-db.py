import requests

# Utility script - Populate db with some initial values (area in square km, population in millions)

url = "http://127.0.0.1:5000/countries/"

new_data = [
    {"area":358000,"capital":"Berlin","id":1,"name":"Germany","population":83},
    {"area":544000,"capital":"Paris","id":2,"name":"France","population":65},
    {"area":244000,"capital":"London","id":3,"name":"UK","population":68},
    {"area":302000,"capital":"Rome","id":4,"name":"Italy","population":58},
    {"area":31000,"capital":"Brussels","id":5,"name":"Belgium","population":12},
    {"area":498000,"capital":"Madrid","id":6,"name":"Spain","population":47},
    {"area":132000,"capital":"Athens","id":7,"name":"Greece","population":10},
    {"area":84000,"capital":"Vienna","id":8,"name":"Austria","population":9},
    {"area":92000,"capital":"Lisbon","id":9,"name":"Portugal","population":10},
    {"area":439000,"capital":"Stockholm","id":10,"name":"Sweden","population":11}
]

# find out how many entries there are already
#response = requests.get(url+str(1))
#print(response)

# TO DO - add exceptions
for item in new_data: 
    response = requests.post(url, json=item)
    print(response)



