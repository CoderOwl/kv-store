from flask import Flask, Response, request
import json
import logging
import pickledb

# Get configurations as json
with open('config.json', 'r') as json_data_file:
    data = json.load(json_data_file)

# Flass app initiation
app = Flask(__name__)
service_port = data['service']['port']
appDebugMode = data['service']['debugMode']

# Database initiation
dbName = data['db']['name']
db = pickledb.load(dbName, False)

# Logging initiation
logging.basicConfig(level=logging.INFO)

# Messages as variables
msg_keyDoesntExist = "Key has not been initiated"
msg_keyAdded = "Key {} has been added to key value store"
msg_keyUpdated = "Value of key {} has been updated to {}"

# printList functionality
def printList(a):
    str = ""
    return str.join(s)

# Index page. No functionality
@app.route('/')
def index():
    return "Welcome to kv service "

# Get list of all keys
@app.route('/keys', methods=['GET'])
def getAllKeys():
    message = printList(db.getall())
    return Response(message, mimetype="text")

# Get value of a key with
@app.route('/getKey', methods=['GET'])
def getKey():
    key = request.args.get('key')
    logging.info("Returning key value for key {}".format(key))
    if(db.get(key)):
        message = db.get(key)
    else:
        message = msg_keyDoesntExist
    return Response(message, mimetype="text")

# Edit or add a key with mapping to value
@app.route('/setKey', methods=['GET'])
def addKey():
    key = request.args.get('key')
    value = request.args.get('value')
    db.set(str(key), value)
    logging.info("Keys has gotten updated")
    print key
    message = msg_keyAdded.format(key)
    return Response(message, mimetype="text")

# Watch key
@app.route('/watch', methods=['GET'])
def watch():
    key = request.args.get('key')
    def stream(key):
        keyValue = db.get(key)
        logging.info("Starting Generator")
        while True:
            newValue = db.get(str(key))
            if keyValue != newValue:
                keyValue = newValue
                msg_keyUpdated.format(key, keyValue)
                yield "data:{}\n\n".format(keyValue)
    # If key is not present, return a message instead of generator function
    if not db.get(key):
         return Response(msg_keyDoesntExist, mimetype="text")
    return Response(stream(key), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=appDebugMode, port=service_port)
