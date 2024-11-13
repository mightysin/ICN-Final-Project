import requests
import tkinter as tk
from tkinter import messagebox

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
window.title("Server Request GUI")
window.geometry("400x200")

# label, entry, button
label = tk.Label(window, text="Input lower case:")
label.pack(pady=5)

entry = tk.Entry(window, width=40)
entry.pack(pady=5)

send_button = tk.Button(window, text="Send to Server", command=send_request)
send_button.pack(pady=10)

result_label = tk.Label(window, text="From Server: ")
result_label.pack(pady=5)


window.mainloop()