import pygame
import tkinter as tk
import shelve
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
pygame.init()

#Setting up the window
windowHeight = 720
windowWidth = 1280
window = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("LOGIC GOAT")
clock = pygame.time.Clock()

#Camera set up
CamX = 0
CamY = 0
CamXBound = 5000
CamYBound = 5000

#Loading the images
bg = pygame.image.load("./images/bg.png")
bg.convert()
clearImg = pygame.image.load("./images/clear.png")
clearImg.convert()
saveImg = pygame.image.load("./images/save.png")
saveImg.convert()
openImg = pygame.image.load("./images/open.png")
openImg.convert()
andImg = pygame.image.load("./images/and.png")
andImg.convert()
nandImg = pygame.image.load("./images/nand.png")
nandImg.convert()
orImg = pygame.image.load("./images/or.png")
orImg.convert()
norImg = pygame.image.load("./images/nor.png")
norImg.convert()
xorImg = pygame.image.load("./images/xor.png")
xorImg.convert()
nxorImg = pygame.image.load("./images/nxor.png")
nxorImg.convert()
notImg = pygame.image.load("./images/not.png")
notImg.convert()
inputImg =pygame.image.load("./images/input.png")
inputImg.convert()
clockImg =pygame.image.load("./images/clock.png")
clockImg.convert()
outputImg =pygame.image.load("./images/output.png")
outputImg.convert()

#--------------CLASSES--------------#
class Connection:
    def __init__(self,connectionType,connectionRect,gate):
        # 0 - input 1 - output
        self.connectionType = connectionType
        # [gate,connection]
        self.connectedTo = []
        self.connectionRect = connectionRect
        self.gate = gate
        self.connected = False
    def connect(self, connection):
        if self.connectionType == 0:
            if connection.connectionType != self.connectionType and self.connected == False:
                self.connectedTo.append(connection)
                self.connected = True
                self.gate.calculateOutput(self)
        else:
            if connection.connectionType != self.connectionType and connection.connected == False:
                self.connectedTo.append(connection)
                self.connected = True
    def disconnect(self, connection):
        if connection == None:
            self.connected = False
            for c in self.connectedTo:
                c.disconnect(self)
            self.connectedTo = []
        else:
            self.connectedTo.remove(connection)
            if len(self.connectedTo) == 0:
                self.connected = False
    def draw(self):
        pygame.draw.ellipse(window,"white",self.connectionRect)
        pygame.draw.ellipse(window,"black",self.connectionRect,2)
        if self.connectionType == 1 and self.connected:
            for c in self.connectedTo:
                pygame.draw.line(window, "black", (self.connectionRect.x+18,self.connectionRect.y+9), (c.connectionRect.x,c.connectionRect.y+9),3)

#Logic gate class
class LogicGate:
    def __init__(self,x,y, img):
        self.value = -1
        self.output = None
        self.gateRect = img.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
        self.connections = []
    def draw(self):
        window.blit(getImg(self.type), self.gateRect)
        for connection in self.connections:
            connection.draw()
    def move(self,rel):
        self.gateRect.move_ip(rel)
        for connection in self.connections:
            connection.connectionRect.move_ip(rel)
    def sendOutput(self,sentGate):
        for c in self.output.connectedTo:
            if c.gate != sentGate:
                c.gate.calculateOutput(self)
    def delete(self):
        for c in self.connections:
            if c.connected:
                c.disconnect(None)

#Child classes
class AndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, andImg)
        self.type = "and"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == 1 and self.inputs[1].connectedTo[0].gate.value == 1:
                self.value = 1
            else:
                self.value = 0
            self.sendOutput(sentGate)
class NAndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, nandImg)
        self.type = "nand"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == 1 and self.inputs[1].connectedTo[0].gate.value == 1:
                self.value = 0
            else:
                self.value = 1
            self.sendOutput(sentGate)
class OrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, orImg)
        self.type = "or"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == 1 or self.inputs[1].connectedTo[0].gate.value == 1:
                self.value = 1
            else:
                self.value = 0
            self.sendOutput(sentGate)
class NOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, norImg)
        self.type = "nor"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == 1 or self.inputs[1].connectedTo[0].gate.value == 1:
                self.value = 0
            else:
                self.value = 1
            self.sendOutput(sentGate)
class XOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, xorImg)
        self.type = "xor"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == self.inputs[1].connectedTo[0].gate.value:
                self.value = 0
            else:
                self.value = 1
            self.sendOutput(sentGate)
class NXOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, nxorImg)
        self.type = "nxor"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connected and self.inputs[1].connected:
            if self.inputs[0].connectedTo[0].gate.value == self.inputs[1].connectedTo[0].gate.value:
                self.value = 1
            else:
                self.value = 0
            self.sendOutput(sentGate)
class NotGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,notImg)
        self.type = "not"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+41,18,18),self)]
        self.connections = [self.inputs[0],self.output]
    def calculateOutput(self, sentGate):
        if self.inputs[0].connectedTo[0].gate.value == 1:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput(sentGate)


#Input class
class InputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,inputImg)
        self.type = "input"
        self.value = 0
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.connections = [self.output]
    def draw(self):
        window.blit(getImg(self.type), self.gateRect)
        DrawText(str(self.value),70,(0,0,0),self.gateRect.x+50,self.gateRect.y+50)
        for connection in self.connections:
            connection.draw()
    def changeValue(self):
        if self.value == 1:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput(self)
class ClockGate(InputGate):
    def __init__(self,x,y):
        InputGate.__init__(self,x,y)
        self.type = "clock"
    def draw(self):
        window.blit(getImg(self.type), self.gateRect)
        for connection in self.connections:
            connection.draw()
#Output class
class OutputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,outputImg)
        self.type = "output"
        self.value = 0
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+41,18,18),self)]
        self.connections = [self.inputs[0]]
    def draw(self):
        window.blit(getImg(self.type), self.gateRect)
        DrawText(str(self.value),70,(0,0,0),self.gateRect.x+85,self.gateRect.y+50)
        for connection in self.connections:
            connection.draw()
    def calculateOutput(self, sentGate):
        self.value = self.inputs[0].connectedTo[0].gate.value

#Sidebar gates
class SidebarGates:
    def __init__(self,x,y,img,type):
        self.img = img
        self.type = type
        self.gateRect = img.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
    def draw(self):
        window.blit(self.img, self.gateRect)

#Class for buttons
class Button:
    def __init__(self,x,y,w,h,function):
        self.x = x
        self.y = y
        self.function = function
        self.xsize = w
        self.ysize = h
        self.color = (220, 95, 0)
        self.textColor = (0,0,0)
    def clicked(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if x>self.x and x<self.x+self.xsize and y>self.y and y<self.y+self.ysize:
            self.function(self)
    

class TextButton(Button):
    def __init__(self, text, x, y, w, h, textSize, function):
        Button.__init__(self, x, y, w, h, function)
        self.text = text
        self.textSize = textSize
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x,self.y,self.xsize,self.ysize),border_radius=10)
        pygame.draw.rect(window, "black", (self.x,self.y,self.xsize,self.ysize),3,border_radius=10)
        DrawText(self.text, self.textSize ,self.textColor,(self.x+self.xsize/2),(self.y+self.ysize/2))

class IconButton(Button):
    def __init__(self, x, y, w, h, img, function):
        Button.__init__(self, x, y, w, h, function)
        self.img = img
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x,self.y,self.xsize,self.ysize),border_radius=10)
        pygame.draw.rect(window, "black", (self.x,self.y,self.xsize,self.ysize),3,border_radius=10)
        imageRect = self.img.get_rect()
        imageRect.center = (self.x+self.xsize/2,self.y+self.ysize/2)
        window.blit(self.img, imageRect)


