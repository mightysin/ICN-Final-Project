import requests
import tkinter as tk
import datetime
import time
from tkinter import messagebox

messageList = []
text_depth = 0

def create_message():
    global text_depth
    sentence = entry.get()
    date = datetime.date.today()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    message = 'client' + '(' + str(date) + ' ' + current_time + ')' + ' -> ' + sentence
    message_list.create_text(10, text_depth * 20, anchor='nw', text=message)
    text_depth += 1

def send_request():
    server_url = "https://f866-140-118-175-99.ngrok-free.app"
    sentence = entry.get()
    try:
        response = requests.post(server_url, data=sentence, timeout=10)
        response.raise_for_status()  # check if the request is successful
        result_label.config(text="From Server: " + response.text)
        print(f"Sent: {sentence}")
        print(f"Received: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        print(f"Error: {e}")

# init tk window
window = tk.Tk()
window.title("Chat Room")
window.geometry("400x600")

# set message field
message_field = tk.Frame(window)
message_field.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
message_list = tk.Canvas(message_field)
scrollbar = tk.Scrollbar(message_field, orient="vertical", command=message_list.yview)
message_list.configure(yscrollcommand=scrollbar.set)
message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# set entry, button
input_panel = tk.Frame(window)
input_panel.pack(side=tk.BOTTOM, pady=10)

entry = tk.Entry(input_panel, width=35)
entry.pack(side=tk.LEFT, anchor='w', pady=10, padx=10)

# 使用 lambda 來延遲調用 create_message
send_button = tk.Button(input_panel, text="Send to Server", command=create_message)
send_button.pack(side=tk.RIGHT, pady=10, padx=10)

window.mainloop()