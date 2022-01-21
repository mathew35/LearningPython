import pygame

FPS = 144
WIDTH, HEIGHT = 900, 500
RES = (WIDTH, HEIGHT)
BLOCK = ( 40, 40)
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

def draw_window():
    WIN.fill(BROWN)
    WIN.blit(pygame.transform.rotate(SNAKE_HEAD,-90),( 0+BLOCK[0], 0))
    WIN.blit(pygame.transform.rotate(SNAKE_RIGHT,-90),( 0, 0))
    WIN.blit(SNAKE_BODY,( 0, 0+BLOCK[1]))
    WIN.blit(SNAKE_BODY,( 0, 0+BLOCK[1]*2))
    WIN.blit(SNAKE_BODY,( 0, 0+BLOCK[1]*3))
    WIN.blit(SNAKE_TAIL,( 0, 0+BLOCK[1]*4))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()