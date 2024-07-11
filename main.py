import pygame
import random

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
    return x+640,y+360

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

#Logic gate class
class LogicGate:
    def __init__(self,x,y):
        self.img = andImg
        self.gateRect = andImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
        self.connection1 = []
        self.connection2 = []
        self.connectedTo = []
    def draw(self):
        window.blit(self.img, self.gateRect)
        pygame.draw.ellipse(window,"white",(self.gateRect.x-18,self.gateRect.y+22,18,18))
        pygame.draw.ellipse(window,"black",(self.gateRect.x-18,self.gateRect.y+22,18,18),2)
        pygame.draw.ellipse(window,"white",(self.gateRect.x-18,self.gateRect.y+61,18,18))
        pygame.draw.ellipse(window,"black",(self.gateRect.x-18,self.gateRect.y+61,18,18),2)
        pygame.draw.ellipse(window,"white",(self.gateRect.x+135,self.gateRect.y+41,18,18))
        pygame.draw.ellipse(window,"black",(self.gateRect.x+135,self.gateRect.y+41,18,18),2)
        if len(self.connectedTo) != 0:
            self.drawConnection()
    def Connect(self, node, connection):
        match node:
            case 0:
                self.connection1 = connection
            case 1:
                self.connection2 = connection
            case 2:
                self.connectedTo = connection
    def Disconnect(self,node):
        match node:
            case 0:
                temp = self.connection1
                if len(temp) != 0:
                    self.connection1 = []
                    gates[temp[0]].Disconnect(temp[1])
            case 1:
                temp = self.connection2
                if len(temp) != 0:
                    self.connection2 = []
                    gates[temp[0]].Disconnect(temp[1])
            case 2:
                temp = self.connectedTo
                if len(temp) != 0:
                    self.connectedTo = []
                    gates[temp[0]].Disconnect(temp[1])
    def drawConnection(self):
        if self.connectedTo[1] == 0:
            pos2 = (gates[self.connectedTo[0]].gateRect.x-18,gates[self.connectedTo[0]].gateRect.y+31)
        else:
            pos2 = (gates[self.connectedTo[0]].gateRect.x-18,gates[self.connectedTo[0]].gateRect.y+70)
        pygame.draw.line(window, "black", (self.gateRect.x+153,self.gateRect.y+50), pos2)
    def returnConnections(self):
        return [pygame.Rect(self.gateRect.x-18,self.gateRect.y+22,18,18),pygame.Rect(self.gateRect.x-18,self.gateRect.y+61,18,18),pygame.Rect(self.gateRect.x+135,self.gateRect.y+41,18,18)]

class AndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y)
        self.img = andImg
        self.gateRect = andImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y

class NAndGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y)
        self.img = nandImg
        self.gateRect = nandImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
    
class OrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y)
        self.img = orImg
        self.gateRect = orImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y

class NOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y)
        self.img = norImg
        self.gateRect = norImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y

class XOrGate(LogicGate):
    def __init__(self,x,y):
        LogicGate.__init__(self,x,y)
        self.img = xorImg
        self.gateRect = xorImg.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y


#Helper functions for development
def printMousePosition():
    print(pygame.mouse.get_pos())
    

#main loop
running = True
gates = []
activeGate = None
activeConnection1 = []
activeConnection2 = []
sq1 = AndGate(*getCameraPosition(0,0))
sq2 = XOrGate(0,100)
gates.append(sq1)
gates.append(sq2)
while running:
    window.fill("grey")
    #Getting all events
    for event in pygame.event.get():
        #Checking if window gets closed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, gate in enumerate(gates):
                    if gate.gateRect.collidepoint(event.pos):
                        activeGate = num
            for num, gate in enumerate(gates):
                for cnum, connection in enumerate(gate.returnConnections()):
                    if connection.collidepoint(event.pos):
                        activeConnection1 = [num,cnum]
            if event.button == 3:
                gates[activeConnection1[0]].Disconnect(activeConnection1[1])
                activeConnection1 = []
        if event.type == pygame.MOUSEMOTION:
            if activeGate != None:
                gates[activeGate].gateRect.move_ip(event.rel)
            elif event.buttons == (1,0,0) and len(activeConnection1) == 0:
                for gate in gates:
                    gate.gateRect.move_ip(event.rel)
                dx,dy = event.rel
                CamX += dx
                CamY += dy
        if event.type == pygame.MOUSEBUTTONUP:
            activeGate = None
            for num, gate in enumerate(gates):
                    for cnum, connection in enumerate(gate.returnConnections()):
                        if connection.collidepoint(event.pos):
                            activeConnection2 = [num,cnum]
            if len(activeConnection1) != 0 and len(activeConnection2) != 0 and activeConnection1 != activeConnection2:
                gates[activeConnection1[0]].Connect(activeConnection1[1],activeConnection2)
                gates[activeConnection2[0]].Connect(activeConnection2[1],activeConnection1)
            activeConnection1 = []
            activeConnection2 = []

    sq1.draw()
    sq2.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()