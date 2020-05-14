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
            self.screen.blit(player.playerSkin, part)


