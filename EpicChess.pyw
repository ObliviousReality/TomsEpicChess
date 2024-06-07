import pygame  # Imports the necessary functions for the game
import math
from time import sleep
from random import randint
from lib.transfer import numtolet # Imports functions that are in seperate files.
from lib.cell_detect2 import detect

pygame.init()  #Initialises all of the pygame modules

display_width = 950 # The size of the display
display_height = 750
gameDisplay = pygame.display.set_mode((display_width, display_height)) # Creates the display
pygame.display.set_caption("Tom's Epic Chess") # Sets the title of the display (written at the top of the screen)
clock = pygame.time.Clock() # Creates a clock used to sync framerates
crashed = False # Variable that controls whether the game is running.
bcolour = (122, 66, 244) # Background colour of the window.
gameIcon = pygame.image.load('pics\misc\gradient.png')
pygame.display.set_icon(gameIcon)

#Constants:
gridsize = 80 # The size of cells
displacement = 30 # Distance between the edge of the screen and the board
black = (0, 0, 0) # Colour variables.
white = (250, 250, 255)
red=(255,0,0)
yellow=(255,255,0)

#Shapes:
quitbutton = pygame.Rect(display_width - 100, display_height - 50, 100, 50) # Creates rectangles for future use. They have top left coordinates and dimensions.
textcentre = display_width - math.ceil((display_width - 8 * gridsize - 60) / 2)
checkyes = pygame.Rect(700, display_height - 205, 250, 50)

#Variables:
select = 0 # If a first piece has been selected
select2 = 0 # If a second piece has been selected
selected = 0 # If the first selected piece is a piece (not an empty cell)
toclear = 0 # Whether to reset variables or not
text3 = "Left click a cell to select a piece." # Informational text
text3x = 0 # offset of informational text
turns = 1 # Turncounter
go = 1 # Turncounter used to calculate whos turn it is. # Could be combined with turns
quitcolour = (0, 107, 249) # Colour of quit text
selectedpiece = "None" # Name of the piece that has been selected
quitpresses = 0 # Number of times the quit button has been pressed. At two the game quits.
invalidcounter = 0 # Timer for length of time text3 is red. 
tocountic = 0 # Whether to change colour of text3 to red
countquit = 0 # Whether to begin the quit counter
quitcounter = 0 # Timer used for length of time between quit presses
check = False # Whether a king is in check
whattext3 = 0 # Which variation of text3 to use
takenpieces = [] # Array of taken pieces
sidex = 750 # x coord of taken piece display
sidey = 240 # y coord of taken piece display
blackscore = 0 # Score of the black team
whitescore = 0 # Score of the white team
tcounter = 0 # Counter used to cycle through the taken pieces array
checkmate = False # Whether a team is in checkmate
victory = False # Whether to run the victory loop displaying the victory screen.
checked = False
lastpiecemoved = "None" # Name of the last piece to be moved
image2 = pygame.image.load("pics\misc\endscreen.png") # Image used on the endscreen
bf = open("lib\\bwins.txt", "r") # Files containing win numbers
wf = open("lib\wwins.txt", "r")
bwins = str(bf.read())
wwins = str(wf.read())
bf.close()
wf.close()
alt=False # Variables used so the game can be closed using alt-F4
f4=False

pieces = [["WPawn1", [1, 2]], ["WPawn2", [2, 2]], ["WPawn3", [3, 2]], ["WPawn4", [4, 2]], ["WPawn5", [5, 2]], ["WPawn6", [6, 2]], ["WPawn7", [7, 2]], ["WPawn8", [8, 2]], ["BPawn1", [1, 7]], ["BPawn2", [2, 7]], ["BPawn3", [3, 7]], ["BPawn4", [4, 7]], ["BPawn5", [5, 7]], ["BPawn6", [6, 7]], ["BPawn7", [7, 7]], ["BPawn8", [8, 7]], ["WCastle1", [1, 1]], ["WHorse1", [2, 1]], ["WBishop1", [3, 1]], ["WQueen", [5, 1]], ["WKing", [4, 1]], ["WBishop2", [6, 1]], ["WHorse2", [7, 1]], ["WCastle2", [8, 1]], ["BCastle1", [1, 8]], ["BHorse1", [2, 8]], ["BBishop1", [3, 8]], ["BQueen", [5, 8]], ["BKing", [4, 8]], ["BBishop2", [6, 8]], ["BHorse2", [7, 8]], ["BCastle2", [8, 8]]]
#[piece,[x,y]] # 3D array of all the pieces and their coordinates. 

#########################################################################################################################################
pawnw = pygame.image.load("pics\white\\pawn.png") # Image variables
pawnb = pygame.image.load("pics\\black\pawn.png")
queenw = pygame.image.load("pics\white\queen.png")
queenb = pygame.image.load("pics\\black\queen.png")
horsew = pygame.image.load("pics\white\horse.png")
horseb = pygame.image.load("pics\\black\horse.png")
bishopw = pygame.image.load("pics\white\\bishop.png")
bishopb = pygame.image.load("pics\\black\\bishop.png")
kingw = pygame.image.load("pics\white\king.png")
kingb = pygame.image.load("pics\\black\king.png")
castlew = pygame.image.load("pics\white\castle.png")
castleb = pygame.image.load("pics\\black\castle.png")

def images(image, x, y): # Function used to put images on the screen
    gameDisplay.blit(image, (x, y))


def winnerf(image, x, y): # Function used to put images on the screen
    gameDisplay.blit(image, (x, y))


def textinit(text, font): # Initialises text for dislay, setting colour as yellow. 
    textp = font.render(text, True, (255, 255, 0))
    return textp, textp.get_rect()


def location3(text3): # Puts the informational text on the screen
    thefont = pygame.font.Font("lib\din1451a.ttf", 40) # Font is provided in a file, size is 40
    if text3 == "Invalid Move":
        text3S, text3R = pieceinit(text3, thefont, (255, 0, 0)) # Sets colour to red
    else:
        text3S, text3R = pieceinit(text3, thefont, (255, 255, 0)) # Sets colour to yellow
    text3R.center = ((text3x), (display_height - 25)) # Sets location
    gameDisplay.blit(text3S, text3R) # Puts it onto the screen


