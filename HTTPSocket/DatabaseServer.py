import socket
import json
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY, type TEXT, sender TEXT, timestamp TEXT, content TEXT)''')
conn.commit()

def handle_client(client_socket):
    try:
        data = client_socket.recv(4096).decode('utf-8')
        request = json.loads(data)

        if request['type'] == 'message':
            c.execute("INSERT INTO messages (type, content) VALUES (?, ?)", (request['type'], request['message']))
        elif request['type'] == 'image':
            c.execute("INSERT INTO messages (type, sender, timestamp, content) VALUES (?, ?, ?, ?)",
                      (request['type'], request['sender'], request['timestamp'], request['image_url']))
        conn.commit()

        # Send back all messages
        c.execute("SELECT * FROM messages")
        all_messages = c.fetchall()
        client_socket.sendall(json.dumps(all_messages).encode('utf-8'))
    except Exception as e:
        client_socket.sendall(f"Server error: {e}".encode('utf-8'))
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 13000))
    server.listen(5)
    print("Database server started at port 13000")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()