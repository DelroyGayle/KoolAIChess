# game.py

import constants
import piece
import os


class Game:
    """
    A class that represents the status of the Chess Game
    This is the main workspace of the program
    It keeps track of the flags, properties and variables related
    to the state of play of the Game
    """

# Class Variables

    # recursion level for evaluate()
    level = 0  # todo
    # worth of play
    score = 0
    # Result of evaluate()
    evaluation_result = 0
    # Keep a record of the best scored coordinates
    best_from_file = ""
    best_from_rank = ""
    best_to_file = ""
    best_to_rank = ""
    new_from_file = ""
    new_from_rank = ""
    new_to_file = ""
    new_to_rank = ""

    # REMOVE?? TODO
    # todo check_flag
    # True means that one is currently in Check
    check_flag = False
    # Player (White) goes first
    player_first_move = True
    # White goes first
    whose_move = constants.PLAYER
    who_are_you = constants.PLAYER
    global_piece_sign = constants.PLAYER
    opponent_who_are_you = constants.COMPUTER

    # Output purposes
    output_stream = ""
    output_chess_move = ""
    error_message = ""
    message_printed = False
    current_print_string = ""
    show_taken_message = ""
    promoted_piece = ""
    promotion_message = ""
    player_castled = False
    computer_castled = False
    player_king_moved = False
    player_king_rook_moved = False
    player_queen_rook_moved = False
    computer_king_moved = False
    computer_king_rook_moved = False
    computer_queen_rook_moved = False
    player_pawn_2squares_advanced_file = None
    player_pawn_2squares_advanced_rank = None
    computer_pawn_2squares_advanced_file = None
    computer_pawn_2squares_advanced_rank = None
    en_passant_status = None
    selected_piece = None

    reading_game_file = None
    writing_game_file = False
    input_stream = ""
    input_stream_previous_contents = ""
    general_string_result = ""
    chess_move_tuple = None
    move_type = ""
    move_count = 0
    move_count_incremented = False
    it_is_checkmate = None
    directory_of_open_inputfile = None

    # For Castling
    evaluate_castle_move = ""

    # For the undo-ing of Pawn Promotions
    # Grows and Shrinks with the calling of the 'evaluate' function
    undo_stack2 = None

    # Flag to indicate that the Kool AI is evaluating its next move
    evaluating = None

    def __init__(self):
        self.board = None
        self.fillboard()

    def fillboard(self):
        """
        The Chess Board as designed by Dean Menezes had the following values:

        -500,"R",-270,"N",-300,"B",-900,"Q",-7500,"K",-300,"B",-270,"N",-500,"R"
        -100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P"
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P"
        500,"R",270,"N",300,"B",900,"Q",5000,"K",300,"B",270,"N",500,"R"

        Black at the top has negative values
        The value of each piece is followed by its letter
        Zero and Space show the empty squares
        Then White at the bottom has positive values

        I chose not to use a 8X8 array with numerical indices
        for the following reason.

        In the Chess World,
        a chessboard consists of eight files and eight ranks.
        Columns are known as files and are labelled left to right with letters,
        a to h.
        Rows are known as ranks and are numbered from the bottom of the board
        upwards, 1 to 8.

        So a chessboard is depicted as
        a8, b8, c8, d8, e8, f8, g8, h8
        a7, b7, c7, d7, e7, f7, g7, h7
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
        a2, b2, c2, d2, e2, f2, g2, h2
        a1, b1, c1, d1, e1, f1, g1, h1

        Therefore rather than a 8X8 array with numerical indices;
        instead I chose to use a Python dictionary to reflect the above scheme.
        The keys being a string e.g. "h8" for the square h8
        Then each value would be a Piece Class instance
        of the form Piece(VALUE, LETTER, SIGN)

        Therefore the Dictionary would look like this
        {a8:value, b8:value, ..., d1:None, ..., e1:None, a1:value, ...,
         h1:value}

        Blank squares have the value None

        """
        self.board = dict(
                 # Black Rooks
                 a8=piece.Rook(constants.ROOK_VALUE, constants.COMPUTER),
                 h8=piece.Rook(constants.ROOK_VALUE, constants.COMPUTER),
                 # Black Knights
                 b8=piece.Knight(constants.KNIGHT_VALUE, constants.COMPUTER),
                 g8=piece.Knight(constants.KNIGHT_VALUE, constants.COMPUTER),
                 # Black Bishops
                 c8=piece.Bishop(constants.BISHOP_VALUE, constants.COMPUTER),
                 f8=piece.Bishop(constants.BISHOP_VALUE, constants.COMPUTER),
                 # Black Queen and King
                 d8=piece.Queen(constants.QUEEN_VALUE, constants.COMPUTER),
                 e8=piece.King(constants.KING_VALUE, constants.COMPUTER),
                 # White Rooks
                 a1=piece.Rook(constants.ROOK_VALUE, constants.PLAYER),
                 h1=piece.Rook(constants.ROOK_VALUE, constants.PLAYER),
                 # White Knights
                 b1=piece.Knight(constants.KNIGHT_VALUE, constants.PLAYER),
                 g1=piece.Knight(constants.KNIGHT_VALUE, constants.PLAYER),
                 # White Bishops
                 c1=piece.Bishop(constants.BISHOP_VALUE, constants.PLAYER),
                 f1=piece.Bishop(constants.BISHOP_VALUE, constants.PLAYER),
                 # White Queen and King
                 d1=piece.Queen(constants.QUEEN_VALUE, constants.PLAYER),
                 e1=piece.King(constants.KING_VALUE, constants.PLAYER))

        for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            # Black Pawns
            self.board[letter + "7"] = piece.Pawn(constants.PAWN_VALUE,
                                                  constants.COMPUTER)
            # White Pawns
            self.board[letter + "2"] = piece.Pawn(constants.PAWN_VALUE,
                                                  constants.PLAYER)
        # Blank Squares
        for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            for number in ["3", "4", "5", "6"]:
                self.board[letter + number] = None

        # Designate the kingside rooks
        self.board["h8"].kingside = True
        self.board["h1"].kingside = True

        # Designate the queenside rooks
        self.board["a8"].queenside = True
        self.board["a1"].queenside = True

    def piece_sign(self, index, rank=""):
        """
        Determine the sign of the value of the piece on the square
        Blank squares have a "sign" of 0
        """

        if rank:
            index += rank

        return getattr(self.board[index], "sign", constants.BLANK)

    def piece_value(self, index, rank=""):
        """
        Determine the numerical value of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # Check first whether it is a promoted pawn
        # If so, return its promoted piece's 'value'
        thevalue =  getattr(self.board[index], "promoted_value", None)
        if thevalue is None:
            thevalue = getattr(self.board[index], "value", constants.BLANK)
        return thevalue

    def piece_letter(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # Check first whether it is a promoted pawn
        # If so, return its promoted piece's 'letter'
        theletter =  getattr(self.board[index], "promoted_letter", None)
        if theletter is None:
            theletter = getattr(self.board[index], "letter", constants.BLANK)
        return theletter

    def showboard(self):
        """
        Display the Chessboard
        """

        space = " "
        left_bracket = " ["
        right_bracket = " ]"

        print()
        # 5 spaces THEN 2 spaces each
        print("{}A  B  C  D  E  F  G  H".format(space*5))

        # 3 spaces and 26 dashes "-"
        print("{}{}".format(space*3, "-"*26))

        for row in range(8, 0, -1):
            # SPACE NUMBER |
            output_string = "{}{} |".format(space, row)
            for column in range(8):
                position = (row + column) % 2
                portion1 = left_bracket[position]
                portion2 = right_bracket[position]
                # characters 'a' to 'h'
                letter = chr(constants.ASCII_A + column)
                number = row
                # characters '1' to '8'
                number = chr(constants.ASCII_ZERO + number)
                thesign = self.piece_sign(letter, number)
                if thesign == constants.BLANK:
                    output_string += portion1 + space + portion2
                elif thesign == constants.COMPUTER:
                    output_string += (portion1
                                      + self.piece_letter(letter, number)
                                      + portion2)
                else:
                    output_string += (portion1
                                      + self.piece_letter(letter, number)
                                      .lower()
                                      + portion2)

            print("{}|".format(output_string))

        # 3 spaces and 26 dashes "-"
        print("{}{}".format(space*3, "-"*26))
        # 5 spaces THEN 2 spaces each
        print("{}A  B  C  D  E  F  G  H".format(space*5))
        print()

    def display(self, message):
        """
        Clear Screen
        Show the Chessboard
        Then display a message
        """
        os.system("clear")
        self.showboard()
        print(message)
