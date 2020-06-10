#import dependencies
import pygame
import random
from time import sleep

#class for the food
class Food:
    def __init__(self, gameArea):
        self.colour = (50, 200, 50)
        self.width = 10
        self.height = 10
        self.x = random.randint(0, gameArea[0]) * 10 % gameArea[0]
        self.y = random.randint(0, gameArea[1]) * 10 % gameArea[0]
        self.count = 1

#class for the snake
class Snake:
    def __init__(self, gameArea):
        self.colour = (200, 50, 50)
        self.width = 10
        self.height = 10
        self.x = random.randint(0, gameArea[0]) * 10 % gameArea[0]
        self.y = random.randint(0, gameArea[1]) * 10 % gameArea[1]
        self.dir = None
        #This is a dictionary of the coordinates of the snake
        self.head = []
        self.tail = []
        self.score = 0
        self.addScore = 5

#set up the game environment
pygame.init()
gameArea = (500, 500)
pygame.display.set_caption("Snake game by Tombra")
display = pygame.display.set_mode(gameArea)
display.fill((0, 0, 0))

#instantiate the food and game
dirValue = {"up": (0, -10), "right": (10, 0), "down": (0, 10), "left": (-10, 0)}
snake = Snake(gameArea)
snake.dir = "right"
food = Food(gameArea)

def drawSnakeFood(snake, food):
    "This function is used to draw the snake and the food in the game area"
    #fill the background before updating
    display.fill((0, 0, 0))

    #draw the food
    pygame.draw.rect(display, food.colour, (food.x, food.y, food.width, food.height))
    # print("Food at: x:{}, y:{}".format(food.x, food.y))
    #draw the snake
    #draw the head of the snake
    pygame.draw.rect(display, snake.colour, (snake.x, snake.y, snake.width, snake.height))
    for items in snake.tail:                
        pygame.draw.rect(display, snake.colour, (items[0], items[1], snake.width, snake.height))
    
def displayMsg(score):
    "This function is used to display the game over texts"
    font = pygame.font.SysFont("times new roman", 30)
    colour = (200, 50, 50)
    msg = font.render("Game Over", True, colour)
    score = font.render(score, True, colour)
    display.fill((200, 200, 200))
    display.blit(msg, (int(gameArea[0] / 3), int(gameArea[1] / 2)))
    display.blit(score, (int(gameArea[0] / 3), int(gameArea[1] / 2 + 40)))
    pygame.display.update()

def moveTail(snake):
    #move the x and y coordinate of the tail of the snake
    if len(snake.tail) >= 1:
        snake.tail.pop()#removes the end of snake tail
        snake.tail.insert(0, (snake.x, snake.y))

#game loop
def game():
    #set up game loop
    food = Food(gameArea)
    snake = Snake(gameArea)
    snake.dir = "right"
    
    crashed = False
    gameLost = False
    clock = pygame.time.Clock()
    gravity = 0.1
    mSeconds = 0
    
    #display the game area
    drawSnakeFood(snake, food)
    pygame.display.update()
    
    while not crashed:
        #get all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameLost = True

                if event.key == pygame.K_SPACE:
                    paused = True
                    while paused:
                        sleep(1)
                        for evt in pygame.event.get():
                            if evt.type == pygame.QUIT:
                                crashed = True
                                print("Closing game when paused/start")
                                break
                            if evt.type == pygame.KEYDOWN:
                                print("Pressed a key when paused")
                                if evt.key == pygame.K_SPACE:
                                    paused = False
                                    print("Game restarted")
                        #break out of the while loop
                        if crashed:
                            break

                if event.key == pygame.K_UP:
                    #move in this direction only if possible
                    if not (snake.dir == "up" or snake.dir == "down"):
                        # change the seconds value for smooth runnning of the game
                        mSeconds = 0
                        #move the tail of the snake
                        #delete the end of the tail of the snake and place the 
                        # head of the snake as the beginning of the tail
                        moveTail(snake)
                        snake.x = snake.x 
                        snake.y -= 10

                        snake.dir = "up"
                        # yMovement -= 10
                        # xMovement -= 0
                        print("Event up: ", event)
                if event.key == pygame.K_RIGHT:
                    # xMovement += 10
                    # yMovement += 0
                    #move in this direction only if possible
                    if not (snake.dir == "right" or snake.dir == "left"):
                        # change the seconds value for smooth runnning of the game
                        mSeconds = 0
                        #move the tail of the snake
                        moveTail(snake)
                        snake.x += 10 
                        snake.y = snake.y
                        snake.dir = "right"
                        print("Event right: ", event)
                if event.key == pygame.K_DOWN:
                    # yMovement += 10
                    # xMovement += 0
                    #move in this direction only if possible
                    if not (snake.dir == "down" or snake.dir == "up"):
                        # change the seconds value for smooth runnning of the game
                        mSeconds = 0
                        #move the tail of the snake
                        moveTail(snake)
                        snake.x = snake.x 
                        snake.y += 10
                        snake.dir = "down"
                        print("Event down: ", event)
                if event.key == pygame.K_LEFT:
                    # xMovement -= 10
                    # yMovement -= 0
                    #move in this direction only if possible
                    if not (snake.dir == "left" or snake.dir == "right"):
                        # change the seconds value for smooth runnning of the game
                        mSeconds = 0
                        #move the tail of the snake
                        moveTail(snake)
                        snake.x -= 10
                        snake.y = snake.y
                        snake.dir = "left"
                        print("Event left: ", event)
        
        mSeconds += clock.get_rawtime()
        # move the snake after 1 second
        if(mSeconds / 100 >= gravity):
            moveTail(snake)

            #move the x and y coordinate of the head of the snake
            snake.x += dirValue[snake.dir][0]
            snake.y += dirValue[snake.dir][1]
            print("Tail: ", snake.tail)

            #check if the snake hits its tail
            if (snake.x, snake.y) in snake.tail:
                gameLost = True
            #reset the timer
            mSeconds = 0
            # continue
    
        #check if the snake has eaten the food
        if(snake.x == food.x and snake.y == food.y):
            print("Snacks eaten")

            #add the food snack to the snake using its coordinates
            #add the snack to the head of the snake
            food.count += 1
            snake.tail.append((food.x, food.y))
            #add the snack to the tail of the snake
            #create a new food snack
            food = Food(gameArea)

            #increase the score of the game
            snake.score += snake.addScore

        #check if the snake has hit the boundary
        if(snake.x < 0 or snake.x > gameArea[0] or snake.y < 0 or snake.y > gameArea[1]):
            print("Game Ended")
            gameLost = True

        drawSnakeFood(snake, food)
        pygame.display.update()

        
        clock.tick(60)

        #when the game is over
        while gameLost:
            #show the user he has lost
            message = "Score: {}".format(snake.score)
            displayMsg(message)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameLost = False
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameLost = False
                        game()

if __name__ == "__main__":
    game()

#Close the game
pygame.quit()
quit()