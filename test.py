import requests
import os
from edgeimpulse_api import Configuration, ApiClient, ProjectsApi

host = "https://studio.edgeimpulse.com/v1"
api_key = 'ei_021629d9ea612d5cb176d36fc5630ccfb4b9b551f06d507fc821f25fb0ba553a'

data_folder = os.getcwd() + '/edge-impulse-omniverse-ext/data/'

for file in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file)
    # Labels are determined from the filename, anything after "." is ignored, i.e.
    # File "object.1.blah.png" will be uploaded as file object.1.blah with label "object"
    label = os.path.basename(file_path).split('.')[0]
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            res = requests.post(url='https://ingestion.edgeimpulse.com/api/training/files',
            headers= {
                'x-label': label,
                'x-api-key': api_key,
                'x-disallow-duplicates': '1'
            },
            files = { 'data': (os.path.basename(file_path), open(file_path, 'rb'), 'image/png') }
        )
    if (res.status_code == 200):
        print('Uploaded file to Edge Impulse', res.status_code, res.content)
    else:
        print('Failed to upload file to Edge Impulse', res.status_code, res.content)

# Create a client object that can connect to our project
config = Configuration(host=host, api_key={"ApiKeyAuthentication": api_key})
client = ApiClient(config)

# Get info about the project
projects = ProjectsApi(client)
project_list = projects.list_projects()
print(project_list.projects[0])