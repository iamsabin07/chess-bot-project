import sys
import time
import chess.engine
import chess
import cv2
import pyautogui as pg
import numpy as np


# constant attributes of the chess board
BOARD_lEFT_COORDINATES = 8
BOARD_TOP_COORDINATES = 180
x = BOARD_lEFT_COORDINATES
y = BOARD_TOP_COORDINATES
BOARD_SIZE = 545
CELL_SIZE = int(BOARD_SIZE/8)

# player's choice
WHITE_PIECES = 0
BLACK_PIECES = 1
player_side = 0

# read user's input
try:
    if sys.argv[1] == 'black':
        player_side = BLACK_PIECES
except:
    print('Try again')
    sys.exit(0)

# position of pieces into coordinates
square_to_coordinates = []

# array to convert board square indices to coordinates
get_square = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
]

# naming the pieces to name FEN string
piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}


# to detect the chess piece in the board
def locate_piece(screenshot, piece_location):
    # loop over the pieces
    for value in range(len(piece_location)):
        piece = piece_location[value]

        # draw rectangle around recognized piece
        cv2.rectangle(screenshot,
                      (piece.left, piece.top),
                      (piece.left + piece.width, piece.top + piece.height),
                      255, 2)
    cv2.imshow('Screenshot', screenshot)
    cv2.waitKey(0)


# to detect the position of the chess piece
def locate_position():
    piece_locations = {
        'black_king': [],
        'black_queen': [],
        'black_rook': [],
        'black_bishop': [],
        'black_knight': [],
        'black_pawn': [],
        'white_knight': [],
        'white_pawn': [],
        'white_king': [],
        'white_queen': [],
        'white_rook': [],
        'white_bishop': []
    }

    # to take the screenshot
    screenshot = pg.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # loop over piece names
    for piece in piece_names.keys():
        # store piece locations by detecting pieces in the selected folder
        for location in pg.locateAllOnScreen('./piece_recognition/pieces/' + piece + '.png', confidence=0.8):
            # to detect noise
            noise = False
            # loop over the matched pieces
            for position in piece_locations[piece]:
                # to detect the noise
                if abs(position.left - location.left) < 8 and abs(position.top - location.top) <=8:
                    noise = True
                    break
                elif piece == 'black_pawn' and abs(position.left - location.left) <= 8:
                    noise = True
                    break
                elif piece == 'black_rook' and abs(position.left - location.left) <= 8:
                    noise = True
                    break
            if noise:
                continue

            # append the piece into piece location
            piece_locations[piece].append(location)
            print("detecting: ", piece, location)
    # return pieces location in the screenshot
    return screenshot, piece_locations

# get FEN string from the piece position
def fen_from_locations(piece_locations):
    # initialize FEN string
    fen_string = ''

    x_coord = BOARD_lEFT_COORDINATES
    y_coord = BOARD_TOP_COORDINATES

    # loop over the rows
    for row in range(8):
        # empty squares count
        empty = 0

        # loop over board columns
        for column in range(8):
            # initialize square
            square = row * 8 + column
            # detect the piece
            is_piece = ()
            # loop over the piece types
            for piece_type in piece_locations.keys():
                # loop over the pieces in the piece locations
                for piece in piece_locations[piece_type]:
                    if abs(piece.left - x_coord) < 8 and abs(piece.top - y_coord) < 8:
                        if empty:
                            fen_string += str(empty)
                            empty = 0
                        # add key corresponding to piece to the FEN string
                        fen_string += piece_names[piece_type]
                        is_piece = (square, piece_names[piece_type])

            if not len(is_piece):
                empty += 1
            # increase x coordinates by cell size
            x_coord += CELL_SIZE

        if empty:
            fen_string += str(empty)
        if row < 7:
            fen_string += '/'
        # restore x coordinates
        x_coord = BOARD_lEFT_COORDINATES
        # increase y coordinates by cell size
        y_coord += CELL_SIZE
    # add side to move to fen
    fen_string += ' ' + 'b' if player_side else ' w'
    # for castling and en passant
    fen_string += ' KQkq - 0 1'

    # return fen string
    return fen_string

# search best moves in the selected position
def search(fen_string):
    print('Looking for the best move in this position: ')
    print(fen_string)
    board = chess.Board(fen=fen_string)
    print(board)

    # load Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("./Stockfish/stockfish.exe")
    # get best move
    best_move = str(engine.play(board, chess.engine.Limit(time=0.1)).move)

    # close engine
    engine.quit()
    # return the best move
    return best_move


# Initial coordinates for the game

# board's top and left coordinates
x = BOARD_lEFT_COORDINATES
y= BOARD_TOP_COORDINATES

# loop over the rows
for row in range(8):
    # loop over column
    for column in range(8):
        # initialize squares
        square = row*8 + column
        # append square with the square coordinates
        square_to_coordinates.append((int(x + CELL_SIZE/2), int(y+CELL_SIZE/2)))

        # increase x coordinates by cell size
        x += CELL_SIZE
    # restore x coordinates
    x = BOARD_lEFT_COORDINATES
    # increase y coordinates by cell size
    y += CELL_SIZE

# Main Driver
while True:
    try:
        # locate the pieces
        screenshot, piece_locations = locate_position()
        # get FEN string from the pieces coordinates
        fen_string = fen_from_locations(piece_locations)
        # search best moves from stockfish
        best_move = search(fen_string)
        print('Best move: ', best_move)

        # extract source and destination square coordinates
        from_sq = square_to_coordinates[get_square.index(best_move[0] + best_move[1])]
        to_sq = square_to_coordinates[get_square.index(best_move[2] + best_move[3])]

        # use pyautoGUI to move the curser to source coordinates
        pg.moveTo(from_sq)
        pg.click()
        # use pyautoGUI to move the curser to destination coordinates
        pg.moveTo(to_sq)
        pg.click()
        # wait for n seconds
        time.sleep(4)

    except:
        # exit system
        sys.exit(0)


