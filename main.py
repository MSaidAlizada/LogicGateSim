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
def getCameraPosition(x,y):
    return x+640,360-y

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
                self.connectedTo.append([connection.gate,connection])
                self.connected = True
        else:
            if connection.connectionType != self.connectionType and connection.connected == False:
                self.connectedTo.append([connection.gate,connection])
                self.connected = True
    def disconnect(self):
        if self.connected:
            self.connected = False
            for i in self.connectedTo:
                i[1].disconnect()
    def draw(self):
        pygame.draw.ellipse(window,"white",self.connectionRect)
        pygame.draw.ellipse(window,"black",self.connectionRect,2)
        if self.connectionType == 1 and self.connected:
            for c in self.connectedTo:
                pygame.draw.line(window, "black", (self.connectionRect.x+18,self.connectionRect.y+9), (c[1].connectionRect.x,c[1].connectionRect.y+9),3)

#Logic gate class
class LogicGate:
    def __init__(self,x,y, img):
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

#Child classes
class AndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, andImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self),Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]

class NAndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, nandImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self),Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]

class OrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, orImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self),Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]

class NOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, norImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self),Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]

class XOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y, xorImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),self),Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),self),Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]

#Input class
class InputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,inputImg)
        self.connections = [Connection(1,pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18),self)]
 
#Output class
class OutputGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y,outputImg)
        self.connections = [Connection(0,pygame.Rect(self.gateRect.x-18,self.gateRect.y+41,18,18),self)]


#--------------HELPER FUNCTIONS--------------#
def AddGate(gateType):
    match gateType:
        case "and":
            gates.append(AndGate(*getCameraPosition(0,0)))
        case "nand":
            gates.append(NAndGate(*getCameraPosition(0,0)))
        case "or":
            gates.append(OrGate(*getCameraPosition(0,0)))
        case "nor":
            gates.append(NOrGate(*getCameraPosition(0,0)))
        case "xor":
            gates.append(XOrGate(*getCameraPosition(0,0)))
        case "input":
            gates.append(InputGate(*getCameraPosition(0,0)))
        case "output":
            gates.append(OutputGate(*getCameraPosition(0,0)))

def GetActiveGate(pos):
    global activeGate
    global prevActiveGate
    for num, gate in enumerate(gates):
                    if gate.gateRect.collidepoint(pos):
                        activeGate = num
                        prevActiveGate = activeGate

#--------------MAIN LOOP--------------#
running = True
gates = []
activeGate = None
prevActiveGate = None
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
            #ON LEFT CLICK
            if event.button == 1:
                GetActiveGate(event.pos)
                for gate in gates:
                    for connection in gate.connections:
                        if connection.connectionRect.collidepoint(event.pos):
                            activeConnection1 = connection
            #ON RIGHT CLICK
            if event.button == 3 and activeConnection1 != None:
                activeConnection1.disconnect()
                activeConnection1 = None
        if event.type == pygame.MOUSEMOTION:
            if activeGate != None:
                gates[activeGate].move(event.rel)
            elif event.buttons == (1,0,0) and activeConnection1 == None:
                for gate in gates:
                    gate.move(event.rel)
                dx,dy = event.rel
                CamX += dx
                CamY += dy
        if event.type == pygame.MOUSEBUTTONUP:
            activeGate = None
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
            #TEMPORARY - key presses to add gates
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                AddGate("and")
            if keys[pygame.K_d]:
                AddGate("output")
            if keys[pygame.K_w]:
                AddGate("or")
            if keys[pygame.K_s]:
                AddGate("input")
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