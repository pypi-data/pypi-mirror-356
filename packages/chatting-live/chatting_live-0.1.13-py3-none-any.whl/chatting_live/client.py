import requests
import threading
import time
import random

SERVER = 'https://socket-l0vq.onrender.com'  # Change to your server address if needed


def get_menu():
    r = requests.get(SERVER + '/info')
    print(r.text)


def poll_messages(room, last_id, user):
    while True:
        try:
            r = requests.get(f"{SERVER}/messages", params={"room": room, "after": last_id[0]})
            if r.status_code == 200:
                messages = r.json()
                for msg in messages:
                    print(f"{msg.get('user', 'User')} : {msg.get('text', '')}")
                    last_id[0] = max(last_id[0], msg.get('id', 0))
            time.sleep(2)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(5)


def send_message(room, text):
    try:
        requests.post(f"{SERVER}/send", json={"room": room, "text": text})
    except Exception as e:
        print("Send error:", e)


def main():
    get_menu()
    username = f"User_{random.randint(1000,9999)}"
    print(f"Your username: {username}")

    while True:
        action = input("Enter option (1-4): ")
        if action == '1':
            # Join a random room (get list, pick one)
            rooms = requests.get(SERVER + '/rooms').json()
            if not rooms:
                print("No rooms available. Create one first.")
                continue
            room = random.choice(rooms)
            print(f"Joining room: {room}")
        elif action == '2':
            room = input("Enter new room name: ")
            resp = requests.post(SERVER + '/create', json={"room": room})
            if resp.status_code != 200:
                print(resp.json().get('error', 'Error creating room'))
                continue
            print(f"Room '{room}' created.")
        elif action == '3':
            room = input("Enter room name to join: ")
        elif action == '4':
            rooms = requests.get(SERVER + '/rooms').json()
            print("Rooms:", ', '.join(rooms))
            continue
        else:
            print("Invalid option")
            continue

        # Join the room
        join_resp = requests.post(SERVER + '/join', json={"room": room, "user": username})
        if join_resp.status_code != 200:
            print(join_resp.json().get('error', 'Error joining room'))
            continue
        print(f"Joined room: {room}")
        last_id = [0]
        t = threading.Thread(target=poll_messages, args=(room, last_id, username), daemon=True)
        t.start()
        while True:
            msg = input()
            if msg == '/menu':
                break
            send_resp = requests.post(f"{SERVER}/send", json={"room": room, "user": username, "text": msg})
            if send_resp.status_code != 200:
                print(send_resp.json().get('error', 'Error sending message'))


if __name__ == '__main__':
    main()
