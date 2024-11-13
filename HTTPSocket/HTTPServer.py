from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        sentence = post_data.decode('utf-8')
        capitalized_sentence = sentence.upper()
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(capitalized_sentence.encode('utf-8'))

serverPort = 12000
server = HTTPServer(('localhost', serverPort), MyHandler)
print(f"Server started at http://localhost:{serverPort}")
server.serve_forever()