def location4(num, n): # Coords of grid
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    text4S, text4R = textinit(num, thefont)
    text4R.center = ((70 + n * gridsize), (15))
    gameDisplay.blit(text4S, text4R)


def location5(num, n): # Coords of grid
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    text5S, text5R = textinit(num, thefont)
    text5R.center = ((15), (70 + n * gridsize))
    gameDisplay.blit(text5S, text5R)


def location6(turn): # Turn counter
    turn = "Turn " + turn
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    text6S, text6R = textinit(turn, thefont)
    text6R.center = ((textcentre), (30))
    gameDisplay.blit(text6S, text6R)


def location7(selectedpiece): # Displays which piece has been selected
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    text7S, text7R = textinit(selectedpiece, thefont)
    text7R.center = ((textcentre), (175))
    gameDisplay.blit(text7S, text7R)


def location8(go): # Display who's go it is
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    if go % 2 == 0: # White plays first, and go starts at 1, so it is black's turn when go is positive
        go = str("Black to play")
        text8S, text8R = pieceinit(go, thefont, (0, 0, 0))
    else:
        go = str("White to play") # White play when go is negative
        text8S, text8R = pieceinit(go, thefont, (255, 255, 255))
    go = go + " to play."
    text8R.center = ((textcentre), (80))
    gameDisplay.blit(text8S, text8R)


def location9(text, quitcolour, x, y): # General purpose text function
    thefont = pygame.font.SysFont("Bahnschrift", 40)
    text9S, text9R = pieceinit(text, thefont, quitcolour)
    text9R.center = (((display_width - x)), math.ceil((display_height - y)))
    gameDisplay.blit(text9S, text9R)


def location10(text):
    thefont = pygame.font.Font("lib\din1451a.ttf", 40)
    text10S, text10R = textinit(text, thefont)
    text10R.center = ((textcentre), (135))
    gameDisplay.blit(text10S, text10R)


def sideinit(text, font, colour): # Sets font settings for taken pieces
    if colour == "B":
        dcolour = (0, 0, 0)
    else:
        dcolour = (255, 255, 255)
    textp = font.render(text, True, dcolour)
    return textp, textp.get_rect()


def sidepieces(x, y, piece, colour): # Displays taken pieces
    thefont = pygame.font.Font("lib\din1451a.ttf", 30)
    textsS, textsR = sideinit(str(piece), thefont, colour)
    textsR.center = (x, y)
    gameDisplay.blit(textsS, textsR)


def scores(x, y, piece, colour): # Displays scores
    thefont = pygame.font.Font("lib\din1451a.ttf", 50)
    textSS, textSR = sideinit(str(piece), thefont, colour)
    textSR.center = (x, y)
    gameDisplay.blit(textSS, textSR)


def pieceinit(text, font, colour): # General purpose initialisation function, used for pieces initially.
    textp = font.render(text, True, (colour))
    return textp, textp.get_rect()


def whitepieces(x, y, piece): # Displays pieces on the board as text (Discontinued)
    thefont = pygame.font.Font("lib\din1451a.ttf", 50)
    textwS, textwR = pieceinit(str(piece), thefont, (255, 0, 0))
    textwR.center = ((((gridsize * x) - 10)), (((gridsize * y) - 10)))
    gameDisplay.blit(textwS, textwR)


def drawpieces(x, y, piece): # Displays pieces on the board as text (Discontinued)
    thefont = pygame.font.Font("lib\din1451a.ttf", 50)
    pcolour = piece[0]
    if pcolour == "W":
        pcolour = (255, 0, 0)
    elif pcolour == "B":
        pcolour = (0, 0, 255)
    textwS, textwR = pieceinit(str(piece[1]), thefont, (pcolour))
    textwR.center = ((((gridsize * x) - 10)), (((gridsize * y) - 10)))
    gameDisplay.blit(textwS, textwR)


def blackpieces(x, y, piece): # Displays pieces on the board as text (Discontinued)
    thefont = pygame.font.Font("lib\din1451a.ttf", 50)
    textbS, textbR = pieceinit(str(piece), thefont, (0, 0, 255))
    textbR.center = ((((gridsize * x) - 10)), (((gridsize * y) - 10)))
    gameDisplay.blit(textbS, textbR)


####
def write(text,font,size,colour,pos): # General purpose function for writing text using top left coords instead of centre coords. 
    font = pygame.font.SysFont(font, size)
    gameDisplay.blit(testinit(text, font, colour),pos)


def testinit(x,font,colour):
    testp=font.render(x, True, (colour))
    return testp
####


def whichpiece(xcells, ycells): # Returns piece name and coords from coords
    xy = [xcells, ycells]
    for i in range(0, len(pieces)):
        if pieces[i][1] == xy:
            return pieces[i][0], pieces[i][1]

    return "None", [0, 0]


def whatpiece(xy, cpiece): # Returns true if the piece in the coords is of the opposite colour
    for i in range(0, len(pieces)):
        if pieces[i][1] == xy and cpiece != str(pieces[i][0])[0]:
            return True
    return False


def wherepiece(name): # Takes the name of a piece and returns its location
    for i in range(0, len(pieces)):
        if pieces[i][0] == name:
            return pieces[i][1][0], pieces[i][1][1]


def whatcheck(x, y, colour): # Taking the coords and colour of the selected piece, returns 1 if the colour of the piece is opposite, 2 if the colour is the same or 0 if there is no piece.
    for i in range(0, len(pieces)):
        if pieces[i][1] == [x, y] and colour != str(pieces[i][0])[0]:
            return 1
        elif pieces[i][1] == [x, y] and colour == str(pieces[i][0])[0]:
            return 2
    return 0


def whichpiece2(xcells, ycells): # Takes the coords of a piece and returns its coords as a list or "none" if there is no piece there. 
    xy = [xcells, ycells]
    for i in range(0, len(pieces)):
        if pieces[i][1] == xy:
            return pieces[i][0]

    return "None"


def whichpiece3(xcells, ycells): # Takes the coords of a piece and returns its full description in the list, or "None" if it does not exist. 
    xy = [xcells, ycells]
    for i in range(0, len(pieces)):
        if pieces[i][1] == xy:
            return pieces[i]

    return "None"

