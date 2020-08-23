import pygame
import random
from objects import Snake
from objects import Segment
from objects import Apple

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((260, 240))
pygame.display.set_caption("Snake")
width = 20
height = 15
side = 10 #px
margin = 2 #px
highscore = 0
fps = 15
font = pygame.font.SysFont('Comic Sans MS', 18)

def draw(grid, snake, apple, score):
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
    pygame.display.flip()

def game():
    # Setup
    score = 0
    global highscore
    grid = []
    for x in range(width):
        grid.append([])
        for y in range(height):
            grid[x].append(0)

    head = Segment(width/2, height/5)
    body = Segment(head.X, head.Y + 1)
    tail = Segment(body.X, head.Y + 1)
    head.setNext(body)
    body.setNext(tail)
    snake = Snake(head, tail)
    apple = Apple(width, height)

    #Game loop 
    finished = False
    while not finished: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        
        # Change direction
        keyPressed = pygame.key.get_pressed()
        
        if snake.direction == "up" or snake.direction == "down":
            if keyPressed[pygame.K_RIGHT]: snake.direction = "right"
            if keyPressed[pygame.K_LEFT]: snake.direction = "left"
        if snake.direction == "right" or snake.direction == "left":
            if keyPressed[pygame.K_UP]: snake.direction = "up"
            if keyPressed[pygame.K_DOWN]: snake.direction = "down"

        snake.move()

        # Check if collected an apple
        if snake.head.X == apple.X and snake.head.Y == apple.Y:
            snake.grow()
            score += 1
            if score > highscore:
                highscore = score
            appleGen = False
            while not appleGen:
                apple.generate()
                if grid[apple.X][apple.Y] == 0: 
                    appleGen = True
        
        # Death check
        if snake.isDead(height, width):
            finished = True
            break

        draw(grid, snake, apple, score)
        clock.tick(fps)

    gameOver()

def gameOver():
    text = font.render("Press Space to restart ", 1, (255, 255, 255))
    screen.blit(text, (10,215))
    pygame.display.flip()
    displayed = True
    while displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displayed = False
                pygame.quit()
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_SPACE]:
                displayed = False
                break
    
    game()

game()