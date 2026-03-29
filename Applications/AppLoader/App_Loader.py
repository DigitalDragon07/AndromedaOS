from gturtle import*
from java.io import File
import os
import copy

userSettings = getUserSettings()
storagePlace = getStoragePlace()

factor = autoRescale(1280, 800)
selectedNames= []
selectedApp = ""
appList = []
tempLst = []


def drawLines():
    width = userSettings["screenWidth"]
    height = userSettings["screenHeight"]
    setPenColor("Black")
    heading(0)
    setPos(0, 0-height/2)
    fd(height)
    setPos(width/2, 0)
    heading(270)
    fd(width)
    
def loadAppPreview():
    global appList
    global newappSetup
    global tempLst
    appList = []
    i = 1
    for f in loadAvailableApps():
        if not (f in getDownloadedApps()):
            appList.append(f)
    newappSetup = copy.deepcopy(appSetup)
    newappSetup["domains"]["main"]["clickableUI"]["field1"]["linkedFunction"] = None
    newappSetup["domains"]["main"]["clickableUI"]["field2"]["linkedFunction"] = None
    newappSetup["domains"]["main"]["clickableUI"]["field3"]["linkedFunction"] = None
    newappSetup["domains"]["main"]["clickableUI"]["field4"]["linkedFunction"] = None
    for x in appList:
        folder = x.split("/")[0]
        for y in File(storagePlace + "/Applications/" + folder).list():
            if y.startswith("icon") or y.endswith("icon.png"):
                if i == 1:
                    newappSetup["domains"]["main"]["clickableUI"]["icon1"]["file"] = storagePlace + "/Applications/" + folder + "/" + y
                    newappSetup["domains"]["main"]["clickableUI"]["icon1"]["rescaling"] = rescaleImageWithSize(newappSetup["domains"]["main"]["clickableUI"]["icon1"]["file"], 75)[1]*factor
                    newappSetup["domains"]["main"]["clickableUI"]["icon1"]["CenterPoint"] = [-550*factor, 300*factor]
                    newappSetup["domains"]["main"]["clickableUI"]["field1"]["linkedFunction"] = N1
                    doStuff(str(i), folder, -500, 315)
                elif i == 2:
                    newappSetup["domains"]["main"]["clickableUI"]["icon2"]["file"] = storagePlace + "/Applications/" + folder + "/" + y
                    newappSetup["domains"]["main"]["clickableUI"]["icon2"]["rescaling"] = rescaleImageWithSize(newappSetup["domains"]["main"]["clickableUI"]["icon2"]["file"], 75)[1]*factor
                    newappSetup["domains"]["main"]["clickableUI"]["icon2"]["CenterPoint"] = [90*factor, 300*factor]
                    newappSetup["domains"]["main"]["clickableUI"]["field2"]["linkedFunction"] = N2
                    doStuff(str(i), folder, 140, 315)
                elif i == 3:
                    newappSetup["domains"]["main"]["clickableUI"]["icon3"]["file"] = storagePlace + "/Applications/" + folder + "/" + y
                    newappSetup["domains"]["main"]["clickableUI"]["icon3"]["rescaling"] = rescaleImageWithSize(newappSetup["domains"]["main"]["clickableUI"]["icon3"]["file"], 75)[1]*factor
                    newappSetup["domains"]["main"]["clickableUI"]["icon3"]["CenterPoint"] = [-550*factor, -100*factor]
                    newappSetup["domains"]["main"]["clickableUI"]["field3"]["linkedFunction"] = N3
                    doStuff(str(i), folder, -500, -85)
                elif i == 4:
                    newappSetup["domains"]["main"]["clickableUI"]["icon4"]["file"] = storagePlace + "/Applications/" + folder + "/" + y
                    newappSetup["domains"]["main"]["clickableUI"]["icon4"]["rescaling"] = rescaleImageWithSize(newappSetup["domains"]["main"]["clickableUI"]["icon4"]["file"], 75)[1]*factor
                    newappSetup["domains"]["main"]["clickableUI"]["icon4"]["CenterPoint"] = [90*factor, -100*factor]
                    newappSetup["domains"]["main"]["clickableUI"]["field4"]["linkedFunction"] = N4
                    doStuff(str(i), folder, 140, -85)
                else:
                    print "Error in loadAppPreview: Too many apps"
                i += 1
    updateAppSetup(newappSetup)
    updateDomain("main", drawLines)
    
def doStuff(number, folder, xpos, ypos):
    global tempLst
    if os.path.exists(storagePlace + "/Applications/" + folder + "/metadata.txt"):
        tempLst = []
        with open(storagePlace + "/Applications/" + folder + "/metadata.txt") as f:
            for x in f:
                tempLst.append(x)
            newappSetup["domains"]["main"]["clickableUI"]["title" + number]["file"] = text(tempLst[0], 30, maxTextLength = 450, maxLineBreak = 0, style = "bold")
            newappSetup["domains"]["main"]["clickableUI"]["title" + number]["CenterPoint"] = [xpos, ypos]
            newappSetup["domains"]["main"]["clickableUI"]["author" + number]["file"] = text("Made by: " + tempLst[1], 30, maxTextLength = 450, maxLineBreak = 100)
            newappSetup["domains"]["main"]["clickableUI"]["author" + number]["CenterPoint"] = [xpos, ypos-40]
            newappSetup["domains"]["main"]["clickableUI"]["description" + number]["file"] = text(tempLst[2], 30, maxTextLength = 450, maxLineBreak = 100)
            newappSetup["domains"]["main"]["clickableUI"]["description" + number]["CenterPoint"] = [xpos, ypos-80]
            selectedNames.append(folder)

def onOpen():
    drawLines()
    loadAppPreview()
    
def onClose():
    pass
    
def N1():
    global selectedApp
    appSetup["domains"]["second"]["clickableUI"]["iconApp"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["icon1"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["AppName"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["title1"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["description"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["description1"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["author"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["author1"]["file"]
    updateAppSetup(appSetup)
    updateDomain("second")
    selectedApp = appList[0]
    
def N2():
    global selectedApp
    appSetup["domains"]["second"]["clickableUI"]["iconApp"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["icon2"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["AppName"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["title2"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["description"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["description2"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["author"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["author2"]["file"]
    updateAppSetup(appSetup)
    updateDomain("second")
    selectedApp = appList[1]
    
def N3():
    global selectedApp
    appSetup["domains"]["second"]["clickableUI"]["iconApp"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["icon3"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["AppName"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["title3"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["description"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["description3"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["author"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["author3"]["file"]
    updateAppSetup(appSetup)
    updateDomain("second")
    selectedApp = appList[2]
    
def N4():
    global selectedApp
    appSetup["domains"]["second"]["clickableUI"]["iconApp"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["icon4"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["AppName"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["title4"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["description"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["description4"]["file"]
    appSetup["domains"]["second"]["clickableUI"]["author"]["file"] = newappSetup["domains"]["main"]["clickableUI"]["author4"]["file"]
    updateAppSetup(appSetup)
    updateDomain("second")
    selectedApp = appList[3]

def idk():
    #downloadApp("Test/Test_App.py")
    updateDomain("second")
    
def testprint():
    print "Yay"
    
def doDownload():
    global selectedApp
    global tempLst
    folder = selectedApp.split("/")[0]
    if downloadApp(selectedApp, False, {"screenWidth": int(tempLst[3]), "screenHeight": int(tempLst[4])}):
        loadAppPreview()
    
appSetup = eval(loadSetup("AppSetup.txt"))
newappSetup = copy.deepcopy(appSetup)