#########################################################################################################################################
#Possible moves functions

def up(piecepos, pmoves, colour, pieces): # Checks tiles above a piece to see of they are free.
    x = piecepos[0]
    y = piecepos[1]
    found = False
    c = 1
    while not found:
        if whatcheck(x, y - c, colour) == 1:
            found = True
            pmoves.append([x, y - c])
        elif whatcheck(x, y - c, colour) == 2:
            found = True
        elif y - c < 1:
            found = True
        else:
            pmoves.append([x, y - c])
            c += 1
    return pmoves


def down(piecepos, pmoves, colour, pieces): # Checks tiles below a piece to see of they are free.
    x = piecepos[0]
    y = piecepos[1]
    found = False
    c = 1
    while not found:
        if whatcheck(x, y + c, colour) == 1:
            found = True
            pmoves.append([x, y + c])
        if whatcheck(x, y + c, colour) == 2:
            found = True
        elif y + c > 8:
            found = True
        else:
            pmoves.append([x, y + c])
            c += 1
    return pmoves


def left(piecepos, pmoves, colour, pieces): # Checks tiles to the left a piece to see of they are free.
    x = piecepos[0]
    y = piecepos[1]
    found = False
    c = 1
    while not found:
        if whatcheck(x - c, y, colour) == 1:
            found = True
            pmoves.append([x - c, y])
        elif whatcheck(x - c, y, colour) == 2:
            found = True
        elif x - c < 1:
            found = True
        else:
            pmoves.append([x - c, y])
            c += 1
    return pmoves


def right(piecepos, pmoves, colour, pieces): # Checks tiles to the right a piece to see of they are free.
    x = piecepos[0]
    y = piecepos[1]
    found = False
    c = 1
    while not found:
        if whatcheck(x + c, y, colour) == 1:
            found = True
            pmoves.append([x + c, y])
        elif whatcheck(x + c, y, colour) == 2:
            found = True
        elif x + c > 8:
            found = True
        else:
            pmoves.append([x + c, y])
            c += 1
    return pmoves


def castle(piecepos, pmoves, colour, pieces): # Combines the up down left right functions into 1.
    pmoves += left(piecepos, pmoves, colour, pieces)
    pmoves += up(piecepos, pmoves, colour, pieces)
    pmoves += right(piecepos, pmoves, colour, pieces)
    pmoves += down(piecepos, pmoves, colour, pieces)
    return pmoves


def bishop(piecepos, pmoves, pieces, colour): # Combines the diagonal functions. 
    pmoves += downright2(piecepos, pmoves, pieces, colour)
    pmoves += downleft2(piecepos, pmoves, pieces, colour)
    pmoves += upright2(piecepos, pmoves, pieces, colour)
    pmoves += upleft2(piecepos, pmoves, pieces, colour)
    return pmoves


def downright2(piecepos, pmoves, pieces, colour): # Checks down and to the right of a piece.
    x = piecepos[0]
    y = piecepos[1]
    c = 1
    stop = False
    while not stop:
        cxy = [x + c, y + c]
        if x + c > 8 or y + c > 8:
            stop = True
        elif whatpiece(cxy, colour):
            pmoves.append(cxy)
            stop = True
        elif whichpiece2(cxy[0], cxy[1]) != "None":
            stop = True
        else:
            pmoves.append(cxy)
            c += 1
    return pmoves


def downleft2(piecepos, pmoves, pieces, colour): # Checks down and to the left of a piece. 
    x = piecepos[0]
    y = piecepos[1]
    c = 1
    stop = False
    while not stop:
        cxy = [x - c, y + c]
        if x - c < 1 or y + c > 8:
            stop = True
        elif whatpiece(cxy, colour):
            pmoves.append(cxy)
            stop = True
        elif whichpiece2(cxy[0], cxy[1]) != "None":
            stop = True
        else:
            pmoves.append(cxy)
            c += 1
    return pmoves


def upright2(piecepos, pmoves, pieces, colour):
    x = piecepos[0]
    y = piecepos[1]
    c = 1
    stop = False
    while not stop:
        cxy = [x + c, y - c]
        if x + c > 8 or y - c < 1:
            stop = True
        elif whatpiece(cxy, colour):
            pmoves.append(cxy)
            stop = True
        elif whichpiece2(cxy[0], cxy[1]) != "None":
            stop = True
        else:
            pmoves.append(cxy)
            c += 1
    return pmoves


def upleft2(piecepos, pmoves, pieces, colour):
    x = piecepos[0]
    y = piecepos[1]
    c = 1
    stop = False
    while not stop:
        cxy = [x - c, y - c]
        if x - c < 1 or y - c < 1:
            stop = True
        elif whatpiece(cxy, colour):
            pmoves.append(cxy)
            stop = True
        elif whichpiece2(cxy[0], cxy[1]) != "None":
            stop = True
        else:
            pmoves.append(cxy)
            c += 1
    return pmoves


def horse(x, y, pmoves, pieces, colour):
    movx1 = 2
    movx2 = 1
    movy1 = 1
    movy2 = 2
    hmoves = []
    for i in range(-1, 2):
        if i == 0:
            pass
        else:
            if x + (movx1 * i) > 0 and x + (movx1 * i) <= 8 and y + (movy1 * i) > 0 and y + (movy1 * i) <= 8:
                hmoves.append([x + (movx1 * i), y + (movy1 * i)])
            if x + (movx2 * i) > 0 and x + (movx2 * i) <= 8 and y + (movy2 * i) > 0 and y + (movy2 * i) <= 8:
                hmoves.append([x + (movx2 * i), y + (movy2 * i)])
            if x + (movx1 * i) > 0 and x + (movx1 * i) <= 8 and y + (movy1 * -i) > 0 and y + (movy1 * -i) <= 8:
                hmoves.append([x + (movx1 * i), y + (movy1 * -i)])
            if x + (movx2 * i) > 0 and x + (movx2 * i) <= 8 and y + (movy2 * -i) > 0 and y + (movy2 * -i) <= 8:
                hmoves.append([x + (movx2 * i), y + (movy2 * -i)])
    for i in hmoves:
        if whatcheck(i[0], i[1], colour) == 2:
            pass
        else:
            pmoves.append(i)
    return pmoves


