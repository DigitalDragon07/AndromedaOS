#Licensed under AndromedaOS LTD. For private use only. Piracy will be punished. See License for further information.

#Imports of libraries
from gturtle import*
from javax.imageio import ImageIO
from java.io import File
from java.awt import Toolkit
from java.lang import*
from time import*
import os
import math
import gc
import copy

#necessary data (think about repositioning this section so no interference with the function which are stored in a variable occur)
userSettings = {
"screenWidth": 1280,
"screenHeight": 800,
"verticalSpace": 70,
"horizontalSpace": 70,
"maxVerticalSpaceBetweenApps": 100,
"maxHorizontalSpaceBetweenApps": 150,
"isUsingDefaultBackground": True,
"currentBackgroundPath": "/Custom_UI/Backgrounds/",
"darkMode": False,
"playIntro": True,
"doGC": True,
"new": False,
}

storagePlace = os.getcwd().replace("\\", "/")

confidentialInformation = {
    "appsOnHomescreen": [],
    "appsAvailable": [],
    "appNames": [], #Folder name
    "appNamesWithFolder": [], #Format: folderName/scriptName.py
    "downloadedAppData": {}, #Folder name
    "defaultApps": ["AppLoader", "Settings"], #Always the folder name
    "currentApp": "Homescreen", #Folder name, uses appNames
}

sharedDict = {}

#custom error class

class AndromedaOSError(globals()["__builtins__"]["Exception"]):
    def __init__(self, *msg):
        newMsg = " ".join(msg)
        newMsg += "\n---------------------------------------"
        globals()["__builtins__"]["Exception"].__init__(self, newMsg)

#Functions with which AndromedaOS runs
def makeBackground():
    if (userSettings["isUsingDefaultBackground"]):
       background = storagePlace + "/Default_UI/Background_1.png"
    else:
        background = storagePlace + userSettings["currentBackgroundPath"]
    background = getImage(background)
    background = scale(background, autoRescale(1280, 800), 0)
    drawImage(background, 0, 0)
    del background
    
def loadUI():
    for l in clickableUI.values():
        if l["file"] != None:
            t1 = clock()
            if type(l["file"]) == str:
                image = l["file"]
                if l["file"].startswith("C") and l["rescaling"] == None:
                    drawImage(l["file"], l["CenterPoint"][0], l["CenterPoint"][1])
                elif l["rescaling"] == None and (not l["file"].startswith("C")):
                    drawImage(image, l["CenterPoint"][0], l["CenterPoint"][1])
                elif l["rescaling"] != None and l["file"].startswith("C"):
                    rescale = rescaleImageWithFactor(l["file"], l["rescaling"])
                    if rescale == None:
                        resclale = 1
                    drawImage(rescale, l["CenterPoint"][0], l["CenterPoint"][1])
                elif l["rescaling"] != None and (not l["file"].startswith("C")):
                    rescale = rescaleImageWithFactor(image, l["rescaling"])
                    if rescale == None:
                        resclale = 1
                    drawImage(rescale, l["CenterPoint"][0], l["CenterPoint"][1])
                else:
                    raise AndromedaOSError("Error in loadUI: Missing Components. Logging important components below:\n", "rescaling:", l["rescaling"], "(Note: Rescale can be None)\n", "file:", l["file"])
                #print "loaded image was", image
                del image
                t2 = clock()
                #print "time for loading UI is", t2-t1
            if type(l["file"]) == list:
                setPenColor(l["file"][4])
                setPos(l["CenterPoint"][0], l["CenterPoint"][1])
                style = l["file"][2]
                rescale = l["rescaling"]
                maxTextLength = l["file"][6]
                maxLineBreak = l["file"][5]
                if rescale == None:
                    rescale = 1
                size = l["file"][3]*rescale
                size = int(round(size))
                if style == "plain" or style == "Plain":     
                    setFont(l["file"][1], Font.PLAIN, size)
                elif style == "bold" or style == "Bold":
                    setFont(l["file"][1], Font.BOLD, size)
                elif style == "italic" or style == "Italic":
                    setFont(l["file"][1], Font.ITALIC, size)
                else:
                    raise Exception("Error in text: Not a valid style")
                if not maxTextLength == None:
                    amountOfLineBreak = 0
                    words = l["file"][0].split(" ")
                    tempList = []
                    actualList = []
                    usedSpaceInTempList = 0
                    for x in words:
                        if getTextWidth(x) > maxTextLength:
                            raise Exception("Error in loadUI: Word was longer then maxTextLength")
                        if maxTextLength < (usedSpaceInTempList + getTextWidth(x)):
                            actualList.append(tempList)
                            tempList = []
                            usedSpaceInTempList = 0
                            amountOfLineBreak += 1
                            if amountOfLineBreak > maxLineBreak:
                                raise Exception("Error in loadUI: exceeded line break limit")
                        tempList.append(x)
                        usedSpaceInTempList += getTextWidth(x)
                    actualList.append(tempList)
                    i = 1
                    for x in actualList:
                        for f in x:
                            label(f + " ")
                            setPos(getX() + getTextWidth(f + " "), getY())
                        setPos(l["CenterPoint"][0], l["CenterPoint"][1]-getTextHeight()*i)
                        i += 1
                else:
                    label(l["file"][0])
    if userSettings["doGC"]:
        gc.collect()
        Runtime.getRuntime().gc()
            
