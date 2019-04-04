import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pymongo

app = Flask(__name__)
wsgi_app = app.wsgi_app
CORS(app)

@app.route("/findImagem", methods=['GET', 'POST'])
def groupImgFilial():

    """
            Função para consulta no banco de dados, de uma imagem especifica, se não achar ele faz uma requisição para o serviço da matriz.

            Argumentos:
                Array:
                        {
                            "CodFornecedor" : "111111",
                            "CodProduto" : "222222"
                        }
            Retorna:
                json contendo o codFornecedor, codProduto e ImgBase64.
    """

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImagesFilial"]
    mycol = mydb["produtos"]

    diretorio = "/volumes/streaming-file-server/images/producao/"

    response = []
    existe = 0

    for x in request.json:
        myquery = {"CodFornecedor": "{}".format(x["CodFornecedor"]),
                   "CodProduto": "{}".format(x["CodProduto"])}
        mydoc = mycol.find(myquery, {'_id': 0})

        for resp in mydoc:
            response.append(resp)
            existe += 1

    if (existe == len(request.json)):
        print("TODAS IMAGENS EXISTEM NO BANCO DA FILIAL")
        return jsonify(response)

    elif (existe < len(request.json)):
        print("FAAZENDO A REQUISIÇÃO PARA MATRIZ")

        url = "http://localhost:5555/imageGroup"

        resp = requests.post(url, data=None, json=request.json)

        for x in resp.json():
            mycol.insert_one(x)

        return jsonify(resp.json())


@app.route("/searchImg", methods=['GET'])
def listarFilial():

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
    mydb = myclient["baseImagesFilial"]
    mycol = mydb["produtos"]

    value = []

    myquery = {"CodFornecedor": "{}".format(codFornecedor), "CodProduto": "{}".format(codProduto)}
    mydoc = mycol.find(myquery, {'_id': 0})

    for x in mydoc:
        value.append(x)
        response = value
        return jsonify(response)
    response["menssage"] = "sem registro"
    return jsonify(response)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '7777'))
    except ValueError:
        PORT = 7777
    app.run(HOST, PORT)