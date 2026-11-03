# Pygame Initialization
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pieceOffset = 50

# Texture loading

textures = []

def textureSetup(textures):
    textures.append(pygame.image.load("img/black-pawn.png"))
    textures.append(pygame.image.load("img/black-rook.png"))
    textures.append(pygame.image.load("img/black-knight.png"))
    textures.append(pygame.image.load("img/black-bishop.png"))
    textures.append(pygame.image.load("img/black-queen.png"))
    textures.append(pygame.image.load("img/black-king.png"))

    textures.append(pygame.image.load("img/white-pawn.png"))
    textures.append(pygame.image.load("img/white-rook.png"))
    textures.append(pygame.image.load("img/white-knight.png"))
    textures.append(pygame.image.load("img/white-bishop.png"))
    textures.append(pygame.image.load("img/white-queen.png"))
    textures.append(pygame.image.load("img/white-king.png"))

textureSetup(textures)

for i in range(12):
    textures[i] = pygame.transform.scale(textures[i], (100, 100))

# --------------- p = pawn, r = rook, n = knight, b = bishop, q = queen, k = king. lowercase letters = black, uppercase letters = white ---------------

piecesDict = {
    "p" : 0,
    "r" : 1,
    "n" : 2, 
    "b" : 3,
    "q" : 4,
    "k" : 5,
    "P" : 6,
    "R" : 7,
    "N" : 8,
    "B" : 9,
    "Q" : 10,
    "K" : 11
}

# Board renderer
def drawBoard(screen, posFrom, posTo):
    for i in range(8):
        for j in range(8):
            color = (255, 221, 171)
            if (i + j) % 2 == 1: # colors the squares based on their position 
                color = (168, 105, 62)
            if posFrom is not None and posTo is not None: # Checks if a piece just moved from / to that square and colors it consequently
                if posFrom == [j, i] or posTo == [j, i]:
                    if (i + j) % 2 == 1:
                        color = (170, 162, 58)
                    else:
                        color = (205, 210, 106)
            elif posFrom is not None and posTo == None:
                if posFrom == [j, i]:
                    if (i + j) % 2 == 1:
                        color = (170, 162, 58)
                    else:
                        color = (205, 210, 106)
            pygame.draw.rect(screen, color, (i * WIDTH / 8, j * HEIGHT / 8, WIDTH / 8, HEIGHT / 8))

# Pieces renderer
def drawPieces(screen, board):
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[j][i] == None: # Checks whether there are pieces in the square
                continue 
            else:
                screen.blit(textures[piecesDict.get(board[j][i])],  (i * WIDTH / 8, j * HEIGHT / 8))

# Initial board configuration
def boardInit():
    return [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None, None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None, None], 
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

# Returns the board position given a screen position (this could be optimized with mod operations)
def getPiece(pos):
    for i in range(8):
        for j in range(8):
            if pos[0] >= i * 100 and pos[0] < (i + 1) * 100 and pos[1] >= j * 100 and pos[1] < (j + 1) * 100:
                boardPos = [j, i]
                return boardPos
            
# Renders the piece if it is being held
def drawMovingPiece(screen, mousePos, piece):
    screen.blit(textures[piecesDict.get(piece)], (mousePos[0] - pieceOffset, mousePos[1] - pieceOffset))

# Checks whether it is a valid move and moves the selected piece
def movePiece(board, pieceType, pos, oldPos):
    if (isValidMove(board, pieceType, pos, oldPos)):
        board[pos[0]][pos[1]] = pieceType
        return True
    return False

