#codigo armarlo primero para macro expresiones y para micro expresiones 
import logging
import json
from flask import Flask, request
from flask_socketio import SocketIO, Namespace
import datetime
from threading import Thread
from time import sleep

format = "%(asctime)s - %(process)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

async_mode = 'eventlet'
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode, logger=False, engineio_logger=False, max_http_buffer_size=1e8)

# config
data = json.load(open('config.json'))

# view
@app.route('/')
def index():
    return 'Hello, World!'

# server Socket
class video(Namespace):
    def on_connect(self):
        logging.info(f"Connect sid: {request.sid}")
    def on_report(self,data):
        socketio.emit('distribution', data, namespace='/conected')
    def on_disconnect(self):
        logging.info(f"Disconnect sid: {request.sid}")  

socketio.on_namespace(video("/video"))


class conected(Namespace):
    def on_connect(self):
        logging.info(f"Connect sid: {request.sid}")

    def on_report(self,data):
        socketio.emit('distribution', data, namespace='/granularMacroMetrics')
    
    def on_disconnect(self):
        logging.info(f"Disconnect sid: {request.sid}")  

socketio.on_namespace(conected("/conected"))



class granularMacroMetrics(Namespace):
    def on_connect(self):
        logging.info(f"Connect granularMacroMetrics sid: {request.sid}")

    def on_report(self,data):
        socketio.emit('distribution', data, namespace='/acumulatedMacroMetrics')

    def on_disconnect(self):
        logging.info(f"Disconnect granularMacroMetrics sid: {request.sid}")  

socketio.on_namespace(granularMacroMetrics("/granularMacroMetrics"))


class acumulatedMacroMetrics(Namespace):
    def on_connect(self):
        logging.info(f"Connect acumulatedMetrics sid: {request.sid}")

    def on_report(self,data):
        print("llego algo en acumulatedMacroMetrics")
        #socketio.emit('distribution', data, namespace='/audioTranscript')

    def on_disconnect(self):
        logging.info(f"Disconnect acumulatedMacroMetrics sid: {request.sid}")  

socketio.on_namespace(acumulatedMacroMetrics("/acumulatedMacroMetrics"))

# Lanzar servicio

if __name__ == '__main__':
    logging.info(f"Server start")
    socketio.run(app, debug=data["mode"], port=data["port"], host=data["host"], log_output=False)
