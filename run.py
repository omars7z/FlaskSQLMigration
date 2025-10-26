from app import create_app
from asgiref.wsgi import WsgiToAsgi
import os

env = os.getenv("FLASK_ENV")

flask = create_app(env)
app = WsgiToAsgi(flask)
# app = create_app(env)

if __name__=='__main__':
    app.run(host='0.0.0.0')