
def onOpen():
    pass

def onClose():
    pass

userSettings = getUserSettings()
storagePlace = getStoragePlace()

appSetup = {
"name": "Settings 123",
"icon": "Settings icon.png", 
"openingFunction": onOpen, 
"closingFunction": onClose,
"screenWidth": 1280,
"screenHeight": 800,
"domains": { 
    "main": { 
        "clickableUI": { 
            "button1":{ 
                "CenterPoint": [0, 0], 
                "Corner1":[],
                "Corner2": [], 
                "linkedFunction": None,
                "file": None, 
                "rescaling": 0.25},
            },
        "background": None,
        },
    }
}