import socket

tcp_ip = '192.168.0.127'
tcp_socket_port = 8080
database_ip = '192.168.0.167'
database_port = 8080

def build_tcp_socket(ip, portNumber):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((ip, portNumber))
    return tcp_socket

socket = build_tcp_socket(database_ip, database_port)