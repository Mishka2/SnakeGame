import os
import time
import keyboard
import random
from colorama import Fore, Back, Style

class Board():

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []
        for row_num in range(rows):
            self.board.append([])

        for row_num in range(len(self.board)):
            for column_num in range(columns):
                self.board[row_num].append(' ')


    def set_color(self, item, end):
        if item == 'X':
            print(Fore.RED + item, end = end)
        elif item == 'O':
            print(Fore.GREEN + item, end = end)
        elif item == '#' or item == '#':
            print(Fore.BLUE + item, end = end)
        elif item == '+':
            print(Fore.RED + item, end = end)
        else:
            print(Style.RESET_ALL + item, end = end)

    def display_board(self):
        os.system("clear")
        for row in range(len(self.board)):
            counter = 0
            for item in self.board[row]:
                if counter < self.columns-1:
                    self.set_color(item, " ")
                    # print(Fore.RED + item, end =" ")
                else:
                    self.set_color(item, None)
                counter += 1
                # print(Style.RESET_ALL)



    def get_board(self):
        return self.board

    def get_board_dim(self):
        return (self.rows, self.columns)

    def clear(self):
        for row_num in range(len(self.board)):
            for index in range(len(self.board[row_num])):
                if self.board[row_num][index] != ' ':
                    self.board[row_num][index] = ' '

    def apply_snake(self, snake, game):
        # print("Body points: " + str(snake.get_body_points()))
        if(self.get_board()[snake.get_body_points()[0][0]][snake.get_body_points()[0][1]] == ' '):
            self.get_board()[snake.get_body_points()[0][0]][snake.get_body_points()[0][1]] = snake.get_head_char()
            for point_index in range(1,len(snake.get_body_points())):
                # print("point_index: " + str(point_index))
                self.get_board()[snake.get_body_points()[point_index][0]][snake.get_body_points()[point_index][1]] = snake.get_body_char()
        elif(self.get_board()[snake.get_body_points()[0][0]][snake.get_body_points()[0][1]] == 'O'): #the snake hit a piece of food
            snake.add_to_body()
            game.food = Food([self.get_board_dim()[0]-1, self.get_board_dim()[1]-1])

    def apply_food(self, food):
        # try:
        # print("error with food: " + str((food.get_coor()[0],food.get_coor()[1])))
        self.get_board()[food.get_coor()[0]][food.get_coor()[1]] = 'O'
        # print("ehllo")

        # except:


    def apply_walls(self, walls):
        #walls = ((top, bottom, left, right))

        for wall in [walls[2],walls[3]]:
            for point in wall:
                # print(point)
                self.get_board()[point[0]][point[1]] = '#'

        for wall in [walls[0],walls[1]]:
            for point in wall:
                # print(point)
                self.get_board()[point[0]][point[1]] = '#'



class Snake():

    def get_head_placement(self):
        return self.get_body_points()[0]

    def set_head_placement(self, coor):
        self.body_points[0] = coor

    def set_next_head_placement(self,coor):
        self.next_head_placement = coor

    def get_next_head_placement(self):
        return self.next_head_placement

    def move_snake_head(self,dir, board):
        curr_coor = self.get_head_placement()
        if dir == 'down':
            self.set_next_head_placement([curr_coor[0]+1,curr_coor[1]])
        elif dir == 'up':
            self.set_next_head_placement([curr_coor[0]-1,curr_coor[1]])
        elif dir == 'right':
            self.set_next_head_placement([curr_coor[0],curr_coor[1]+1])
        elif dir == 'left':
            self.set_next_head_placement([curr_coor[0],curr_coor[1]-1])

    def move_snake_body(self):
        original_body_points = self.get_body_points()

        #making a copy of the original list
        old_body = []
        for point in original_body_points:
            old_body.append(point)

        #making the first point the new point
        new_body= []
        new_body.append(self.next_head_placement)

        #adding the first elements to the new list
        for point_index in range(len(old_body)-1):
            new_body.append(old_body[point_index])

        #making the original list into the "new list"
        for point_index in range(len(new_body)):
            self.body_points[point_index] = new_body[point_index]



    def add_body_point(self, point_coor):
        self.body_points.append(point_coor)

    def get_head_char(self):
        return self.head_character

    def get_body_char(self):
        return self.body_character

    def get_body_points(self):
        return self.body_points

    def get_curr_dir(self):
        return self.last_dir

    def set_curr_dir(self, new_dir):
        self.last_dir = new_dir

    def __init__(self):
        self.initial_head_pos = [2,2]
        self.body_points = [self.initial_head_pos, [self.initial_head_pos[0] -1 , self.initial_head_pos]]
        self.head_character = 'X'
        self.body_character = '+'
        self.last_dir = "down"

    def add_to_body(self):
        last_body_piece = self.get_body_points()[-1]
        if(len(self.get_body_points()) >= 2):
            second_to_last_body_piece = self.get_body_points()[-2]

        #*****************************************************************
        #****IF YOU START WITH ONLY ONE PIECE*****************************
        # else:
        #     dir = self.get_curr_dir()
        #     if dir == 'down':
        #         second_to_last_body_piece = [self.get_body_points()[-1][0]+1, self.get_body_points()[-1][1]]
        #     elif dir == 'up':
        #         second_to_last_body_piece = [self.get_body_points()[-1][0]-1, self.get_body_points()[-1][1]]
        #     elif dir == 'left':
        #         second_to_last_body_piece = [self.get_body_points()[-1][0], self.get_body_points()[-1][1]-1]
        #     elif dir == 'right':
        #         second_to_last_body_piece = [self.get_body_points()[-1][0], self.get_body_points()[-1][1]+1]
        #
        #*****************************************************************

        x_diff = last_body_piece[0] - second_to_last_body_piece[0]
        y_diff = last_body_piece[1] - second_to_last_body_piece[1]

        new_point = [last_body_piece[0]+ x_diff, last_body_piece[1] + y_diff]

        self.add_body_point(new_point)

