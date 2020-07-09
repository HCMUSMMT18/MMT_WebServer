import json
import os

with open("config.JSON") as config_file:
    data = json.load(config_file)

def set_rootpath():
    root = data['rootpath']

    os.rename('ESC', root)
    filename = os.getcwd() + "\\" + root
    print(filename)
   

def set_server(server):
    server = data['server']
    return server

set_rootpath()





