from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import base64
import pymongo
import os
from PIL import Image

app = Flask(__name__)
wsgi_app = app.wsgi_app
CORS(app)

@app.route("/imageGroup", methods=['GET', 'POST'])
def groupImgMatriz():

    """
            Função para compacta, redimensionar a imagem, tranforma em base64 e salvar no banco de dados.

            Argumentos:
                Array:
                        {
                            "CodFornecedor" : "111111",
                            "CodProduto" : "222222"
                        }
            Retorna:
                json contendo um array com codFornecedor, codProduto e ImgBase64, imagem compactada em base64.
    """

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
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

    if(existe == len(request.json)):
        print("TODAS IMAGENS EXISTEM NO BANCO")
        return jsonify(response)

    elif (existe < len(request.json)):
        print("NOVA IMAGEM, COMPACTAR & TRASFORMA EM BASE64")
        try:

            arquivo = diretorio + x["CodFornecedor"] + "/" + x["CodProduto"] + ".JPG"

            basewidth = 400

            img = Image.open(arquivo)

            wpercent = (basewidth / float(img.size[0]))

            hsize = int((float(img.size[1]) * float(wpercent)))

            new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)

            new_img.save(diretorio + x["CodFornecedor"] + "/newImg" + x["CodProduto"] + ".JPG", optimize=True)

        except FileNotFoundError:

            print("UMA DAS IMAGEM NAO EXISTEM, DEVOLVER APENAS AS EXISTENTES")

            newResponse = []

            for i in request.json:
                myquery = {"CodFornecedor": "{}".format(i["CodFornecedor"]),
                           "CodProduto": "{}".format(i["CodProduto"])}
                mydoc = mycol.find(myquery, {'_id': 0})

                for resp in mydoc:
                    newResponse.append(resp)

            return jsonify(newResponse)

        new_arquivo = diretorio + x["CodFornecedor"] + "/newImg" + x["CodProduto"] + ".JPG"

        f = open(new_arquivo, 'rb')
        imgCompact = f.read()
        f.close()

        encodedImg = base64.b64encode(imgCompact)

        documento = {"CodFornecedor": x["CodFornecedor"], "CodProduto": x["CodProduto"],
                     "ImgBase64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
        x = mycol.insert_one(documento)

        os.remove(new_arquivo)

    newResponse = []

    for i in request.json:
        myquery = {"CodFornecedor": "{}".format(i["CodFornecedor"]),
                   "CodProduto": "{}".format(i["CodProduto"])}
        mydoc = mycol.find(myquery, {'_id': 0})

        for resp in mydoc:
            newResponse.append(resp)

    return jsonify(newResponse)

@app.route("/searchImg", methods=['GET'])
def listarMatriz():

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
    response["menssage"] = "sem registro"
    return jsonify(response)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)