from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import base64
import pymongo
import os
from PIL import Image
import gzip

app = Flask(__name__)
wsgi_app = app.wsgi_app
CORS(app)

@app.route("/imageGroup", methods=['GET', 'POST'])
def groupImg():

    myclient = pymongo.MongoClient("mongodb://localhost:28017/")
    mydb = myclient["baseImages"]
    mycol = mydb["produtos"]

    diretorio = "/volumes/streaming-file-server/images/producao/"

    response = []
    exite = 0

    for x in request.json:
        myquery = {"CodFornecedor": "{}".format(x["CodFornecedor"]),
                   "CodProduto": "{}".format(x["CodProduto"])}
        mydoc = mycol.find(myquery, {'_id': 0})

        for resp in mydoc:
            response.append(resp)
            exite += 1

    if(exite == len(request.json)):
        print("TODAS IMAGENS EXISTEM NO BANCO")
        gzip.compress(response)
        return jsonify(response)

    elif (exite < len(request.json)):
        print("NOVA IMAGEM, COMPACTAR & TRASFORMA EM BASE64")
        try:

            arquivo = diretorio + x["CodFornecedor"] + "/" + x["CodProduto"] + ".JPG"

            basewidth = 400

            img = Image.open(arquivo)

            wpercent = (basewidth / float(img.size[0]))

            hsize = int((float(img.size[1]) * float(wpercent)))

            new_img = img.resize((basewidth,hsize), Image.ANTIALIAS)

            new_img.save(diretorio + x["CodFornecedor"] + "/newImg" + x["CodProduto"] + ".JPG", optimize=True)

        except FileNotFoundError:

            abort(404)

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

    gzip.compress(newResponse)

    return jsonify(newResponse)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)