import socket
import json
import os
import base64

server_ip = '192.168.1.127'
server_port = 1274
database_ip = '192.168.1.178'
database_port = 1274

def save_text_to_json(text):
    JSON_FILE = "received_messages.json"
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            messages = json.load(file)
    else:
        messages = []

    messages.append(text)
    with open(JSON_FILE, 'w') as file:
        json.dump(messages, file)

def save_image_to_folder(image_data, image_name):
    os.makedirs("received_images", exist_ok=True)
    image_path = os.path.join("received_images", image_name)
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_data))

def main_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((database_ip, database_port))
        server_socket.listen(5)

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Received message: {message}")

                    try:
                        obj = json.loads(message)
                        if obj['type'] == 'text':
                            save_text_to_json(obj['message'])
                        elif obj['type'] == 'image':
                            save_image_to_folder(obj['image'], obj['image_name'])
                        conn.sendall("got message".encode())
                    except json.JSONDecodeError:
                        print("Invalid JSON received")
                        conn.sendall("Invalid JSON".encode())

if __name__ == "__main__":
    main_loop()