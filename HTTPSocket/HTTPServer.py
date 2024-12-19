from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os
import time
import socket
import threading

# 全局變數儲存訊息
messages = []
JSON_FILE = "messages.json"  # 儲存訊息的檔案

# variables
http_server_port = 12000
http_server_ip = '0.0.0.0'
server_ip = '192.168.1.127'
server_port = 1274
database_ip = '192.168.1.178'
database_port = 1274


# HTTP Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.path == "/upload_image":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                image_data = data.get("image")
                sender = data.get("sender")
                if not image_data or not sender:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"No image data or sender provided")
                    return

                # 儲存影像
                os.makedirs("uploads", exist_ok=True)
                image_path = os.path.join("uploads", f"uploaded_image_{int(time.time())}.png")
                with open(image_path, "wb") as f:
                    f.write(base64.b64decode(image_data))

                # 使用公開 URL
                server_host = self.headers['Host']
                image_url = generate_image_url(image_path, server_host)

                # 返回圖片訊息
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                image_message = f"{sender}({timestamp}) -> [Image Uploaded: {image_url}]"
                messages.append(image_message)
                save_message()

                # Send to database
                db_response = send_to_database({"type": "image", "sender": sender, "timestamp": timestamp, "image_url": image_url})

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(db_response).encode('utf-8'))
                return

            # 處理文字訊息
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            sentence = post_data.decode('utf-8')
            print(f"Received: {sentence}")
            if sentence:
                messages.append(sentence)
                save_message()

                # Send to database
                db_response = send_to_database({"type": "message", "message": sentence})

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(db_response).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {e}".encode('utf-8'))
            print(f"Error: {e}")

    def do_GET(self):
        try:
            if self.path.startswith("/get_image"):
                # 提取圖片名稱
                image_name = self.path.split("/")[-1]
                image_path = os.path.join("uploads", image_name)
                with open(image_path, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.end_headers()
                    self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Image not found")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {e}".encode('utf-8'))
            print(f"Error: {e}")


# HTTP Functions
# --------------------------------
# Set up HTTP server
def build_http_server(Myhandler):
    server = HTTPServer((http_server_ip, http_server_port), MyHandler)
    print(f"Server started at http://localhost:{http_server_port}")
    return server
# Save messages from HTTP connections
def save_message():
    """保存訊息到 JSON 文件"""
    with open(JSON_FILE, 'w') as file:
        file.write(json.dumps(messages))
# Save images from HTTP connections
def generate_image_url(image_path, server_host):
    """生成公開的圖片 URL"""
    if "ngrok" in server_host:
        return f"https://{server_host}/get_image/{os.path.basename(image_path)}"
    return f"http://{server_host}/get_image/{os.path.basename(image_path)}"


# TCP Functions
# --------------------------------
# TCP loop
def tcp_main_loop():
    # """Continuously checks connection with the database and sends a message if disconnected."""
    # connected = False
    # while True:
    #         try:
    #             # Connect to the database
    #             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as db_socket:
    #                 db_socket.connect((database_ip, database_port))
    #                 connected = True
    #                 print("Connected to database!")
    #         except (ConnectionRefusedError, OSError) as e:
    #             print(f"Database connection lost: {e}")
    #             if connected:
    #                 connected = False
    while True:
        send_to_database()
        time.sleep(0.5)
# Open another thread to maintain TCP communication
def start_tcp_threading():
    s_thread = threading.Thread(target=tcp_main_loop)
    s_thread.daemon = True
    s_thread.start()
# Send data through TCP to database
def send_to_database():
    """Send data to the database server via TCP socket"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as db_socket:
        db_socket.connect((database_ip, database_port))  # Assuming the database server is on the same machine
        db_socket.sendall('hello world'.encode('utf-8'))
        response = db_socket.recv(4096).decode('utf-8')
        print(response)
        #return json.loads(response)


# Program body
# --------------------------------
# Build up TCP socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((server_ip, server_port))
start_tcp_threading()


# Set HTTP Server and Handler
http_server = build_http_server(MyHandler)
http_server.serve_forever()