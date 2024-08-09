'''Calls an API - mostly used for populating and deleting data from a db
'''

import requests

url = "http://127.0.0.1:5000/countries/"

# If populate-db is required, post some default data

# data = list of json records to be posted

# call requests.post for each one ...
# for item in data: 
#   requests.post(url, json=item)
#   print(response.json())


# if clear-db is required, delete data

# requests.delete data
