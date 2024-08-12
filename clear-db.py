import requests

# Utility script - clear countries DB - converse of populate-db

url = "http://127.0.0.1:5000/countries/"

# For countries rest API only, delete all records using url string + str(id) (id = primary key)
# Assume id starts at 0 and has max of 19 - any non-existing will return 404
# If id is outside of assumptions, deletion will not happen

# TO DO - add exceptions
for i in range(20):
    response = requests.delete(url+str(i))
    print(response)