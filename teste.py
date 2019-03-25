from flask import Flask
from flask import request
import base64
from pymongo import MongoClient
import json
from bson.json_util import dumps

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route('/')
def main():
    """Lendo a imagem e transformando em Base64, devolvendo uma tag <img>"""

    arquivo = "./img/pmz.png"
    f = open(arquivo, 'rb')
    chunk = f.read()
    f.close()
    # Lendo o Arquivo no diretorio

    encodedImg = base64.b64encode(chunk)
    # transformando em Base64

    html = '<img src="data:image/png;base64,{}">'.format(encodedImg).replace("b'", "").replace("'", "")
    # transformando em uma tag <img>, para rederizar na pagina

    return html


client = MongoClient('localhost:27017')
db = client.ContactDB

@app.route("/add_contact/", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        user_img = data['img']
        if user_name and user_contact:
            status = db.Contacts.insert_one({
                "name": user_name,
                "contact": user_contact,
                "img": user_img
            })
        return dumps({'message': 'SUCCESS'})
    except ValueError:
        return dumps({'erro: ': str(ValueError)})

@app.route("/get_all_contact", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.Contacts.find()
        return dumps(contacts)
    except ValueError:
        return dumps({'error: ': str(ValueError)})

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

