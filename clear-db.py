import requests

# Utility script - clear countries DB - converse of populate-db

url = "http://127.0.0.1:5000/countries/"

# For the countries rest API only, delete all records using url string + str(id) (id = primary key)
# Assume id starts at 0 and has max of 19 - any non-existing will return 404
# If id is outside of assumptions, deletion will not happen

for i in range(20):
    try:
        response = requests.delete(url+str(i))
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print ("HTTP Error:", http_err)
    except requests.exceptions.ConnectionError as conn_err:
        print ("Connection error:", conn_err)
    except requests.exceptions.Timeout as timeout_err:
        print ("Timeout error:", timeout_err)
    except requests.exceptions.RequestException as err:
        print ("Unknown error:", err)
    print(response)