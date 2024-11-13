from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class MassageForm:
    def __init__(self, username, time, content):
        self.username = username
        self.time = time
        self.content = content

messages = ['test massage1', 'test massage2', 'test massage3']

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Keep track of all the massages from client
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        sentence = post_data.decode('utf-8')
        messages.insert(sentence)
        
        # Send back all message to client
        for message in messages:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

serverPort = 12000
server = HTTPServer(('localhost', serverPort), MyHandler)
print(f"Server started at http://localhost:{serverPort}")
server.serve_forever()