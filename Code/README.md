# CPE400-Project
 Group - Brendan Aguiar, Nicholas Ang
# UDP-based reliable data transfer algorithm

# Running Instructions:
Start the server
* Open a terminal
* Type and run python3 server.py

Start the client
* Open a separate terminal to the server's terminal
* Type and run python3 client.py
* Input text file name
* Text file name example: apple.txt

Simulating timeout
* Uncomment time.sleep(1) in server.py
* Test with apple.txt for relatively short download time (~20 seconds)

Simulating packet loss
* To adjust rate of packet loss, change the x value in random.randInt(0, x) in server.py

