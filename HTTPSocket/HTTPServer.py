from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os
import time
import socket

# 全局變數儲存訊息
messages = []
JSON_FILE = "messages.json"  # 儲存訊息的檔案

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
            
            if "exit" in sentence:
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
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _sock.connect((database_ip, database_port))        
        for message in messages:
            sock.sendall(json.dumps(message).encode('utf-8'))
            # 如果需要確認，接收回應
            response = sock.recv(4096).decode('utf-8')
            print(f"Response from database: {response}")
        sock.close()
    except Exception as e:
        print(f"Error: {e}")

# 啟動伺服器
serverPort = 12000
server = HTTPServer(('0.0.0.0', serverPort), MyHandler)
# thread = threading.Thread(target=wait_stop_signal)
# thread.start()
print(f"Server started at http://localhost:{serverPort}")
# server.serve_forever()
while True:
    server.handle_request()
    if stop_signal:
        print("Server stopped")
        break
server.shutdown()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_ip, server_port))
backup_to_database()