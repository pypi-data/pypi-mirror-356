import requests
import websocket
import threading
import time
import json
from queue import Queue

SERVER = 'https://socket-l0vq.onrender.com'
WS_SERVER = 'wss://socket-l0vq.onrender.com/socket.io/?EIO=4&transport=websocket'

message_queue = Queue()
ws_lock = threading.Lock()
global_ws = None
should_exit = False

def get_menu():
    r = requests.get(SERVER + '/info')
    print(r.text)

def listen():
    global global_ws, should_exit
    while not should_exit:
        ws = None
        try:
            with ws_lock:
                ws = global_ws
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
        except Exception:
            time.sleep(1)  # Wait before next recv attempt

def ws_manager():
    global global_ws, should_exit
    while not should_exit:
        try:
            ws = websocket.create_connection(WS_SERVER)
            ws.recv()
            ws.send('40')
            ws.recv()
            with ws_lock:
                global_ws = ws
            # Start listening thread for this ws
            t = threading.Thread(target=listen, daemon=True)
            t.start()
            # Wait until this ws is closed
            while not should_exit:
                if ws.sock and ws.sock.connected:
                    time.sleep(1)
                else:
                    break
        except Exception:
            time.sleep(2)
        finally:
            with ws_lock:
                if global_ws:
                    try:
                        global_ws.close()
                    except:
                        pass
                    global_ws = None
            time.sleep(2)

def send_menu(option, data=None):
    with ws_lock:
        ws = global_ws
        if ws and ws.sock and ws.sock.connected:
            if data:
                ws.send(f'42["menu", {option}, "{data}"]')
            else:
                ws.send(f'42["menu", {option}]')
        else:
            print("Not connected. Please wait...")

def send_chat(msg):
    with ws_lock:
        ws = global_ws
        if ws and ws.sock and ws.sock.connected:
            ws.send(f'42["chat", "{msg}"]')
        else:
            print("Not connected. Message not sent.")

def main():
    global should_exit
    get_menu()
    # Start websocket manager thread
    ws_thread = threading.Thread(target=ws_manager, daemon=True)
    ws_thread.start()
    try:
        while True:
            choice = input('Enter option (1-4): ')
            if choice == '1':
                send_menu(1)
            elif choice == '2':
                room = input('Enter new room name: ')
                send_menu(2, room)
            elif choice == '3':
                room = input('Enter room name to join: ')
                send_menu(3, room)
            elif choice == '4':
                send_menu(4)
            else:
                print('Invalid option')
                continue
            while True:
                msg = input()
                if msg == '/menu':
                    break
                send_chat(msg)
    except KeyboardInterrupt:
        should_exit = True
        print('Exiting...')
        with ws_lock:
            if global_ws:
                try:
                    global_ws.close()
                except:
                    pass

if __name__ == '__main__':
    main()
