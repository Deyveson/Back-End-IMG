from flask import Flask
from PIL import Image
import webbrowser
import base64

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route('/')
def main():
    """Lendo a imagem e transformando em Base64, devolvendo uma tag <img>"""

    arquivo = "./img/tech.jpg"

    f = open(arquivo, 'rb')
    chunk = f.read()
    f.close()

    encodedImg = base64.b64encode(chunk)
    f = open(arquivo.replace(".jpg", ".txt"), 'w')
    f.write(str(encodedImg))
    f.close()

    html = '<html><head></head><body>'
    html += '<img src="data:image/gif;base64,{}">'.format(encodedImg)
    html += '</body></html>'

    return html

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
