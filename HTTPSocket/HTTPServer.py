from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os
import time

# 全局變數儲存訊息
messages = []
JSON_FILE = "messages.json"  # 儲存文字訊息的檔案


def save_message():
    """保存訊息到 JSON 文件"""
    with open(JSON_FILE, 'w') as file:
        file.write(json.dumps(messages) + '\n')


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 處理影像上傳
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

                # 創建消息格式
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                image_message = f"{sender}({timestamp}) -> [Image Uploaded: {image_path}]"
                messages.append(image_message)
                save_message()

                # 回應完整的消息列表
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(messages).encode('utf-8'))
                return

            # 處理文字訊息
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            sentence = post_data.decode('utf-8')
            print(f"Received: {sentence}")
            if sentence != '':
                messages.append(sentence)
                save_message()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode('utf-8'))
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


serverPort = 12000
server = HTTPServer(('localhost', serverPort), MyHandler)
print(f"Server started at http://localhost:{serverPort}")
server.serve_forever()
