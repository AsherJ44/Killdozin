import pygame 
import random
import time

pygame.init()

#Importing sound effects and music
crashSound = pygame.mixer.Sound("Crash.wav")
dodge = pygame.mixer.Sound("Dodge.wav")
star = pygame.mixer.Sound("Star.wav")
win = pygame.mixer.Sound("Win.wav")

gameMusic = pygame.mixer.music.load("GameMusic.wav")

pause = False


#Defining the unpause function, which allows the game to be resumed 
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


#Defining the paused function, which allows the game to be paused
def paused(flickerInts, quitGame, gameDisplay, black, centerText, largeText, button, clock):
    while pause:

        pygame.mixer.music.pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        flickerInt = random.choice(flickerInts)
        flickerRed = (flickerInt, 0, 0)

        gameDisplay.fill(black)
        centerText("Paused", largeText, flickerRed)

        button("Continue",300,400,150,50,flickerRed,unpause)
        button("Quit",500,400,150,50,flickerRed,quitGame)

        pygame.display.update()
        clock.tick(10)



#Defining the gameLoop function, which runs the majority of the game
def gameLoop(displayWidth, displayHeight, scale, scaleChange, quitGame, paused, gameDisplay, bgImg, obstacle, tree, player, score, dozerWidth, winAnim, crash, clock, flickerInts, black, centerText, largeText, button):
    global pause

    pygame.mixer.music.play(-1)

    playerX = (displayWidth * 0.45)
    playerY = (displayHeight * 0.7)
    xChange = 0
    obstacleSpeed = int(4*scale)
    treeY = 0
    trees = scaleChange([38, 843], scale)
    treeX = random.choice(trees)
    treeSpeed = 5

    list = scaleChange([random.randrange(150, 760), -550, 50, 91], scale)
    obstacleX = list[0]
    obstacleY = list[1]
    obstacleWidth = list[2]
    obstacleHeight = list[3]
    dodged = 0
    stars = 0

    bounds = scaleChange([155, 805], scale)
    boundLeft = bounds[0]
    boundRight = bounds[1]

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xChange = -7

                elif event.key == pygame.K_RIGHT:
                    xChange = 7
                    
                elif event.key == pygame.K_p:
                    pause = True
                    paused(flickerInts, quitGame, gameDisplay, black, centerText, largeText, button, clock)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xChange = 0


        playerX += xChange

        gameDisplay.blit(bgImg, (0,0))
        
        obstacle(obstacleX, obstacleY)
        obstacleY += obstacleSpeed

        tree(treeX, treeY)
        treeY += treeSpeed

        player(playerX, playerY)

        score(stars)

        if playerX > boundRight - dozerWidth or playerX < boundLeft:
            xChange = 0

        if obstacleY > displayHeight:
            pygame.mixer.Sound.play(dodge)
            list = scaleChange([random.randrange(150, 760), -550], scale)
            obstacleX = list[0]
            obstacleY = list[1]

            dodged += 1
            if dodged == 5:
                obstacleSpeed = int(6*scale)
                stars = 1
                pygame.mixer.Sound.play(star)

            if dodged == 10:
                obstacleSpeed = int(8*scale)
                stars = 2
                pygame.mixer.Sound.play(star)
                
            if dodged > 14:
                obstacleSpeed = 0
                stars = 3
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(win)
                winAnim(playerX)
                

        if playerY < obstacleY+obstacleHeight:
            if playerX + dozerWidth > obstacleX and playerX < obstacleX:
                obstacleSpeed = 0
                pygame.mixer.Sound.play(crashSound)
                time.sleep(0.5)
                crash()

        if treeY > displayHeight:
            treeY = 0 
            trees = scaleChange([38, 843], scale)
            treeX = random.choice(trees)

        pygame.display.update()
        clock.tick(60)

