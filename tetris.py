import pygame
import random

SCRN_WIDTH = 700
SCRN_HEIGHT = 700
I = ([(0,-1),(0,0),(0,1),(0,2)],"I")
L = ([(0,-1),(0,0),(0,1),(-1,1)],"L" )
J = ([(-1,-1),(0,-1),(0,0),(0,1)],"J" )
O = ([(0,0),(-1,0),(0,1),(-1,1)],"O" )
S = ([(0,-1),(0,0),(-1,0),(-1,1)],"S" )
Z = ([(-1,-1),(-1,0),(0,0),(0,1)],"Z" )
T = ([(0,-1),(0,0),(0,1),(-1,0)],"T" )
SHAPE_LIST = [I,L,J,O,S,Z,T]
COLOURS = [(0,200,200),(200,200,0),(128,0,128),(0,128,0),(0,0,200),(200,0,0),(200,165,0)]

WIN = pygame.display.set_mode((SCRN_WIDTH,SCRN_HEIGHT))
pygame.display.set_caption("Tetris clone (by Arruran.K)")

class Board:
    def __init__(self):
        self.score = 0
        self.board = []
        for i in range(21):
            self.board.append([])
        for i in range(21):
            for j in range(10):
                self.board[i].append(Tile())
    
    def addPiece(self, piece):
        for tile in piece.shape:
            self.board[tile[0]][tile[1]].value = 1
            self.board[tile[0]][tile[1]].colour = piece.colour
    def removeFullRows(self):
        for row in self.board:
            if sum([tile.value for tile in row]) == 10:
                row = [tile.reset() for tile in row]
                self.score+=1000
                self.dropDown()
    def dropDown(self):
        for i in range(len(self.board)-1,1,-1):
            if sum([tile.value for tile in self.board[i]]) == 0:
                for j in range(i,0,-1):
                    for index in range(10):
                        self.board[j][index].value = self.board[j-1][index].value
                        self.board[j][index].colour = self.board[j-1][index].colour

                break


class Tile:
    def __init__(self):
        self.value = 0
        self.colour = (0,0,0)
    
    def reset(self):
        self.value = 0
        self.colour = (0,0,0)


class Piece:
    def __init__(self):
        self.tetrimono = random.choice(SHAPE_LIST)
        self.coords = self.tetrimono[0]
        self.type = self.tetrimono[1]
        self.offset = (0,5)
        self.shape = [(coords[0]+self.offset[0],coords[1]+self.offset[1]) for coords in self.coords]
        self.colour = random.choice(COLOURS)
    
    def reset(self):
        self.tetrimono = random.choice(SHAPE_LIST)
        self.coords = self.tetrimono[0]
        self.type = self.tetrimono[1]
        self.offset = (0,5)
        self.shape = [(coords[0]+self.offset[0],coords[1]+self.offset[1]) for coords in self.coords]
        self.colour = random.choice(COLOURS)
    
    def move(self,x,y):
        self.offset = (self.offset[0]+y,self.offset[1]+x)
        self.shape = [(coords[0]+self.offset[0],coords[1]+self.offset[1]) for coords in self.coords]
    
    def rotate(self):
        if self.type != "O":
            self.coords = [(-coord[1],coord[0]) for coord in self.coords]
            self.shape = [(coords[0]+self.offset[0],coords[1]+self.offset[1]) for coords in self.coords]



def main():
    clock = pygame.time.Clock()
    pygame.font.init()
    state = "Menu"
    run = True
    while run:
        WIN.fill((0,0,0))
        clock.tick(60)
        if state == "Menu":
            state = runMenu()
        elif state == "Game":
            state = runGame()
        elif state == "Quit":
            pygame.quit()
            run = False


def runMenu():
    run = True
    pygame.draw.rect(WIN,(245,245,220),pygame.Rect(275, 400, 150, 50))
    font = pygame.font.Font('freesansbold.ttf', 32)
    buttonText = font.render('PLAY', True, (0,0,0))
    font2 = pygame.font.Font('freesansbold.ttf', 60)
    title = font2.render('Tetris', True, (245,245,220))
    WIN.blit(buttonText,(310,410))
    WIN.blit(title,(265,250))
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 275 <= mouse[0] <= 425 and 400 <= mouse[1] <= 450:
                    return "Game"

        pygame.display.update()

def runGame():
    board = Board()
    piece = Piece()
    running = True
    clock = pygame.time.Clock()
    tick = 0
    speed = 20
    font = pygame.font.Font('freesansbold.ttf', 20)

    while running:
        tick+=1
        clock.tick(60)
        WIN.fill((0,0,0))
        score = font.render('Score: '+str(board.score), True, (245,245,220))
        WIN.blit(score,(550,50))
        moves = font.render('Use wasd or arrow keys to move pieces (up to rotate a piece)', True, (245,245,220))
        WIN.blit(moves,(50,650))
        pygame.draw.rect(WIN,(245,245,220),pygame.Rect(45, 45, 70, 35))
        back = font.render('BACK', True, (0,0,0))
        WIN.blit(back,(50,50))

        if speed>2:
            speed = 20 - (board.score//3000) 

        if tick%4==0:
            move = getPlayerMove(board, piece)
            if move == "Quit":
                return "Quit"
            elif move == "Menu":
                return "Menu"

        if tick%speed == 0:
            piece.move(0,1)
            if not validMove(piece, board):
                piece.move(0,-1)

                if outOfBounds(piece):
                    running = False

                board.addPiece(piece)

                board.removeFullRows()
                piece.reset()



        drawBoard(board, piece)
        pygame.display.update()
    return "Menu"


def addBackground():
    print("Hi")

def getPlayerMove(board, piece):
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 45 <= mouse[0] <= 115 and 45 <= mouse[1] <= 80:
                    return "Menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    piece.rotate()
                    if not validMove(piece, board):
                        piece.move(1,0)
                        if not validMove(piece, board):
                            piece.move(-2,0)
                            if not validMove(piece, board):
                                piece.move(1,0)
                                piece.rotate()
                                piece.rotate()
                                piece.rotate()

    keysPressed = pygame.key.get_pressed()
    if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
        piece.move(-1,0)
        if not validMove(piece, board):
            piece.move(1,0)
    if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
        piece.move(1,0)
        if not validMove(piece, board):
            piece.move(-1,0)
    if keysPressed[pygame.K_s] or keysPressed[pygame.K_DOWN]:
        piece.move(0,1)
        if not validMove(piece, board):
            piece.move(0,-1)
    
    return "nothing"


def outOfBounds(piece):
    for tile in piece.shape:
        if tile[0]>=1:
            return False
    return True

def validMove(piece, board):
    for tile in piece.shape:
        if tile[0]>20 or tile[1]<0 or tile[1]>9:
            return False
        if tile[0]>=0:
            if board.board[tile[0]][tile[1]].value == 1:
                return False
    return True

def drawBoard(board, piece):
    x = 225
    y = 100 
    for i in range(21):
        if i>0:
            for j in range(10):
                colour = board.board[i][j].colour
                if (i,j) in piece.shape:
                    colour = piece.colour
                pygame.draw.rect(WIN,colour,pygame.Rect(x, y, 25, 25))
                pygame.draw.rect(WIN,(245,245,220),pygame.Rect(x, y, 25, 25),1)
                x+=25
            x=225
            y+=25




if __name__ == "__main__":
    main()