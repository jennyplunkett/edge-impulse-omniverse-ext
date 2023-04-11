# SPDX-License-Identifier: Apache-2.0

import omni.ext
import omni.ui as ui
import asyncio
import aiohttp
from omni.ui import style_utils
from functools import partial
import requests
import os

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[edgeimpulse.dataingestion] some_public_function was called with x: ", x)
    return x ** x

     
#hex to float conversion for transforming hex color codes to float values
def hextofloats(h):
    #Convert hex rgb string in an RGB tuple (float, float, float)
    return tuple(int(h[i:i + 2], 16) / 255. for i in (1, 3, 5)) # skip '#'   


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

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    def on_startup(self, ext_id):
        print("[edgeimpulse.dataingestion] Edge Impulse Data Ingestion startup")

        #create a new window        
        self._window = ui.Window("Edge Impulse Data Ingestion", width=260, height=270)
        with self._window.frame:
            with ui.VStack(alignment=ui.Alignment.CENTER):
                
                #ui.Label("Click the button to upload your data",height=30)
                ui.Label("Data Path", name="header_attribute_name", width=70)
                ui.StringField(name="path").model.set_value("/data")

                ui.Label("EI API Key", name="header_attribute_name", width=70)
                ui.StringField(name="api_key").model.set_value("ei_02162...")

                api_key = 'ei_021...'
                data_folder = os.getcwd() + '/edge-impulse-omniverse-ext/data/'

                #create a button to trigger the api call
                def on_click():
                    asyncio.ensure_future(upload_data(api_key, data_folder))
                
                ui.Button("Upload to Edge Impulse", clicked_fn=on_click)

                #we execute the api call once on startup
                #asyncio.ensure_future(get_colors_from_api(color_widgets))

             
                

    def on_shutdown(self):
        print("[edgeimpulse.dataingestion] Edge Impulse Data Ingestion shutdown")

   

    
