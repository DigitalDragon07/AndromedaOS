from gamegrid import*
import math
from random import*
gamex = 1000
gamey = 500
cellSize = 1
makeGameGrid(gamex, gamey, cellSize)
moveStep = 15
lootboxCanMove = False
currentCards = []

userSettings = getUserSettings()
storagePlace = getStoragePlace()

class Lootbox(Actor):
    def __init__(self):
        self.counter = 0
        self.new = True
        self.wait_counter = 0
        self.onStage = False
        self.overlaptime = 20
        self.lastX = 0
        Actor.__init__(self, True, "sprites/nemo.gif")
    def act(self):
        global lootboxCanMove
        if not(self.onStage):
            if self.new:
                self.counter += 1
                if self.counter >= self.time:
                    self.move(moveStep)
                    self.onStage = True
                    self.new = False
            else:
                self.wait_counter += 1
                poses = [box1.getX(), box2.getX(), box3.getX()]
                checkList = []
                for x in poses:
                    checkList.append(x > 0 and x <= gamex//2)
                if True in checkList:
                    canGo2 = False
                else:
                    canGo2 = True
                if lootboxCanMove and canGo2:
                    lootboxCanMove = False
                    self.move(moveStep)
                    self.wait_counter = 0
                    self.onStage = True
        else:
            self.move(moveStep)
        if self.getX() >= (gamex+8):
            self.setLocation(Location(-50, self.getY()))
            self.onStage = False
        if self.getX() >= gamex//2 and self.lastX <= gamex//2:
            lootboxCanMove = True
        self.lastX = self.getX()

def chooseCard():
    loottable = [0.1, 0.01, 0.001, 0.0005]
    names = ["Anthony", "Celine", "Joscha", "Wiktor", "Benjamin", "Mirsad", "Louis", "Melissa", "Nick", "Jayden", "Noemi", "Enya", "Jonathan", "Lena", "Wim", "Philipp", "Laurin", "Sipan", "Colin"]
    nameOfRarities = ["bronze", "silver", "gold", "diamond"]
    p = random()
    rarity = ""
    person = ""
    i = 0
    suml = 0
    while suml <= p:
        if i != 4:
            suml += loottable[i]
            rarity = nameOfRarities[i]
        else:
            rarity = "common"
            break
        i += 1
    randNum = randint(1, len(names))
    chosenName = names[randNum-1]
    return [chosenName, rarity]
            
box1 = Lootbox()
box1.time = 0
box2 = Lootbox()
box2.time = gamex//2//moveStep
box3 = Lootbox()
box3.time = gamex//moveStep

def doRoll():
    addActor(box1, Location(-50, int(round(gamey/2, 0))))
    addActor(box2, Location(-50, int(round(gamey/2, 0))))
    addActor(box3, Location(-50, int(round(gamey/2, 0))))
    show()
    doRun()
    
setSimulationPeriod(10)
slowdown_timer = 1
interval_timer1 = 100
interval_timer2 = 150
interval_timer3 = 200

def chooseCard():
    loottable = [0.1, 0.01, 0.001, 0.0005]
    names = ["Anthony", "Celine", "Joscha", "Wiktor", "Benjamin", "Mirsad", "Louis", "Melissa", "Nick", "Jayden", "Noemi", "Enya", "Jonathan", "Lena", "Wim", "Philipp", "Laurin", "Sipan", "Colin"]
    nameOfRarities = ["bronze", "silver", "gold", "diamond"]
    p = random()
    rarity = ""
    person = ""
    i = 0
    suml = 0
    while suml <= p:
        if i != 4:
            suml += loottable[i]
            rarity = nameOfRarities[i]
        else:
            rarity = "common"
            break
        i += 1
    randNum = randint(1, len(names))
    chosenName = names[randNum-1]
    return [chosenName, rarity]

def onAct():
    global slowdown_timer
    global moveStep
    slowdown_timer -= 1
    if slowdown_timer == 0:
        if moveStep != 1:
            moveStep -= 1
        if moveStep >= 8:
            slowdown_timer = interval_timer1
        elif moveStep >= 5 and moveStep < 8:
            slowdown_timer = interval_timer2
        else:
            slowdown_timer = interval_timer3
    if moveStep == 1:
        lo1 = box1.getX()
        lo2 = box2.getX()
        lo3 = box3.getX()
        pos = gamex//2
        if lo1 == pos or lo2 == pos or lo3 == pos:
            doPause()
            slowdown_timer = -1
            print chooseCard()

registerAct(onAct)
setBgColor(60, 69, 192)


def onOpen():
    doRoll()

def onClose():
    storeData("currentCards", currentCards)

appSetup = {
"name": "New App" ,
"icon": "icon.png", 
"openingFunction": onOpen, 
"closingFunction": onClose,
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