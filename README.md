### Key Value Store


This project encapsulates the server side code for a simple key value store and a CLI client for basic operations of get, set and watch for the KV Store.


### Server setup


Requirements:

Python 2.7


Packages:

flask 1.0.3

pickledb 0.9.2


PS: The server was seen to not work in my instance of virtual environment in OSX. Further debugging of the issue will be soon added to this document.s


### CLI Tool


The CLI tool is run using by calling the client.py script with Python 2.7


##### Set value of key


python client.py set <key_name> <value>


##### Get value of key


python client.py get <key_name>


##### Watch key


python client.py watch <key_name>


### Configuration


The configuration files for both client and server are separated(in the same directory) from the code and can be used to configure accordingly.
