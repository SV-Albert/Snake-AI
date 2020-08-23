import numpy as np
import pygame
import random
import math
import os
from objects import Snake
from objects import Segment
from objects import Apple

state_dict = dict()
actions = ["right", "left", "wait"]

# Assign integer IDs to all of the possible states
def init_state_dict():
    id = 0
    directons = ["up", "down", "right", "left"]
    appleLocations = ["up", "down", "right", "left", "upRight", "upLeft", "downRight", "downLeft"]
    for frontObst in range(0, 2):
        for leftObst in range(0, 2):
            for rightObst in range(0, 2):
                for direction in directons:
                    for appleLocation in appleLocations:
                        state_dict[str(frontObst) + ", " + str(leftObst) + ", " + str(rightObst) + ", " + direction + ", " + appleLocation] = id
                        id += 1
    return id

# Return a string representation of a current state
def getState(snake, apple):
    direction = snake.direction
    if snake.head.X < apple.X:
        if snake.head.Y < apple.Y: appleLocation = "downRight"
        elif snake.head.Y > apple.Y: appleLocation = "upRight"
        else: appleLocation = "right"  
    elif snake.head.X > apple.X:
        if snake.head.Y < apple.Y: appleLocation = "downLeft"
        elif snake.head.Y > apple.Y: appleLocation = "upLeft"
        else: appleLocation = "left"
    else:
        if snake.head.Y < apple.Y: appleLocation = "down"
        else: appleLocation = "up"

    rightObst = 0
    leftObst = 0
    frontObst = 0
    rightX = 0
    leftX = 0
    frontX = 0
    rightY = 0
    leftY = 0
    frontY = 0
    if direction == "up":
        if snake.head.X == 0: leftObst = 1
        elif snake.head.X == width-1: rightObst = 1
        else:
            rightX = snake.head.X + 1
            leftX = snake.head.X - 1
            rightY = snake.head.Y
            leftY = snake.head.Y
        if snake.head.Y == 0: frontObst = 1
        else: 
            frontX = snake.head.X
            frontY = snake.head.Y - 1

    elif direction == "down":
        if snake.head.X == width-1: leftObst = 1
        elif snake.head.X == 0: rightObst = 1
        else:
            rightX = snake.head.X - 1
            leftX = snake.head.X + 1
            rightY = snake.head.Y
            leftY = snake.head.Y
        if snake.head.Y == height - 1: frontObst = 1
        else: 
            frontX = snake.head.X
            frontY = snake.head.Y + 1
    elif direction == "left":
        if snake.head.Y == height-1: leftObst = 1
        elif snake.head.Y == 0: rightObst = 1
        else:
            rightX = snake.head.X
            leftX = snake.head.X
            rightY = snake.head.Y + 1
            leftY = snake.head.Y - 1
        if snake.head.X == 0: frontObst = 1
        else: 
            frontX == snake.head.X - 1
            frontY == snake.head.Y
    elif direction == "right":
        if snake.head.Y == 0: leftObst = 1
        elif snake.head.Y == height-1: rightObst = 1
        else:
            rightX = snake.head.X
            leftX = snake.head.X
            rightY = snake.head.Y - 1
            leftY = snake.head.Y + 1
        if snake.head.X == width - 1: frontObst = 1
        else: 
            frontX == snake.head.X + 1
            frontY == snake.head.Y

    if snake.length > 4:
        currentSeg = snake.head.next.next.next.next
        for i in range(snake.length - 4):
            if currentSeg.X == rightX and currentSeg.Y == rightY: rightObst = 1
            elif currentSeg.X == leftX and currentSeg.Y == leftY: leftObst = 1
            elif currentSeg.X == frontX and currentSeg.Y == frontY: frontObst = 1
            if i < snake.length - 5: 
                currentSeg = currentSeg.next

    state = str(frontObst) + ", " + str(leftObst) + ", " + str(rightObst) + ", " + direction + ", " + appleLocation
    return state

