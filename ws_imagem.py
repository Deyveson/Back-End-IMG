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

        print("CHEGOU AQUI")

        arquivo = diretorio + codFornecedor + "/" + codProduto + ".JPG"

        basewidth = 400

        img = Image.open(arquivo)

        wpercent = (basewidth / float(img.size[0]))

        hsize = int((float(img.size[1]) * float(wpercent)))

        new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)

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

    codFornecedor = request.args.get('codFornecedor')
    codProduto = request.args.get('codProduto')

    response = {}

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    value = []

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        value.append(x)
        response = value
        return jsonify(response)

    return abort(404)

@app.route("/listAll", methods=['GET'])
def listAll():

    response = {}

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    # mydb.mycol.remove()
    #
    # mydb.mycol.find()

    mycol.delete_one({"CodFornecedor": "653", "CodProduto": "JTS497"})
    # mycol.delete_one({"CodFornecedor": "767", "CodProduto": "ZL0365"})

    # value = []
    #
    # for x in mycol.find({}, {"_id": 0}):
    #     print(x)
    #     value.append(x)
    #
    # response = value

    return jsonify(response)

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