def pawn(piecepos, pmoves, cpeice, leftm, rightm, frontm, vfrontm, pieces):
    x = piecepos[0]
    y = piecepos[1]
    if cpeice == "W":
        if y == 2:
            movx = 0
            movy = 2
        else:
            movx = 0
            movy = 1
        for i in range(1, movy + 1):
            pmoves.append([x, y + i])
        if leftm:
            pmoves.append([x - 1, y + 1])
        if rightm:
            pmoves.append([x + 1, y + 1])
        if frontm:
            pmoves.remove([x, y + 1])
        if vfrontm and y == 2:
            pmoves.remove([x, y + 2])
        if frontm and y == 2:
            pmoves.remove([x, y + 2])
    elif cpeice == "B":
        if y == 7:
            movx = 0
            movy = 2
        else:
            movx = 0
            movy = 1
        for i in range(1, movy + 1):
            pmoves.append([x, y - i])
        if leftm:
            pmoves.append([x - 1, y - 1])
        if rightm:
            pmoves.append([x + 1, y - 1])
        if frontm:
            pmoves.remove([x, y - 1])
        if vfrontm and y == 7:
            pmoves.remove([x, y - 2])
        if frontm and y == 7:
            pmoves.remove([x, y - 2])
    return(pmoves)


def king(piecepos, pmoves, pieces, colour):
    x = piecepos[0]
    y = piecepos[1]
    kmoves = []
    for i in range(-1, 2):
        if i == 0:
            pass
        else:
            if x + i > 0 and x + i <= 8:
                kmoves.append([x + i, y])
            if y + i > 0 and y + i <= 8:
                kmoves.append([x, y + i])
            for j in range(-1, 2):
                if i == 0:
                    pass
                else:
                    if x + i > 0 and x + i <= 8 and y + j > 0 and y + j <= 8:
                        kmoves.append([x + i, y + j])
    for i in kmoves:
        if whatcheck(i[0], i[1], colour) == 2:
            pass
        elif colour == "W":
            if checkcheck(i[0], i[1], "W"):
                pass
            else:
                pmoves.append(i)
        else:
            if checkcheck(i[0], i[1], "B"):
                pass
            else:
                pmoves.append(i)
    return(pmoves)

#########################################################################################################################################


def newright(x, y, colour):
    found = False
    check = False
    c = 1
    poss = ["C", "Q"]
    notposs = ["B", "P", "K", "H"]
    while not found:
        if whatcheck(x + c, y, colour) == 1 and whichpiece2(x + c, y)[1] in poss:
            found = True
            check = True
            break
        elif whatcheck(x + c, y, colour) == 2:
            found = True
            check = False
            break
        elif whatcheck(x + c, y, colour) == 1 and whichpiece2(x + c, y)[1] in notposs:
            found = True
            check = False
            break
        elif x + c > 8:
            found = True
            check = False
            break
        else:
            c += 1
    return check


def newleft(x, y, colour):
    found = False
    check = False
    c = 1
    poss = ["C", "Q"]
    notposs = ["B", "P", "K", "H"]
    while not found:
        if whatcheck(x - c, y, colour) == 1 and whichpiece2(x - c, y)[1] in poss:
            found = True
            check = True
            break
        elif whatcheck(x - c, y, colour) == 2:
            found = True
            check = False
            break
        elif whatcheck(x - c, y, colour) == 1 and whichpiece2(x - c, y)[1] in notposs:
            found = True
            check = False
            break
        elif x - c < 0:
            found = True
            check = False
            break
        else:
            c += 1
    return check


def newdown(x, y, colour):
    found = False
    check = False
    c = 1
    poss = ["C", "Q"]
    notposs = ["B", "P", "K", "H"]
    while not found:
        if whatcheck(x, y + c, colour) == 1 and whichpiece2(x, y + c)[1] in poss:
            found = True
            check = True
            break
        elif whatcheck(x, y + c, colour) == 2:
            found = True
            check = False
            break
        elif whatcheck(x, y + c, colour) == 1 and whichpiece2(x, y + c)[1] in notposs:
            found = True
            check = False
            break
        elif y + c > 8:
            found = True
            check = False
            break
        else:
            c += 1
    return check


def newup(x, y, colour):
    found = False
    check = False
    c = 1
    poss = ["C", "Q"]
    notposs = ["B", "P", "K", "H"]
    while not found:
        if whatcheck(x, y - c, colour) == 1 and whichpiece2(x, y - c)[1] in poss:
            found = True
            check = True
            break
        elif whatcheck(x, y - c, colour) == 2:
            found = True
            check = False
            break
        elif whatcheck(x, y - c, colour) == 1 and whichpiece2(x, y - c)[1] in notposs:
            found = True
            check = False
            break
        elif y - c < 0:
            found = True
            check = False
            break
        else:
            c += 1
    return check


def horse2(x, y, colour):
    l = []
    check = False
    l = horse(x, y, l, pieces, colour)
    for i in range(0, len(l)):
        if whichpiece2(l[i][0], l[i][1])[0] != colour and whichpiece2(l[i][0], l[i][1])[1] == "H":
            check = True
            break

    return check


def pawn2(x, y, colour):
    check = False
    if colour == "W":
        if whatcheck(x - 1, y + 1, colour) == 1 and whichpiece2(x - 1, y + 1)[1] == "P":
            check = True
        if whatcheck(x + 1, y + 1, colour) == 1 and whichpiece2(x + 1, y + 1)[1] == "P":
            check = True
    if colour == "B":
        if whatcheck(x + 1, y - 1, colour) == 1 and whichpiece2(x + 1, y - 1)[1] == "P":
            check = True
        elif whichpiece2(x + 1, y - 1)[1] == "P" and whichpiece2(x + 1, y - 1)[0] != colour:
            check = True
        elif whatcheck(x - 1, y - 1, colour) == 1 and whichpiece2(x - 1, y - 1)[1] == "P":
            check = True
        elif whichpiece2(x - 1, y - 1)[1] == "P" and whichpiece2(x - 1, y - 1)[0] != colour:
            check = True
    return check


