from graphics import *
import math
import random
import decimal
import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

WINDOW_WIDTH = 400;
WINDOW_HEIGHT = 500;

win = GraphWin("Calculator", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground(color_rgb(240,240,240))

class button:
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text

    def build(self):
        self.p1= Point(self.position[0], self.position[1])
        self.p2= Point(self.p1.getX()+self.size[0], self.p1.getY()+self.size[1])
        self.buttonOverlay = Rectangle(self.p1, self.p2)
        self.textToDraw = Text(Point(self.p1.getX()+(self.size[0]/2), self.p1.getY()+(self.size[1]/2)), self.text)

    def draw(self, win):
        self.buttonOverlay.draw(win)
        self.textToDraw.draw(win)

    def undraw(self):
        self.buttonOverlay.undraw()
        self.textToDraw.undraw()

    def inside(self, point):
        ll = self.buttonOverlay.getP1()
        ur = self.buttonOverlay.getP2()

        return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

    def activateFunction(self):
        if(self.attrib1 != None):
            self.func(self.attrib1)
        else:
            self.func()

    def setFunction(self, function, attrib1 = None):
        self.func = function
        self.attrib1 = attrib1

    function = property(activateFunction, setFunction)


def buttons():
    howMannyButtons = (4, 7)
    height = 5
    pos = (0, WINDOW_HEIGHT/height +10*(howMannyButtons[1]/2))
    height=WINDOW_HEIGHT *((height-1)/height)
    size = (WINDOW_WIDTH/howMannyButtons[0] - 10, height/howMannyButtons[1] -10)
    buttonsText = ('rand','x rand y','x % y','','x mod y', 'x root y', 'x pow y', 'x pow x', 'CE', 'C', 'del', 'x / y', '7', '8', '9', 'x X y', '4', '5', '6', 'x - y', '1', '2', '3', 'x + y', '+/- x', '0', ',', '=')

    buttons = []
    for i in range(len(buttonsText)):
        newPos= (pos[0]+(size[0]*(i%howMannyButtons[0]))+5+(10*(math.floor(i%howMannyButtons[0]))), pos[1]+(size[1]*math.floor(i/howMannyButtons[0]))+5*math.floor(i/howMannyButtons[0]))
        newButt = button(newPos, size, buttonsText[i])
        newButt.build()
        newButt.draw(win)

        text =buttonsText[i]
        try:
            if(int(text) >= int("0") and int(text) <= int("9")):
                newButt.setFunction( addNumber, int(text) )
        except:
            if(text == 'CE'):
                newButt.function = clearNumber
            if(text == 'C'):
                newButt.function = clearEveryNumber
            elif(text == 'del'):
                newButt.function = delNumber
            elif(text == ','):
                newButt.function = numberToFloat
            elif(text == '+/- x'):
                newButt.function = changeNumCharacter
            elif(text == 'hist'):
                pass #newButt.function = openHistory

            elif(text == "x + y" or text == "x - y" or text == "x X y" or text == "x / y" or text == "x mod y" or text == "x root y" or text == "x pow y"  or text == "x % y" or text == "x rand y"):
                newButt.setFunction( addSymbol, text )
            elif(text == "x pow x" or text == "rand"):
                newButt.setFunction( instantAction, text )
            elif (text == "="):
                newButt.setFunction(calcThat, text)

        buttons.append(newButt)

    return buttons

def histMenButtons():
    howMannyButtons = (3, 6)
    height = 5
    pos = (0, WINDOW_HEIGHT/height +10*(howMannyButtons[1]/2))
    height=WINDOW_HEIGHT *((height-1)/height)
    size = (WINDOW_WIDTH/howMannyButtons[0] - 10, height/howMannyButtons[1] -10)
    buttonsText = ('down', 'back', 'up')

    buttons = []
    for i in range(len(buttonsText)):
        newPos= (pos[0]+(size[0]*(i%howMannyButtons[0]))+5+(10*(math.floor(i%howMannyButtons[0]))), pos[1]+(size[1]*math.floor(i/howMannyButtons[0]))+5*math.floor(i/howMannyButtons[0]))
        newButt = button(newPos, size, buttonsText[i])
        newButt.build()

        text = buttonsText[i]

        if (text == 'back'):
            newButt.function = closeHistory

        buttons.append(newButt)
    return buttons

calcHistory = []
resultHistory = []
calcNumbers = [0]
calcSymbols = []
floatVal = [int(0)]

def newNumber():
    calcNumbers.append(0)

def addNumber(num):
    numb = calcNumbers[len(calcNumbers)-1]
    if(type(numb) == int):
        numb = (numb * 10) + num
        floatVal[0] = 0
    else:
        floatVal[0] +=1
        numb = (numb + ( num * math.pow(0.1, floatVal[0])))
    calcNumbers[len(calcNumbers)-1] = round(numb, floatVal[0])

def addSymbol(symb):
    newNumber()
    calcSymbols.append(symb[2:-2])

def delNumber():
    numb = calcNumbers[len(calcNumbers)-1]
    if numb == 0 and len(calcSymbols) >= 1:
        calcNumbers.pop(len(calcNumbers)-1)
        calcSymbols.pop(len(calcSymbols)-1)
    else:
        t = type(numb)
        if(type(numb) == int):
            num = numb % 10
            numb = (numb - num)/10
        elif (floatVal[0]>0):
            num = numb % math.pow(0.1, floatVal[0]-1)
            numb = (numb - num)
        numb = t(numb)
        if(floatVal[0]>0):
            floatVal[0]-=1
        else:
            if (numb % 1 == 0):
                numb = int(numb)

        calcNumbers[len(calcNumbers)-1] = numb

def numberToFloat():
    numb = calcNumbers[len(calcNumbers)-1]
    calcNumbers[len(calcNumbers)-1] = float(numb)

def clearNumber():
    calcNumbers[len(calcNumbers)-1] = 0

def clearEveryNumber():
    calcNumbers.clear()
    calcSymbols.clear()
    calcNumbers.append(0)

def changeNumCharacter():
    numb = calcNumbers[len(calcNumbers)-1]
    calcNumbers[len(calcNumbers)-1] = -(numb)

def instantAction(symb):
    lastNum = len(calcNumbers) - 1
    if (symb == "rand"):
         calcNumbers[lastNum] = random.randint(0, 1000000)
    elif (symb == "x pow x"):
         calcNumbers[lastNum] **= calcNumbers[lastNum]

def calcThat(symb):
    addSymbol(symb)
    result = calcNumbers[0]
    history = str(calcNumbers[0]) + " "
    for i in range(len(calcSymbols)-1):
        try:
            if(result == "Error"):
                result = 0
            if(calcSymbols[i] == "+"):
                result += calcNumbers[i+1]
            elif(calcSymbols[i] == "-"):
                result -= calcNumbers[i+1]
            elif(calcSymbols[i] == "X"):
                result *= calcNumbers[i+1]
            elif(calcSymbols[i] == "/"):
                result /= calcNumbers[i+1]
            elif(calcSymbols[i] == "pow"):
                result **= calcNumbers[i+1]
            elif(calcSymbols[i] == "mod"):
                result %= calcNumbers[i+1]
            elif(calcSymbols[i] == "root"):
                result = calcNumbers[i+1]**(1/result)
            elif (calcSymbols[i] == "rand"):
                sub = 0
                if(result<calcNumbers[i+1]):
                    sub =result
                result += (random.random() * ( calcNumbers[i+1] - sub) )
            elif (calcSymbols[i] == "%"):
                result = (result * (calcNumbers[i+1]/100))

            if (result % 1 == 0):
                result = int(result)
        except:
            result = "Error"

        history += str(calcSymbols[i]) + " " + str(calcNumbers[i+1]) + " "

    calcHistory.append((history + "="))
    resultHistory.append(result)
    calcNumbers.clear()
    calcSymbols.clear()
    calcNumbers.append( result )
    floatVal[0] = abs((decimal.Decimal(str(result))).as_tuple().exponent)

centerPoint = Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10)
def texts():
    texts = []
    for i in range(2):
        fontSize = 30
        point = Point(centerPoint.getX(), (centerPoint.getY()*2 -10 - fontSize*i*1.5))
        if(i == 0):
            text = Text(point, "0")
            text.setSize(fontSize)
        else:
            text = Text(point, "")
            text.setTextColor("grey")
            text.setSize(fontSize-10)
        text.draw(win)
        texts.append(text)
    return texts

