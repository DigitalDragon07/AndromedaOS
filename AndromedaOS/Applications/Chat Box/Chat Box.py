from mqttclient import*

userSettings = getUserSettings()
storagePlace = getStoragePlace()

client = None
def onOpen():
    pass

def onClose():
    pass

def onMessageReceived(msg):
    print msg

def onStateChanged(state):
    print state

def enterRoom1():
    global client
    print "click"
    myTopic = "/chatBox/room/1"
    host = "broker.emqx.io"
    althost = "test.mosquitto.org"
    updateDomain("chatroom")
    client = GameClient(onStateChanged, onMessageReceived, myTopic)
    client.connect(althost)
    
def leaveRoom():
    global client
    client.disconnect()
    updateDomain("main")

appSetup = {
"name": "Chat Box",
"icon": "messageicon.png", 
"openingFunction": onOpen, 
"closingFunction": onClose, 
"domains": {
    "main": {
        "clickableUI": { 
            "button1":{ 
                "CenterPoint": [0, 0], 
                "Corner1":[], 
                "Corner2": [], 
                "linkedFunction": enterRoom1, 
                "file": text("Enter Room 1", 100, color = "Blue"), 
                "rescaling": 1}, 
            },
        "background": None, 
        },
    "chatroom": {
        "clickableUI": {
            "leaveButton":{ 
                "CenterPoint": [0, 0], 
                "Corner1":[], 
                "Corner2": [], 
                "linkedFunction": leaveRoom, 
                "file": text("Leave", 200, color = "Red"), 
                "rescaling": 1}, 
            },
        "background": None,
        }
    }
}