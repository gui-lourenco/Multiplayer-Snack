import pygame 
from pygame.locals import *
from random import randint

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

BLACK = (0,0,0)
RED = (255, 0, 0)
WHIGT = (255,255,255)

class Screen:
    
    def __init__(self, heigth, width, color=WHIGT):
        self.heigth = heigth
        self.width = width
        self.color = color
        self.context = {}

    def createScreen(self): 
        screenDim = (self.width, self.heigth)
        screen = pygame.display.set_mode(screenDim)
        self.screen = screen
        screen.fill(self.color)

    def setColor(self, color):
        self.color = color

    def addContext(self, contextFunc, *args):
        self.context[contextFunc] = args
        
    def updateScreen(self):
        self.screen.fill(self.color)
        for drawContextFunc, args in self.context.items():
            if args != None:
                drawContextFunc(*args)

            else:
                drawContextFunc()

        pygame.display.update()
    
    def drawPlayer(self, player):
        for part in player.body:
            self.screen.blit(player.skin, part)

    def drawFruit(self, fruit):
        pygame.draw.rect(self.screen, fruit.color, fruit.rect)


class KeyboardHandle:

    def __init__(self):
        self.observers = []

    def subscribe(self, observerFunction):
        self.observers.append(observerFunction)

    def notifyAll(self, command):
        for observerFunction in self.observers:
            observerFunction(command)

    def notifyEvent(self):
        for event in pygame.event.get():
            self.notifyAll(event)

class Player:

    oposed = {
        UP:DOWN,
        DOWN:UP,
        LEFT:RIGHT,
        RIGHT:LEFT
    }

    def __init__(self, posX, posY, limitX, limitY, color=BLACK):
        width = 10
        heigth = 10
        self.limitX = limitX
        self.limitY = limitY
        self.body = [(posX, posY), (posX+10, posY), (posX+20,posY)] 
        self.color = color
        self.skin = pygame.Surface((width,heigth))
        self.skin.fill((color))
        self.direction = RIGHT
        self.moveTo = {
            UP:self.moveUp,
            DOWN:self.moveDown,
            LEFT:self.moveLeft,
            RIGHT:self.moveRight
        }

    def setDirection(self, direction):
        if self.direction != Player.oposed[direction]:
            self.direction = direction

    def move(self):
        moveFunc = self.moveTo[self.direction]
        moveFunc()

    def moveUp(self):
        self.body[0] = (self.body[0][0], self.body[0][1] - 10)
        print('[Game] Moving to Up')

    def moveDown(self):
        self.body[0] = (self.body[0][0], self.body[0][1] + 10)
        print('[Game] Moving to Down')

    def moveLeft(self):
        self.body[0] = (self.body[0][0] - 10, self.body[0][1])
        print('[Game] Moving to Left')

    def moveRight(self):
        self.body[0] = (self.body[0][0] + 10, self.body[0][1])
        print('[Game] Moving to Right')

    def extendBody(self):
        self.body.append((0,0))

    def collisionMyself(self):
        head = self.body[0]
        body = self.body
        bodyLength = len(body)
        for i in range(1, bodyLength):
            if head == body[i]: 
                return True

        return False

    def updatePlayerBody(self):
        bodyLength = len(self.body)
        for i in range(bodyLength-1, 0, -1):
            previewX = self.body[i-1][0]
            previewY = self.body[i-1][1]
            self.body[i] = (previewX, previewY)
        
        self.outLimit()
        self.move()

    def outLimit(self):
        if self.body[0][0] < -10:
            self.body[0] = (self.limitX , self.body[0][1])
            print('[Game] out')

        elif self.body[0][0] > self.limitX:
            self.body[0] = (-10 , self.body[0][1])
            print('[Game] out')

        elif self.body[0][1] < -10:
            self.body[0] = (self.body[0][0], self.limitY)
            print('[Game] out')

        elif self.body[0][1] > self.limitY:
            self.body[0] = (self.body[0][0], -10)
            print('[Game] out')

class Fruit:

    def __init__(self, posX, posY, color=RED):
        width = 10
        heigth = 10
        self.posX = posX
        self.posY = posY
        self.color = color
        self.rect = pygame.Rect(self.posX, self.posY, 
                    width, heigth)
    
class Game:

    def __init__(self, limitX, limitY):
        self.clock = pygame.time.Clock()
        self.player = Player(10,10, limitX, limitY)
        self.fruit = Fruit(limitX//2, limitY//2)
        self.limitX = limitX
        self.limitY = limitY
        self.runnig = True

        self.acceptedMoves = {
            K_UP:UP,
            K_DOWN:DOWN,
            K_LEFT:LEFT,
            K_RIGHT:RIGHT,
        }
    
    def chooseMove(self, command):
        if command.type == KEYDOWN:
            direction = self.acceptedMoves.get(command.key)
            if direction != None:
                self.player.setDirection(direction)
            
            else:
                print('[Game] Key not accepted')

    def checkCollision(self):
        if self.player.collisionMyself():
            print('[Game] Player collision')

        if self.fruitCollision():
            self.randonFruitMove(self.limitX, self.limitY)
            self.player.extendBody()
            print('[Game] Fruit collision')

    def fruitCollision(self):
        head = self.player.body[0]
        fruitPos = self.fruit.posX, self.fruit.posY
        if head == fruitPos:
            return True

        return False

    def randonFruitMove(self, limitX, limitY):
        x = randint(0, limitX)
        y = randint(0, limitY)
        posX, posY = x//10 * 10, y//10 * 10
        self.fruit = Fruit(posX, posY)
        

    def quitGame(self, command):
        if command.type == QUIT:
            self.runnig = False

if __name__ == '__main__':
    screenLimitX = 500
    screenLimitY = 500
    screen = Screen(screenLimitX, screenLimitY)
    screen.createScreen()
    game = Game(screenLimitX, screenLimitY)
    keyboardInput = KeyboardHandle()
    keyboardInput.subscribe(game.chooseMove)
    keyboardInput.subscribe(game.quitGame)
    screen.addContext(screen.drawPlayer, game.player)
    screen.addContext(screen.drawFruit, game.fruit)

    while game.runnig:
        game.clock.tick(10)
        keyboardInput.notifyEvent()
        game.checkCollision()
        # Para passar pro contexto alterações na posição da fruta devido a colisão
        #Medida Temporária
        screen.addContext(screen.drawFruit, game.fruit) 
        game.player.updatePlayerBody()
        screen.updateScreen()

    pygame.quit()