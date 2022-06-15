import pygame
import random
FPS = 144
tick_counter = 0
speed = 3
score = 0
spd = FPS
BLOCK_SIZE = 40
WIDTH, HEIGHT = 22*BLOCK_SIZE, 12*BLOCK_SIZE
RES = (WIDTH, HEIGHT)
BLOCK = (BLOCK_SIZE, BLOCK_SIZE)
BLOCK_MAX_WIDTH = WIDTH//BLOCK_SIZE
BLOCK_MAX_HEIGHT = HEIGHT//BLOCK_SIZE-1
START_LENGTH=2

WHITE = (255,255,255)
BROWN = (200,100,50)

WIN = pygame.display.set_mode(RES)
pygame.display.set_caption("Snake Game")



Assets="SnakeGame\Assets\\"
SNAKE_HEAD_IMG = pygame.image.load(Assets+'SnakeHead.png')
SNAKE_HEAD = pygame.transform.scale(SNAKE_HEAD_IMG,BLOCK)

SNAKE_BODY_IMG = pygame.image.load(Assets+'SnakeBody.png')
SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMG,BLOCK)

SNAKE_LEFT_IMG = pygame.image.load(Assets+'SnakeTurnLeft.png')
SNAKE_LEFT = pygame.transform.scale(SNAKE_LEFT_IMG,BLOCK)

SNAKE_RIGHT_IMG = pygame.image.load(Assets+'SnakeTurnRight.png')
SNAKE_RIGHT = pygame.transform.scale(SNAKE_RIGHT_IMG,BLOCK)

SNAKE_TAIL_IMG = pygame.image.load(Assets+'SnakeTail.png')
SNAKE_TAIL = pygame.transform.scale(SNAKE_TAIL_IMG,BLOCK)

APPLE_IMG_FILE = pygame.image.load(Assets+'Apple.xcf')
APPLE_IMG = pygame.transform.scale(APPLE_IMG_FILE,BLOCK)

pygame.font.init()
font = pygame.font.Font(None, BLOCK_SIZE)
SCORE = font.render("Score: " + str(score),True,(10,10,10))
SCORE_POS = SCORE.get_rect(x = 3, centery = BLOCK_SIZE/2)

class APPLE:
    img = APPLE_IMG
    posX = 0
    posY = 0

class SNAKE:
    img = SNAKE_HEAD
    posX = 0
    posY = 0
    rot = 0
    previous_ptr = None

apple = APPLE()
apple.posX = BLOCK[0]*5
apple.posY = BLOCK[1]*2
snake = []