def loadHomescreen():
    t1 = clock()
    makeBackground()
    t2 = clock()
    loadAvailableApps()
    t3 = clock()
    addAppsToHomescreen() 
    t4 = clock()
    #print t2-t1, t3-t2, t4-t3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    
def onMousePressed(x, y):
    global clickableUI
    global userSettings
    for l in clickableUI.values():
        if ("Corner1" in l) and ("Corner2" in l):
            if l["Corner1"] != [] and l["Corner2"] != []:
                maxx = max(l["Corner1"][0], l["Corner2"][0])
                minx = min(l["Corner1"][0], l["Corner2"][0])
                maxy = max(l["Corner1"][1], l["Corner2"][1])
                miny = min(l["Corner1"][1], l["Corner2"][1])
                if x < maxx and x > minx and y < maxy and y > miny:
                    if (l["linkedFunction"] != None):
                        func = l["linkedFunction"]
                        if "appName" in l:
                            openApp(l["appName"])
                        func()
                        break
            
def onMouseMoved(x, y):
    pass  
            
def getPictureSize(image_file): #Add security check that file exists!
    img_file = File(image_file)
    image = ImageIO.read(img_file)
    width = image.getWidth()
    height = image.getHeight()
    del img_file
    del image
    return [width, height]

def rescaleImageWithSize(image_file, newSize, hasToBeSquare = False, preferedSide = "x"):
    pictureSize = getPictureSize(image_file)
    if (hasToBeSquare and (pictureSize[0] != pictureSize[1])):
        raise AndromedaOSError("Error in rescaleImage: Picture was not a square")
        return
    if (preferedSide == "x"):
        factor = newSize/pictureSize[0]
    else:
        factor = newSize/pictureSize[1]
    newImageFile = getImage(image_file)
    newImage = scale(newImageFile, factor, 0)
    del newImageFile
    del pictureSize
    return [newImage, factor]

def rescaleImageWithFactor(image_file, newSizeAsFactor, hasToBeSquare = False):
    pictureSize = getPictureSize(image_file)
    if (hasToBeSquare and (pictureSize[0] != pictureSize[1])):
        raise AndromedaOSError("Error in rescaleImage: Picture was not a square")
        return
    newImageFile = getImage(image_file)
    newImage = scale(newImageFile, newSizeAsFactor, 0)
    return newImage

def autoRescale(currentScreenWidth, currentScreenHight, currentFactor = 1, prefferWidth = True):
    newScreenWidth = int(userSettings["screenWidth"])
    newScreenHeight = int(userSettings["screenHeight"])
    if prefferWidth:
        factor = newScreenWidth/currentScreenWidth
    else:
        factor = newScreenHeight/currentScreenHight
    return factor*currentFactor

def testScript():
    print "hi"
    