#--------------HELPER FUNCTIONS--------------#
def AddGate(gateType):
    x,y = pygame.mouse.get_pos()
    x -= 67.5
    y -= 50
    match gateType:
        case "and":
            gates.append(AndGate(x,y))
        case "nand":
            gates.append(NAndGate(x,y))
        case "or":
            gates.append(OrGate(x,y))
        case "nor":
            gates.append(NOrGate(x,y))
        case "xor":
            gates.append(XOrGate(x,y))
        case "nxor":
            gates.append(NXOrGate(x,y))
        case "not":
            gates.append(NotGate(x,y))
        case "input":
            gates.append(InputGate(x,y))
        case "clock":
            gates.append(ClockGate(x,y))
        case "output":
            gates.append(OutputGate(x,y))

def GetActiveGate1(pos):
    global activeGate
    global prevActiveGate
    for num, gate in enumerate(gates):
        if gate.gateRect.collidepoint(pos):
            activeGate = num
            prevActiveGate = activeGate

def AddSideGate(pos):
    global activeGate
    global prevActiveGate
    global sideBarMode
    if sideBarMode == "GATES":
        g = sideGates
    else:
        g = sideIO
    for gate in g:
        if gate.gateRect.collidepoint(pos):
            activeGate = len(gates)
            prevActiveGate = activeGate
            AddGate(gate.type)

