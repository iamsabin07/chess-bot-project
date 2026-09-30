# ML Chess Engine

Standalone machine-learning chess engine for the chess-bot project.

## Contract

Input: FEN string

Output: UCI move such as `e2e4`

The ML engine is developed independently from the existing OpenCV/PyAutoGUI bot. Once validated, it will replace the Stockfish-backed `search(fen_string)` implementation.

## V1 roadmap

1. Encode a `python-chess` board as an 18 x 8 x 8 tensor.
2. Generate labeled positions using Stockfish offline.
3. Train a neural value network.
4. Rank legal moves by evaluating resulting positions.
5. Add alpha-beta search using the neural network at leaf nodes.
6. Plug the engine into the existing chess bot.

## Board encoding

Channels 0-11 are piece planes:

- white pawn, knight, bishop, rook, queen, king
- black pawn, knight, bishop, rook, queen, king

Channels 12-17:

- side to move
- white kingside castling
- white queenside castling
- black kingside castling
- black queenside castling
- en-passant target square

Board coordinates use row 0 = rank 8 and column 0 = file a.
