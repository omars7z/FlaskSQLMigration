from app import create_app
from asgiref.wsgi import WsgiToAsgi


flask = create_app()
app = WsgiToAsgi(flask)

if __name__=='__main__':
    app.run(host='0.0.0.0')