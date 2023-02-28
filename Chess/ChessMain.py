"""
This is our main driver file. It will be responsible for handling user input and displaying the current Gamstate object.
"""

import pygame
import ChessEngine

WIDTH = HEIGHT = 512 #400 is another good option
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
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    
    
    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected initially - will keep track of last click by user
    playerClicks = [] #have 2 tuples [(from_row, from_col), (to_row, to_col)]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row,col): #user clicked same sqaure twice - undo action
                    sqSelected = () #unselect
                    playerClicks = [] #resetting this as well
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append both 1st and 2nd click
                
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False 
            
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