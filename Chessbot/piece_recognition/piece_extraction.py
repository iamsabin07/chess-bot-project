import cv2
import pyautogui as pg
import numpy as np

screenshot = pg.screenshot()

screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# to locate the chess board in the screenshot
chess_board = pg.locateOnScreen('chess_board.png')

# constant of the chess board in the screenshot
y = chess_board.top
x = chess_board.left
BOARD_SIZE = 948
CELL_SIZE = int(BOARD_SIZE/8)

# mapping the chess pieces
piece_names = {
    '0': 'black_king',
    '1': 'black_queen',
    '2': 'black_rook',
    '3': 'black_bishop',
    '4': 'black_knight',
    '5': 'black_pawn',
    '6': 'white_knight',
    '7': 'white_pawn',
    '8': 'white_king',
    '9': 'white_queen',
    '10': 'white_rook',
    '11': 'white_bishop',
}

pg.screenshot('screen.png')
screen = cv2.imread('screen.png')

# initializing the chess piece code
piece_code = 0

# looping through each row of chess board
for row in range(8):
    # looping through each column of chess board
    for column in range(8):
        if row in [0, 1, 5, 6]:
            if row == 0 or row == 6:
                if column == 0 or column == 2 or column == 4 or column == 6:
                    # cropping the piece by slicing numpy array
                    piece_image = screen[y:y + CELL_SIZE, x:x + CELL_SIZE]
                    cv2.imshow('pieces', piece_image)
                    cv2.waitKey(0)
                    # saving the chess piece image in the directory
                    cv2.imwrite('./pieces/' + piece_names[str(piece_code)] + '.png', piece_image)
                    piece_code += 1
            if row == 1 or row == 5:
                if column == 1 or column == 3:
                    # cropping the piece by slicing numpy array
                    piece_image = screen[y:y + CELL_SIZE, x:x + CELL_SIZE]
                    cv2.imshow('pieces', piece_image)
                    cv2.waitKey(0)
                    cv2.imwrite('./pieces/' + piece_names[str(piece_code)] + '.png', piece_image)
                    piece_code += 1
        x += CELL_SIZE
    x = chess_board.left
    y += CELL_SIZE

cv2.destroyAllWindows()
