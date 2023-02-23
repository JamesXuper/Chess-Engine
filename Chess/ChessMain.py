"""
This is our main driver file. It will be responsible for handling user input and displaying the current Gamstate object.
"""

import pygame
import ChessEngine

WIDTH = HEIGHT = 400 #400 is another good option
DIMENSION = 8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animation 
IMAGES = {}

'''
Initialise a global dictionary of images. This will be called exactly once in the main.
'''

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by calling the dictionary key
    
'''
The main driver for our code. Handle user input and updating the graphics.
'''

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() #only do this once, before the while loop
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()
    
'''
Responsible for all the graphics within a current game state.
'''  
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    
    #add in piece highlighting or move suggestions
    drawPieces(screen, gs.board) #draw pieces on top of those squares
    
'''
Draw the squares on the board
'''
def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')] #COLORS
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty space
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
    
    
    
if __name__ == "__main__":
    main()