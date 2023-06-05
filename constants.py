import re

"""
Various Constants used throughout the program
"""
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
ASCII_ZERO = 48
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

PLAYER_SIDE_ROW = 7  # White - Bottom row i.e. Row 7
COMPUTER_SIDE_ROW = 0  # Black - Top row i.e. Row 0

# kingside rook must be present in column 7 in order to be castled
KINGSIDE_ROOK_COLUMN = 7
# queenside rook must be present in column 7 in order to be castled
QUEENSIDE_ROOK_COLUMN = 0
# A king must be present in column 4 in order to be castled
CASTLING_KING_COLUMN = 4
# This is the column where the king piece will end up after castling
KINGSIDE_KING_COLUMN = 5

# Note: the ranks are always ordered from White's perspective,
# so it is labelled White's fourth rank
# Likewise for the fifth rank
FOURTH_RANK = 4
FIFTH_RANK = 3

# The rank (row) of white pieces
PLAYER_PAWNS_RANK = 6
# The rank (row) of black pieces
COMPUTER_PAWNS_RANK = 1


NONE = -1
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

LPAREN = "("
RPAREN = ")"
LBRACKET = "["
RBRACKET = "]"
CHECK_INDICATION = "+"
CHECKMATE_INDICATION = "#"

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

# Regular Expressions

castling_pattern = re.compile(r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z")
chess_move_pattern = re.compile(r"([a-h][1-8]){2}")
