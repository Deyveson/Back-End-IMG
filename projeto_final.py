from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import base64
import pymongo
import os
from PIL import Image

app = Flask(__name__)
wsgi_app = app.wsgi_app
CORS(app)

@app.route("/imagem", methods=['GET'])
@cross_origin()
def insert():
    """
            Função compacta a imagem, tranforma em base64 e salva no banco de dados.

            Argumentos:
                codFornecedor: string
                codProduto: string
            Retorna:
                json contendo o codFornecedor, codProduto e ImgBase64, imagem compactada em base64.
    """

    codFornecedor = request.args.get('codigoFornecedor')
    codProduto = request.args.get('codigo')
    response = {}
    value = []

    diretorio = "/volumes/streaming-file-server/images/producao/"

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        value.append(x)
        response = value
        return jsonify(response)

    try:

        arquivo = diretorio + codFornecedor + "/" + codProduto + ".JPG"

        img = Image.open(arquivo)

        new_img = img.resize((800, 600))

        new_img.save(diretorio + codFornecedor+"/newImg"+codProduto+".JPG")

    except FileNotFoundError:
        abort(404)

    new_arquivo = diretorio + codFornecedor + "/newImg" + codProduto+".JPG"

    f = open(new_arquivo, 'rb')
    imgCompact = f.read()
    f.close()

    encodedImg = base64.b64encode(imgCompact)

    documento = {"CodFornecedor": codFornecedor, "CodProduto": codProduto, "ImgBase64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
    x = mycol.insert_one(documento)

    os.remove(new_arquivo)

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        value.append(x)
        response = value

    return jsonify(response)

@app.route("/searchImg", methods=['GET'])
def listar():

    """
        Função para consulta no banco de dados, de uma imagem especifica.

        Argumentos:
            codFornecedor: string
            codProduto: string
        Retorna:
            json contendo o codFornecedor, codProduto e ImgBase64.
    """

    codFornecedor = request.args.get('codigoFornecedor')
    codProduto = request.args.get('codigo')

    response = {}

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    # mycol.delete_one({"CodFornecedor": "373", "CodProduto": "1752" })

    value = []

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        value.append(x)
        response = value
        return jsonify(response)

    return abort(404)

# @app.route("/listAll", methods=['GET'])
# def listAll():
#
#     response = {}
#
#     myclient = pymongo.MongoClient("mongodb://localhost:28017/")
#     mydb = myclient["baseImages"]
#     mycol = mydb["produtos"]
#
#     mycol.delete_one({"CodFornecedor": "292", "CodProduto": "BAH0094" })
#
#     # value = []
#     #
#     # for x in mycol.find({}, {"_id": 0, "CodFornecedor": 1, "CodProduto": 1, "ImgBase64": 1}):
#     #     print(x)
#     #     value.append(x)
#     #
#     # response = value
#
#     return jsonify(response)

@app.route("/imageGroup", methods=['GET', 'POST'])
def groupImg():

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    value = []

    for x in request.json:
        myquery = {"CodFornecedor": "{}".format(x["CodFornecedor"]),
                   "CodProduto": "{}".format(x["CodProduto"])}
        mydoc = mycol.find(myquery, {'_id': 0})
        for resp in mydoc:
            value.append(resp)

    return jsonify(value)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)