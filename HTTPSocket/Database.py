import socket

server_ip = '192.168.0.127'
server_port = 8080
database_ip = '192.168.0.167'
database_port = 8080

def build_tcp_socket(ip, portNumber):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((ip, portNumber))
    return tcp_socket

def tcp_main_loop():
  """Continuously checks connection with the database and sends a message if disconnected."""
  connected = False
  while True:
    try:
      # Connect to the database
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server_socket:
        tcp_server_socket.connect((server_ip, server_port))
        connected = True
        print("Connected to server!")
        # Your existing code for sending data to the database can go here
        # ...
    except (ConnectionRefusedError, OSError) as e:
      if connected:
        print(f"Server connection lost: {e}")
        connected = False
    

db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
db_socket.bind((database_ip, database_port))
db_socket.listen(5)
tcp_main_loop()