# Calculate Eucledean distance from the snakes head to apple
def distanceToApple(snake, apple):
    return math.sqrt(math.pow(snake.head.X - apple.X, 2) + math.pow(snake.head.Y - apple.Y, 2))

# Initialise PyGame, set the display size, board size and the fonts
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((260, 270))
pygame.display.set_caption("SnakeAI Training")
width = 20
height = 15
side = 10 #px
margin = 2 #px
font = pygame.font.SysFont('Comic Sans MS', 18)

# Display current game state
def draw(grid, snake, apple, score, episode, highscore, mode):
    screen.fill((73, 79, 112))
    for x in range(width):
        for y in range(height):
            grid[x][y] = 0

    currentSeg = snake.head
    for i in range(snake.length):
        grid[int(currentSeg.X)][int(currentSeg.Y)] = 1
        if i < snake.length-1:
            currentSeg = currentSeg.next

    grid[int(apple.X)][int(apple.Y)] = 2

    for x in range(width):
        for y in range(height):
            if grid[x][y] == 1:
                color = (0, 255, 0)
            elif grid[x][y] == 2:
                color = (255, 0, 0)
            else: color = (50, 50, 50)
            pygame.draw.rect(screen, color, [(margin + side) * x + side, (margin + side) * y + side, side, side])

    # Display score
    scoreText = font.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(scoreText, (10,190))
    hscoreText = font.render("Highscore: " + str(highscore), 1, (255, 255, 255))
    screen.blit(hscoreText, (120,190))
    episodeText = font.render("Games played: " + str(episode), 1, (255, 255, 255))
    screen.blit(episodeText, (10,215))
    modeText = font.render("Mode: " + mode, 1, (255, 255, 255))
    screen.blit(modeText, (10, 240))
    pygame.display.flip()

