from api import db
import requests

# init tables
db.create_all()

# create one user
api_url = 'http://localhost:5000/'

def create_user(user_id, name):

    data = {'id':user_id, 'name':name}
    response = requests.post(url=api_url+'user', json=data)
    return response

response = create_user(1,'Fred')
print(response.text)