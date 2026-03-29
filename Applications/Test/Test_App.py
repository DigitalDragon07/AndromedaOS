import gamegrid

userSettings = getUserSettings()
storagePlace = getStoragePlace()

def TheFirstTest():
#    gamegrid.makeGameGrid(50, 50, 50, gamegrid.Color.red)
#    gamegrid.show()
#    print "testing worked!"
    storeData("Hello", "Testtest")

def redirectToSecond():
    updateDomain("second")
    print "Data is", getData("Hello")
    closeApp()
 
def keyRegistration(key, code):
    print key
    
def mouseRegistration(x, y):
    print x, y
       
print "globals are", globals()
appSetup = eval(loadSetup("AppSetup.txt"))

