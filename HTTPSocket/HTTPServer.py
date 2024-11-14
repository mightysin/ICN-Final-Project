from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

messages = []
JSON_FILE = "messages.json" # store messages from clinent
def save_massage(massage):
        with open(JSON_FILE, 'w') as file:
            file.write(json.dumps(messages))

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # recieve message from client
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            sentence = post_data.decode('utf-8')
            print(f"Received: {sentence}")
            messages.append(sentence)
            # write message into json file
            save_massage(sentence)
            # send json file as response
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(JSON_FILE.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Server error: {e}".encode('utf-8'))
            print(f"Error: {e}")

serverPort = 12000
server = HTTPServer(('localhost', serverPort), MyHandler)
print(f"Server started at http://localhost:{serverPort}")
server.serve_forever()