# Returns true if the move follows chess ruleset    
def isValidMove(board, pieceType, pos, oldPos):
    if pieceType.lower() == 'r':
        validPos = getValidPositionsForRook(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    elif pieceType.lower() == 'n':
        validPos = getValidPositionsForKnight(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    elif pieceType.lower() == 'b':
        validPos = getValidPositionsForBishop(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    elif pieceType.lower() == 'k':
        validPos = getValidPositionsForKing(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    elif pieceType.lower() == 'q':
        validPos = getValidPositionsForQueen(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    elif pieceType.lower() == 'p':
        validPos = getValidPositionsForPawn(board, oldPos, pieceType)
        if validPos != None:
            for i in validPos:
                if pos == i and i != oldPos:
                    return True
    return False

# Each one of the next functions, returns [[,],[,],[,],[,], ...] with the valid positions

def getValidPositionsForRook(board, pos, pieceType):
    validPos = []
    
    for i in range(pos[0] + 1, 8):
        if board[i][pos[1]] != None:
            if board[i][pos[1]].isupper() != pieceType.isupper():
                validPos.append([i, pos[1]])
            break
        else:
            validPos.append([i, pos[1]])
    for i in range(pos[0] - 1, -1, -1):
        if board[i][pos[1]] != None:
            if board[i][pos[1]].isupper() != pieceType.isupper():
                validPos.append([i, pos[1]])
            break
        else:
            validPos.append([i, pos[1]])
    for j in range(pos[1] + 1, 8):
        if board[pos[0]][j] != None:
            if board[pos[0]][j].isupper() != pieceType.isupper():
                validPos.append([pos[0], j])
            break    
        else:
            validPos.append([pos[0], j])
    for j in range(pos[1] - 1, -1, -1):
        if board[pos[0]][j] != None:
            if board[pos[0]][j].isupper() != pieceType.isupper():
                validPos.append([pos[0], j])
            break
        else:
            validPos.append([pos[0], j])
    return validPos

def getValidPositionsForKnight(board, pos, pieceType):
    validPos = []

    for i in range(-2, 3, 1):
        if i == 0:
            continue
        for k in range(-1, 2, 2):

            if i < 0:
                j = k * (3 + i)
            else:
                j = k * (3 - i)
            if pos[0] + i < 0 or pos[0] + i >= 8 or pos[1] + j < 0 or pos[1] + j >= 8:
                continue
            if board[pos[0] + i][pos[1] + j] != None:
                if board[pos[0] + i][pos[1] + j].isupper() != pieceType.isupper():
                    validPos.append([pos[0] + i,pos[1] + j])
            else:
                validPos.append([pos[0] + i, pos[1] + j])
    return validPos        

def getValidPositionsForBishop(board, pos, pieceType):
    validPos = []

    for i in range(min(8 - pos[0], 8 - pos[1])):
        if board[pos[0] + i][pos[1] + i] != None:
            if board[pos[0] + i][pos[1] + i].isupper() != pieceType.isupper():
                validPos.append([pos[0] + i, pos[1] + i])
            break
        else:
            validPos.append([pos[0] + i, pos[1] + i])
    for i in range(min(8 - pos[0], pos[1] + 1)):
        if board[pos[0] + i][pos[1] - i] != None:
            if board[pos[0] + i][pos[1] - i].isupper() != pieceType.isupper():
                validPos.append([pos[0] + i, pos[1] - i])
            break
        else:
            validPos.append([pos[0] + i, pos[1] - i])
    for i in range(min(pos[0] + 1, 8 - pos[1])):
        if board[pos[0] - i][pos[1] + i] != None:
            if board[pos[0] - i][pos[1] + i].isupper() != pieceType.isupper():
                validPos.append([pos[0] - i, pos[1] + i])
            break
        else:
            validPos.append([pos[0] - i, pos[1] + i])
    for i in range(min(pos[0] + 1, pos[1] + 1)):
        if board[pos[0] - i][pos[1] - i] != None:
            if board[pos[0] - i][pos[1] - i].isupper() != pieceType.isupper():
                validPos.append([pos[0] - i, pos[1] - i])
            break
        else:
            validPos.append([pos[0] - i, pos[1] - i])

    while validPos.count(pos) > 0:
        validPos.remove(pos)
    
    return validPos     
# -----------  MISSING CASTLING  --------------- #
def getValidPositionsForKing(board, pos, pieceType):
    validPos = []
    for i in range(max(pos[0] - 1, 0), min(pos[0] + 2, 8)):
        for j in range(max(pos[1] - 1, 0), min(pos[1] + 2, 8)):
            if i == pos[0] and j == pos[1]:
                continue
            if board[i][j] == None or board[i][j].isupper() != pieceType.isupper():
                validPos.append([i, j])
    return validPos

def getValidPositionsForQueen(board, pos, pieceType):
    validPos = []
    # ROOK PART
    for i in range(pos[0] + 1, 8):
        if board[i][pos[1]] != None:
            if board[i][pos[1]].isupper() != pieceType.isupper():
                validPos.append([i, pos[1]])
            break
        else:
            validPos.append([i, pos[1]])
    for i in range(pos[0] - 1, -1, -1):
        if board[i][pos[1]] != None:
            if board[i][pos[1]].isupper() != pieceType.isupper():
                validPos.append([i, pos[1]])
            break
        else:
            validPos.append([i, pos[1]])
    for j in range(pos[1] + 1, 8):
        if board[pos[0]][j] != None:
            if board[pos[0]][j].isupper() != pieceType.isupper():
                validPos.append([pos[0], j])
            break    
        else:
            validPos.append([pos[0], j])
    for j in range(pos[1] - 1, -1, -1):
        if board[pos[0]][j] != None:
            if board[pos[0]][j].isupper() != pieceType.isupper():
                validPos.append([pos[0], j])
            break
        else:
            validPos.append([pos[0], j])
    # BISHOP PART
    for i in range(min(8 - pos[0], 8 - pos[1])):
        if board[pos[0] + i][pos[1] + i] != None:
            if board[pos[0] + i][pos[1] + i].isupper() != pieceType.isupper():
                validPos.append([pos[0] + i, pos[1] + i])
            break
        else:
            validPos.append([pos[0] + i, pos[1] + i])
    for i in range(min(8 - pos[0], pos[1] + 1)):
        if board[pos[0] + i][pos[1] - i] != None:
            if board[pos[0] + i][pos[1] - i].isupper() != pieceType.isupper():
                validPos.append([pos[0] + i, pos[1] - i])
            break
        else:
            validPos.append([pos[0] + i, pos[1] - i])
    for i in range(min(pos[0] + 1, 8 - pos[1])):
        if board[pos[0] - i][pos[1] + i] != None:
            if board[pos[0] - i][pos[1] + i].isupper() != pieceType.isupper():
                validPos.append([pos[0] - i, pos[1] + i])
            break
        else:
            validPos.append([pos[0] - i, pos[1] + i])
    for i in range(min(pos[0] + 1, pos[1] + 1)):
        if board[pos[0] - i][pos[1] - i] != None:
            if board[pos[0] - i][pos[1] - i].isupper() != pieceType.isupper():
                validPos.append([pos[0] - i, pos[1] - i])
            break
        else:
            validPos.append([pos[0] - i, pos[1] - i])
    
    return validPos
# ----------  MISSING EN PASSANT  ------------- #
def getValidPositionsForPawn(board, pos, pieceType):
    validPos = []
    if pieceType.isupper() == True:
        if pos[0] != 0:
            if board[pos[0] - 1][pos[1]] == None:
                validPos.append([pos[0] - 1, pos[1]])
            if pos[0] == 6:
                if board[pos[0] - 2][pos[1]] == None:
                    validPos.append([pos[0] - 2, pos[1]])
            if pos[1] != 0:
                if board[pos[0] - 1][pos[1] - 1] != None and board[pos[0] - 1][pos[1] - 1].isupper() == False:
                    validPos.append([pos[0] - 1, pos[1] - 1])
            if pos[1] != 7:
                if board[pos[0] - 1][pos[1] + 1] != None and board[pos[0] - 1][pos[1] + 1].isupper() == False:
                    validPos.append([pos[0] - 1, pos[1] + 1])
    else:
        if pos[0] != 7:
            if board[pos[0] + 1][pos[1]] == None:
                validPos.append([pos[0] + 1, pos[1]])
            if pos[0] == 1:
                if board[pos[0] + 2][pos[1]] == None:
                    validPos.append([pos[0] + 2, pos[1]])
            if pos[1] != 0:
                if board[pos[0] + 1][pos[1] - 1] != None and board[pos[0] + 1][pos[1] - 1].isupper() == True:
                    validPos.append([pos[0] + 1, pos[1] - 1])
            if pos[1] != 7:
                if board[pos[0] + 1][pos[1] + 1] != None and board[pos[0] + 1][pos[1] + 1].isupper() == True:
                    validPos.append([pos[0] + 1, pos[1] + 1])
    return validPos
    
def notMovePiece(board, pieceType, pos):
    board[pos[0]][pos[1]] = pieceType

def main():
    run = True
    clock = pygame.time.Clock()

    selectedPiece = None
    currPos = None
    newPos = None
    selectedSquare = None

    # 0 = white, 1 = black
    turn = 0

    board = boardInit()

    while run:
        screen.fill('black')
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: # Logic for choosing the selected squares
                mousetype = pygame.mouse.get_pressed()
                if mousetype[0] == True:
                    mousepos = pygame.mouse.get_pos()
                    selectedPiece = getPiece(mousepos)
                    selectedPieceType = board[selectedPiece[0]][selectedPiece[1]]
                    if selectedPieceType != None and selectedPieceType.isupper() == turn:
                        selectedPiece = None
                        selectedPieceType = None
                        break
                    selectedSquare = None
                    if selectedPieceType == None:
                        selectedPiece = None
                    else:
                        board[selectedPiece[0]][selectedPiece[1]] = None
            if event.type == pygame.MOUSEBUTTONUP:
                mousetype = pygame.mouse.get_pressed()
                if mousetype[0] == False:
                    if selectedPiece != None:
                        mousepos = pygame.mouse.get_pos()
                        newPos = getPiece(mousepos)
                        if newPos == selectedPiece:
                            selectedSquare = selectedPiece
                            notMovePiece(board, selectedPieceType, newPos)
                        else:
                            movable = movePiece(board, selectedPieceType, newPos, selectedPiece)
                            if not movable:
                                notMovePiece(board, selectedPieceType, selectedPiece)
                                currPos = selectedPiece
                                newPos = None
                                selectedSquare = selectedPiece
                            else:
                                turn = not turn
                                currPos = selectedPiece
                                selectedSquare = None
                                selectedPiece = None
                                selectedPieceType = None

        # Render
        drawBoard(screen, currPos, newPos)
        drawPieces(screen, board)
        
        if selectedPiece != None and selectedSquare == None:
            mousePos = pygame.mouse.get_pos()
            drawMovingPiece(screen, mousePos, selectedPieceType)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()