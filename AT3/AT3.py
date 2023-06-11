#Created by Asher Johnston from 15th May to (insert date here)
#Function is as a simple game, where the player has to dodge randomly positioned objects
#Game is built using the pygame module for python, and is based off an in-class tutorial series


#Importing modules: pygame to run the game, random for RNG, time for pacing elements, gameLoop to run the game, paused to pause the game, and unpause to resume it
import pygame 
import random
import time
from Functions import paused
from Functions import unpause
from Functions import gameLoop


#Setting screen size and scale
scale = 1.0
displayWidth = 960
displayHeight = 540


displaySizes = ["s", "m", "l"]
displaySize = input("What size is your display (s, m, l)? ")
while displaySize.lower() not in displaySizes:
    displaySize = input("What size is your display (s, m, l)? ")

userName = input("What would you like me to call you? ")

#Setting the display scale based on the users answer
if displaySize == displaySizes[0]:
    scale = 1.0
    imgs = ("KilldozerS.png", "CopCarS.png", "BgS.png", "StarS.png", "TreeS.png", "LeftArrowS.png", "RightArrowS.png", "PKeyS.png", "CrashDodgeS.png")

elif displaySize == displaySizes[1]:
    scale = 1.5
    imgs = ("KilldozerM.png", "CopCarM.png", "BgM.png", "StarM.png", "TreeM.png", "LeftArrowM.png", "RightArrowM.png", "PKeyM.png", "CrashDodgeM.png")

elif displaySize == displaySizes[2]:
    scale = 2.0
    imgs = ("KilldozerL.png", "CopCarL.png", "BgL.png", "StarL.png", "TreeL.png", "LeftArrowL.png", "RightArrowL.png", "PKeyL.png", "CrashDodgeL.png")


displayWidth = int(960*scale)
displayHeight = int(540*scale)
dozerWidth = int(100*scale)

#Defining the scaleChange function, used to change the scale of elements to match the users scale choice
def scaleChange(list, scale):
    newList = []
    for item in list:
        item = int(item*scale)
        newList.append(item)
    return newList


#Initializing Pygame and creating the pygame window
pygame.init()
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption("Killdozin'")
clock = pygame.time.Clock()


#Defining colours
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
brightRed = (255,0, 0)

green = (0,200,0)
brightGreen = (0,255,0)

blue = (0,0,200)
brightBlue = (0,0,255)


flickerInts = (150, 175, 200, 225, 230, 235, 240, 245, 250, 255)


#Importing images for use throughout the program
playerImg = pygame.image.load(imgs[0])
obstacleImg = pygame.image.load(imgs[1])
bgImg = pygame.image.load(imgs[2])
starImg = pygame.image.load(imgs[3])
treeImg = pygame.image.load(imgs[4])
leftImg = pygame.image.load(imgs[5])
rightImg = pygame.image.load(imgs[6])
pKeyImg = pygame.image.load(imgs[7])
crashdodgeImg = pygame.image.load(imgs[8])

#Importing the intro music
intro = pygame.mixer.Sound("IntroMusic.wav")


#Defining different size fonts
helpText = pygame.font.SysFont("times.ttf", (int(18*scale)))
smallText = pygame.font.Font("VerminVibes1989.ttf", (int(25*scale)))
mediumText = pygame.font.Font("VerminVibes1989.ttf", (int(50*scale)))
largeText = pygame.font.Font("VerminVibes1989.ttf", (int(75*scale)))
titleText = pygame.font.Font("VerminVibes1989.ttf", (int(125*scale)))


pause = False


#Defining the quitGame function, which can be called at any point to quit the program
def quitGame():
    pygame.quit()
    quit()


#Defining the score function, which tracks the users score
def score(dodged):
    if dodged == 1:
        gameDisplay.blit(starImg, (int(0*scale),int(0*scale)))

    elif dodged == 2:
        gameDisplay.blit(starImg, (int(0*scale),int(0*scale)))
        gameDisplay.blit(starImg, (int(50*scale),int(0*scale)))

    elif dodged == 3:
        gameDisplay.blit(starImg, (int(0*scale),int(0*scale)))
        gameDisplay.blit(starImg, (int(50*scale),int(0*scale)))
        gameDisplay.blit(starImg, (int(100*scale),int(0*scale)))

#Defining the obstacle function, which creates obstacles to dodge
def obstacle(x, y):
    gameDisplay.blit(obstacleImg, (x,y))
   

#Defining the tree function, which creates trees to make a sense of movement
def tree(x, y):
    gameDisplay.blit(treeImg, (x,y))


#Defining the player function, which draws the users sprite
def player(x,y):
    gameDisplay.blit(playerImg, (x,y))


#Defining the textObjects function, which simplifies the displaying of text
def textObjects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


#Defining the centerText function, which displays text in the center of the screen
def centerText(text, font, colour):
    textSurf, textRect = textObjects(text, font, colour)
    textRect.center = ((displayWidth/2), (displayHeight/2))
    gameDisplay.blit(textSurf, textRect)


#Defining the freeText function, which displays text at a chosen x and y coordinates
def freeText(text, font, colour, x, y):
    textSurf, textRect = textObjects(text, font, colour)
    coordinates = scaleChange([x,y], scale)
    textX = coordinates[0]
    textY = coordinates[1]
    textRect.center = (textX,textY)
    gameDisplay.blit(textSurf, textRect)