def printText():
    if (len(calcNumbers) == 1 and len(calcHistory) >= 1):
        #print(calcHistory[len(calcHistory)-1])
        return calcHistory[len(calcHistory)-1]
    elif (len(calcNumbers) == 1):
        return  ""
    else:
        result = ""
        for i in range(len(calcNumbers)):
            if(i < len(calcNumbers)-1):
                result += str(calcNumbers[i]) + " "
                result += calcSymbols[i] + " "
        return result

historyMode = [False]
def openHistory():
    for button in buttons:
        button.undraw()
    for button in histMenuButtons:
        button.draw(win)
    historyMode[0] = True
def closeHistory():
    for button in histMenuButtons:
        button.undraw()
    for button in buttons:
        button.draw(win)
    historyMode[0] = False

buttons = buttons()
outputTexts = texts()

#print(histMenButtons())
histMenuButtons = histMenButtons()
#print(histMenuButtons)
#historyButtons = buttons()


while True:
    clickPoint = win.getMouse()
    isActuallyClicking = False
    if clickPoint is None:
        isActuallyClicking = False
    elif isActuallyClicking == False:
        isActuallyClicking = True

        if(historyMode[0] == False):
            for button in buttons:
                if(button.inside(clickPoint)):
                    try:
                        button.activateFunction()
                    except:
                        pass
                    outputTexts[0].setText( round(calcNumbers[len(calcNumbers)-1], floatVal[0]))
                    outputTexts[1].setText(printText())
                    break
        else:
            for button in histMenuButtons:
                if(button.inside(clickPoint)):
                    try:
                        button.activateFunction()
                    except:
                        pass

win.close()