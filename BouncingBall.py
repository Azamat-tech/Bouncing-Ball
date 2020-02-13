#IMPORT LIBRARIES
import pygame
from random import randint
#IMPORT COLORS
Black = (0,0,0)
White = (255,255,255)
#Setting the screen
Size_x = 800
Size_y = 700
#assigning blocks properties
Brick_Width = 60
Brick_Height = 15

pygame.init()
Screen = pygame.display.set_mode((Size_x, Size_y))
pygame.display.set_caption("Bouncing Ball")
Clock = pygame.time.Clock()

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.paddle_width = 120
        self.paddle_height = 15
        self.paddle_color = Black
        #creates an image with height and width
        self.image = pygame.Surface((self.paddle_width, self.paddle_height))
        #sets the color
        self.image.fill(White)
        self.image.set_colorkey(White)
        #getting the coordinates
        self.rect = self.image.get_rect()
        #draw the paddle
        pygame.draw.rect(self.image, self.paddle_color, [0, 0, self.paddle_width, self.paddle_height])

    def move_left(self,pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self,pixels):
        self.rect.x += pixels
        if self.rect.x > Size_x - 120:
            self.rect.x = Size_x-120

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.ball_color = Black
        #creates an image with height and width
        self.image = pygame.Surface((self.radius, self.radius))
        #sets the color
        self.image.fill(White)
        self.image.set_colorkey(White)
        #get the coordinates of the ball
        self.rect = self.image.get_rect()
        #assigns its velocity
        self.velocity_x = randint(2,4)
        self.velocity_y = -randint(2,3)
        #draw the ball
        pygame.draw.rect(self.image, self.ball_color,[0,0,self.radius,self.radius])

    def resetBall(self):
        self.rect.x = int(Size_x//2)
        self.rect.y = int(Size_y//2)        
        self.velocity_x = randint(2,4)
        self.velocity_y = -randint(2,3)

    def update(self): 
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def bounce(self):
        if self.velocity_y < 0:
            self.velocity_y = randint(2,5)
        else:
            self.velocity_y = - randint(2,5)

#creating class of bricks
class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Brick_color = Black
        self.image = pygame.Surface((Brick_Width,Brick_Height))
        self.image.fill(White)
        self.image.set_colorkey(White)
        self.rect = self.image.get_rect()
        #draw the brics
        pygame.draw.rect(self.image,self.Brick_color,[0,0,Brick_Width, Brick_Height])

#list that containes the sprites of ball, paddle and bricks
all_sprites_list = pygame.sprite.Group()
#create the paddle
paddle = Paddle()
paddle.rect.x = Size_x//2 - 60
paddle.rect.y = Size_y - 20
#create the ball
ball = Ball()
ball.rect.x = Size_x//2
ball.rect.y = Size_y//2
#add objects to the sprtie list
Blocks = pygame.sprite.Group()
Balls = pygame.sprite.Group()
all_sprites_list.add(paddle)
all_sprites_list.add(ball)
Balls.add(ball)


def draw_bricks(Blocks,all_sprites_list):
    pos_y = 50
    count = 13
    for i in range(5):
        for j in range(0,count):
            block = Brick()
            block.rect.x = j * (Brick_Width + 2) + 1
            block.rect.y = pos_y
            Blocks.add(block)
            all_sprites_list.add(block)
        pos_y += Brick_Height + 2

def key_getPressed(paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        paddle.move_left(5)
    if keys[pygame.K_d]:
        paddle.move_right(5)

def reprGameOver(Score):
    font = pygame.font.Font(None, 30)
    Text = font.render("Game Over to start again press space",1,Black)
    Text1 = font.render("Your score is: " + str(Score),1,Black)
    TextRect = (Size_x//2 - 170, Size_y//2)
    TextRect1 = (Size_x//2 - 80, Size_y//2 + 25)
    Screen.blit(Text, TextRect)
    Screen.blit(Text1, TextRect1)
    pygame.display.update()

def reprGameWon(Score):
    font = pygame.font.Font(None, 30)
    Text = font.render("Congratulations, you won!!!",1,Black)
    Text1 = font.render("Your score is: " + str(Score),1,Black)
    Text2 = font.render("Do you want to play again? Press SPACE to restart or ESCAPE to exit ",1,Black)
    TextRect = (Size_x//2 - 170, Size_y//2)
    TextRect1 = (Size_x//2 - 80, Size_y//2 + 25)
    TextRect2 = (Size_x//2- 350, Size_y//2 + 50)
    Screen.blit(Text, TextRect)
    Screen.blit(Text1, TextRect1)
    Screen.blit(Text2, TextRect2)
    pygame.display.update()

def score_life_display(Score,Life):
    font = pygame.font.Font(None, 50)
    Repr_Score = font.render("Score: " + str(Score), 1, Black)
    Repr_Life = font.render("Life: " + str(Life), 1, Black)
    Screen.blit(Repr_Score, (150,8))
    Screen.blit(Repr_Life, (500,8))
    pygame.display.update()

def collisionWall(ball):
    if ball.rect.y<=10:
        ball.velocity_y = -ball.velocity_y
    if ball.rect.x >= Size_x-10:
        ball.velocity_x = -ball.velocity_x
    if ball.rect.x <= 10:
        ball.velocity_x = -ball.velocity_x

def ball_paddle_collision(ball, paddle):
        if pygame.sprite.collide_mask(ball, paddle):
            ball.bounce()

#Main Program
def loop_of_the_game():
    Run = False
    Score = 0
    Life = 3
    #building the wall
    draw_bricks(Blocks, all_sprites_list)

    while not Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Run = True
                elif event.key == pygame.K_p:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            break

        key_getPressed(paddle)
        #Game logic
        all_sprites_list.update()
        collisionWall(ball)
        if ball.rect.y>=Size_y:
            ball.resetBall()
            Life -= 1
        if Life < 0:
            while True:
                reprGameOver(Score)
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    Life = 3
                    Score = 0
                    draw_bricks(Blocks,all_sprites_list)
                    break 
        #Detect collisions between the ball and the paddles
        ball_paddle_collision(ball,paddle)

        killedBricks = pygame.sprite.spritecollide(ball, Blocks, True)
        if len(killedBricks)>0:
            ball.bounce()
            Score += 1
            if len(Blocks) == 0:
                while True:
                    reprGameWon(Score)
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        Score = 0
                        Life = 3
                        draw_bricks(Blocks, all_sprites_list)
                        ball.resetBall()
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        Run = True

        Screen.fill(White)
        all_sprites_list.draw(Screen)
        #Display scores:
        score_life_display(Score,Life)
        Clock.tick(60)
    pygame.quit()
    quit()

loop_of_the_game()
