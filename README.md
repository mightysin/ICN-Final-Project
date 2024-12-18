# ICN-Final-Project

## Dependencies
* *pip install requests*
* *pip install pyinstaller*
* make sure to install them as administrator to add them to the environment automatically

## Excuting Steps (ngrok)
* Sign a ngrok account
* Install ngrok
> * "*choco install ngrok*"
> * "*ngrok config add-authtoken <your_token>*"
> * https://dashboard.ngrok.com/get-started/setup/windows to check your token if you're already logged
* Launch server "*python HTTPSocket/HTTPServer.py*"
* Use another terminal to launch ngrok "*ngrok http 12000*"
* Then you will see a url in console, copy it to *server_url=<your_url>, line 6, HTTPClient.py*
* The url is shown as "Forwarding  <*your_url*> -> http://localhost:12000"
* Use the third terminal, type "*pyinstaller --onefile --windowed HTTPSocket/HTTPClient.py*"
* The excutable file will be in *dist* directory
* Make sure the 1st(server) and 2nd(ngrok) terminal keep running
* Now you can execute "*HTTPClient.exe*" in any other device and network