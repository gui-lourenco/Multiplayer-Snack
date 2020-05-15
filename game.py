import pygame 

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

    def createScreen(self): 
        screenDim = (self.width, self.heigth)
        screen = pygame.display.set_mode(screenDim)
        self.screen = screen
        screen.fill(self.color)

    def setColor(self, color):
        self.color = color

    def updateScreen(self):
        pygame.display.update()
    
    def drawPlayer(self, player):
        for part in player.body:
            self.screen.blit(player.skin, part)

    def drawFruit(self, fruit):
        pygame.draw.rect(self.screen, fruit.color, fruit.rect)


class Player:

    def __init__(self, posX, posY, color=BLACK):
        width = 10
        heigth = 10
        self.body = [(posX, posY), (posX+10, posY), (posX+20,posY)] 
        self.color = color
        self.skin = pygame.Surface((width,heigth))
        self.skin.fill((color))
        self.direction = LEFT


class Fruit:

    def __init__(self, color=RED):
        posX = 250
        posY = 250
        width = 10
        heigth = 10
        self.rect = pygame.Rect(posX, posY, 
                    width, heigth)
        self.color = color

class Game:

    def __init__(self, limitX, limitY):
        self.clock = pygame.time.Clock()
        self.player = Player(10,10)
        self.fruit = Fruit()
        self.limitX = limitX
        self.limitY = limitY

    def moveUp(self):
        print('Moving to Up')

    def moveDown(self):
        print('Moving to Down')

    def moveLeft(self):
        print('Moving to Left')

    def moveRight(self):
        print('Moving to Right')

    def checkCollision(self):
        print('collision')

    def outLimit(self):
        print('out')

if __name__ == '__main__':
    screenLimitX = 500
    screenLimitY = 500
    screen = Screen(screenLimitX, screenLimitY)
    screen.createScreen()
    game = Game(screenLimitX, screenLimitY)

    while True:
        screen.drawPlayer(game.player)
        screen.drawFruit(game.fruit)
        screen.updateScreen()