#HEAD
snake.append(SNAKE())
snake[0].img=SNAKE_HEAD
snake[0].rot=-90
snake[0].posX=BLOCK[0]*(BLOCK_MAX_WIDTH//3+1)
snake[0].posY=BLOCK[1]*(BLOCK_MAX_HEIGHT-1)

#TAIL
snake.append(SNAKE())
snake[1].img=SNAKE_TAIL
snake[1].rot=-90
snake[1].posX=BLOCK[0]*(BLOCK_MAX_WIDTH//3)
snake[1].posY=BLOCK[1]*(BLOCK_MAX_HEIGHT-1)
snake[1].previous_ptr=snake[0]


def draw_window():
    WIN.fill(BROWN)
    pygame.draw.rect(WIN, WHITE,(pygame.Rect(0,35,WIDTH,5)))

    #Score
    SCORE = font.render("Score: " + str(score),True,(10,10,10))
    WIN.blit(SCORE,SCORE_POS)

    #Draw Apple
    WIN.blit(apple.img,(apple.posX,apple.posY))

    #Draw Snake
    for s in snake:
        WIN.blit(pygame.transform.rotate(s.img,s.rot),(s.posX,s.posY))
    pygame.display.update()

def move_snake(direction):
    global tick_counter
    global speed
    if tick_counter > FPS//speed and direction != None:
        tick_counter = 0
        for s in reversed(snake):
            if s.previous_ptr == None:
                break;
            s.posX=s.previous_ptr.posX
            s.posY=s.previous_ptr.posY
            s.rot=s.previous_ptr.rot
        if direction == "RIGHT":
            # snake[1].posX=snake[1].previous_ptr.posX
            # snake[1].posY=snake[1].previous_ptr.posY
            # snake[1].rot=snake[1].previous_ptr.rot            
            snake[0].posX+=BLOCK_SIZE
            snake[0].rot=-90
        if direction == "LEFT":   
            # snake[1].posX=snake[1].previous_ptr.posX
            # snake[1].posY=snake[1].previous_ptr.posY
            # snake[1].rot=snake[1].previous_ptr.rot            
            snake[0].posX-=BLOCK_SIZE
            snake[0].rot=90
        if direction == "UP":   
            # snake[1].posX=snake[1].previous_ptr.posX
            # snake[1].posY=snake[1].previous_ptr.posY
            # snake[1].rot=snake[1].previous_ptr.rot            
            snake[0].posY-=BLOCK_SIZE
            snake[0].rot=0
        if direction == "DOWN":    
            # snake[1].posX=snake[1].previous_ptr.posX
            # snake[1].posY=snake[1].previous_ptr.posY
            # snake[1].rot=snake[1].previous_ptr.rot            
            snake[0].posY+=BLOCK_SIZE
            snake[0].rot=180
        adjust_snake_imges()
        for s in snake:
            if s.posX < 0:
                s.posX += BLOCK_MAX_WIDTH*BLOCK_SIZE
            if s.posX > (BLOCK_MAX_WIDTH-1)*BLOCK_SIZE:
                s.posX = 0
            if s.posY < BLOCK_SIZE:
                s.posY = BLOCK_MAX_HEIGHT*BLOCK_SIZE
            if s.posY > BLOCK_MAX_HEIGHT*BLOCK_SIZE:
                s.posY = BLOCK_SIZE
    else:
        tick_counter+=1

def adjust_snake_imges():
    for s in reversed(snake):
        if s.previous_ptr != None:
            if s.previous_ptr.previous_ptr != None:
                LR1 = s.previous_ptr.previous_ptr.posX - s.posX
                UD1 = s.previous_ptr.previous_ptr.posY - s.posY
                LR2 = s.previous_ptr.previous_ptr.posX - s.previous_ptr.posX
                UD2 = s.previous_ptr.previous_ptr.posY - s.previous_ptr.posY
                if LR1== 0 or UD1 == 0:
                    s.previous_ptr.img = SNAKE_BODY
                    if LR1 > 0:
                        s.previous_ptr.rot = -90
                    elif LR1 <0:
                        s.previous_ptr.rot = 90
                    if UD1 > 0:
                        s.previous_ptr.rot = 180
                    elif UD1 < 0:
                        s.previous_ptr.rot = 0
                elif UD1 > 0:
                    if LR1 > 0:
                        if LR2 == 0:
                            s.previous_ptr.img = SNAKE_RIGHT
                            s.previous_ptr.rot = 180
                        else:
                            s.previous_ptr.img = SNAKE_LEFT
                            s.previous_ptr.rot = -90
                    else:
                        if LR2 == 0:
                            s.previous_ptr.img = SNAKE_LEFT
                            s.previous_ptr.rot = 180
                        else:
                            s.previous_ptr.img = SNAKE_RIGHT
                            s.previous_ptr.rot = 90
                else:
                    if LR1 > 0:
                        if LR2 == 0:
                            s.previous_ptr.img = SNAKE_LEFT
                            s.previous_ptr.rot = 0
                        else:
                            s.previous_ptr.img = SNAKE_RIGHT
                            s.previous_ptr.rot = -90
                    else:
                        if LR2 == 0:
                            s.previous_ptr.img = SNAKE_RIGHT
                            s.previous_ptr.rot = 0
                        else:
                            s.previous_ptr.img = SNAKE_LEFT
                            s.previous_ptr.rot = 90
        
def snake_add():
    newTail = SNAKE()
    newTail.posX = snake[-1].posX
    newTail.posY = snake[-1].posY
    newTail.rot = snake[-1].rot
    newTail.img = snake[-1].img
    newTail.previous_ptr = snake[-1]
    snake.append(newTail)
  
def handle_apple():
    global spd
    global score
    if (snake[0].posX == apple.posX) and (snake[0].posY == apple.posY): 
        snake_add()
        score += 1
        if score % 10 == 0:
            spd +=5
            while len(snake)>3:
                snake.pop()
            snake[-1].img = SNAKE_TAIL
        generated = False
        while(not generated):
            apple.posX = BLOCK[0]*random.randrange(0,BLOCK_MAX_WIDTH)
            apple.posY = BLOCK[1]*(random.randrange(0,BLOCK_MAX_HEIGHT)+1)
            generated = True
            for s in snake:
                if s.posX == apple.posX and s.posY == apple.posY:
                    generated = False
def main():
    run = True
    clock = pygame.time.Clock()
    direction = "RIGHT"
    while run:
        clock.tick(spd)
        move_snake(direction)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            direction = ("UP")
        elif keys_pressed[pygame.K_DOWN]:
            direction = ("DOWN")
        elif keys_pressed[pygame.K_LEFT]:
            direction = ("LEFT")
        elif keys_pressed[pygame.K_RIGHT]:
            direction = ("RIGHT")
        elif keys_pressed[pygame.K_ESCAPE]:
            exit()
        elif keys_pressed[pygame.K_SPACE]:
            direction = None
        handle_apple()
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()