def DrawText(text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    window.blit(text, textRect)

def SwitchBarMode(btn):
    global sideBarMode
    sideBarMode = btn.text

def Clear(btn):
    global gates
    global menu
    global prevActiveGate
    gates = []
    prevActiveGate = None
    menu = False  

def OpenFile(btn):
    global gates
    global menu
    file = filedialog.askopenfilename(title='Select Logic Gate file', filetypes=[('All Files', '*.*')])
    if file == '':
        return False
    shelve_file = shelve.open(file[:-3])
    gates = shelve_file['gates']
    menu = False
    shelve_file.close()
    return True

def Save(btn):
    global gates
    file = filedialog.asksaveasfilename(title='Select Image file', filetypes=[('All Files', '*.*')])
    shelve_file = shelve.open(file)
    shelve_file['gates'] = gates
    shelve_file.close()
    shelve_file = shelve.open(file)
    shelve_file.close()

def getImg(type):
    match type:
        case "and":
            return andImg
        case "nand":
            return nandImg
        case "or":
            return orImg
        case "nor":
            return norImg
        case "xor":
            return xorImg
        case "nxor":
            return nxorImg
        case "not":
            return notImg
        case "input":
            return inputImg
        case "clock":
            return clockImg
        case "output":
            return outputImg

#--------------MAIN LOOP--------------#
running = True
menu = True
gates = []
sideGates = [SidebarGates(5,100,andImg,"and"),SidebarGates(160,100,nandImg,"nand"),SidebarGates(5,220,orImg,"or"),SidebarGates(160,220,norImg,"nor"),SidebarGates(5,330,xorImg,"xor"),SidebarGates(160,330,nxorImg,"nxor"),SidebarGates(82.5,440,notImg,"not")]
sideIO = [SidebarGates(5,100,inputImg,"input"),SidebarGates(160,100,outputImg,"output"), SidebarGates(82.5,220,clockImg,"clock")]
activeGate = None
prevActiveGate = None
motion = False
activeConnection1 = None
activeConnection2 = None
sideBarMode = "GATES"
timer = 0
#Buttons
GateBtn = TextButton("GATES",30,10,100,50,17,SwitchBarMode)
IOBtn = TextButton("I/O",170,10,100,50,17,SwitchBarMode)
ClearBtn = IconButton(10,650,80,50,clearImg,Clear)
SaveBtn = IconButton(100,650,80,50,saveImg,Save)
OpenBtn = IconButton(190,650,80,50,openImg,OpenFile)
NewBtn = TextButton("NEW",490,300,300,100,50,Clear)
LoadBtn = TextButton("LOAD",490,450,300,100,50,OpenFile)
while running:
    #Getting all events
    for event in pygame.event.get():
        #Checking if window gets closed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for gate in gates:
                    for connection in gate.connections:
                        if connection.connectionRect.collidepoint(event.pos):
                            activeConnection1 = connection
            #ON LEFT CLICK
            if event.button == 1:
                if menu:
                    NewBtn.clicked()
                    LoadBtn.clicked()
                else:
                    if event.pos[0] > 300:
                        GetActiveGate1(event.pos)
                    else:
                        AddSideGate(event.pos)
                        GateBtn.clicked()
                        IOBtn.clicked()
                        ClearBtn.clicked()
                        SaveBtn.clicked()
                        OpenBtn.clicked()
            #ON RIGHT CLICK
            if event.button == 3 and activeConnection1 != None:
                activeConnection1.disconnect(None)
                activeConnection1 = None
        if event.type == pygame.MOUSEMOTION:
            #Move gate
            if activeGate != None:
                nextPos = (gates[activeGate].gateRect.move(event.rel).x,gates[activeGate].gateRect.move(event.rel).y)
                if  nextPos[0] < 1145 and nextPos[0] > 0 and nextPos[1] > 0 and nextPos[1] < 620:
                    gates[activeGate].move(event.rel)
                    motion = True
            #Move camera
            elif event.buttons == (1,0,0) and activeConnection1 == None:
                dx,dy = event.rel
                if abs(CamX+dx)<CamXBound and abs(CamY+dy)<CamYBound:
                    for gate in gates:
                        gate.move(event.rel)
                    CamX += dx
                    CamY += dy
        if event.type == pygame.MOUSEBUTTONUP:
            #Change input value
            if activeGate != None and motion == False:
                if gates[activeGate].type == "input":
                    gates[activeGate].changeValue()
            activeGate = None
            motion = False
            for gate in gates:
                    for connection in gate.connections:
                        if connection.connectionRect.collidepoint(event.pos):
                            activeConnection2 = connection
            #Connecting two connections
            if activeConnection1 != None and activeConnection2 != None and activeConnection1.gate != activeConnection2.gate:
                #Connect output to input first then input to output
                if activeConnection1.connectionType == 1:
                    activeConnection1.connect(activeConnection2)
                    activeConnection2.connect(activeConnection1)
                else:
                    activeConnection2.connect(activeConnection1)
                    activeConnection1.connect(activeConnection2)
            activeConnection1 = None
            activeConnection2 = None
        if event.type == pygame.KEYDOWN:
            #key presses to add gates
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                AddGate("and")
            if keys[pygame.K_2]:
                AddGate("or")
            if keys[pygame.K_3]:
                AddGate("xor")
            if keys[pygame.K_4]:
                AddGate("nand")
            if keys[pygame.K_5]:
                AddGate("nor")
            if keys[pygame.K_6]:
                AddGate("nxor")
            if keys[pygame.K_7]:
                AddGate("not")
            if keys[pygame.K_8]:
                AddGate("input")
            if keys[pygame.K_9]:
                AddGate("output")
            #Deleting a gate
            if keys[pygame.K_BACKSPACE]:
                if prevActiveGate != None:
                    gates[prevActiveGate].delete()
                    gates.pop(prevActiveGate)
                    prevActiveGate = None
    if menu:
        window.blit(bg,(0,0))
        DrawText("LOGIC GOAT",120,"black",640,80)
        NewBtn.draw()
        LoadBtn.draw()
    else:
        window.fill((104, 109, 118))
        #updating clocks
        timer += 1
        if (timer % 60 == 0):
            timer = 0
            for g in gates:
                if g.type == "clock":
                    g.changeValue()
        #Drawing the gates
        for gate in gates:
            gate.draw()
        #Drawing the side bar
        pygame.draw.rect(window,(55, 58, 64), (0,0,300,720))  
        GateBtn.draw()
        IOBtn.draw()
        ClearBtn.draw()
        SaveBtn.draw()
        OpenBtn.draw()
        if sideBarMode == "GATES":
            for g in sideGates:
                g.draw()
        else:
            for g in sideIO:
                g.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()