def castle2(x, y, colour):
    if newleft(x, y, colour):
        return True
    elif newup(x, y, colour):
        return True
    elif newright(x, y, colour):
        return True
    elif newdown(x, y, colour):
        return True


def bishop2(x, y, colour):
    c = 1
    found = False
    dr = True
    dl = True
    ur = True
    ul = True
    poss = ["B", "Q"]
    notposs = ["P", "H", "K", "C"]
    while not found:
        # DownRight
        if whichpiece2(x + c, y + c)[0] != colour and whichpiece2(x + c, y + c)[1] in poss and x + c < 9 and y + c < 9 and dr:
            check = True
            found = True
            return check
        elif whichpiece2(x + c, y + c)[0] != colour and whichpiece2(x + c, y + c)[1] in notposs and x + c < 9 and y + c < 9 and dr:
            dr = False
        elif whichpiece2(x + c, y + c)[0] == colour and x + c < 9 and y + c < 9 and dr:
            dr = False
        # DownLeft
        if whichpiece2(x - c, y + c)[0] != colour and whichpiece2(x - c, y + c)[1] in poss and x - c > 0 and y + c < 9 and dl:
            check = True
            found = True
            return check
        elif whichpiece2(x - c, y + c)[0] != colour and whichpiece2(x - c, y + c)[1] in notposs and x - c > 0 and y + c < 9 and dl:
            dl = False
        elif whichpiece2(x - c, y + c)[0] == colour and x - c > 0 and y + c < 9:
            dl = False
        # UpRight
        if whichpiece2(x + c, y - c)[0] != colour and whichpiece2(x + c, y - c)[1] in poss and x + c < 9 and y - c > 0 and ur:
            check = True
            found = True
            return check
        elif whichpiece2(x + c, y - c)[0] != colour and whichpiece2(x + c, y - c)[1] in notposs and x + c < 9 and y - c > 0 and ur:
            ur = False
        elif whichpiece2(x + c, y - c)[0] == colour and x + c < 9 and y - c > 0:
            ur = False
        # UpLeft
        if whichpiece2(x - c, y - c)[0] != colour and whichpiece2(x - c, y - c)[1] in poss and x - c > 0 and y - c > 0 and ul:
            check = True
            found = True
            return check
        elif whichpiece2(x - c, y - c)[0] != colour and whichpiece2(x - c, y - c)[1] in notposs and x - c > 0 and y - c > 0 and ul:
            ul = False
        elif whichpiece2(x - c, y - c)[0] == colour and x - c > 0 and y - c > 0:
            ul = False
        if c > 8:
            return False
        else:
            c += 1


def checkcheck(x, y, colour):
    if bishop2(x, y, colour):
        return True
    if castle2(x, y, colour):
        return True
    if pawn2(x, y, colour):
        return True
    if horse2(x, y, colour):
        return True
    else:
        return False


#########################################################################################################################################


