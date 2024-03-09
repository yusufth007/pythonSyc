import asyncio
import pickle
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


async def receive_messages(reader):
    data = await reader.read(1024)
    global message
    message = pickle.loads(data)

    print(f'Received: {message!r}')


@app.route('/data')
def displaymessages():
    asyncio.new_event_loop().run_until_complete(tcp_client())
    print(message)
    return {
        'positions': {
            'x': message['positions']['x'],
            'y': message['positions']['y'],
            'z': message['positions']['z'],
        },
        'orientations': {
            'roll': message["orientations"]["roll"],
            'pitch': message["orientations"]["pitch"],
            'yaw': message["orientations"]["yaw"],
        },
        'thrusters': {
            'e1': message["thrusters"]["e1"],
            'e2': message["thrusters"]["e2"],
            'e3': message["thrusters"]["e3"],
            'e4': message["thrusters"]["e4"],
        }
    }

async def tcp_client():
    reader, writer = await asyncio.open_connection('25.58.205.100', 5000)

    await asyncio.create_task(receive_messages(reader))
    writer.close()
    await writer.wait_closed()



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=4001)