def addUICorners():
    global clickabelUI
    for x in clickableUI.values():
        if x["file"] != None:
            if type(x["file"]) ==  str:
                pictureSize = getPictureSize(x["file"])
                x["Corner1"] = [x["CenterPoint"][0]-(pictureSize[0]/2)*x["rescaling"], x["CenterPoint"][1]-(pictureSize[0]/2)*x["rescaling"]]
                x["Corner2"] = [x["CenterPoint"][0]+(pictureSize[1]/2)*x["rescaling"], x["CenterPoint"][1]+(pictureSize[1]/2)*x["rescaling"]]
            elif type(x["file"]) == list:
                x["Corner1"] = [x["CenterPoint"][0], x["CenterPoint"][1]-x["file"][7]*getTextHeight()]
                if x["file"][7] == 0:
                    x["Corner2"] = [getTextWidth(x["file"][0]) + x["CenterPoint"][0], getTextHeight()  + x["CenterPoint"][1]]
                else:
                    x["Corner2"] = [x["file"][6] + x["CenterPoint"][0], getTextHeight()  + x["CenterPoint"][1]]
            
def test():
    print "Test successful"

def calculateAppDistance():
    global homescreenUI
    global clickableUI
    global confidentialInformation
    global userSettings
    verticalDistance = 100000
    horizontalDistance = 100000
    verticalApps = 0
    horizontalApps = 0
    width = userSettings["screenWidth"]
    height = userSettings["screenHeight"]
#    t1 = clock()
    while verticalDistance > userSettings["maxVerticalSpaceBetweenApps"]:
        verticalApps += 1
        check = height - 2*userSettings["verticalSpace"]
        verticalDistance = check // verticalApps
    while horizontalDistance > userSettings["maxHorizontalSpaceBetweenApps"]:
        horizontalApps += 1
        check = width - 2*userSettings["horizontalSpace"]
        horizontalDistance = check // horizontalApps
#    t2 = clock()
    storeData("verticalApps", verticalApps, "appDistance")
    storeData("verticalDistance", verticalDistance, "appDistance")
    storeData("horizontalApps", horizontalApps, "appDistance")
    storeData("horizontalDistance", horizontalDistance, "appDistance")
    
def addAppsToHomescreen():
    global homescreenUI
    global clickableUI
    global confidentialInformation
    global userSettings
    width = userSettings["screenWidth"]
    height = userSettings["screenHeight"]
    centerpointY = height/2 - userSettings["verticalSpace"]
    centerpointX = 0 - (width/2 - userSettings["horizontalSpace"])
    counter = 1
    homescreenUI = {}
    verticalApps = eval(getData("verticalApps", "appDistance"))
    verticalDistance = eval(getData("verticalDistance", "appDistance"))
    horizontalApps = eval(getData("horizontalApps", "appDistance"))
    horizontalDistance = eval(getData("horizontalDistance", "appDistance"))
    for app in confidentialInformation["appNamesWithFolder"]:
        folder = str(app.split("/").pop(0))
        theFile = str(storagePlace + "/Applications/" + folder + "/" + confidentialInformation["downloadedAppData"][confidentialInformation["appNames"][counter-1]]["icon"])
        homescreenUI[app] = {
            "CenterPoint": [centerpointX, centerpointY],
            "Corner1":[],
            "Corner2": [],
            "linkedFunction": confidentialInformation["downloadedAppData"][confidentialInformation["appNames"][counter-1]]["openingFunction"],
            "file": theFile,
            "rescaling": autoRescale(1280, 800, rescaleImageWithSize(theFile, 300/4)[1]),
            "appName": confidentialInformation["appNames"][counter-1],}
        centerpointY -= verticalDistance
        if (counter >= (verticalApps*horizontalApps)):
            raise AndromedaOSError("Error in addAppsToHomescreen: Had to load more apps than space available")
            break
        if (counter % verticalApps) == 0:
            centerpointY = height/2 - userSettings["verticalSpace"]
            centerpointX += horizontalDistance
        counter += 1
    clickableUI = homescreenUI
#    t3 = clock()
    addUICorners()
#    t4 = clock()
    loadUI()
#    t5 = clock()
    #print "inside:", round(t2-t1, 2), t3-t2, t4-t3, t5-t4
    del verticalApps
    del verticalDistance
    del horizontalApps
    del horizontalDistance
    
def closeApp():
    global confidentialInformation
    if confidentialInformation["downloadedAppData"][confidentialInformation["currentApp"]]["closingFunction"] != None:
        confidentialInformation["downloadedAppData"][confidentialInformation["currentApp"]]["closingFunction"]()
    confidentialInformation["currentApp"] = "Homescreen"
    loadHomescreen()
    
