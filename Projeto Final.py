from flask import Flask, jsonify
import base64
import pymongo
import os
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

    diretorio = "/volumes/streaming-file-server/images/producao/"

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

    try:

        arquivo = diretorio + codFornecedor + "/" + codProduto + ".JPG"
        print("Diretorio: {}".format(arquivo))

        img = Image.open(arquivo)

        new_img = img.resize((800, 600))

        new_img.save(diretorio + codFornecedor+"/newImg"+codProduto+".JPG")

    except FileNotFoundError:
        response["menssage"] = "Diretorio ou imagem nao encontrado"
        return jsonify(response)

    new_arquivo = "/volumes/streaming-file-server/images/producao/"+codFornecedor+"/newImg"+codProduto+".JPG"

    f = open(new_arquivo, 'rb')
    imgCompact = f.read()
    f.close()

    encodedImg = base64.b64encode(imgCompact)

    documento = {"CodFornecedor": codFornecedor, "CodProduto": codProduto, "ImgBase64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
    x = mycol.insert_one(documento)

    os.remove(new_arquivo)

    # html = '<img src="data:image/jpeg;base64,{}">'.format(encodedImg).replace("b'", "").replace("'", "")
    # se quisesse devolver uma tag HTML

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

    # mycol.delete_one({"CodFornecedor": "3178", "CodProduto": "311" })

    value = []

    for x in mycol.find({}, {"_id": 0, "CodFornecedor": 1, "CodProduto": 1, "ImgBase64": 1}):
        print(x)
        value.append(x)

    response = value

    return jsonify(response)

@app.route("/delete/<codFornecedor>/<codProduto>", methods=['GET'])
def delete(codFornecedor, codProduto):

    response = {}

    diretorio = "./img/"+codFornecedor+"/newImage/"+codProduto

    os.remove(diretorio)

    print("Exclui: {}".format(diretorio))

    response["menssage"] = "Imagem exlcuida com sucesso"

    return jsonify(response)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)