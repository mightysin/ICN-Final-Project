import socket

server_ip = '192.168.1.127'
server_port = 1274
database_ip = '192.168.1.178'
database_port = 1274

def main_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((database_ip, database_port))
        server_socket.listen(5)

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Received message: {message}")
                    conn.sendall("got message".encode())

if __name__ == "__main__":
    main_loop()