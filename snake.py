"""
Author: Michelle Loven github.com/Mishka2
Date created: July 28, 2019
Last edited: August 7, 2019

Snake game!
sudo python snake.py
"""

import os
import time
import keyboard
import random
from colorama import Fore, Back, Style

"""
Board holds all information for the terminal display system 
This class sets the colors of the objects within the game, draws the snake and food 
and builds the board on terminal 
"""
class Board():

    #Initialize the board with #rows and #columns 
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []

        self.head_char = 'X'
        self.body_char = '+'
        self.food_char = 'O'
        self.wall_char = '#'

        for row_num in range(rows):
            self.board.append([])

        for row_num in range(len(self.board)):
            for column_num in range(columns):
                self.board[row_num].append(' ')

    #Sets the color of each character when printed on terminal 
    def set_color(self, item, end):
        if item == self.head_char:
            print(Fore.RED + item, end = end)
        elif item == self.food_char:
            print(Fore.GREEN + item, end = end)
        elif item == self.wall_char:
            print(Fore.BLUE + item, end = end)
        elif item == self.body_char:
            print(Fore.RED + item, end = end)
        else:
            print(Style.RESET_ALL + item, end = end)

    #Prints every character into terminal 
    def display_board(self):
        os.system("clear")
        for row in range(len(self.board)):
            counter = 0
            for item in self.board[row]:
                if counter < self.columns-1:
                    self.set_color(item, " ")
                else:
                    self.set_color(item, None)
                counter += 1

    #Returns the board object
    def get_board(self):
        return self.board

    #returns the board dimensions 
    def get_board_dim(self):
        return (self.rows, self.columns)

    #clears the board from terminal to reset the page
    def clear(self):
        for row_num in range(len(self.board)):
            for index in range(len(self.board[row_num])):
                if self.board[row_num][index] != ' ':
                    self.board[row_num][index] = ' '

    #Draws the snake onto the board based on the Snake object's information
    def apply_snake(self, snake, game):
        snake_x = snake.get_body_points()[0][0]
        snake_y = snake.get_body_points()[0][1]
        if(self.get_board()[snake_x][snake_y] == ' '):
            self.get_board()[snake_x][snake_y] = self.head_char
            for point_index in range(1,len(snake.get_body_points())):
                x_coor = snake.get_body_points()[point_index][0]
                y_coor = snake.get_body_points()[point_index][1]
                self.get_board()[x_coor][y_coor] = self.body_char
        elif(self.get_board()[snake_x][snake_y] == self.food_char): #the snake hit a piece of food
            snake.add_to_body()
            game.add_to_score(10)
            game.food = Food([self.get_board_dim()[0]-1, self.get_board_dim()[1]-1])

    #Displays the food 
    def apply_food(self, food):
        self.get_board()[food.get_coor()[0]][food.get_coor()[1]] = self.food_char

    #Draws the walls 
    def apply_walls(self, walls):
        #walls = (top, bottom, left, right)
        for wall in walls:
            for point in wall:
                self.get_board()[point[0]][point[1]] = self.wall_char

"""
Board holds all information for the snake direction, length, and placement
This class handles the snake movements based on the last pressed keyboard button 
This class also handles the addition of body parts based on the food intake of the snake
"""
class Snake():

    #Returns the coordinate points of the head of the snake
    def get_head_placement(self):
        return self.get_body_points()[0]

    #Sets the coordinate of the head
    def set_head_placement(self, coor):
        self.body_points[0] = coor

    #Sets the next coordinate of the head
    def set_next_head_placement(self,coor):
        self.next_head_placement = coor

    #Gets the coordinate of the head
    def get_next_head_placement(self):
        return self.next_head_placement

    #Changes the direction of the snake based on key press
    def move_snake_head(self,dir, board):
        curr_coor = self.get_head_placement()
        #Puts the head in the next place, will recursively move the rest of body 
        if dir == 'down':
            self.set_next_head_placement([curr_coor[0]+1,curr_coor[1]])
        elif dir == 'up':
            self.set_next_head_placement([curr_coor[0]-1,curr_coor[1]])
        elif dir == 'right':
            self.set_next_head_placement([curr_coor[0],curr_coor[1]+1])
        elif dir == 'left':
            self.set_next_head_placement([curr_coor[0],curr_coor[1]-1])

    #Recursively move the rest of the snake body
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

    #Add a point to the end of the snake body if the snake eats
    def add_body_point(self, point_coor):
        self.body_points.append(point_coor)

    #gets the list of coordinate points for the snake sprite
    def get_body_points(self):
        return self.body_points

    #Gets the current direction of the snake
    def get_curr_dir(self):
        return self.last_dir

    #Sets the current direction of the snake
    def set_curr_dir(self, new_dir):
        self.last_dir = new_dir

    #initialize the snake 
    def __init__(self):
        self.initial_head_pos = [2,2]
        self.body_points = [self.initial_head_pos, [self.initial_head_pos[0] -1 , self.initial_head_pos]]
        self.last_dir = "down"

    #Add piece to body 
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

