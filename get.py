import json
import requests

api_url='https://api.parking-pilot.com/'

api_key='?api_key=HUK_Team4'

def get_parkingspaces(method):

    r = requests.get(url=api_url+'parkingspaces/61720/'+method+api_key)
    print(r.text)

get_parkingspaces('')