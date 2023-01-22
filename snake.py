# https://www.edureka.co/blog/snake-game-with-pygame/
import pygame
import time
import random

pygame.init()


class Cube:
    def __init__(self, dis, color_tuple, size, x_coord, y_coord):
        self.dis = dis
        self.color_tuple = color_tuple
        self.size = size
        self.x_coord = x_coord
        self.y_coord = y_coord

    def move_cube(self, new_x, new_y):
        self.x_coord = new_x
        self.y_coord = new_y

    def draw_cube(self):
        pygame.draw.rect(self.dis, self.color_tuple, [self.x_coord, self.y_coord, self.size, self.size])

    def getcoord(self):
        return self.x_coord,self.y_coord


class MySnake:
    def __init__(self, cube):
        self.snake = []
        self.add_new_cube(cube)

    def add_new_cube(self, cube):
        self.snake.insert(0,cube)

    def size(self):
        return len(self.snake)

    def getsnake(self):
        return self.snake

    def move_snake(self, x_change, y_change):
        self.previous_x = x_change
        self.previous_y = y_change
        for cube in self.snake:
            x_change = self.previous_x
            y_change = self.previous_y
            self.previous_x = cube.x_coord
            self.previous_y = cube.y_coord
            cube.move_cube(x_change, y_change)

    def check_collision(self, dis_width, dis_height):
        for cube in self.snake[1:-1]:
            if cube.getcoord() == self.snake[0].getcoord():
                return True
        coord = self.snake[0].getcoord()
        if dis_width <= coord[0] or \
           coord[0] < 0 or \
           coord[1] < 0 or \
           dis_height <= coord[1]:
            return True
        return False


class Color:
    def __init__(self):
        self.r = self.random_value()
        self.g = self.random_value()
        self.b = self.random_value()

    def random_value(self):
        return random.randint(0, 255)


    def make_tuple(self):
        while self.r < 128 and self.g < 128 and self.b < 128:
            self.r = self.random_value()
            self.g = self.random_value()
            self.b = self.random_value()
        return (self.r, self.g, self.b)


def check_highscore():
    with open("highscore.txt", "r") as f:
        value = f.readline()
        if value is None or value == "":
            return None
        return int(value)


def highscore(score):
    current_highscore = check_highscore()
    highscore = str(score) + "\n"
    if current_highscore is None or current_highscore == 0 or current_highscore < score:
        with open("highscore.txt", "w") as g:
            g.write(highscore)


def accelerate(current_speed):
    return current_speed * 1.01


def make_color_array():
    array=[]
    i = 0
    while i < 100:
        color = Color()
        array.append(color.make_tuple())
        i += 1
    return array

white = (255, 255, 255)
yellow = (255, 255, 102)
red = (213, 50, 80)
black = (0, 0, 0)
# color_array = [(87, 235, 186),
#                (87, 212, 242),
#                (90, 129, 219),
#                (120, 87, 242),
#                (195, 86, 235),
#                (66, 255, 240),
#                (58, 222, 129),
#                (85, 245, 75),
#                (163, 224, 40),
#                (250, 234, 50)]
color_array = make_color_array()

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Kevin')

clock = pygame.time.Clock()

snake_block = 10
Snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)


def make_new_cube():
    cube = Cube(dis, random_color(), snake_block,
                round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0,
                round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0)
    return cube


def random_color():
    random_number = round(random.randint(0, len(color_array) - 1))
    return color_array[random_number]


def Your_score(score):
    value = score_font.render(f"Your Score: {str(score)}", True, yellow)
    dis.blit(value, [0, 0])


def Your_highscore():
    text = score_font.render(f"Highscore: {str(check_highscore())}", True, yellow)
    text_rect = text.get_rect()
    text_rect.right = dis_width
    dis.blit(text, text_rect)

def our_snake(snake):
    for x in snake.getsnake():
        x.draw_cube()


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    snake_speed = Snake_speed
    increase = True

    x1_change = 0
    y1_change = 0

    snake = MySnake(Cube(dis, random_color(), snake_block, x1, y1))
    last_move = ""

    food_cube = make_new_cube()
    write_score = True

    while not game_over:

        while game_close:
            if write_score:
                highscore(snake.size() - 1)
                write_score = False
            snake_speed = Snake_speed
            increase = True
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(snake.size() - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return gameLoop()

        move = True


        """
        Change log:
        change directions:
        Up Down
        Left Right
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and move == True:
                if (event.key in (pygame.K_LEFT, pygame.K_a) and
                        last_move != "x"):
                    x1_change = -snake_block
                    y1_change = 0
                    last_move = "x"
                    move = False
                elif (event.key in (pygame.K_RIGHT, pygame.K_d) and
                      last_move != "x"):
                    x1_change = snake_block
                    y1_change = 0
                    last_move = "x"
                    move = False
                elif (event.key in (pygame.K_UP, pygame.K_w) and
                      last_move != "y"):
                    y1_change = -snake_block
                    x1_change = 0
                    last_move = "y"
                    move = False
                elif (event.key in (pygame.K_DOWN, pygame.K_s) and
                      last_move != "y"):
                    y1_change = snake_block
                    x1_change = 0
                    last_move = "y"
                    move = False


        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        food_cube.draw_cube()

        # How snake moves
        snake.move_snake(x1,y1)

        if snake.check_collision(dis_width, dis_height):
            game_close = True

        our_snake(snake)
        Your_score(snake.size() - 1)
        Your_highscore()

        pygame.display.update()

        foodx = food_cube.getcoord()[0]
        foody = food_cube.getcoord()[1]

        # Food has been eaten
        if x1 == foodx and y1 == foody:
            snake.add_new_cube(food_cube)
            food_cube = make_new_cube()

        if (snake.size() - 1) > 0 == ((snake.size() - 1) % 1):
            if increase:
                snake_speed = accelerate(snake_speed)
                increase = False
        else:
            increase = True

        clock.tick(snake_speed)
        move = True

    snake_speed = Snake_speed
    pygame.quit()
    quit()


gameLoop()