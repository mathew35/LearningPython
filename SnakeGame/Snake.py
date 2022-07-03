import pygame
import random
FPS = 144
tick_counter = 0
speed = 3
score = 0
spd = FPS
game_over = False
BLOCK_SIZE = 40
WIDTH, HEIGHT = 22*BLOCK_SIZE, 12*BLOCK_SIZE
RES = (WIDTH, HEIGHT)
BLOCK = (BLOCK_SIZE, BLOCK_SIZE)
BLOCK_MAX_WIDTH = WIDTH//BLOCK_SIZE
BLOCK_MAX_HEIGHT = HEIGHT//BLOCK_SIZE-1
START_LENGTH=2
prev_dir = None

WHITE = (255,255,255)
BROWN = (200,100,50)

pygame.init()
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

GAME_OVER = pygame.Surface(pygame.Rect(0, 0, WIDTH, HEIGHT).size, pygame.SRCALPHA)

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
snake[0].posX=BLOCK[0]*(5)
snake[0].posY=BLOCK[1]*(BLOCK_MAX_HEIGHT-1)

#BODY
snake.append(SNAKE())
snake[1].img=SNAKE_BODY
snake[1].rot=-90
snake[1].posX=BLOCK[0]*(4)
snake[1].posY=BLOCK[1]*(BLOCK_MAX_HEIGHT-1)
snake[1].previous_ptr=snake[0]

#TAIL
snake.append(SNAKE())
snake[2].img=SNAKE_TAIL
snake[2].rot=-90
snake[2].posX=BLOCK[0]*(3)
snake[2].posY=BLOCK[1]*(BLOCK_MAX_HEIGHT-1)
snake[2].previous_ptr=snake[1]


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
    
    #game_over overlay
    global game_over
    if game_over :
        pygame.draw.rect(GAME_OVER,pygame.Color(0,0,0,196),pygame.Rect(0, 0, WIDTH, HEIGHT))
        WIN.blit(SCORE,(WIDTH/2,HEIGHT/2))
        WIN.blit(GAME_OVER,(0,0))
    
    pygame.display.update()

def move_snake(direction):
    global tick_counter
    global speed
    global game_over
    global prev_dir
    global score
    dir_error = {"RIGHT":"LEFT","LEFT":"RIGHT","UP":"DOWN","DOWN":"UP"}
    if tick_counter > FPS//speed and direction != None:
        tick_counter = 0
        
        new_posX = snake[0].posX
        new_posY = snake[0].posY
        new_rot = snake[0].rot

        if dir_error.get(direction) != prev_dir:
            prev_dir = direction
        else:
            direction = prev_dir

        if direction == "RIGHT":       
            new_posX+=BLOCK_SIZE
            new_rot=-90

        if direction == "LEFT":           
            new_posX-=BLOCK_SIZE
            new_rot=90

        if direction == "UP":             
            new_posY-=BLOCK_SIZE
            new_rot=0

        if direction == "DOWN":           
            new_posY+=BLOCK_SIZE
            new_rot=180
                
        if(new_posX < 0 or
           new_posX > (BLOCK_MAX_WIDTH - 1) * BLOCK_SIZE or
           new_posY < BLOCK_SIZE or
           new_posY > BLOCK_MAX_HEIGHT * BLOCK_SIZE):
            game_over = True
            direction = None
        else:
            intersection = None
            for s in reversed(snake):
                if s.previous_ptr == None:
                    break;
                if (s.posX == snake[0].posX and
                    s.posY == snake[0].posY):
                    intersection = snake.index(s)
                    
                    while(len(snake)>intersection):
                        score -= 1
                        snake.pop()
                        
                    snake[-1].img = SNAKE_TAIL
                
            for s in reversed(snake):
                if s.previous_ptr == None:
                    break;
                s.posX=s.previous_ptr.posX
                s.posY=s.previous_ptr.posY
                s.rot=s.previous_ptr.rot

            snake[0].posX = new_posX
            snake[0].posY = new_posY
            snake[0].rot = new_rot
            adjust_snake_imges()
    else:
        tick_counter+=1
    return direction

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
            spd +=10
            while len(snake)>4:
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
                    
def reset_game():
    while len(snake)>4:
        snake.pop()
    global game_over
    game_over = False
    return "RIGHT"

def main():
    global game_over
    run = True
    clock = pygame.time.Clock()
    direction = "RIGHT"
    while run:
        clock.tick(spd)
        direction = move_snake(direction)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            exit()
        if game_over == False:    
            if keys_pressed[pygame.K_UP]:
                direction = ("UP")
            elif keys_pressed[pygame.K_DOWN]:
                direction = ("DOWN")
            elif keys_pressed[pygame.K_LEFT]:
                direction = ("LEFT")
            elif keys_pressed[pygame.K_RIGHT]:
                direction = ("RIGHT")
            elif keys_pressed[pygame.K_SPACE]:
                direction = None
        else:
            if keys_pressed[pygame.K_r]:
                direction = reset_game()
        handle_apple()
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()