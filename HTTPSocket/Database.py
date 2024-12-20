import socket
import json
import os

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
        f.write(image_data)

def main_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as db_socket:
        db_socket.bind((database_ip, database_port))
        db_socket.listen(5)
        while True:
            conn, addr = db_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    # 接收文本消息
                    text_data = conn.recv(4096).decode('utf-8')
                    # 保存文本消息
                    save_text_to_json(text_data)
                    print(f"Received text: {text_data}")

                    # 檢查是否有圖片數據需要接收
                    if "Image Uploaded" in text_data:
                        # 提取圖片名稱
                        conn.sendall(b"Data received successfully")
                        start_index = text_data.find("uploaded_image_")
                        image_name = text_data[start_index:-1].split()[0]  # 獲取圖片名稱
                        image_name = f"{image_name}"  # 加上文件擴展名
                        # 接收圖片數據
                        image_data = b''
                        chunk = conn.recv(20000000)
                        image_data += chunk
                        # 確保圖片數據不為空
                        if image_data:
                            save_image_to_folder(image_data, image_name)
                            print(f"Received image: {image_name}")
                            conn.sendall(b"Data received successfully")
                        else:
                            print("No image data received.")
                        
                    
                    # 回應客戶端
                    if (text_data != "ENDOFDATA"):
                        conn.sendall(b"Data received successfully")
                        

if __name__ == "__main__":
    print("Database started")
    main_loop()