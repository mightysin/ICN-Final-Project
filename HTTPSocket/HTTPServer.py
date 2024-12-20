from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os
import time
import socket

# 全局變數儲存訊息
messages = []
JSON_FILE = "messages.json"  # 儲存訊息的檔案


# Global variables
stop_signal = False
server_ip = '192.168.1.127'
server_port = 1274
database_ip = '192.168.1.178'
database_port = 1274



def save_message():
    """保存訊息到 JSON 文件"""
    with open(JSON_FILE, 'w') as file:
        file.write(json.dumps(messages))


def generate_image_url(image_path, server_host):
    """生成公開的圖片 URL"""
    if "ngrok" in server_host:
        return f"https://{server_host}/get_image/{os.path.basename(image_path)}"
    return f"http://{server_host}/get_image/{os.path.basename(image_path)}"


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global stop_signal
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

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(messages).encode('utf-8'))
                return

            # 處理文字訊息
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            sentence = post_data.decode('utf-8')
            print(f"Received: {sentence}")
            if sentence:
                messages.append(sentence)
                save_message()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode('utf-8'))
            
            if "STOPSERVER" in sentence:
                stop_signal = True

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
    
    def close_server(self):
        self.server.server_close()

def backup_to_database():
    """備份訊息到資料庫"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock: 
            s_sock.connect((database_ip, database_port))        
            for message in messages:
                s_sock.sendall(message.encode('utf-8')) # Send text object to database
                if "uploaded_image_" in message:
                    start_index = message.find("uploaded_image_") # Sendn image object to database
                    image_name = message[start_index:-1]
                    with open(os.path.join("uploads", f"{image_name}"), "rb") as f:
                        image_data = f.read()
                        s_sock.sendall(image_data)
                print(f"Response from database: {s_sock.recv(4096).decode('utf-8')}") # Print response from database
            s_sock.close()
    except Exception as e:
        print(f"Error: {e}")

# 啟動伺服器
serverPort = 12000
server = HTTPServer(('0.0.0.0', serverPort), MyHandler)

print(f"Server started at http://localhost:{serverPort}")
while True:
    server.handle_request()
    if stop_signal:
        print("Server stopped")
        break
server.server_close()

backup_to_database()