#Defining the button function, which allows a button to be drawn in accordance with parameters
def button(msg, x, y, width, height, colour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    textColour = colour

    list = scaleChange([x, y, width, height], scale)
    x = list[0]
    y = list[1]
    width = list[2]
    height = list[3]

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, colour, (x,y,width,height))
        textColour = black
        if click[0] == 1 and action != gameLoop:
            action()
        elif click[0] == 1 and action == gameLoop:
            action(displayWidth, displayHeight, scale, scaleChange, quitGame, paused, gameDisplay, bgImg, obstacle, tree, player, score, dozerWidth, winAnim, crash, clock, flickerInts, black, centerText, largeText, button)
        
    else:
        pygame.draw.rect(gameDisplay, colour, (x,y,width,height)) 
        pygame.draw.rect(gameDisplay, black, ((x+5),(y+5),(width-10),(height-10)))


    textSurf, textRect = textObjects(msg, smallText, textColour)
    textRect.center = ( (x + (width/2)), (y + (height/2)) )
    gameDisplay.blit(textSurf, textRect)


#Defining the crash function, which handles the event of the player crashing
def crash():

    pygame.mixer.music.stop()
    crashed = True
    while crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        flickerInt = random.choice(flickerInts)
        flickerRed = (flickerInt, 0, 0)

        gameDisplay.fill(black)
        centerText("Sorry "+userName+", you Crashed", largeText, flickerRed)

        button("Play again",200,400,150,50,flickerRed,gameLoop)
        button("Home",400,400,150,50,flickerRed,mainMenu)
        button("Quit",600,400,150,50,flickerRed,quitGame)

        pygame.display.update()
        clock.tick(10)


#Defining the winAnim function, which plays a short animation when the player finishes the game
def winAnim(x):

    playerY = (displayHeight * 0.7)
    yChange = int(5*scale)
    while playerY > (0 - int(151*scale)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.blit(bgImg, (0,0))
        playerY -= yChange
        player(x, playerY)
        score(3)
        pygame.display.update()
        clock.tick(60)
    time.sleep(1)
    winScreen(userName)


#Defining the winScreen function, which activates when the user has won the game
def winScreen(name):
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        flickerInt = random.choice(flickerInts)
        flickerRed = (flickerInt, 0, 0)

        gameDisplay.fill(black)
        centerText(("You won "+name+"!"), largeText, flickerRed)

        button("Play again",200,400,150,50,flickerRed,gameLoop)
        button("Home",400,400,150,50,flickerRed,mainMenu)
        button("Quit",600,400,150,50,flickerRed,quitGame)
       
        pygame.display.update()
        clock.tick(10)


#Defining the gameIntro function, which introduces the player to the concept of the game and the controls
def gameIntro():
    strings = ('This game is based on the story of Marvin Heemeyer and his infamous "Killdozer"', "This game does not endorse his actions, it simply tells his story", 
               "Right arrow to move right. Left arrow to move left.", "Dodge 5 cops for a star. 3 stars wins the game", "Good Luck.")
    
    #pygame.mixer.Sound.play(intro)

    for string in strings:
        gameDisplay.fill(black)
        centerText(string, smallText, brightRed)
        pygame.display.update()
        time.sleep(6)
        

    gameLoop(displayWidth, displayHeight, scale, scaleChange, quitGame, paused, gameDisplay, bgImg, obstacle, tree, player, score, dozerWidth, winAnim, crash, clock, flickerInts, black, centerText, largeText, button)


#Defining the help function, which provides the user with various help information
def help():
    help = True
    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(black)
        flickerInt = random.choice(flickerInts)
        flickerRed = (flickerInt, 0, 0)
        
        freeText("Help", largeText, flickerRed, 480, 50)
        
        freeText("Aim of the game", smallText, flickerRed, 160, 100)
        freeText("Controls", smallText, flickerRed, 480, 100)
        freeText("Tips", smallText, flickerRed, 795, 100)

        freeText("In this game, the aim is to dodge 15 cops to escape.", helpText, brightRed, 160, 125)
        freeText("Go to either the left or the right to dodge them", helpText, brightRed, 160, 140)
        gameDisplay.blit(crashdodgeImg, (int(20*scale),int(160*scale)))

        freeText("To go left, press the left arrow key", helpText, brightRed, 480, 125)
        gameDisplay.blit(leftImg, (int(403*scale),int(135*scale)))

        freeText("To go right, press the right arrow key", helpText, brightRed, 480, 250)
        gameDisplay.blit(rightImg, (int(403*scale),int(260*scale)))

        freeText("Press p to pause", helpText, brightRed, 800, 125)
        gameDisplay.blit(pKeyImg, (int(750*scale),int(135*scale)))
        freeText("If the game window is too small or large, you can", helpText, brightRed, 795, 250)
        freeText("change the size by restarting the program and ", helpText, brightRed, 795, 265)
        freeText("selecting a different display size", helpText, brightRed, 795, 280)
        button("Back",0,0,150,50,flickerRed,mainMenu)

        pygame.display.update()
        clock.tick(10)


#Defining the mainMenu function, which provides the user with their initial options
def mainMenu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        flickerInt = random.choice(flickerInts)
        flickerRed = (flickerInt, 0, 0)

        gameDisplay.fill(black)
        centerText("Killdozin'", titleText, flickerRed)

        button("Play",200,400,150,50,flickerRed,gameIntro)
        button("Help",400,400,150,50,flickerRed,help)
        button("Quit",600,400,150,50,flickerRed,quitGame)
        #button("Further Info",400,400,100,50,brightYellow,story)
        

        pygame.display.update()
        clock.tick(10)


#Calling the functions to run the game
mainMenu()
pygame.quit()
quit()