class Food():

    def get_coor(self):
        return self.placement

    def __init__(self, board_dim):
        self.placement = self.make_rand_food_coor(board_dim)

    def make_rand_food_coor(self, board_dim):
        x = random.randint(2,board_dim[0]-2)
        y = random.randint(2,board_dim[1]-2)

        return [x,y]



class SnakeGame():

    def __init__(self, dimx, dimy):
        self.board = Board(dimx, dimy)
        self.snake = Snake()
        self.food = Food(self.board.get_board_dim())
        self.walls = self.make_walls(dimx,dimy)
        self.curr_key = ''
        self.lose = False
        os.system("clear")

    def get_food(self):
        return self.food

    def set_food(self, food):
        self.food = food

    def any_arrow_pressed(self):
        arrows = ["up", "down", "left", "right", "r"]
        pressed = False
        # print("arrow pressed")
        for arrow in arrows:
            # print("arrow: " + str(pressed))
            pressed = keyboard.is_pressed(arrow)
            if pressed:
                # print("second press: " + str(pressed))
                self.curr_key = arrow
                return pressed

    def check_board_dim(self, coordinates, dir):
        if dir == "down":
            top_bottom =  self.board.get_board_dim()[0] > coordinates[0]+2 >= 0
            left_right =  self.board.get_board_dim()[1] > coordinates[1] >= 0
        elif dir == "right":
            top_bottom =  self.board.get_board_dim()[0] > coordinates[0] >= 0
            left_right =  self.board.get_board_dim()[1] > coordinates[1]+2 >= 0
        elif dir == "up":
            top_bottom =  self.board.get_board_dim()[0] > coordinates[0]-2 >= 0
            left_right =  self.board.get_board_dim()[1] > coordinates[1] >= 0
        elif dir == "left":
            top_bottom =  self.board.get_board_dim()[0] > coordinates[0] >= 0
            left_right =  self.board.get_board_dim()[1] > coordinates[1]-2 >= 0

        return top_bottom and left_right

    def make_walls(self, dimx, dimy):
        #making coordinates of the walls
        top_wall = []
        bottom_wall = []
        left_wall = []
        right_wall = []

        #top_wall
        for place in range(dimy):
            top_wall.append((0,place))

        #left_wall
        for place in range(dimx):
            left_wall.append((place, 0))

        #bottom_wall
        for place in range(dimy):
            bottom_wall.append((dimx-1,place))

        #right_wall
        for place in range(dimx):
            right_wall.append((place,dimy-1))

        # return (top_wall, bottom_wall, left_wall, right_wall)
        return (top_wall, bottom_wall, left_wall, right_wall)


    def display_game(self):
        self.board.clear()
        self.board.apply_food(self.food)
        self.board.apply_snake(self.snake, self)
        self.board.apply_walls(self.walls)
        self.board.display_board()
        self.board.clear()


    def get_opposite(self, key):
        if(key == 'down'):
            return 'up'
        elif(key == 'up'):
            return 'down'
        elif(key == 'left'):
            return 'right'
        elif(key == 'right'):
            return 'left'
        else:
            return ' '


    def run_game(self):
        #self.snake.get_last_dir() = "down"
        time.sleep(.1)
        valid_arrow_press = self.any_arrow_pressed()
        opposite_key = self.get_opposite(self.snake.get_curr_dir())

        #TODO PREVENT snake from moving backwards
        # if(not valid_arrow_press or self.curr_key == opposite_key):
        if(not valid_arrow_press or self.curr_key == opposite_key or self.snake.get_curr_dir() == self.curr_key):
            if(self.check_board_dim(self.snake.get_body_points()[0], self.snake.get_curr_dir()) and not self.snake.get_body_points()[0] in self.snake.get_body_points()[1:]):
                self.snake.move_snake_head(self.snake.get_curr_dir(),self.board)
                self.snake.move_snake_body()
                self.display_game()
            else: #the snake hits the wall
                self.lose = True

        elif(valid_arrow_press):
            self.snake.set_curr_dir(self.curr_key)
            if(self.check_board_dim(self.snake.get_body_points()[0], self.snake.get_curr_dir()) and not self.snake.get_body_points()[0] in self.snake.get_body_points()[1:]):
                self.snake.move_snake_head(self.snake.get_curr_dir(),self.board)
                self.snake.move_snake_body()
                self.display_game()
                # print("Food: " + str(self.food.get_coor()))
            else: #the snake hits the wall
                self.lose = True

        # print("rerun")

        if not self.lose:
            self.run_game()
        else:
            print("YOU LOSE!")

# while(True):
#     if(keyboard.read_key() == 'up'):
#         print("he")
if __name__ == '__main__':
    #rows columns
    SnakeGame(20,30).run_game()

#
# print(" ")
