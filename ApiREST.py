from flask import Flask
import base64

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route('/')
def main():
    """Lendo a imagem e transformando em Base64, devolvendo uma tag <img>"""

    arquivo = "./img//544/456.jpg"
    f = open(arquivo, 'rb')
    chunk = f.read()
    f.close()
    # Lendo o Arquivo no diretorio

    encodedImg = base64.b64encode(chunk)
    # transformando em Base64

    html = '<img src="data:image/jpeg;base64,{}">'.format(encodedImg).replace("b'", "").replace("'", "")
    # transformando em uma tag <img>, para rederizar na pagina

    return html

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '4444'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)