def openApp(appName):
    global clickableUI
    global storagePlace
    global confidentialInformation
    #sleep(0.15)
    clear()
    if type(confidentialInformation["downloadedAppData"][appName]["domains"]["main"]["background"]) == str:
        background = storagePlace + confidentialInformation["downloadedAppData"][appName]["domains"]["main"]["background"]
        drawImage(background)
    else:
        setPenColor("White")
        dot(10000)
    clickableUI = confidentialInformation["downloadedAppData"][appName]["domains"]["main"]["clickableUI"]
    for l in neededUI:
        clickableUI[l] = neededUI[l]
    confidentialInformation["currentApp"] = appName
    addUICorners()
    loadUI()
    
def updateDomain(newDomain, callingFunction = None):
    global clickableUI
    global storagePlace
    if newDomain in confidentialInformation["downloadedAppData"][confidentialInformation["currentApp"]]["domains"]:
        clickableUI = confidentialInformation["downloadedAppData"][confidentialInformation["currentApp"]]["domains"][newDomain]["clickableUI"]
        for l in neededUI:
            clickableUI[l] = neededUI[l]
        if type(confidentialInformation["downloadedAppData"][confidentialInformation["currentApp"]]["domains"][newDomain]["background"]) == str:
            background = storagePlace + confidentialInformation["downloadedAppData"][currentidentialInformation["currentApp"]]["domains"][newDomain]["background"]
            drawImage(background)
        else:
            setPenColor("White")
            dot(10000)
        loadUI()
        addUICorners()
    else:
        raise AndromedaOSError("Error in updateDomain: domain doesn't exist")
        return
    if callingFunction != None:
        if type(callingFunction) == list:
            for x in callingFunction:
                x()
        else:
            callingFunction()

def loadAvailableApps():
    global confidentialInformation
    tempList = []
    confidentialInformation["appsAvailable"] = []
    App_file = File(storagePlace + "/Applications" ).list()
    for folder in App_file:
        App_file2 = File(storagePlace + "/Applications/" + folder).list()
        defaultApp = False
        if folder in confidentialInformation["defaultApps"]:
            defaultApp = True
        for app in App_file2:
            if (app.endswith(".py")):
                path = folder + "/" + app
                tempList.append(path)
                appWithoutPy = app.replace(".py", "")
                if defaultApp and not (folder in confidentialInformation["downloadedAppData"]):
                    x = (folder in confidentialInformation["downloadedAppData"])
                    downloadApp(path, True)
                break
    confidentialInformation["appsAvailable"] = tempList
    del App_file
    return tempList

def getDownloadedApps():
    return confidentialInformation["appNamesWithFolder"]

def getStoragePlace():
    return storagePlace

def getUserSettings():
    return copy.deepcopy(userSettings)
    
def downloadApp(appName, noPermissionNeeded = False, additionalData = {}):
    global sharedDict
    global confidentialInformation
    global storagePlace
    global sharedDict
    usedDict = sharedDict.copy()
    if noPermissionNeeded or confirmDownload():
        folderName = appName.split("/")[0]
        if folderName in confidentialInformation["defaultApps"]:
            for l in additionalSharedDict:
                usedDict[l] = additionalSharedDict[l]
        execfile(storagePlace + "/Applications/" + appName, usedDict)#if nameError: storagePlace not defined appears, look that the shared dict is defined before
        appSetup = usedDict["appSetup"]
        for l in additionalData:
            appSetup[l] = additionalData[l]
        confidentialInformation["downloadedAppData"][folderName] = appSetup
        confidentialInformation["appNames"].append(folderName)
        confidentialInformation["appNamesWithFolder"].append(appName)
        appSetup = {}
        del usedDict
        if confidentialInformation["currentApp"] == "Homescreen":
            addAppsToHomescreen()
        return True
    else:
        return False

def confirmDownload():
    installApplication = askYesNo("                                                                    Warning!\nApps which are added additionally could contain malicious code.\nOnly proceed if you trust the developer of this app. If your not sure please contact Oclona Studios. Du you want to install this application?", False)
    if installApplication == None:
        installApplication = False
    return installApplication

def initialiseOS():
    try:
        os.mkdir(storagePlace + "/Data")
        os.mkdir(storagePlace + "/Custom_UI")
        os.mkdir(storagePlace + "/Custom_UI/Backgrounds")
    except:
        raise AndromedaOSError("Error in initialiseOS: Folders already exist")
    userSettings["screenWidth"] = int(getScreenSize()[0]/3*2)
    userSettings["screenHeight"] = int(getScreenSize()[1]/3*2)
    calculateAppDistance()
    userSettings["new"] = False

