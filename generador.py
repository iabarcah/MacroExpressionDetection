import asyncio
from email.mime import image
import socketio
import time
import cv2
import numpy as np
import base64
sio1 = socketio.AsyncClient()
import matplotlib.pyplot as plt
import os

async def main():
    await sio1.connect('http://localhost:80', namespaces=["/video"])
   # await sio1.wait()
    face_cascade =  cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Opens the inbuilt camera of laptop to capture video.
    capture = cv2.VideoCapture('test_video.mp4')
    path='frames'

    cont = 0


    while (capture.isOpened()):
        ret, frame = capture.read()
        if (ret == True):
            #print('leyendo')
            cv2.imwrite('Frames/IMG_%04d.png' % cont, frame)    
            cont += 1
            if (cv2.waitKey(1) == ord('s')):
                print('break 1')
                break
        else:
            print('break2')
            break
            
    print('sali while')
    
    capture.release()
    cv2.destroyAllWindows()
    contenido = os.listdir('Frames/')
    imagen_bin= image.tobytes()
    imagen_string = base64.decodebytes(imagen_bin)
    
    while(1):
        time.sleep(3)
        print("Mandando")

        await sio1.emit('distribution', imagen_string, namespace="/video")

if __name__ == '__main__':
    asyncio.run(main())