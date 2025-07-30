import requests
import websocket
import threading
import time
import json

SERVER = 'https://socket-l0vq.onrender.com'
WS_SERVER = 'wss://socket-l0vq.onrender.com/socket.io/?EIO=4&transport=websocket'

def get_menu():
    r = requests.get(SERVER + '/info')
    print(r.text)

def listen(ws):
    while True:
        try:
            msg = ws.recv()
            if msg:
                if msg.startswith('42'):
                    payload = json.loads(msg[2:])
                    event, data = payload
                    if event == 'message' or event == 'chat':
                        print(data)
                    elif event == 'joined':
                        print(f'Joined room: {data}')
                    elif event == 'rooms':
                        print('Rooms:', ', '.join(data))
        except Exception as e:
            break

def send_menu(ws, option, data=None):
    if data:
        ws.send(f'42["menu", {option}, "{data}"]')
    else:
        ws.send(f'42["menu", {option}]')

def send_chat(ws, msg):
    ws.send(f'42["chat", "{msg}"]')

def main():
    get_menu()
    ws = websocket.create_connection(WS_SERVER)
    ws.recv()
    ws.send('40')
    ws.recv()

    t = threading.Thread(target=listen, args=(ws,), daemon=True)
    t.start()

    while True:
        try:
            choice = input('Enter option (1-4): ')
            if choice == '1':
                send_menu(ws, 1)
            elif choice == '2':
                room = input('Enter new room name: ')
                send_menu(ws, 2, room)
            elif choice == '3':
                room = input('Enter room name to join: ')
                send_menu(ws, 3, room)
            elif choice == '4':
                send_menu(ws, 4)
            else:
                print('Invalid option')
                continue
            while True:
                msg = input()
                if msg == '/menu':
                    break
                send_chat(ws, msg)
        except KeyboardInterrupt:
            break
    ws.close()

if __name__ == '__main__':
    main()
