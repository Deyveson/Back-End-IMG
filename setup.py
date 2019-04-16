from setuptools import setup
import json
import os

with open('./metadata.json') as json_file:
    _, _, files = zip(*os.walk('src/resources/'))
    properties = ['src/resources/{}'.format(file) for file in files[0] if 'properties' in file]
    data = json.load(json_file)
    setup(
        name=data['name'],
        version=data['version'],
        scripts=['ws_imagem.py'],
        package_dir={'ws-imagem': ''},
        data_files=[
            ('resources', properties)
        ]
    )
