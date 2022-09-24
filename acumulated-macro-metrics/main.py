import socketio
import logging
import json
import requests
import asyncio
from datetime import datetime
import asyncio
import socketio
import deepface

#Realizar cambio de 

#cliente
sio = socketio.AsyncClient()
   
@sio.on('distribution', namespace='/acumulatedMacroMetrics')
async def on_distribution(message):
    #print("llego algo")
    Graph1=list()
    Graph2=list()
    Graph3=list()
    while(message['device']['ontherecord']==True):
        if(message['face_channel']['face_detection'] =='happy'or message['face_channel']['face_detection'] =='sad'):
            Graph1.append((message['device']['channel'],message['face_channel']['face_detection']))
        elif(message['face_channel']['face_detection'] =='surprise'or message['face_channel']['face_detection'] =='disgust'):
            Graph2.append((message['device']['channel'],message['face_channel']['face_detection']))  
        elif(message['face_channel']['face_detection'] =='angry'or message['face_channel']['face_detection'] =='fear'):
            Graph3.append((message['device']['channel'],message['face_channel']['face_detection']))     
    jeyson={
            'ontherecord':message["ontherecord"],
            'name':message["device"]["name"],
            'id_device': message["device"]["id_device"],
            'time':message["device"]["time"],
            'type':message["device"]["type"],
            'channels':message["device"]["channels"],
            'Graph1': Graph1,
            'Graph2': Graph2,
            'Graph3': Graph3,
            },
            
async def main():
    await sio.connect('http://localhost:80', namespaces=["/acumulatedMacroMetrics"])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