def validateApp(appName):
    pass

def updateAppSetup(newAppSetup):
    currentApp = confidentialInformation["currentApp"]
    confidentialInformation["downloadedAppData"][currentApp] = newAppSetup

def storeData(nameOfData, data, additionalFolderPath = ""): #, storeInSystem = False
    currentApp = confidentialInformation["currentApp"]
    if currentApp == "Homescreen":# or storeInSystem:
        currentApp = "System"
    if not os.path.exists(storagePlace + "/Data/" + currentApp):
        os.mkdir(storagePlace + "/Data/" + currentApp)
    alreadyMadePath = "/"
    for l in additionalFolderPath.split("/"):
        if not os.path.exists(storagePlace + "/Data/" + currentApp + alreadyMadePath + l):
            os.mkdir(storagePlace + "/Data/" + currentApp + alreadyMadePath + l)
        alreadyMadePath += l + "/"
    with open(storagePlace + "/Data/" + currentApp + "/" + alreadyMadePath + nameOfData, "w+") as f:
        f.write(str(data))
    
def getData(nameOfData, additionalFolderPath = ""):
    currentApp = confidentialInformation["currentApp"]
    if currentApp == "Homescreen":
        currentApp = "System"
    if additionalFolderPath != "":
        additionalFolderPath += "/"
    if os.path.exists(storagePlace + "/Data/" + currentApp + "/" + additionalFolderPath + nameOfData):
        with open(storagePlace + "/Data/" + currentApp + "/" + additionalFolderPath + nameOfData, "r") as f:
            return f.read()
    else:
        raise AndromedaOSError("Error in getData: file doesn't exist.\n", "Searched place for getData:", storagePlace + "/Data/" + currentApp + "/" + nameOfData)
        
def text(text, size, **settings):
    #available settings: font, style, color, maxLineBreak, maxTextLength
    if "color" in settings:
        color = settings["color"]
    else:
        color = "Black"
    if "font" in settings:
        font = settings["font"]
    else:
        font = "Calibri"
    if "style" in settings:
        style = settings["style"]
    else:
        style = "plain"
    if "maxLineBreak" in settings:
        maxLineBreak = settings["maxLineBreak"]
    else:
        maxLineBreak = 100000
    if "maxTextLength" in settings:
        maxTextLength = settings["maxTextLength"]
    else:
        maxTextLength = None
    if maxTextLength != None:
        neededBreaks = getTextWidth(text)//maxTextLength
    else:
        neededBreaks = 0
    return [text, font, style, size, color, maxLineBreak, maxTextLength, neededBreaks]

#Starting procedure
gc.collect()
Runtime.getRuntime().gc()
setPlaygroundSize(userSettings["screenWidth"], userSettings["screenHeight"])
makeTurtle(mousePressed = onMousePressed, mouseMoved = onMouseMoved)
setPenColor("White")
sharedDict = {"test": test, "getStoragePlace": getStoragePlace, "updateDomain": updateDomain, "updateAppSetup": updateAppSetup, "autoRescale": autoRescale, "rescaleImageWithSize": rescaleImageWithSize, "rescaleImageWithFactor": rescaleImageWithFactor, "storeData": storeData, "getData": getData, "text": text, "getUserSettings": getUserSettings}
additionalSharedDict = {"downloadApp": downloadApp, "loadAvailableApps": loadAvailableApps, "getDownloadedApps": getDownloadedApps}

neededUI = {
"ExitSign":{
    "CenterPoint": [userSettings["screenWidth"]/2-autoRescale(1280, 800, 0.03)*getPictureSize(storagePlace + "/Default_UI/Buttons/red-x.png")[0]/2, userSettings["screenHeight"]/2-autoRescale(1280, 800, 0.03)*getPictureSize(storagePlace + "/Default_UI/Buttons/red-x.png")[1]/2-8],
    "Corner1":[],
    "Corner2": [],
    "linkedFunction": closeApp,
    "file": (storagePlace + "/Default_UI/Buttons/red-x.png"),
    "rescaling": 0.03},
}

ht()
if userSettings["new"]:
    initialiseOS()
homescreenUI = {}
loadHomescreen()

#Testing & Debugging

gc.collect()
Runtime.getRuntime().gc()
print "Hello World"