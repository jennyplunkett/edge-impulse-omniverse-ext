# SPDX-License-Identifier: Apache-2.0

import omni.ext
import omni.ui as ui
import asyncio
import aiohttp
from omni.ui import style_utils
from functools import partial
import requests
import os

def upload_data(api_key, data_folder):
    host = "https://studio.edgeimpulse.com/v1"

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

def getPath(label, text):
    #label.text = f"You wrote '{text}'"
    DataIngestion.DATA_FOLDER = os.path.normpath(text)
    #print("Data Path Changed:", DataIngestion.DATA_FOLDER)

def getEIAPIKey(label, text):
    #label.text = f"You wrote '{text}'"
    DataIngestion.API_KEY = text
    #print("Edge Impulse API Key Changed:", DataIngestion.API_KEY)

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class DataIngestion(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    API_KEY = ''
    DATA_FOLDER = ''

    def on_startup(self, ext_id):
        print("[edgeimpulse.dataingestion] Edge Impulse Data Ingestion startup")

        self._window = ui.Window("Edge Impulse Data Ingestion", auto_resize=True)
        with self._window.frame:
            with ui.VStack(spacing=8):
                
                with ui.HStack(height=20):
                    ui.Spacer(width=3)
                    ui.Label("Create a free Edge Impulse account: https://studio.edgeimpulse.com/", height=20, word_wrap=True)
                    ui.Spacer(width=3)

                with ui.HStack(height=20):
                    ui.Spacer(width=3)
                    data_path_label = ui.Label("Data Path", name="header_attribute_name", width=70)
                    ui.Spacer(width=8)
                    data_path = ui.StringField(name="path")
                    data_path.model.set_value("C:\\Users\\...")
                    data_path.model.add_value_changed_fn(lambda m, label=data_path_label: getPath(data_path_label, m.get_value_as_string()))
                    ui.Spacer(width=3)

                with ui.HStack(height=20):
                    ui.Spacer(width=3)
                    ei_api_key_label = ui.Label("Edge Impulse API Key", name="header_attribute_name", width=70)
                    ui.Spacer(width=8)
                    ei_api_key = ui.StringField(name="ei_api_key")
                    ei_api_key.model.set_value("ei_02162...")
                    ei_api_key.model.add_value_changed_fn(lambda m, label=ei_api_key_label: getEIAPIKey(ei_api_key_label, m.get_value_as_string()))
                    ui.Spacer(width=3)

                def on_click():
                    asyncio.ensure_future(upload_data(self.API_KEY, self.DATA_FOLDER))
                
                with ui.HStack(height=20):
                    ui.Button("Upload to Edge Impulse", clicked_fn=on_click)
                

    def on_shutdown(self):
        print("[edgeimpulse.dataingestion] Edge Impulse Data Ingestion shutdown")

   

    