"""
Food holds all information for the food displayed on the board
THis class stores the coordinates for the food 
"""
class Food():

    def get_coor(self):
        return self.placement

    def __init__(self, board_dim):
        self.placement = self.make_rand_food_coor(board_dim)

    #Randomize the next placement of food
    def make_rand_food_coor(self, board_dim):
        x = random.randint(2,board_dim[0]-2)
        y = random.randint(2,board_dim[1]-2)

        return [x,y]


"""
SnakeGame holds all information for each game. 
This class checks for highscore file, creates a file, and reads/writes from 
the highschore file
This class checks for input from keyboard and responds accordingly 
This class creates the walls for the baord and displays the highscore 
"""
class SnakeGame():

    #initialize snake game, with the correct dimensions sent to Board
    def __init__(self, dimx, dimy):
        self.board = Board(dimx, dimy)
        self.snake = Snake()
        self.food = Food(self.board.get_board_dim())
        self.walls = self.make_walls(dimx,dimy)
        self.curr_key = ''
        self.score = 0
        self.high_score = 0
        self.check_highscore_file("highscore.txt")
        self.check_highscore("highscore.txt")
        self.lose = False
        os.system("clear")

    #check if there is a highscore file
    def check_highscore_file(self, file_name):
        try:
            file = open(file_name, 'r')
            file.close()
        except:
            file = open(file_name, 'w+')
            file.close()

    #Refresh highscore
    def refresh_highscore(self, file_name):
        if self.score > self.high_score:
            # print("bigger")
            self.high_score = self.score
            file = open(file_name, 'w')
            file.write(str(self.high_score))
            file.close()

    #checks highscore from file
    def check_highscore(self, file_name):
        file = open(file_name, 'r')
        file_list = file.readlines()
        if file_list != []:
            self.high_score = int(file_list[0])
        file.close()

    #Get the food object
    def get_food(self):
        return self.food

    #Set the food object to be a certain character
    def set_food(self, food):
        self.food = food

    #Return which key has been pressed
    def any_arrow_pressed(self):
        arrows = ["up", "down", "left", "right", "r"]
        pressed = False
        for arrow in arrows:
            pressed = keyboard.is_pressed(arrow)
            if pressed:
                self.curr_key = arrow
                return pressed

    #Check that the snake hasn't hit a wall
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


    #Display all objects in terminal
    def display_game(self):
        self.board.clear()
        self.board.apply_food(self.food)
        self.board.apply_snake(self.snake, self)
        self.board.apply_walls(self.walls)
        self.board.display_board()
        self.board.clear()

    #Make sure that the user cannot make the snake go in the opposite direction as currently heading
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

    #adds to current score
    def add_to_score(self, add):
        self.score += add

    #Final display
    def final_display(self):
        self.snake.move_snake_head(self.snake.get_curr_dir(),self.board)
        self.snake.move_snake_body()
        self.display_game()

    #run the game!
    def run_game(self):
        time.sleep(.05)
        valid_arrow_press = self.any_arrow_pressed()
        opposite_key = self.get_opposite(self.snake.get_curr_dir())

        if(not valid_arrow_press or self.curr_key == opposite_key or self.snake.get_curr_dir() == self.curr_key):
            if(self.check_board_dim(self.snake.get_body_points()[0], self.snake.get_curr_dir())
                and not self.snake.get_body_points()[0] in self.snake.get_body_points()[1:]):
                self.final_display()
            else: #the snake hits the wall
                self.lose = True

        elif(valid_arrow_press):
            self.snake.set_curr_dir(self.curr_key)
            if(self.check_board_dim(self.snake.get_body_points()[0], self.snake.get_curr_dir())
                and not self.snake.get_body_points()[0] in self.snake.get_body_points()[1:]):
                self.final_display()
            else: #the snake hits the wall
                self.lose = True

    #Display the score
    def display_score(self):
        print(Fore.MAGENTA + "Score: " + str(self.score))
        self.refresh_highscore("highscore.txt")
        # self.get_highscore("highscore.txt")
        print(Fore.MAGENTA + "Highscore: " + str(self.high_score))
        print(Style.RESET_ALL)


if __name__ == '__main__':
    game = SnakeGame(20,30)
    while(not game.lose):
        game.display_score()
        game.run_game()

    print("YOU LOSE!")
