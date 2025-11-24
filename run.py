from app import create_app
from asgiref.wsgi import WsgiToAsgi
import uvicorn

flask = create_app()
app = WsgiToAsgi(flask)

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)