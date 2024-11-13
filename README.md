# ICN-Final-Project

## Dependencies
* *pip install requests*
* *pip install pyinstaller*
* make sure to install them as administrator to add them to the environment automatically

## Excuting Steps
* Terminal type "*HTTPSocket/HTTPServer.py*"
* Launch another terminal, type "*lt --port 12000*"
* You will see the second terminal shows a url
* Copy it to *server_url=<your_url>, line 6, HTTPClient.py*
* Launch the third terminal, type "*pyinstaller --onefile --windowed HTTPClient.py*"
* The excutable file will be in *dist* directory
* Make sure the 1st and 2nd terminal keep running
* Now you can excute "*HTTPClient.exe*" in any other device and network
* Sometimes you'll receive a bad gateway message, idk why