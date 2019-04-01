from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

app = Flask(__name__)
wsgi_app = app.wsgi_app
CORS(app)


@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    '''Exemplo com body application/json
    :argument
        recebendo um array
    '''

    print(request.json[1]['CodProduto'])

    print(request.json)

    return "SUCESSO"

    # req_data = request.get_json()
    #
    # codFornecedor = req_data['codFornecedor']
    # codProduto = req_data['codProduto']
    #
    # print(req_data)
    #
    # return '''
    #        Codigo Fornecedor: {}
    #        Codigo Produto: {}'''.format(codFornecedor, codProduto)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)