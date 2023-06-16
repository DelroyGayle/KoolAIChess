"""
constants.py
Various Constants used throughout the program
"""

import re

# maximum recursive calls for the function evaluate()
# 5 normal play; 3 dumber and quicker
MAXLEVEL = 5

# Negative number used to represent Black
COMPUTER = -1
# Positive number used to represent White
PLAYER = 1

# Values of each piece
VALUE_OF_COMPUTER_KING = -7500  # Black
VALUE_OF_PLAYER_KING = 5000  # White

# Value of each Chess Piece
KING_VALUE = 5000
QUEEN_VALUE = 900
ROOK_VALUE = 500
BISHOP_VALUE = 300
KNIGHT_VALUE = 270
PAWN_VALUE = 100

ASCII_SPACE = 32
ASCII_A_MINUS1 = 96
ASCII_A = 97
ASCII_ZERO = 48
ASCII_EIGHT = 56
BLANK = 0
# Seven Tag Rosters expected
STR_TOTAL = 7

# 7 Characters being the longest Move Text (e.g., "Qa6xb7#", "fxg1=Q+")
LINESIZE = 80 - 7
FILE_SIZE_LIMIT = 10000
EVALUATE_THRESHOLD_SCORE = 10000
# If the 'evaluate' functions computes a score less than this value,
# then the Computer will resign
STALEMATE_THRESHOLD_SCORE = -2500

DESTINATION_SQUARE_ONLY = 1  # EG e4 OR Ne2
PAWN_CAPTURE_FILE = 2  # EG exd4
PIECE_DESTINATION_SQUARE = 3  # EG Qxe1
PIECE_FILE_MOVE = 4  # EG Nge2 Nfxe4
PIECE_RANK_MOVE = 5  # EG N2d4 N6xe4
PIECE_BOTH_SQUARES = 6   # EG  Nd2xe4
LONG_NOTATION = 7  # EG Ng1f3
CASTLING_MOVE = 8  # O-O or O-O-O

PLAYER_SIDE_RANK = "1"    # White - Bottom row
COMPUTER_SIDE_RANK = "8"  # Black - Top row

# kingside rook  must be present in file 'h' in order to be castled
KINGSIDE_ROOK_FILE = "h"
# queenside rook must be present in file "a" in order to be castled
QUEENSIDE_ROOK_FILE = "a"
# A king must be present in file 'e' in order to be castled
CASTLING_KING_FILE = "e"

# Note: the ranks are always ordered from White's perspective,
# so it is labelled White's fourth rank
# Likewise for the fifth rank
FOURTH_RANK = "4"  # a4...h4
FIFTH_RANK = "5"  # a5...h5

# The rank (row) of white pieces
PLAYER_PAWNS_RANK = "2"  # a2...h2
# The rank (row) of black pieces
COMPUTER_PAWNS_RANK = "7"  # a7...h7


NOVALUE = -1
INVALID = 1
VALID = 2
ALREADY_CASTLED = 3
NO_KING_ROOK = 4
KING_MOVED = 5
ROOK_MOVED = 6
NOT_ALL_BLANK = 7
KING_IN_CHECK = 8
THROUGH_CHECK = 9
END_UP_IN_CHECK = 10
KINGSIDE = 11
QUEENSIDE = 12

TAB = "\t"  # TODO
SPACE = " "
CHECK_INDICATION = "+"
CHECKMATE_INDICATION = "#"
CASTLING_KINGSIDE = "O-O"
CASTLING_QUEENSIDE = "O-O-O"

# Defined this way to keep the linter happy :)
# Note the SPACE at the end
BAD_CHESS_MOVE_FROMFILE = ("Legal Chess Move Expected From Input File. "
                           "Instead: "
                           )
# Note the SPACE at the end
BAD_EN_PASSANT_FROMFILE = "Illegal En Passant Read From Input File: "

PLAYER_WON = "1-0"
COMPUTER_WON = "0-1"

KING_LETTER = "K"
QUEEN_LETTER = "Q"
ROOK_LETTER = "R"
BISHOP_LETTER = "B"
KNIGHT_LETTER = "N"
PAWN_LETTER = "P"

"""
Generate a list of the entire chessboard coordinates
['a1', 'a2' ... 'h7', 'h8']
In order to save time with 'evaluate'
generated such a list from scratch
"""

PRESET_CHESSBOARD = [chr(j+97) + chr(k+49)
                     for j in range(8)
                     for k in range(8)]

# FILE I/O

INPUT_PGN_NAME = "input.pgn"
OUTPUT_PGN_NAME = "output.pgn"
SLEEP_VALUE = 2  # Pause 2 seconds

# Regular Expressions
percent_pattern = re.compile(r"(\A%)|(\n%)")
en_passant_pattern = re.compile(r"\Ae\.p\.[ \n]*")
nag_pattern = re.compile(r"\A\$[0-9]+")
parens_pattern = re.compile(r"[()]")
periods_pattern = re.compile(r"\A[.]+")
move_number_pattern = re.compile(r"\A[0-9]+[. ]*")
move_number_suffix_pattern = re.compile(r"\A[.][ \n]*")
game_termination_pattern = re.compile(r"\A((1-0)|(0-1)|(1/2-1/2)|[*])")

# 7
long_notation_pattern = re.compile(r"\A([KQRBN]?)([a-h][1-8])([a-h][1-8])",
                                   flags=re.IGNORECASE | re.ASCII)

# 6
capture_2squares_pattern = re.compile(r"\A([KQRBN]?)([a-h][1-8])x([a-h][1-8])",
                                      flags=re.IGNORECASE | re.ASCII)
# 1
one_square_pattern = re.compile(r"\A([KQRBN]?)([a-h][1-8])",
                                flags=re.IGNORECASE | re.ASCII)
# 2
pawn_capture_pattern = re.compile(r"\A([a-h])x?([a-h][1-8])",
                                  flags=re.IGNORECASE | re.ASCII)
# 3
nonpawn_capture_pattern = re.compile(r"\A([KQRBN])x([a-h][1-8])",
                                     flags=re.IGNORECASE | re.ASCII)

# 4
file_pattern = re.compile(r"\A([KQRBN])([a-h])x?([a-h][1-8])",
                          flags=re.IGNORECASE | re.ASCII)

# 5
rank_pattern = re.compile(r"\A([KQRBN])([1-8])x?([a-h][1-8])",
                          flags=re.IGNORECASE | re.ASCII)

castling_inputfile_pattern = re.compile(r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))")

chess_move_suffix_pattern = re.compile(r"\A[A-Za-z0-9+#=:\-]*")

castling_keyboard_pattern = re.compile(r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z")
chess_move_pattern = re.compile(r"([a-h][1-8]){2}")
