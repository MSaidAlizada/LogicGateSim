import pygame
pygame.init()

#Setting up the window
windowHeight = 720
windowWidth = 1280
window = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Logic Gates Sim")
clock = pygame.time.Clock()

#Camera set up
CamX = 0
CamY = 0
CamXBound = 5000
CamYBound = 5000
def getCameraPosition(x,y):
    return x+640,360-y
def getWorldPosition(x,y):
    return x-640,360+y

#Loading the images
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
inputImg =pygame.image.load("./images/input.png")
inputImg.convert()
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
        self.img = img
        self.gateRect = img.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
        self.connections = []
    def draw(self):
        window.blit(self.img, self.gateRect)
        for connection in self.connections:
            connection.draw()
    def move(self,rel):
        self.gateRect.move_ip(rel)
        for connection in self.connections:
            connection.connectionRect.move_ip(rel)
    def sendOutput(self):
        for c in self.output.connectedTo:
            c.gate.calculateOutput()

#Child classes
class AndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, andImg)
        self.type = "and"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self):
        if self.inputs[0].connectedTo[0].gate.value == 1 and self.inputs[1].connectedTo[0].gate.value == 1:
            self.value = 1
        else:
            self.value = 0
        self.sendOutput()
class NAndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, nandImg)
        self.type = "nand"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self):
        if self.inputs[0].connectedTo[0].gate.value == 1 and self.inputs[1].connectedTo[0].gate.value == 1:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput()
class OrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, orImg)
        self.type = "or"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self):
        if self.inputs[0].connectedTo[0].gate.value == 1 or self.inputs[1].connectedTo[0].gate.value == 1:
            self.value = 1
        else:
            self.value = 0
        self.sendOutput()
class NOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, norImg)
        self.type = "nor"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self):
        if self.inputs[0].connectedTo[0].gate.value == 1 or self.inputs[1].connectedTo[0].gate.value == 1:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput()
class XOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, xorImg)
        self.type = "xor"
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self)]
        self.connections = [self.inputs[0],self.inputs[1], self.output]
    def calculateOutput(self):
        if self.inputs[0].connectedTo[0].gate.value == self.inputs[1].connectedTo[0].gate.value:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput()
#Input class
class InputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,inputImg)
        self.type = "input"
        self.value = 0
        self.output = Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)
        self.connections = [self.output]
    def draw(self):
        window.blit(self.img, self.gateRect)
        DrawText(str(self.value),70,(0,0,0),self.gateRect.x+50,self.gateRect.y+50)
        for connection in self.connections:
            connection.draw()
    def changeValue(self):
        if self.value == 1:
            self.value = 0
        else:
            self.value = 1
        self.sendOutput()
#Output class
class OutputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,outputImg)
        self.type = "output"
        self.value = 0
        self.inputs = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+41,18,18),self)]
        self.connections = [self.inputs[0]]
    def draw(self):
        window.blit(self.img, self.gateRect)
        DrawText(str(self.value),70,(0,0,0),self.gateRect.x+85,self.gateRect.y+50)
        for connection in self.connections:
            connection.draw()
    def calculateOutput(self):
        self.value = self.inputs[0].connectedTo[0].gate.value
        


#--------------HELPER FUNCTIONS--------------#
def AddGate(gateType):
    match gateType:
        case "and":
            gates.append(AndGate(*pygame.mouse.get_pos()))
        case "nand":
            gates.append(NAndGate(*pygame.mouse.get_pos()))
        case "or":
            gates.append(OrGate(*pygame.mouse.get_pos()))
        case "nor":
            gates.append(NOrGate(*pygame.mouse.get_pos()))
        case "xor":
            gates.append(XOrGate(*pygame.mouse.get_pos()))
        case "input":
            gates.append(InputGate(*pygame.mouse.get_pos()))
        case "output":
            gates.append(OutputGate(*pygame.mouse.get_pos()))

def GetActiveGate(pos):
    global activeGate
    global prevActiveGate
    for num, gate in enumerate(gates):
                    if gate.gateRect.collidepoint(pos):
                        activeGate = num
                        prevActiveGate = activeGate

def DrawText(text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    window.blit(text, textRect)
#--------------MAIN LOOP--------------#
running = True
gates = []
activeGate = None
prevActiveGate = None
motion = False
activeConnection1 = None
activeConnection2 = None
while running:
    window.fill("grey")
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
                GetActiveGate(event.pos)
            #ON RIGHT CLICK
            if event.button == 3 and activeConnection1 != None:
                activeConnection1.disconnect(None)
                activeConnection1 = None
        if event.type == pygame.MOUSEMOTION:
            if activeGate != None:
                nextPos = (gates[activeGate].gateRect.move(event.rel).x,gates[activeGate].gateRect.move(event.rel).y)
                if  nextPos[0] < 1145 and nextPos[0] > 0 and nextPos[1] > 0 and nextPos[1] < 620:
                    gates[activeGate].move(event.rel)
                    motion = True
            elif event.buttons == (1,0,0) and activeConnection1 == None:
                dx,dy = event.rel
                if abs(CamX+dx)<CamXBound and abs(CamY+dy)<CamYBound:
                    for gate in gates:
                        gate.move(event.rel)
                    CamX += dx
                    CamY += dy
        if event.type == pygame.MOUSEBUTTONUP:
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
                activeConnection1.connect(activeConnection2)
                activeConnection2.connect(activeConnection1)
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
                AddGate("input")
            if keys[pygame.K_7]:
                AddGate("output")
            #Deleting a gate
            if keys[pygame.K_BACKSPACE]:
                if prevActiveGate != None:
                    gates.pop(prevActiveGate)
                    prevActiveGate = None
    #Drawing the gates
    for gate in gates:
        gate.draw()  
    pygame.display.update()
    clock.tick(60)
pygame.quit()