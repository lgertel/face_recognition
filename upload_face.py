import requests


files = {'file': open('/Users/lgertel/Downloads/Demo ADT/Marco Seraphim.jpeg','rb')}
r = requests.post('https://adtwelcome.mybluemix.net/face',
    files = files,
    data = {
        'label':'Marco Seraphim',
        'email': 'marco.seraphim@adtsys.com.br',
        'type': 1
    })


import os
import swiftclient.client as swiftclient

auth_url = 'https://identity.open.softlayer.com/v3'
project_id = '6dab3b9835a94f828e11ed11ad425384'
user_id = 'a686c59615c34693abaa06efbb70c265'

# Swift region
region_name = 'dallas'

# Password for authentication
password = 'g98O=H==_[G2)t-('

# Get a Swift client connection object
conn = swiftclient.Connection(
        key=password,
        authurl=auth_url,
        auth_version='3',
        os_options= {
            "project_id": project_id,
             "user_id": user_id,
             "region_name": region_name
             })


here = os.path.dirname(os.path.realpath(__file__))
subdir = "subdir"

for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
        obj = conn.get_object(container['name'], data['name'])
        filepath = os.path.join(here, "pictures_of_people_i_know", data['name'])
        f = open(filepath, 'wb')
        f.write(obj[1])
        f.close()
