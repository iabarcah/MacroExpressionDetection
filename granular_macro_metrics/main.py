import socketio
import logging
import json
import requests
import asyncio
from datetime import datetime
from deepface import DeepFace
import base64


#cliente
sio = socketio.AsyncClient()
    

@sio.on('distribution', namespace='/granularMacroMetrics')
async def on_distribution(message):
    face_detection_list=list()
    face_demography_list=list()
    for i in message['device']['face_channel']:
        base64_img_bytes = i.encode('utf-8')
        face_detection = DeepFace.detectFace(img_path =  base64_img_bytes, target_size = (300, 300), detector_backend = 'retinaface',enforce_detection=False)
        face_detection_list.append(face_detection['dominant_emotion'])
#facial analysis
        demography = DeepFace.analyze(img_path = base64_img_bytes , detector_backend ='retinaface',enforce_detection=False)
        face_demography_list.append(demography)

    
    jeyson={
            'ontherecord':message["ontherecord"],
            'name':message["device"]["name"],
            'id_device': message["device"]["id_device"],
            'time':message["device"]["time"],
            'type':message["device"]["type"],
            'channels':message["device"]["channels"],
            'face_channel':{
                "face_detection":face_detection_list,
                "face_demography":face_demography_list
            },
            }
            
    
    

async def main():
    await sio.connect('http://localhost:80', namespaces=["/granularMacroMetrics"])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())