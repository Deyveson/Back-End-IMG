from flask import Flask, jsonify
import base64
import pymongo
from PIL import Image

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route("/<codFornecedor>/<codProduto>", methods=['GET'])
def insert(codFornecedor, codProduto):

    """
        Função compacta a imagem, tranforma em base64 e salva no banco de dados.

        Argumentos:
            codFornecedor: string
            codProduto: string
        Retorna:
            json contendo o codFornecedor, codProduto e ImgBase64, imagem compactada em base64.
    """

    response = {}
    value = []

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        print(x)
        value.append(x)
        response = value
        return jsonify(response)

    arquivo = "./img/"+codFornecedor+"/"+codProduto+".jpg"

    img = Image.open(arquivo)
    new_img = img.resize((300, 256))
    new_img.save("./img/"+codFornecedor+"/newImage/"+codProduto, 'jpeg')

    new_arquivo = "./img/"+codFornecedor+"/newImage/"+codProduto

    f = open(new_arquivo, 'rb')
    imgCompact = f.read()
    f.close()

    encodedImg = base64.b64encode(imgCompact)

    documento = {"CodFornecedor": codFornecedor, "CodProduto": codProduto, "ImgBase64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
    x = mycol.insert_one(documento)

    # html = '<img src="data:image/jpeg;base64,{}">'.format(encodedImg).replace("b'", "").replace("'", "")

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        print(x)
        value.append(x)
        response = value

    return jsonify(response)

@app.route("/list", methods=['GET'])
def listar():

    response = {}

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    # mycol.delete_one({"CodFornecedor": "544", "CodProduto": "456" })

    value = []

    for x in mycol.find({}, {"_id": 0, "CodFornecedor": 1, "CodProduto": 1, "ImgBase64": 1}):
        print(x)
        value.append(x)

    response = value

    return jsonify(response)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)