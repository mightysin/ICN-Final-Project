import requests
import tkinter as tk
from tkinter import messagebox

messagee = []

def send_request():
    server_url = "https://eleven-guests-spend.loca.lt"
    sentence = entry.get()
    try:
        response = requests.post(server_url, data = sentence)
        result_label.config(text = "From Server: " + response.text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", "Request failed: {e}")

# init tk window
window = tk.Tk()
window.title("Server Request GUI")
window.geometry("800x600")

# label, entry, button
label = tk.Label(window, text="Input lower case:")
label.pack(pady=5)

entry = tk.Entry(window, width=40)
entry.pack(pady=5)

send_button = tk.Button(window, text = "Send to Server", command = send_request)
send_button.pack(pady=10)

result_label = tk.Label(window, text="From Server: ")
result_label.pack(pady=5)

window.mainloop()