while not crashed:
    # print("refresh")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0):
            xm, ym = pygame.mouse.get_pos()
            xcells, ycells = detect(xm, ym)
            select = 1
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (0, 0, 1):
            xm, ym = pygame.mouse.get_pos()
            xcells2, ycells2 = detect(xm, ym)
            select2 = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitbutton.collidepoint(event.pos) and quitpresses == 1:
                crashed = True
            elif quitbutton.collidepoint(event.pos) and pygame.mouse.get_pressed() == (1, 0, 0):
                quitpresses += 1
                quitcolour = ((249, 0, 0))
                countquit = 1
            elif not quitbutton.collidepoint(event.pos) and quitpresses == 1 and pygame.mouse.get_pressed() == (1, 0, 0):
                quitpresses -= 1
                quitcolour = (0, 107, 249)
                countquit = 0
            if checkyes.collidepoint(event.pos) and checkmate and pygame.mouse.get_pressed() == (1, 0, 0):
                checkmate = True
                if go % 2 == 0:
                    winner = white
                else:
                    winner = black
                victory = True
                if winner == black:
                    bwins = int(bwins)
                    bf = open("lib\\bwins.txt", "w")
                    bf.write((str((bwins + 1))))
                    bf.close()
                else:
                    wwins = int(wwins)
                    wf = open("lib\wwins.txt", "w")
                    wf.write((str((wwins + 1))))
                    wf.close()
                crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                crashed = True
            if event.key == pygame.K_r:
                toclear = 1
            if event.key == pygame.K_RETURN:
                go += 1
                turns += 1
            if event.key == pygame.K_LALT:
                alt=True
            if event.key == pygame.K_F4:
                f4=True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                toclear = 0
            if event.key == pygame.K_LALT:
                alt=False
            if event.key == pygame.K_F4:
                f4=False

    gameDisplay.fill(bcolour)

    for j in range(0, 8):
        for i in range(0, 8):
            if j % 2 == 0:
                if i % 2 == 0:
                    pygame.draw.rect(gameDisplay, white, pygame.Rect(displacement + gridsize * i, displacement + gridsize * j, gridsize, gridsize))
                else:
                    pygame.draw.rect(gameDisplay, black, pygame.Rect(displacement + gridsize * i, displacement + gridsize * j, gridsize, gridsize))
            else:
                if i % 2 == 0:
                    pygame.draw.rect(gameDisplay, black, pygame.Rect(displacement + gridsize * i, displacement + gridsize * j, gridsize, gridsize))
                else:
                    pygame.draw.rect(gameDisplay, white, pygame.Rect(displacement + gridsize * i, displacement + gridsize * j, gridsize, gridsize))

    for i in range(0, len(pieces)):  # THIS IS WHAT MAKE PIECE GO
        # drawpieces(pieces[i][1][0], pieces[i][1][1], str(pieces[i][0])) #LETTERS
        if (pieces[i][0])[1] == "P" and (pieces[i][0])[0] == "W":
            images(pawnw, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "P" and (pieces[i][0])[0] == "B":
            images(pawnb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "Q" and (pieces[i][0])[0] == "W":
            images(queenw, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "Q" and (pieces[i][0])[0] == "B":
            images(queenb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "B" and (pieces[i][0])[0] == "W":
            images(bishopw, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "B" and (pieces[i][0])[0] == "B":
            images(bishopb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "K" and (pieces[i][0])[0] == "W":
            images(kingw, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "K" and (pieces[i][0])[0] == "B":
            images(kingb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "C" and (pieces[i][0])[0] == "W":
            images(castlew, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "C" and (pieces[i][0])[0] == "B":
            images(castleb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "H" and (pieces[i][0])[0] == "W":
            images(horsew, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))
        elif (pieces[i][0])[1] == "H" and (pieces[i][0])[0] == "B":
            images(horseb, 30 + 80 * (pieces[i][1][0] - 1), 30 + 80 * (pieces[i][1][1] - 1))

    pygame.draw.rect(gameDisplay, (20, 58, 119), pygame.Rect(8 * gridsize + 60, 0, display_width - 8 * gridsize + 60, display_height))
    pygame.draw.rect(gameDisplay, (20, 58, 119), pygame.Rect(0, 60 + 8 * gridsize, display_width, display_height))
    pygame.draw.rect(gameDisplay, (215, 66, 244), quitbutton)

    for i in range(0, len(takenpieces)):
        if i > 19:
            sidepieces(sidex + 100, sidey + (i - 20) * 30, takenpieces[i][1], takenpieces[i][0])
        elif i > 9:
            sidepieces(sidex + 50, sidey + (i - 10) * 30, takenpieces[i][1], takenpieces[i][0])
        else:
            sidepieces(sidex, sidey + i * 30, takenpieces[i][1], takenpieces[i][0])

    if tocountic == 1:
        invalidcounter += 1
        if whattext3 == 1:
            text3 = "Invalid Move"
        elif whattext3 == 2:
            text3 = "Check!"
        if invalidcounter == 50:
            tocountic = 0
            invalidcounter = 0
            text3 = "Left click a cell to select a piece."
    else:
        text3 = "Left click a cell to select a piece."

    if countquit == 1:
        quitcounter += 1
        quitcolour = (249, 0, 0)
        if quitcounter == 50:
            countquit = 0
            quitcounter = 0
            quitpresses = 0
            quitcolour = (0, 107, 249)
    else:
        quitcolour = (0, 107, 249)

    text3x = 0
    selectedpiece = ("None")

    xm, ym = pygame.mouse.get_pos()
    xcell, ycell = detect(xm, ym)

    if quitbutton.collidepoint(xm, ym) and quitpresses == 0:
        quitcolour = (255, 93, 0)
    elif not quitbutton.collidepoint(xm, ym) and quitpresses == 0:
        quitcolour = (0, 107, 249)

    if ycell != 0 and xcell != 0:
        if (ycell + xcell) % 2 == 0:
            cellc = (0, 255, 100)
        elif (ycell + xcell) % 2 == 1:
            cellc = (0, 255, 100)
        pygame.draw.rect(gameDisplay, cellc, pygame.Rect(30 + gridsize * (xcell - 1), 30 + gridsize * (ycell - 1), gridsize, gridsize), 5) # Highlight

    if toclear == 1:
        xcells, ycells, xcells2, ycells2 = 0, 0, 0, 0
        select, select2 = 0, 0
        toclear = 0
        selectedpiece = "None"
        checked = False

    if select == 1 and xcells > 0 and ycells > 0 and  whichpiece2(xcells,ycells)!="None":
        selected = 1
        text3 = "Right click a red cell to move the piece."
        text3x = 0
        selectedpiece, piecepos = whichpiece(xcells, ycells)
        piece = (selectedpiece[1])
        pmoves = []
        cpiece = selectedpiece[0]
        if go % 2 == 0:
            pcolour = "B"
        else:
            pcolour = "W"
        if cpiece == pcolour:
            if piece == "P":
                if cpiece == "B":
                    frontm = False
                    leftm = whatpiece([xcells - 1, ycells - 1], cpiece)
                    rightm = whatpiece([xcells + 1, ycells - 1], cpiece)
                    frontm = whichpiece2(xcells, ycells - 1)
                    if frontm != "None":
                        frontm = True
                    if frontm == "None":
                        frontm = False
                    vfrontm = whichpiece2(xcells, (ycells - 2 ))###############################
                    if vfrontm == "None":
                        vfrontm = False
                    pawn(piecepos, pmoves, cpiece, leftm, rightm, frontm, vfrontm, pieces)
                else:
                    frontm = False
                    leftm = whatpiece([xcells - 1, ycells + 1], cpiece)
                    rightm = whatpiece([xcells + 1, ycells + 1], cpiece)
                    frontm = whichpiece2(xcells, ycells + 1)
                    if frontm != "None":
                        frontm = True
                    if frontm == "None":
                        frontm = False
                    vfrontm = whichpiece2(xcells, (ycells+2 ))###############################
                    if vfrontm == "None":
                        vfrontm = False
                    pawn(piecepos, pmoves, cpiece, leftm, rightm, frontm, vfrontm, pieces)
            elif piece == "Q":
                bishop(piecepos, pmoves, pieces, cpiece)
                castle(piecepos, pmoves, cpiece, pieces)
            elif piece == "C":
                castle(piecepos, pmoves, cpiece, pieces)
            elif piece == "B":
                bishop(piecepos, pmoves, pieces, cpiece)
            elif piece == "H":
                horse(piecepos[0], piecepos[1], pmoves, pieces, cpiece)
            elif piece == "K":
                king(piecepos, pmoves, pieces, cpiece)

            if [xcells, ycells] == [4, 1]:
                if whichpiece2(2, 1) == "None" and whichpiece2(3, 1) == "None" and whichpiece2(4, 1) == "WKing" and whichpiece2(1, 1) == "WCastle1":
                    pmoves.append([1, 1])
            if [xcells, ycells] == [4, 1]:
                if whichpiece2(5, 1) == "None" and whichpiece2(6, 1) == "None" and whichpiece2(7, 1) == "None" and whichpiece2(4, 1) == "WKing" and whichpiece2(8, 1) == "WCastle2":
                    pmoves.append([8, 1])
            if [xcells, ycells] == [4, 8]:
                if whichpiece2(5, 8) == "None" and whichpiece2(6, 8) == "None" and whichpiece2(7, 8) == "None" and whichpiece2(4, 8) == "BKing" and whichpiece2(8, 8) == "BCastle2":
                    pmoves.append([8, 8])
            if [xcells, ycells] == [4, 8]:
                if whichpiece2(3, 8) == "None" and whichpiece2(2, 8) == "None" and whichpiece2(4, 8) == "BKing" and whichpiece2(1, 8) == "BCastle1":
                    pmoves.append([1, 8])

            for i in range(0, len(pmoves)):
                pygame.draw.rect(gameDisplay, (255, 0, 0), pygame.Rect(displacement + gridsize * (pmoves[i][0] - 1), displacement + gridsize * (pmoves[i][1] - 1), gridsize, gridsize), 7)
        if whichpiece2(xcells,ycells)!="None":
            pygame.draw.rect(gameDisplay, (76, 191, 61), pygame.Rect(displacement + gridsize * (xcells - 1), displacement + gridsize * (ycells - 1), gridsize, gridsize), 7)###############################
    elif select != 1 or xcells < 1 or ycells < 1 or xcells > 8 or ycells > 8:
        select = 0
        xcells = 0
        ycells = 0
        selected = 0
        selectedpiece = "None"
        checked = False

    if select == 1:
        if xcells == xcells2 and ycells == ycells2:
            select2 = 0
            xcells2 = 0
            ycells2 = 0

    if select2 == 1 and xcells2 > 0 and ycells2 > 0 and selected == 1:
        #pygame.draw.rect(gameDisplay, (255, 56, 56), pygame.Rect(displacement + gridsize * (xcells2 - 1), displacement + gridsize * (ycells2 - 1), gridsize, gridsize), 7)
        lastpiecemoved = whichpiece3(xcells, ycells)
        targetpiece, targetpos = whichpiece(xcells2, ycells2)
        prevtarget = whichpiece(xcells2, ycells2)
        calculated = False
        if go % 2 == 0:
            pcolour = "B"
        else:
            pcolour = "W"
        scolour = selectedpiece[0]
        if targetpiece != "None" and selectedpiece != "None":
            # ("Take")
            spos = pieces.index([selectedpiece, piecepos])
            tpos = pieces.index([targetpiece, targetpos])
            tcolour = targetpiece[0]
            if scolour != tcolour and targetpiece[1] != "K" and scolour == pcolour and [xcells2, ycells2] in pmoves:
                domove = False
                pieces[spos][1][0], pieces[spos][1][1] = targetpos
                pieces.pop(tpos)
                if scolour == "W":
                    cxw, cyw = wherepiece("WKing")
                    if checkcheck(cxw, cyw, "W"):
                        pieces.append(prevtarget)
                        pieces[spos][1][0], pieces[spos][1][1] = xcells, ycells
                    else:
                        domove = True
                else:
                    cxb, cyb = wherepiece("BKing")
                    if checkcheck(cxb, cyb, "B"):
                        pieces.append(prevtarget)
                        pieces[spos][1][0], pieces[spos][1][1] = xcells, ycells
                    else:
                        domove = True
                if domove:
                    takenpieces.append([tcolour, targetpiece[1]])
                    select2, select = 0, 0
                    go += 1
                    turns += 1
                    if selectedpiece[1] == "P" and piecepos[1] == 1 and scolour == "B":
                        pieces[spos][0] = "BQueen"
                    if selectedpiece[1] == "P" and piecepos[1] == 8 and scolour == "W":
                        pieces[spos][0] = "WQueen"
                else:
                    tocountic = 1
                    whattext3 = 1
                    select2, select = 0, 0

        elif targetpiece == "None" and scolour == pcolour and [xcells2, ycells2] in pmoves:
            # print("Move")
            domove = False
            spos = pieces.index([selectedpiece, piecepos])
            pieces[spos][1][0], pieces[spos][1][1] = xcells2, ycells2
            if scolour == "W":
                cxw, cyw = wherepiece("WKing")
                if checkcheck(cxw, cyw, "W"):
                    pieces[spos][1][0], pieces[spos][1][1] = xcells, ycells
                else:
                    domove = True
            else:
                cxb, cyb = wherepiece("BKing")
                if checkcheck(cxb, cyb, "B"):
                    pieces[spos][1][0], pieces[spos][1][1] = xcells, ycells
                else:
                    domove = True
            if domove:
                select2, select = 0, 0
                go += 1
                turns += 1
                if selectedpiece[1] == "P" and piecepos[1] == 1 and scolour == "B":
                    pieces[spos][0] = "BQueen"
                if selectedpiece[1] == "P" and piecepos[1] == 8 and scolour == "W":
                    pieces[spos][0] = "WQueen"
            else:
                tocountic = 1
                text3 = "Invalid Move"
                select2, select = 0, 0

        elif scolour != pcolour or [xcells2, ycells2] not in pmoves:
            tocountic = 1
            whattext3 = 1
            select2, select = 0, 0

        if [xcells, ycells] == [4, 1] and [xcells2, ycells2] == [1, 1]:
            if whichpiece2(2, 1) == "None" and whichpiece2(3, 1) == "None" and whichpiece2(4, 1) == "WKing" and whichpiece2(1, 1) == "WCastle1":
                spos = pieces.index([selectedpiece, piecepos])
                tpos = pieces.index([targetpiece, targetpos])
                pieces[spos][1][0], pieces[spos][1][1] = 2, 1
                pieces[tpos][1][0], pieces[tpos][1][1] = 3, 1
                select2, select = 0, 0
                go += 1
                turns += 1
                checked = False
        elif [xcells, ycells] == [4, 1] and [xcells2, ycells2] == [8, 1]:
            if whichpiece2(5, 1) == "None" and whichpiece2(6, 1) == "None" and whichpiece2(7, 1) == "None" and whichpiece2(4, 1) == "WKing" and whichpiece2(8, 1) == "WCastle2":
                spos = pieces.index([selectedpiece, piecepos])
                tpos = pieces.index([targetpiece, targetpos])
                pieces[spos][1][0], pieces[spos][1][1] = 7, 1
                pieces[tpos][1][0], pieces[tpos][1][1] = 6, 1
                select2, select = 0, 0
                go += 1
                turns += 1
                checked = False

        elif [xcells, ycells] == [4, 8] and [xcells2, ycells2] == [8, 8]:
            if whichpiece2(5, 8) == "None" and whichpiece2(6, 8) == "None" and whichpiece2(7, 8) == "None" and whichpiece2(4, 8) == "BKing" and whichpiece2(8, 8) == "BCastle2":
                spos = pieces.index([selectedpiece, piecepos])
                tpos = pieces.index([targetpiece, targetpos])
                pieces[spos][1][0], pieces[spos][1][1] = 7, 8
                pieces[tpos][1][0], pieces[tpos][1][1] = 6, 8
                select2, select = 0, 0
                go += 1
                turns += 1
                checked = False

        elif [xcells, ycells] == [4, 8] and [xcells2, ycells2] == [1, 8]:
            if whichpiece2(3, 8) == "None" and whichpiece2(2, 8) == "None" and whichpiece2(4, 8) == "BKing" and whichpiece2(1, 8) == "BCastle1":
                spos = pieces.index([selectedpiece, piecepos])
                tpos = pieces.index([targetpiece, targetpos])
                pieces[spos][1][0], pieces[spos][1][1] = 2, 8
                pieces[tpos][1][0], pieces[tpos][1][1] = 3, 8
                select2, select = 0, 0
                go += 1
                turns += 1
                checked = False

    elif select2 != 1 or xcells2 < 0 or ycells2 < 0 or selected == 0:
        select2 = 0
        xcells2 = 0
        ycells2 = 0
        checked = False

    for n in range(0, 8):  # Could be a different colour?
        location4(str(numtolet(n + 1)), n)
        location5(str(n + 1), n)

    cxw, cyw = wherepiece("WKing")
    cxb, cyb = wherepiece("BKing")
    kmvs = []
    if checkcheck(cxw, cyw, "W"):
        check = True
        bcolour = (255, 0, 0)
        checkt = "White"
        king([cxw, cyw], kmvs, pieces, "W")
        if len(kmvs) == 0 and not checkcheck(lastpiecemoved[1][0], lastpiecemoved[1][1], "B"):
            checkmate = True
    elif checkcheck(cxb, cyb, "B"):
        check = True
        bcolour = (255, 0, 0)
        checkt = "Black"
        king([cxb, cyb], kmvs, pieces, "B")
        if len(kmvs) == 0 and not checkcheck(lastpiecemoved[1][0], lastpiecemoved[1][1], "W"):
            checkmate = True
    else:
        bcolour = (122, 66, 244)
        check = False
        checkmate = False

    if checkmate:
        text3 = checkt + " is in Checkmate!"
        text3x = 150
    elif check:
        text3 = checkt + " is in Check!"
        text3x = 175
    elif tocountic == 1:
        text3x = 250
        pass
    elif selected == 1:
        text3 = "Right click a red cell to move the piece."
    else:
        text3 = "Left click a cell to select a piece."

    for i in range(tcounter, len(takenpieces)):
        tcounter += 1
        if takenpieces[i][0] == "B":
            thepiece = takenpieces[i][1]
            if thepiece == "P":
                whitescore += 1
            elif thepiece == "H" or thepiece == "B":
                whitescore += 3
            elif thepiece == "C":
                whitescore += 5
            elif thepiece == "Q":
                whitescore += 9

        else:
            thepiece = takenpieces[i][1]
            if thepiece == "P":
                blackscore += 1
            elif thepiece == "H" or thepiece == "B":
                blackscore += 3
            elif thepiece == "C":
                blackscore += 5
            elif thepiece == "Q":
                blackscore += 9

    scores(textcentre, display_height - 80, "White:  " + str(whitescore), "W")
    scores(textcentre, display_height - 130, "Black:  " + str(blackscore), "B")

    if alt and f4:
        break

    if checkmate:
        pygame.draw.rect(gameDisplay, (0, 255, 0), checkyes)
        write("Click to End","Bahnschrift",30,(0,0,255),(display_width-200,display_height-200))
    #location3(text3)
    if text3=="White is in Check!" or text3=="Black is in Check!":
        text3c=(239, 120, 2)
    elif text3=="Invalid Move" or text3=="Black is in Checkmate!" or text3=="White is in Checkmate!":
        text3c=red
    else:
        text3c=yellow
    write(text3,"Bahnschrift",40,text3c,(5+text3x,display_height-52))
    #      write("Test","din1451a.ttf",12,(255,0,0),(100,100))
    location6(str(turns))
    if selectedpiece[1] == "P":
        selectedpiece = selectedpiece[1:-1]
    elif selectedpiece[1] == "K" or selectedpiece[1] == "Q":
        selectedpiece = selectedpiece[1:]
    elif selectedpiece == "None":
        pass
    else:
        selectedpiece = selectedpiece[1:-1]

    location7(selectedpiece)
    location8(go)
    location9("Quit", quitcolour, 50, 25)
    #images(play,display_width-180,display_height-50)
    location10("Selected:")
    pygame.display.update()
    clock.tick(60)

##########################################################################################################################################################################################################

while victory:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            victory = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_r:
                bf.close()
                wf.close()
                bf = open("lib\\bwins.txt", "w")
                wf = open("lib\wwins.txt", "w")
                bf.write("0")
                wf.write("0")
                bf.close()
                wf.close()
            else:
                victory = False


    gameDisplay.fill(winner)
    winnerf(image2, display_width/2-213, display_height/2-125)
    bf = open("lib\\bwins.txt", "r")
    wf = open("lib\wwins.txt", "r")
    bwins = str(bf.read())
    wwins = str(wf.read())
    location9("Victory!", (randint(1,255),randint(1,255),randint(1,255)), (display_width/2), 550)
    location9("Black Wins: " + str(bwins), (bcolour), 825, 100)
    location9("White Wins: " + str(wwins), (bcolour), 125, 100)
    location9("Press any key to quit", (62, 178, 143), display_width / 2, 100)
    location9("Press R to reset wins", (62, 178, 143), display_width / 2, 60)

    bf.close()
    wf.close()
    pygame.display.update()
    clock.tick(10)
pygame.quit()
#quit()
