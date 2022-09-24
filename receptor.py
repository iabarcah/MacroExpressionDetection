import asyncio
import socketio
import time

sio1 = socketio.AsyncClient()
sio2 = socketio.AsyncClient()

@sio1.on('distribution', namespace='/video')
async def on_distribution(data):
    '''
    while(1):
        time.sleep(3)
        print("Mandando")
        await sio1.emit('distribution', 'Hola mundo', namespace="/video")'''
    print(data)
    await sio2.emit('report', data, namespace="/conected")



async def main():
    await sio1.connect('http://localhost:82', namespaces=["/video"])
    await sio2.connect('http://localhost:80', namespaces=["/conected"])
    await sio1.wait()
    await sio2.wait()

if __name__ == '__main__':
    asyncio.run(main())