import requests
import tkinter as tk
import datetime
import time
import json
import random
import string
import base64
from tkinter import messagebox, filedialog, Text
from PIL import Image, ImageTk

messages = []
clientName = ''


def generate_client_name(length=5):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return 'client ' + random_string


def create_message():
    global clientName
    sentence = entry.get()
    date = datetime.date.today()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    message = f"{clientName}({date} {current_time}) -> {sentence}"
    send_request(message)
    entry.delete(0, tk.END)


def send_request(content):
    server_url = " https://7968-118-150-218-49.ngrok-free.app"  # 若使用 ngrok，替換為公開 URL
    try:
        response = requests.post(server_url, data=content, timeout=10)
        response.raise_for_status()
        unupdated_message = json.loads(response.text)
        for item in unupdated_message:
            if item not in messages:
                update_canvas(item)
                messages.append(item)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        print(f"Error: {e}")


def send_image(image_path):
    server_url = "https://7968-118-150-218-49.ngrok-free.app/upload_image"
    try:
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        payload = {"image": image_data, "sender": clientName}
        response = requests.post(server_url, json=payload, timeout=10)
        response.raise_for_status()
        unupdated_message = json.loads(response.text)
        for item in unupdated_message:
            if item not in messages:
                update_canvas(item)
                messages.append(item)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Image upload failed: {e}")




def display_image(image_url):
    try:
        response = requests.get(image_url, stream=True, timeout=10)  # 增加超時限制
        response.raise_for_status()
        img = Image.open(response.raw)
        img.thumbnail((300, 300))  # 縮放圖片
        photo = ImageTk.PhotoImage(img)

        # 插入圖片到 Text 控件
        message_list.config(state="normal")
        message_list.image_create(tk.END, image=photo)
        message_list.insert(tk.END, "\n")  # 插入換行
        message_list.config(state="disabled")
        message_list.see(tk.END)

        # 保存圖片引用，防止垃圾回收
        if not hasattr(message_list, "image_refs"):
            message_list.image_refs = []
        message_list.image_refs.append(photo)
    except requests.exceptions.RequestException as e:
        print(f"Error loading image: {e}")
        messagebox.showerror("Error", f"Unable to load image: {e}")
    except Exception as e:
        print(f"Error displaying image: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")


def update_canvas(message):
    message_list.config(state="normal")
    if "[Image Uploaded:" in message:
        # 提取圖片路徑
        image_path = message.split("[Image Uploaded: ")[1].strip("]")
        # 顯示圖片消息
        message_list.insert(tk.END, message.split(" -> ")[0] + " -> [Image]\n")
        display_image(image_path)
    else:
        # 顯示普通文字
        message_list.insert(tk.END, message + "\n")
    message_list.config(state="disabled")
    message_list.see(tk.END)

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        send_image(file_path)


def auto_update():
    send_request('')
    window.after(2000, auto_update)  # 每 2 秒更新一次訊息


# 初始化 Tkinter 視窗
window = tk.Tk()
window.title("Chat Room")
window.geometry("400x600")

# 訊息顯示區域
message_field = tk.Frame(window)
message_field.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
message_list = Text(message_field, wrap="word", state="disabled", height=25)
message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(message_field, orient="vertical", command=message_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_list.config(yscrollcommand=scrollbar.set)

# 輸入欄位與按鈕
input_panel = tk.Frame(window)
input_panel.pack(side=tk.BOTTOM, pady=10)

entry = tk.Entry(input_panel, width=25)
entry.pack(side=tk.LEFT, anchor='w', pady=10, padx=5)

send_button = tk.Button(input_panel, text="Send to Server", command=create_message)
send_button.pack(side=tk.LEFT, pady=10, padx=5)

upload_button = tk.Button(input_panel, text="Upload Image", command=upload_image)
upload_button.pack(side=tk.LEFT, pady=10, padx=5)

# 自動更新訊息
auto_update()
clientName = generate_client_name()
window.mainloop()
