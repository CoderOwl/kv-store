import sys
import json

# Get configurations as json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

serverAddress = data['server']['host']
serverPort = data['server']['port']
baseUrl = '{}:{}'.format(serverAddress, serverPort)

msg_commandNotFound = "Command not found"

def with_urllib3(url):
    """Get a streaming response for the given event feed using urllib3."""
    import urllib3
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False)

def getWatchUrl(baseUrl, key):
    watchUrl = 'http://{}/watch?key={}'.format(baseUrl,key)
    return watchUrl

def getGetUrl(baseUrl, key):
    getUrl ='http://{}/getKey?key={}'.format(baseUrl,key)
    return getUrl

def getSetUrl(baseUrl, key):
    setUrl ='http://{}/setKey?key={}&value={}'.format(baseUrl,key,value)
    return setUrl

def getKey(key):
    url = getGetUrl(baseUrl,key)
    response = with_urllib3(url)
    print response.read()

def setKey(key, value):
    url = getSetUrl(baseUrl,key)
    response = with_urllib3(url)
    print response.read()

def watchKey(key):
    url = getWatchUrl(baseUrl,key)
    response = with_urllib3(url)
    for event in response:
        print event

command = sys.argv[1]
if(command == 'get'):
    key = sys.argv[2]
    getKey(key)
elif(command == 'set'):
    key = sys.argv[2]
    value = sys.argv[3]
    setKey(key, value)
elif(command == 'watch'):
    key = sys.argv[2]
    watchKey(key)
else:
    print msg_commandNotFound