def run():
    alpha = 0.15 #learning rate
    gamma = 0.7 #discount factor
    epsilon = 0 #exploration value
    demoEpsilon = 0 #Epsilon value for the demo mode
    dynamicEpsilon = False #If True, the exploration rate will be reducing as more of the state-space is dicovered, if False the rate will be static
    training_episodes = 1000000
    deathAfter = 250 #Kill the snake after a certain number of moves to prevent it from getting stuck in a cycle 
    qTableSave = os.path.join(os.sys.path[0], "saves", "QTable.txt")
    counterSave = os.path.join(os.sys.path[0], "saves", "GameCounter.txt")
    fps = 30
    displayMode = "Demo"
    
    # Load existing Q-Table and episode counter or create new ones
    numberOfStates = init_state_dict()
    Q = np.zeros((numberOfStates, len(actions)))
    try:
        Q = np.loadtxt(qTableSave).reshape(numberOfStates, len(actions))
    except:
        print("Could not load an existing Q-Table")
    try:
        counterFile = open(counterSave, "r")
        startEpisode = int(counterFile.read())
        counterFile.close()
    except:
        startEpisode = 0

    highscore = 0
    for episode in range(startEpisode, training_episodes + 1):
        killApp = False
        try:
            if(episode % 100 == 0):
                count = 0
                qFile = open(qTableSave, "w")
                for row in Q:
                    if not "0. 0. 0." in str(row):
                        count += 1
                    np.savetxt(qFile, row)
                qFile.close()
                counterFile = open(counterSave, "w")
                counterFile.write(str(episode))
                counterFile.close
                exploredPercentage = count/(numberOfStates)
                if dynamicEpsilon:
                    if exploredPercentage < 0.95:
                        epsilon = (1 - exploredPercentage)/2 #Reduce exploration value as more states get explored
                    else: 
                        epsilon = 0.05
                print(str(exploredPercentage * 100) + "%" + " of state-space explored")
        except:
            print("Save error")
        
        # Initialise the game grid and the score counter
        score = 0
        grid = []
        for x in range(width):
            grid.append([])
            for y in range(height):
                grid[x].append(0)

        # Create the snake and the apple
        head = Segment(width/2, height/5)
        body = Segment(head.X, head.Y + 1)
        tail = Segment(body.X, head.Y + 1)
        head.setNext(body)
        body.setNext(tail)
        snake = Snake(head, tail)
        apple = Apple(width, height)
        startStateID = state_dict[getState(snake, apple)]
        nextStateID = startStateID
        prevDistToApple = distanceToApple(snake, apple)
        deathCountdown = deathAfter

        #Game loop 
        finished = False
        paused = False
        while not finished: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    killApp = True
            
            # Pause/unpause, switch the mode between training and demo
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_SPACE]: 
                paused = True
            elif keyPressed[pygame.K_RETURN]:
                paused = False
            elif keyPressed[pygame.K_UP]:
                fps = 10000
                displayMode = "Training"
                dynamicEpsilon = True
            elif keyPressed[pygame.K_DOWN]:
                fps = 30
                displayMode = "Demo"
                dynamicEpsilon = False
                epsilon = demoEpsilon 
            elif keyPressed[pygame.K_END]:
                killApp = True
            
            if not paused:
                reward = 0
                stateID = nextStateID
                # Choose action
                if random.uniform(0,1) < epsilon:
                    unexplored = False
                    for i in range(0, 3): #Unlike classic Q-Learning, the algorithm prefers to go to a previously unexplored state, instead of choosing an action randomly
                        if Q[stateID, i] == 0.:
                            actionID = i
                            unexplored = True
                            break
                    if not unexplored: #If no unexplored states were found, choose a random action
                        actionID = random.randint(0, 2)
                else:
                    actionID = np.argmax(Q[stateID])

                # Change direction
                if actions[actionID] != "wait":
                    if snake.direction == "up":
                        snake.direction = actions[actionID]
                    elif snake.direction == "down":
                        if actions[actionID] == "right": snake.direction = "left"
                        if actions[actionID] == "left": snake.direction = "right"
                    elif snake.direction == "left":
                        if actions[actionID] == "right": snake.direction = "up"
                        if actions[actionID] == "left": snake.direction = "down"
                    elif snake.direction == "right":
                        if actions[actionID] == "right": snake.direction = "down"
                        if actions[actionID] == "left": snake.direction = "up"

                snake.move()

                distToApple = distanceToApple(snake, apple)
                # Check if collected an apple
                if snake.head.X == apple.X and snake.head.Y == apple.Y:
                    snake.grow()
                    score += 1
                    if score > highscore: 
                        highscore = score
                    reward += 500
                    deathCountdown = deathAfter
                    appleGen = False
                    while not appleGen:
                        apple.generate()
                        if grid[apple.X][apple.Y] == 0: 
                            appleGen = True
                            prevDistToApple = distanceToApple(snake, apple)
                else:
                    deathCountdown -= 1
                    distToApple = distanceToApple(snake, apple)
                    if distToApple >= prevDistToApple: 
                        reward -= 5
                    else: 
                        reward += 1
                    prevDistToApple = distToApple

                # Death check
                if snake.isDead(height, width) or deathCountdown <= 0:
                    finished = True
                    reward -= 10000
                    nextStateID = startStateID
                    oldQ = Q[stateID, actionID]
                    nextMax = -10000
                    updatedQ = (1 - alpha) * oldQ + alpha * (reward + gamma * nextMax)
                    Q[stateID, actionID] = updatedQ
                else:
                    nextState = getState(snake, apple)
                    nextStateID = state_dict[nextState]
                    nextMax = np.max(Q[nextStateID])
                    oldQ = Q[stateID, actionID]
                    updatedQ = (1 - alpha) * oldQ + alpha * (reward + gamma * nextMax)
                    Q[stateID, actionID] = updatedQ

                    draw(grid, snake, apple, score, episode, highscore, displayMode)

            clock.tick(fps)
            if killApp == True: break

        if killApp == True: break

run()
