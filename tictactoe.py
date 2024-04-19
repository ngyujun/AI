import pygame
import sys
from PIL import ImageGrab
from PIL import Image
import pyautogui
import time
import numpy as np
import os
import subprocess
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import math


# Load model
model = tf.keras.models.load_model('circle_cross_blank_model.h5')

# Initialize Pygame
pygame.init()

# Constants
SS = True
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (10, 231, 255)
CROSS_COLOR = (255, 66, 66)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board setup
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_test_board(test_board):
    for row in test_board:
        print(" | ".join(row))
        print("-" * 9)

def evaluate(test_board):
    for row in test_board:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return row[0]

    for col in range(len(test_board)):
        if test_board[0][col] == test_board[1][col] == test_board[2][col] and test_board[0][col] != ' ':
            return test_board[0][col]

    if test_board[0][0] == test_board[1][1] == test_board[2][2] and test_board[0][0] != ' ':
        return test_board[0][0]

    if test_board[0][2] == test_board[1][1] == test_board[2][0] and test_board[0][2] != ' ':
        return test_board[0][2]

    if any(' ' in row for row in test_board):
        return None
    return 'tie'

def minimax(test_board, is_maximizing):
    result = evaluate(test_board)

    if result == 'X':
        return -1
    elif result == 'O':
        return 1
    elif result == 'tie':
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if test_board[i][j] == ' ':
                    test_board[i][j] = 'O'
                    score = minimax(test_board, False)
                    test_board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if test_board[i][j] == ' ':
                    test_board[i][j] = 'X'
                    score = minimax(test_board, True)
                    test_board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def find_best_move(test_board):
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if test_board[i][j] == ' ':
                test_board[i][j] = 'O'
                print_test_board(test_board)
                score = minimax(test_board, False)
                test_board[i][j] = ' '
                print(score, best_score)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# Draw lines for Tic-Tac-Toe board
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw Xs and Os on the board
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)
    
    
                
def test(SS, player, game_over):
    if SS and not game_over and player == "O":
        clear_directory()
        
        subprocess.call(['C:/Windows/pyw.exe', 'C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/img.pyw'])
        print("")
        print("")
        test_board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

        
        # Load your image
        for num in range(9):
            test_image_path = 'C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/screenshots/'+str(num)+'.png'
            print(test_image_path)
            
            test_image = Image.open(test_image_path)
            #test_image = screenshot

            # Resize the image to the same size as training images (200x200)
            test_image = test_image.convert('RGB')
            test_image_resized = test_image.resize((200, 200))

            # Convert image to array and rescale pixel values to [0, 1]
            test_image_array = np.array(test_image_resized) / 255.0

            # Expand dimensions to match model input shape
            test_image_input = np.expand_dims(test_image_array, axis=0)

            # Make prediction
            prediction = model.predict(test_image_input)

            # Get the index of the class with the highest probability
            predicted_class_index = np.argmax(prediction)
            print(predicted_class_index)
            nums = num + 1
            row = num // 3
            col = num % 3

            # Print prediction
            if predicted_class_index == 0:
                test_board[row][col] = " "
            elif predicted_class_index == 1:
                test_board[row][col] = "O"
            else:
                test_board[row][col] = "X"
        print("final")
        print_test_board(test_board)
        print("above")
        best_move = find_best_move(test_board)
        pyautogui.moveTo(760 + (best_move[1] * 200),340 + (best_move[0] * 200))
        pyautogui.click()
        print(best_move)

        
        

def clear_directory():
    directory = 'C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/screenshots/'
    # Get a list of all the files in the directory
    files = os.listdir(directory)
    
    # Iterate over each file and delete it
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")



        
# Mark the square where the player clicked
def mark_square(row, col, player):
    board[row][col] = player

# Check if the square is empty
def is_square_empty(row, col):
    return board[row][col] == ' '

# Check if there's a winner
def check_winner(player):
    # Check rows and columns
    for i in range(BOARD_ROWS):
        if all(board[i][j] == player for j in range(BOARD_COLS)) or \
                all(board[j][i] == player for j in range(BOARD_ROWS)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or \
            all(board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)):
        return True

    return False

# Main game loop
def main():
    global board
    global player
    player = 'X'
    game_over = False
    while not game_over:
        SS = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("wuh woh")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE
                SS = True
                if is_square_empty(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_winner(player):
                        game_over = True
                    elif all(board[i][j] != ' ' for i in range(BOARD_ROWS) for j in range(BOARD_COLS)):
                        game_over = True
                    if not game_over:
                        player = 'O' if player == 'X' else 'X'


        screen.fill(WHITE)
        draw_lines()
        draw_figures()
        pygame.display.update()
        test(SS,player, game_over)
    print("exit")
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = 'X'
    main()

if __name__ == "__main__":
    main()

