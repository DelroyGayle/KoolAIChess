"""

This Python Program is Based on
'How To Write A Chess Program in QBASIC By Dean Menezes.'

To quote Rod Bird who also adopted Menezes' program :-
    "Qudos to Mr Menezes for such a stunningly short and powerful Chess AI."

Menezes' QBASIC program can be found at
 http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt

"""

import constants
import piece
import fileio
import os
import re
import time


class CustomException(Exception):
    """
    My custom exception class
    Just in case a Chess Logic Error that I had not anticipated happens!
    This definition is based on
    https://www.pythontutorial.net/python-oop/python-custom-exception/
    """


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
    # todo check_flag
    # True means that one is currently in Check
    check_flag = False
    # Player (White) goes first
    player_first_move = True
    # White goes first
    whose_move = constants.PLAYER
    who_are_you = constants.PLAYER
    opponent_who_are_you = constants.COMPUTER

    # Output purposes
    output_stream = ""
    output_chess_move = ""
    error_message = ""
    message_printed = False
    computer_print_string = ""
    show_taken_message = ""

    promoted_piece = ""
    player_castled = False
    computer_castled = False
    player_king_moved = False
    player_king_rook_moved = False
    player_queen_rook_moved = False
    computer_king_moved = False
    computer_king_rook_moved = False
    computer_queen_rook_moved = False
    player_pawn_2squares_advanced_col = None
    player_pawn_2squares_advanced_row = None
    computer_pawn_2squares_advanced_col = None
    computer_pawn_2squares_advanced_row = None
    en_passant_status = None
    selected_piece = None

    reading_game_file = None
    writing_game_file = False
    input_stream = ""
    input_stream_previous_contents = ""
    move_type = ""
    skipped_seven_tag_rosters = False
    tag_pair_count = 0
    move_count = 0
    move_count_incremented = False
    it_is_checkmate = None

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

        # space = " " todo
        return getattr(self.board[index], "value", constants.BLANK)

    def piece_letter(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # space = " " todo
        return getattr(self.board[index], "letter", None)

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


def goodbye():
    """
    End of Game Message
    """

    print()
    print("Thank You For Playing")
    print("Goodbye")
    quit()


def computer_resigns():
    """
    Computer has determined that its next course of action is to
    Resign! It cannot win!
    """

    print("Kool AI resigns!")
    output_all_chess_moves(constants.PLAYER_WON)
    goodbye()
    # Computer Resigns
    # *** END PROGRAM ***


def handle_internal_error():
    """
    Hopefully this method is not necessary
    I added this method just in case there is some kind of logic error
    that causes a chess logic problem e.g. a King piece being taken!
    If such a thing happens then abort this program with an error message
    """

    print("Computer resigns due to an internal error")
    print("Please investigate")
    # output_all_chess_moves(constants.PLAYER_WON) todo
    goodbye()
    # Internal Error
    # *** END PROGRAM ***


def is_piece_taken(chess, to_file, to_rank, piece_sign):
    """
    Set up a message showing which user took which piece
    Return the positive value of the piece taken

    In addition I added a test to check that the attacking/taking logic
    is correctly working
    If a 'King' is about to be taken, raise an error because such a move
    is illegal in Chess

    Note the Kings' values are:
        Computer's King (-7500) and Player's King (5000)
    """

    Game.show_taken_message = ""
    piece_taken = chess.piece_value(to_file, to_rank)

    # Return None for a Blank Square
    if not piece_taken:
        return None

    # Check whether a King is about to be actually taken!
    # Note the Kings' values: Computer's King (-7500) and Player's King (5000)
    if (piece_taken == constants.VALUE_OF_COMPUTER_KING or
            piece_taken == constants.VALUE_OF_PLAYER_KING):

        """
        This means the PLAYER/COMPUTER was allowed to make an illegal move
        i.e. KING cannot actually be taken
        One can attack a KING - Not take a King
        This should never happen!
        Some internal logic error has occurred
        """
        raise CustomException("Internal Error: King piece about to be taken: "
                              + str(piece_taken))

    # Check whether the same colour is about to be taken
    # Of course, this should never happen!
    if ((piece_sign < 0 and chess.piece_sign(to_file, to_rank) < 0)
       or
       (piece_sign > 0 and chess.piece_sign(to_file, to_rank) > 0)):
        """
        Some internal logic error has occurred
        """
        raise CustomException("Internal Error: "
                              "Piece of the same colour about to be taken: "
                              + str(piece_taken))

    # Convert to a positive number
    piece_taken = abs(piece_taken)

    if piece_sign < 0:
        message = "Computer took your "
    else:
        message = "Player took my "

    index = to_file + to_rank
    Game.show_taken = message + chess.board[index].print_string()
    return piece_taken


def make_move_to_square(chess, from_square, to_square, to_file, to_rank):
    """
    Fill the square taken
    """

    chess.board[to_square] = chess.board[from_square]

    # erase square vacated
    chess.board[from_square] = None
    # promote pawn if it reaches the board edge
    any_promotion(chess, to_file, to_rank)


def advance_vertical(rank, steps):
    """
    Calculate the new rank
    by adding 'steps' to the current 'rank'
    (8 at the top, 1 at the bottom)
    If the sum is not within the range 1 - 8
    then return None
    """

    newrank = chr(ord(rank) + steps)
    return newrank if "1" <= newrank <= "8" else None


def advance_horizontal(file, steps):
    """
    Calculate the new file
    by adding 'steps' to the current 'file'
    ('a' to the far left, 'h' to the far right)
    If the sum is not within the range a - h
    then return None
    """

    newfile = chr(ord(file) + steps)
    return newfile if "a" <= newfile <= "h" else None


def check_horizontally(chess, file_start, limit, step, rank,
                       moves_list, piece_sign):
    """
    Move either right to left OR left to right
    For each blank square append the square's coordinates
    When an opponent piece has been reached, append the square's coordinates
    and return the list
    When a piece of the same colour has been reached
    or the edge of the board has been reached,
    return the list
    """

    for m in range(file_start, limit, step):
        newfile = chr(m + constants.ASCII_A_MINUS1)  # 96
        square_sign = chess.piece_sign(newfile, rank)
        if piece_sign != square_sign:
            # Either an opponent piece or a blank square
            moves_list.append(newfile + rank)

        # Reached an occupied square - proceed no further
        if square_sign != constants.BLANK:
            return moves_list

    return moves_list


def check_vertically(chess, rank_start, limit, step,
                     file, moves_list, piece_sign):
    """
    Move either from top to bottom OR from bottom to top
    For each blank square append the square's coordinates
    When an opponent piece has been reached, append the square's coordinates
    and return the list
    When a piece of the same colour has been reached
    or the edge of the board has been reached,
    return the list
    """

    for m in range(rank_start, limit, step):
        newrank = chr(m + constants.ASCII_ZERO)  # 48
        square_sign = chess.piece_sign(file, newrank)
        if piece_sign != square_sign:
            # Either an opponent piece or a blank square
            moves_list.append(file + newrank)

        # Reached an occupied square - proceed no further
        if square_sign != constants.BLANK:
            return moves_list

    return moves_list


def horizontal_vertical(chess, file, rank, moves_list, piece_sign):
    """
    Record blank squares or an opponent's square
    whilst scanning both horizontally and vertically
    """

    # Convert 'file' i.e. 'a' to 'h' to a number between 1 to 8
    base_file_number = ord(file) - constants.ASCII_A_MINUS1  # 96

    # Move from the current piece's position,
    # towards the left until reaching a nonblank square
    # or the edge of the board
    moves_list = check_horizontally(chess, base_file_number - 1, 0, -1,
                                    rank, moves_list, piece_sign)

    # Move from the current piece's position,
    # towards the right until reaching a nonblank square
    # or the edge of the board
    moves_list = check_horizontally(chess, base_file_number + 1, 8, 1,
                                    rank, moves_list, piece_sign)

    # Convert 'rank' i.e. '1' to '8' to a number between 1 to 8
    base_rank_number = ord(rank) - constants.ASCII_ZERO  # 48

    # Move from the current piece's position,
    # towards the bottom until reaching a nonblank square
    # or the edge of the board
    moves_list = check_vertically(chess, base_rank_number - 1, 0, -1,
                                  file, moves_list, piece_sign)

    # Move from the current piece's position,
    # towards the top until reaching a nonblank square
    # or the edge of the board
    moves_list = check_vertically(chess, base_rank_number + 1, 8, 1,
                                  file, moves_list, piece_sign)

    return moves_list


def check_diagonally(chess, basefile, baserank,
                     horizontal, vertical, piece_sign):
    """
    Move diagonally by one square
    If the coordinates are off the board, return False
    If a piece of the same colour has been reached return False
    If the square is blank return the square's coordinates
    If an opponent piece has been reached return the square's coordinates
    """

    newfile = chr(basefile + horizontal)
    newrank = chr(baserank + vertical)
    if not (("a" <= newfile <= "h") and ("1" <= newrank <= "8")):
        return None

    square_sign = chess.piece_sign(newfile, newrank)
    if piece_sign == square_sign:
        # Same colour piece
        return None

    # Either an opponent piece or a blank square
    return newfile + newrank


def diagonal(chess, file, rank, moves_list, piece_sign):
    """
    Record blank squares or an opponent's square
    whilst scanning diagonally
    """

    # Convert 'file' i.e. 'a' to 'h' to its corresponding code
    base_file_number = ord(file)
    # Convert 'rank' i.e. '1' to '8' to its corresponding code
    base_rank_number = ord(rank)

    # Move from the current piece's position,
    # diagonally bottom-left until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  -m, -m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square and continue
        moves_list.append(result)

    # Move from the current piece's position,
    # diagonally bottom-right until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  -m, m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square and continue
        moves_list.append(result)

    # Move from the current piece's position,
    # diagonally top-left until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  m, -m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square and continue
        moves_list.append(result)

    # Move from the current piece's position,
    # diagonally top-right until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  m, m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square and continue
        moves_list.append(result)

    return moves_list


def generate_moves_for_pawn(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the Pawn piece
    The legality of the moves are checked later
    """

    rank_plus1 = advance_vertical(rank, piece_sign)
    if not rank_plus1:
        # Reached the edge of the board
        return moves_list

    # Capture left?
    newfile = advance_horizontal(file, -1)
    # Is there an opponent piece present?
    if newfile and chess.piece_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # Capture right?
    newfile = advance_horizontal(file, 1)
    # Is there an opponent piece present?
    if newfile and chess.piece_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # one step forward?
    # Is this square blank?
    if chess.piece_sign(file, rank_plus1) == constants.BLANK:
        moves_list.append(file + rank_plus1)

    # two steps forward?
    rank_plus2 = (advance_vertical(rank, 2) if piece_sign == constants.PLAYER
                  else advance_vertical(rank, -2))

    if rank == "2" and piece_sign == constants.PLAYER:
        rank_plus2 = advance_vertical(rank, 2)
    elif rank == "7" and piece_sign == constants.COMPUTER:
        rank_plus2 = advance_vertical(rank, -2)
    else:
        rank_plus2 = False

    if rank_plus2:
        # Is this square blank?
        if chess.piece_sign(file, rank_plus2) == constants.BLANK:
            moves_list.append(file + rank_plus2)

    return moves_list


def generate_moves_for_rook(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the Rook piece
    The legality of the moves are checked later
    """

    return horizontal_vertical(chess, file, rank, moves_list, piece_sign)


def examine_this_square(diffs_tuple, chess, file, rank, piece_sign):
    """
    Check if it is possible for this piece to land on this square
    Calculate the square's coordinates using the numbers in 'diffs_tuple'
    """

    (file_diff, rank_diff) = diffs_tuple

    # Is it on the board?
    newfile = chr(ord(file) + file_diff)
    if not ("a" <= newfile <= "h"):
        return False

    newrank = chr(ord(rank) + rank_diff)
    if not ("1" <= newrank <= "8"):
        return False

    index = newfile + newrank
    square_sign = chess.piece_sign(newfile, newrank)

    # True: Either an opponent piece or a blank square
    # False: Otherwise same coloured piece
    return piece_sign != square_sign


def add_knight_king_square(diffs_tuple, file, rank):
    """
    Having determined that it is possible
    for a Knight piece or a King piece
    to land on a particular square
    Create the coordinates of this square using the numbers in 'diff_tuple'
    e.g. (1, 2) means file += 1, rank += 2.
    """

    (file_diff, rank_diff) = diffs_tuple
    newfile = chr(ord(file) + file_diff)
    newrank = chr(ord(rank) + rank_diff)
    return newfile + newrank


def generate_moves_for_knight(chess, file, rank,
                              moves_list, piece_sign):
    """
    Generate all the possible moves of the Knight piece
    The legality of the moves are checked later
    """

    knight_moves = [
        (-1, -2),  # down 1, left 2
        (-1, 2),   # down 1, right 2
        (-2, -1),  # down 2, left 1
        (-2, 1),   # down 2, right 1
        (1, -2),   # up 1, left 2
        (1, 2),    # up 1, right 2
        (2, -1),   # up 2, left 1
        (2, 1),    # up 2, right 1
    ]

    moves_list += [add_knight_king_square(diffs, file, rank)
                   for diffs in knight_moves
                   if examine_this_square(diffs, chess,
                                          file, rank, piece_sign)]
    return moves_list


def generate_moves_for_bishop(chess, file, rank,
                              moves_list, piece_sign):
    """
    Generate all the possible moves of the Bishop piece
    The legality of the moves are checked later
    """

    return diagonal(chess, file, rank, moves_list, piece_sign)


def generate_moves_for_queen(chess, file, rank,
                             moves_list, piece_sign):
    """
    Generate all the possible moves of the Queen piece
    The legality of the moves are checked later
    """

    moves_list = diagonal(chess, file, rank, moves_list, piece_sign)
    moves_list = horizontal_vertical(chess, file, rank, moves_list, piece_sign)
    return moves_list


def generate_moves_for_king(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the King piece
    The legality of the moves are checked later
    """

    king_moves = [
        (0, 1),     # up
        (0, -1),    # down
        (-1, 0),    # left
        (1, 0),     # right
        (-1, 1),    # diagonal up-left
        (1, 1),     # diagonal up-right
        (-1, -1),   # diagonal down-left
        (1, -1),    # diagonal down-right
    ]

    moves_list += [add_knight_king_square(diffs, file, rank)
                   for diffs in king_moves
                   if examine_this_square(diffs, chess,
                                          file, rank, piece_sign)]

    return moves_list


def determine_generate_move_method(piece_letter):
    """
    Use a dictionary to determine which method to call
    """

    methods_dictionary = {
        constants.PAWN_LETTER:      generate_moves_for_pawn,
        constants.ROOK_LETTER:      generate_moves_for_rook,
        constants.KNIGHT_LETTER:    generate_moves_for_knight,
        constants.BISHOP_LETTER:    generate_moves_for_bishop,
        constants.QUEEN_LETTER:     generate_moves_for_queen,
        constants.KING_LETTER:      generate_moves_for_king,
    }

    themethod = methods_dictionary.get(piece_letter, "Unknown letter: "
                                       + piece_letter)

    if isinstance(themethod, str):
        raise CustomException("Internal Error: " + themethod)

    return themethod


def generate_moves(self, piece_sign):
    """
    Generate a list of valid moves for a particular piece
    """
    ...
    # todo


def movelist(chess, from_file, from_rank, piece_sign, evaluating=False):
    """
    Get a list of possible moves for a particular piece
    """

    index = from_file + from_rank
    letter = (chess.board[index]).letter
    if not letter:
        return []  # blank square

    # Determine which function to call
    generate_moves_method = determine_generate_move_method(letter)
    all_the_moves = generate_moves_method(chess,
                                          from_file, from_rank,
                                          [],
                                          chess.board[index].sign)

    return all_the_moves


"""
    if bpiece(x, y)
        elif == asc("P")
            pawn(x, y, piece_sign)
        elif == asc("N")
            knight(x, y, piece_sign)
        elif == asc("B")
            bishop(x, y, piece_sign)
        elif == asc("R")
            rook(x, y, piece_sign)
        elif == asc("Q")
            queen(x, y, piece_sign)
        elif == asc("K")
            king(x, y, piece_sign)
# Determine whether a Castling move is feasible
            if evaluating:
                  print("Castle", evaluating, level)  # todo
                  evaluate_castle(x, y, piece_sign)
todo
"""


def in_check(chess, user_sign):
    """
    To quote Rod Bird:
    this function [ scans ] all squares to see if any opposition piece
    has the King in Check
    """

    opponent_sign = -user_sign

    # Go through each square on the board
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            index = letter + number
            if chess.piece_sign(index) == opponent_sign:
                all_the_moves = movelist(chess, letter, number,
                                         opponent_sign, False)
                # Start scanning each move
                for m in range(len(all_the_moves)):
                    if (chess.piece_letter(all_the_moves[m])
                       == constants.KING_LETTER):
                        # Opponent King is in Check!
                        return True

    # Indicate that the Opponent King is not in Check at all
    return False


def test_each_move(chess, who_are_you,
                   from_square,
                   to_square):
    """
    Go through each possible move
    To see if there is one whereby the king
    is no longer 'in check'
    """

    # store From and To data so that it may be restored
    save_from_square = chess.board[from_square]
    save_to_square = chess.board[to_square]
    to_file = to_square[0]
    to_rank = to_square[1]

    # Make the move so that it can be tested for 'Check'
    make_move_to_square(chess,
                        from_square, to_square, to_file, to_rank)
    check_flag = in_check(chess, who_are_you)

    # Restore previous squares
    chess.board[from_square] = save_from_square
    chess.board[to_square] = save_to_square

    if not check_flag:
        # A suitable move has been found
        # Therefore it is not Checkmate
        return True

    # Otherwise continue the loop i.e. continue testing
    return False


def is_it_checkmate(chess, who_are_you):
    """
    Determine whether the opponent is in Checkmate
    That is, the opponent's king is under attack,
    and there is no possible chess move available
    to save the king

    To determine whether Checkmate:
    This is done by going through each piece of the same colour as the King
    To see if there is any move generated which does not put the King in check
    If there is no such move then CHECKMATE!
    """

    # Filter all the squares containing the same colour
    same_colour_pieces_list = [index for index in constants.PRESET_CHESSBOARD
                               if chess.piece_sign(index) == who_are_you]

    # Go through each square and see if a piece can make a play
    # such that the king is no longer under threat
    for index in same_colour_pieces_list:
        from_file = index[0]
        from_rank = index[1]
        all_the_moves = movelist(chess, from_file, from_rank,
                                 who_are_you, False)

        # Loop through each possible move
        for m in range(len(all_the_moves)):
            exit_loop = test_each_move(chess, who_are_you,
                                       index, all_the_moves[m])

            if exit_loop:
                # Not Checkmate!
                return False

            # Otherwise continue testing
            continue

    # No move found so definitely Checkmate!
    Game.it_is_checkmate = who_are_you
    return True


def is_player_move_illegal(chess, from_file, from_rank, to_file, to_rank):

    """
    Determine whether the PLAYER'S move is illegal
    For example:
    1) Does the PLAYER'S move put the PLAYER in Check?
    2) Can the chosen piece make that move?
    """

    piece_sign = constants.PLAYER  # white piece
    all_possible_moves = movelist(chess, from_file, from_rank,
                                  piece_sign, False)

    from_square = from_file + from_rank
    to_square = to_file + to_rank
    # Start scanning each move
    for m in range(len(all_possible_moves)):
        if all_possible_moves[m] == to_square:

            """
            Found the move that matches the Piece,
                  the From square and the To square

            Print a Message if a piece is about to be taken
            At the same time,
            Check whether the Computer's King is about to be literally taken
            If so, this indicates an Internal Logic Error
            """

            taken = is_piece_taken(chess, to_file, to_rank, piece_sign)
            # No error raised - so the above test passed

            from_square = from_file + from_rank
            to_square = to_file + to_rank

            # store From and To data so that it may be restored
            save_from_square = chess.board[from_square]
            save_to_square = chess.board[to_square]

            # Make the Player's move
            make_move_to_square(chess,
                                from_square, to_square, to_file, to_rank)

            # Does this PLAYER's move place the PLAYER in Check?
            # If so, illegal move!

            check_flag = in_check(chess, constants.PLAYER)
            if check_flag:
                # reset play and restore board pieces
                # check_flag todo
                # checkmate # todo
                print("You are in Check")
                chess.board[from_square] = save_from_square
                chess.board[to_square] = save_to_square
                # Indicate that the chosen move placed the Player in Check
                return (True, True, taken)

            # Indicate not in check
            # check_flag todo
            return (False, False, taken)

    # Indicate that no legal move has been found
    return (True, None, None)


def output_attacking_move(chess, who_are_you,
                          from_file, from_rank, to_file, to_rank):
    """
    Create a output message for the current chess move
    Showing who played what, the from square and the to square
    """
    strings_dict = {
        constants.KING_LETTER:   "King",
        constants.QUEEN_LETTER:  "Queen",
        constants.ROOK_LETTER:   "Rook",
        constants.BISHOP_LETTER: "Bishop",
        constants.KNIGHT_LETTER: "Knight",
        constants.PAWN_LETTER:   "Pawn"
    }
    dict_entry = strings_dict.get(chess.piece_letter(from_file, from_rank), "")
    print_string = (from_file + from_rank + "-" + to_file + to_rank
                    + " Piece: " + dict_entry)

    if who_are_you == constants.PLAYER:
        return "Checking Player move for " + print_string
    else:
        return "Computer moves " + print_string


def convert_played_piece(letter, from_file, from_rank, to_file, to_rank):
    """
    Convert the piece into output format
    e.g. e2e4 for a pawn move
         Ng1f3 for a knight move
    """

    Game.output_chess_move = letter if letter != constants.PAWN_LETTER else ""
    Game.output_chess_move += from_file + from_rank + to_file + to_rank


def add_capture_promotion(taken):
    """
    If a piece has been taken indicate this
    by adding 'x' before the last two characters e.g. e5d5 ==> e5xd4
    If a Pawn has been promoted to, for example, a Queen; indicate this
    by adding =Q at the end of the Chess move e.g. f1xg1=Q
    """

    if taken:
        # add 'x' before the last two characters e.g. e5d5 ==> e5xd4
        length = len(Game.output_chess_move)
        suffix = Game.output_chess_move[-2:]
        Game.output_chess_move = (Game.output_chess_move[0:length - 2] + "x"
                                  + suffix)

    if Game.promoted_piece:
        # EG Add =Q at the end if a Pawn was promoted to a Queen e.g. fxg1=Q
        Game.output_chess_move += "=" + Game.promoted_piece


def add_check_to_output():
    """
    Indicate Check!
    """

    Game.output_chess_move += constants.CHECK_INDICATION


def add_checkmate_to_output(thestring):
    """
    Indicate Checkmate!
    Remove any trailing '+' OR SPACE first; then add # and SPACE afterwards
    """

    return (thestring.rstrip(constants.CHECK_INDICATION + constants.SPACE)
            + constants.CHECKMATE_INDICATION + constants.SPACE)


def setup_output_chess_move_add_promotion(letter, from_file, from_rank,
                                          to_file, to_rank, taken):
    """
    Convert the current chess move into an output format
    to show
    1) What piece has been played
    2) Does it do a capture?
    3) Is it a promoted pawn?
    """

    # Convert the chess move in order to output it
    convert_played_piece(letter, from_file, from_rank, to_file, to_rank)

    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # this is denoted as =Q e.g. f1xg1=Q
    add_capture_promotion(taken)


# promote pawn if it reaches board edge
def any_promotion(chess, to_file, to_rank):
    """
    Pawn Promotion
    Promote Pawn Piece if it reaches the board edge
    """

    to_square = to_file + to_rank
    if (to_rank == "8"
       and chess.piece_value(to_square) == constants.PAWN_VALUE):

        # The Player has reached the top of the board
        # Promote the White Pawn to a White Queen
        chess.board[to_square].value = constants.QUEEN_VALUE
        chess.board[to_square].letter = constants.QUEEN_LETTER
        Game.promoted_piece = constants.QUEEN_LETTER

    elif (to_rank == to_rank == "1"
          and chess.piece_value(to_square) == -constants.PAWN_VALUE):
        # The Computer has reached the bottom of the board
        # Promote the Black Pawn to a Black Queen
        chess.board[to_square].value = -constants.QUEEN_VALUE
        chess.board[to_square].letter = constants.QUEEN_LETTER
        Game.promoted_piece = constants.QUEEN_LETTER

    else:
        Game.promoted_piece = ""


def coords_formula(file, rank):
    """
    Need to convert chessboard squares coordinates
    from chess algebraic notation to
    computer array notation
    COLUMN FIRST that is Y then X

    EG
    a8 TOP LEFT to 0,0 TOP LEFT
    h1 BOTTOM RIGHT to 7,7 BOTTOM RIGHT

    a8 to 0,0
    a7 to 0,1
    a1 to 0,7
    b8 to 1,0
    h8 to 7,0
    h7 to 7,1
    h1 to 7,7
    etc
    """

    file_number = ord(file) - constants.ASCII_A  # 97
    rank_number = constants.ASCII_EIGHT - ord(rank)
    return (file_number, rank_number)


def do_evaluation(chess, level, piece_sign, prune_factor,
                  from_file, from_rank,
                  to_file, to_rank,
                  bestscore):
    """
    Perform the evaluation using
    minimax/negamax formula
    """

    from_square = from_file + from_rank
    to_square = to_file + to_rank

    # store From and To data so that it may be restored
    save_from_square = chess.board[from_square]
    save_to_square = chess.board[to_square]
    targetvalue = chess.piece_value(to_square)
    (to_file_number, to_rank_number) = coords_formula(to_file, to_rank)
    # Make the move so that it can be evaluated
    make_move_to_square(chess,
                        from_square, to_square, to_file, to_rank)

    # negamax formula
    if level < constants.MAXLEVEL:
        temp_calc = (bestscore - targetvalue + piece_sign
                     * (8 - abs(4 - to_file_number) - abs(4 - to_rank_number)))

        Game.score += evaluate(chess,
                               level,
                               -piece_sign,
                               temp_calc)

    """
    Rod Bird's comment:
    Unwind the recursion by coming back here
    until we finally return to the main program flow
    Work out the score adding a small amount
    to favour forwards and central play
    """

    temp_calc = (8 - abs(4 - to_file_number) - abs(4 - to_rank_number))
    Game.score += targetvalue - piece_sign * temp_calc

    """
    Rod Bird's comment:
    If it results in a better score than previously
    then store it as the best
    """

    if ((piece_sign < 0 and Game.score > bestscore)
       or
       (piece_sign > 0 and Game.score < bestscore)):
        bestscore = Game.score
        if level == 1:
            # Record the best move found so far
            Game.best_from_file = from_file
            Game.best_from_rank = from_rank
            Game.best_to_file = to_file
            Game.best_to_rank = to_rank

        # Restore previous squares
        chess.board[from_square] = save_from_square
        chess.board[to_square] = save_to_square

        """
        Rod Bird's comment:
        If it is not as good as a previous piece move
        then cut the search short
        Exit the loop in 'evaluate'
        """

        if ((piece_sign < 0 and bestscore >= prune_factor)
           or
           (piece_sign > 0 and bestscore <= prune_factor)):
            exitloop = True

        else:
            # Continue the loop i.e. continue evaluating
            exitloop = False

        return (exitloop, bestscore)

    # Restore previous squares
    chess.board[from_square] = save_from_square
    chess.board[to_square] = save_to_square
    # Continue the loop i.e. continue evaluating
    exitloop = False
    return (exitloop, bestscore)


def evaluate(chess, level, piece_sign, prune_factor):
    """
    To quote Rod Bird:
    This function checks all squares for players
    to move then recursively test plays.
    It plays its own move then plays the opponent's best move,
    recursively over four moves.
    So getting the potential net worth of each moveable player on the board.
    The highest scored determines the computer's next move.
    It is a classic mini max evaluation shortened
    to its a negamax form with pruning
    i.e. it does not waste time on lower value plays.
    """

    # Update recursion level
    level += 1
    if level > constants.MAXLEVEL:
        raise CustomException("Internal Error: Level Number Overflow: "
              + str(level))

    bestscore = constants.EVALUATE_THRESHOLD_SCORE * piece_sign
    # Go through each square on the board

    """
    PRESET_CHESSBOARD is a list containing the entire chessboard coordinates
    ['a1', 'a2' ... 'h7', 'h8']
    In order to
    1) save time in regards to generating such a list from scratch
    2) the need for two nested for-loops in regards to generating the list
    3) Instead I filter PRESET_CHESSBOARD for all the pieces of
       the same colour of the current user using a List Comprehension
    """

    same_colour_pieces_list = [index for index in constants.PRESET_CHESSBOARD
                               if chess.piece_sign(index) == piece_sign]

    for index in same_colour_pieces_list:
        # Have a same coloured piece - evaluate its score
        from_file = index[0]
        from_rank = index[1]

        all_the_moves = movelist(chess, from_file, from_rank,
                                 piece_sign, level == 1)
        # if level == 1:  # Level 1 # todo refactor with level == 1 ==>
        #     all_the_moves = movelist(chess, from_file, from_rank,
        #                              piece_sign, True)
        # else:
        #     all_the_moves = movelist(chess, from_file, from_rank,
        #                              piece_sign, False)

        # Loop through each possible move
        for m in range(len(all_the_moves)):
            # todo
            # For level=1, add logic to handle castling

            (to_file, to_rank) = all_the_moves[m]
            oldscore = Game.score
            (exit_loop, bestscore) = do_evaluation(chess, level,
                                                   piece_sign,
                                                   prune_factor,
                                                   from_file, from_rank,
                                                   to_file, to_rank,
                                                   bestscore)

            # Restore 'score'
            Game.score = oldscore
            if exit_loop:
                return bestscore  # Done!

            # Otherwise continue evaluating
            continue

    return bestscore  # Done!


def execute_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    Carry out the chess move that was produced
    by the 'evaluate' function
    """

    piece_sign = constants.COMPUTER  # black piece
    # display the move
    attacking_piece_letter = chess.piece_letter(from_file, from_rank)

    Game.computer_print_string = output_attacking_move(chess,
                                                       constants.COMPUTER,
                                                       from_file, from_rank,
                                                       to_file, to_rank)

    """
    Check whether a Player's piece is about to be taken
    Print a Message if this is true
    At the same time,
    Check whether the Player's King is about to be literally taken
    If so, this indicates an Internal Logic Error
    It would mean the COMPUTER's best move is an illegal move!
    'Kings' cannot actually be taken in Chess!
    """

    from_square = from_file + from_rank
    to_square = to_file + to_rank
    taken = is_piece_taken(chess, to_file, to_rank, piece_sign)
    # No error raised - so the above test passed

    # Make the Computer's move
    make_move_to_square(chess, from_square, to_square, to_file, to_rank)

    # If the COMPUTER cannot play out of check then resign
    check_flag = in_check(chess, constants.COMPUTER)
    if check_flag:
        computer_resigns()

# todo
# Has the king been moved?
# Has a rook been moved
#       record_if_king_or_rook_have_moved(constants.COMPUTER, x, y, x1, y1)

# As the opponent advanced a pawn two squares?
#       If yes, record the pawn's position
#       record_pawn_that_advanced_by2(constants.COMPUTER, x, y, x1, y1)

# Convert the chess move in order to output it
# Add a 'x' to the output chess move if a piece was taken
# Add the promoted piece if a promotion took place
# Then output the piece to the output file
    setup_output_chess_move_add_promotion(attacking_piece_letter,
                                          from_file, from_rank,
                                          to_file, to_rank, taken)
    # return (attacking_piece, taken)  # todo


def finalise_computer_move(chess):
    """
    Now that the Computer's move has been performed
    Output the chess move to the output stream
    Determine whether the Player is in Check
    If so, determine to see if the Computer has won
    That is, is it Checkmate?
    """

    # Display the Computer's move
    chess.display(Game.computer_print_string)
    if (Game.show_taken_message):
        # Show what piece the Computer took
        print(Game.show_taken_message)

    # check_flag todo

    check_flag = in_check(chess, constants.PLAYER)
    if check_flag:
        # todo
        # showboard()
        # print("You are in check")
        # todo checkmate
        print("You are in check")
        add_check_to_output()
        check_flag = is_it_checkmate(chess, constants.PLAYER)
        if check_flag:
            print("Checkmate!! I Win!")
            # todo print(Game.output_chess_move)
            # Keep Linter happy
            chess_move = Game.output_chess_move
            Game.output_chess_move = add_checkmate_to_output(chess_move)

            # todo
#            append_to_output(Game.output_chess_move + constants.SPACE)
# keep this flag unset from now on; so that the move count is incremented
# g_move_count_incremented = False
# todo

            time.sleep(3)
            chess.display("Checkmate!! I Win!")


def process_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    This routine handles the playing of the Computer's move
    """

    # todo
    # just_performed_castling = False
    computer_move_finalised = False

    if Game.player_first_move:
        # Player goes first so on the very first iteration
        # there is no processing of Computer Moves
        Game.player_first_move = False
        return

    # From this point onwards, process the Computer's move

    # king on king end game?
    # Stalemate?
    if Game.evaluation_result < constants.STALEMATE_THRESHOLD_SCORE:
        computer_resigns()

# Validate, Execute then Finalise the Computer Chess Move
# (if it was not a Castling Chess Move)
    if not computer_move_finalised:
        execute_computer_move(chess,
                              from_file, from_rank,
                              to_file, to_rank)
        # todo
        # finalise_computer_move
        # (check_flag, Game.output_chess_move, g_move_count_incremented)
        finalise_computer_move(chess)


def finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                         print_string,
                         attacking_piece_letter, taken):
    """
    Now that the Player's move has been performed
    Output the chess move to the output stream
    Determine whether the Computer is in Check
    If so, determine to see if the Player has won
    That is, is it Checkmate?
    """

    # TODO just_performed_castling, attacking_piece

    # TODO
    # Increment Move Number
    #        if not g_move_count_incremented:
    #            g_move_count+=1

    #        g_move_count_incremented = False
    # keep this flag unset from now on; so that the move count is incremented

    # Output the Move Number
    #     append_to_output(lstrip(str(g_move_count)) + "." + constants.SPACE)

    # Convert the chess move in order to output it
    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # Then output the piece to the output file
    setup_output_chess_move_add_promotion(attacking_piece_letter,
                                          from_file, from_rank,
                                          to_file, to_rank, taken)

    # Display the move
    chess.display(print_string)
    if (Game.show_taken_message):
        # Show what piece the Player took
        print(Game.show_taken_message)

# Now that the opponent has played, see if the computer is in Check
# check_flag todo

    check_flag = in_check(chess, constants.COMPUTER)
    if check_flag:
        print("I am in Check")
        add_check_to_output()
        check_flag = is_it_checkmate(chess, constants.COMPUTER)
        if check_flag:
            # Keep Linter happy
            chess_move = Game.output_chess_move
            Game.output_chess_move = add_checkmate_to_output(chess_move)
            print("Checkmate!! You Win!")
            # todo
#            append_to_output(Game.output_chess_move + constants.SPACE)
#            output_all_chess_moves(constants.PLAYER_WON)
# todo
            print()
            goodbye()
            # Checkmate!
            # *** END PROGRAM ***


def handle_input_from_game_file(chess, from_file, from_rank, to_file, to_rank,
                                attacking_piece_letter, taken):
    """
    For testing purposes I read Chess moves from an input file
    Therefore, if this option is ON
    Handle chess moves from an input file
    """

    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"
    if not Game.reading_game_file:
        # No File Handling. Fetch the chess move from the user
        return do_next

    # File Input ...
    # Ensure that these are set correctly
    Game.who_are_you = constants.PLAYER
    Game.opponent_who_are_you = constants.COMPUTER
    
    fileio.fetch_chess_move_from_file()

    # Was a castling move read from the file? If so, process it
    if Game.reading_game_file and Game.move_type == constants.CASTLING_MOVE:
        # A Castling Move has been read from the file - process it
        just_performed_castling = handle_castling(constants.PLAYER)

        if not just_performed_castling:
            # The Castling that was read from the input file was invalid!
            # 'handle_castling() redisplays the Board and displays the appropriate error messaging
            # No further input from the input file - rather fetch from the user
            do_next = "continue"
            return do_next

        """
        The Castling that was read from the input file was valid!
        Castling Validation has already been performed 
        to see whether Castling would put the Player in Check
        'indicate_castling_done()' displays the appropriate messaging 
        regarding the Castling

        Since this chess move is not a pawn that has advanced two squares
        Ensure that previous values for 'Player' have been reset
        """
        
        reset_2squares_pawn_positions(constants.PLAYER)
        # Increment the move count
        # Convert player's chess move for output
        # Output the chess move
        # TODO 
        finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                             print_string, # todo
                             attacking_piece_letter, taken)
        do_next = "return"
        return do_next

    # Otherwise 'pass'
    return do_next


def handle_castling_input(chess, from_file, from_rank, to_file, to_rank):
    """
    *** CASTLING ***
    This is denoted by using capital 'O'
    that is O-O and O-O-O
    It is not PGN notation to use ZEROS
    However will cater for 0-0 and 0-0-0
    """

    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"
    if not constants.castling_pattern.match(input_string):
            # \A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z"
        # No Castling move. Determine what this chess move is
        return do_next

    Game.general_string_result = input_string
    just_performed_castling = handle_castling(constants.PLAYER)
    if not just_performed_castling:
        # This Castling move is invalid!
        # 'handle_castling() redisplays the Board and displays the appropriate error messaging
        do_next = "continue"
        return do_next

    """
    The Castling move was valid!
    Castling Validation has already been performed 
    to see whether Castling would put the Player in Check
    'indicate_castling_done()' displays the appropriate messaging 
    regarding the Castling

    Since this chess move is not a pawn that has advanced two squares
    Ensure that previous values for 'Player' have been reset
    """
        
    reset_2squares_pawn_positions(constants.PLAYER)
    # Increment the move count
    # Convert player's chess move for output
    # Output the chess move
    # TODO - Refactor - see above
    finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                             print_string, # todo
                             attacking_piece_letter, taken)
    do_next = "return"
    return do_next


def player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank):
    """
    Input Validation of the Player's Move
    Main Validation Loop
    """

    # todo                      (just_performed_castling,
    # todo                            attacking_piece_letter, taken)

    # print(just_performed_castling, attacking_piece_letter, taken) # todo
    
    while True:

        print()

        # Are the moves being read from the input game file?
        # If so, fetch the next move from there
        do_next = handle_input_from_game_file(chess, from_file, from_rank, to_file, to_rank)
        if do_next == "return":
            return
        elif do_next == "continue":
            continue
        # else pass

        # handle_en_passant # todo

        # If not reading from the input file, then fetch the next move from the player from keyboard
        if not Game.reading_game_file:
            # fetch the next move from the player from the keyboard
            input_string = input("YOUR MOVE (e.g. e2e4): ").strip()

            if input_string == "R" or input_string == "r":
                chess.display("Player Resigned")
                # output_all_chess_moves(chess.COMPUTER_WON) todo
                goodbye()
                # Player Resigned
                # *** END PROGRAM ***

        # *** CASTLING ***
        do_next = handle_castling_input(chess, from_file, from_rank, to_file, to_rank)
        if do_next == "return":
            return
        elif do_next == "continue":
            continue
        # else pass

        # General User Input Validation
        if input_string == "":
            chess.display("Null Input! Enter 'R' to Resign")
            continue

        lower_string = input_string.lower()
        if (len(lower_string) != 4
            # Pattern: ([a-h][1-8]){2}
                or not constants.chess_move_pattern.match(lower_string)):
            chess.display("")
            print("I do not understand this input:", input_string)
            print("Format of Chess moves ought to be 4 characters e.g. e2e4")
            print("Files should be a letter from a to h")
            print("Ranks should be a number from 1 to 8")
            continue

        # Determine the file and rank of each board name
        # e.g. e2 ==> file 'e', rank '2'
        from_file = lower_string[0]
        from_rank = lower_string[1]
        to_file = lower_string[2]
        to_rank = lower_string[3]
        print(lower_string)  # todo

        attacking_piece_letter = chess.piece_letter(from_file, from_rank)

        print_string = output_attacking_move(chess, constants.PLAYER,
                                             from_file, from_rank,
                                             to_file, to_rank)
        # print() todo
        # print(print_string)

        piece_value = chess.piece_value(from_file, from_rank)

        # Loop until a valid move is played

        if piece_value == constants.BLANK:  # BLANK SQUARE
            chess.display(print_string)
            print("There is no piece to be played, instead a Blank Square")
            # todo
            ...
            continue

        if piece_value < 0:  # negative numbers are the Computer's Pieces
            chess.display(print_string)
            print("This is not your piece to move")
            # todo
            ...
            continue

        (illegal,
         illegal_because_in_check,
         taken) = is_player_move_illegal(chess,
                                         from_file, from_rank,
                                         to_file, to_rank)
        if illegal_because_in_check:
            if not Game.it_is_checkmate:
                chess.display(print_string)
                print("Illegal move because you are in check")
            else:
                chess.display(print_string)
                print("Illegal move because it is Checkmate!")
            # todo
            ...
            continue
        elif illegal:
            chess.display(print_string)
            print("Illegal move")
            # todo
            ...
            continue

        # Has the king been moved?
        # Has a rook been moved
        # TODO record_if_king_or_rook_have_moved(constants.PLAYER,
        #       from_file, from_rank, to_file, to_rank)

        # As the opponent advanced a pawn two squares?
        # If yes, record the pawn's position
        # TODO record_pawn_that_advanced_by2(constants.PLAYER,
        #       from_file, from_rank, to_file, to_rank)

        # Increment the move count
        # Convert player's chess move for output
        # Output the chess move
        finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                             print_string,
                             attacking_piece_letter, taken)
        # TODO just_performed_castling, attacking_piece_letter, taken)

        # Valid move has been played - show the updated board
        # todo - REMOVE
        # os.system("clear")
        # chess.showboard()

        # Display the Player's Move
        chess.display(print_string)
        # Pause for 2 seconds so that the Player
        # can see the description of the move that the Player chose
        time.sleep(2)
        # Inform Player that Kool AI is thinking!
        print("I am evaluating my next move...")
        return


def play_2_moves(chess, from_file, from_rank, to_file, to_rank, result):
    """
    1) Play and show the result of the Computer move
    2) Then get, validate and play the Player's move
    """

    # From this point onwards, process computer moves
    # todo
    (just_performed_castling, attacking_piece, taken) = (None, None, None)

    process_computer_move(chess, from_file, from_rank, to_file, to_rank)
    #  todo        just_performed_castling, attacking_piece_letter, taken)

    player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank)

    """
    todo
                                just_performed_castling,
                                attacking_piece_letter,
                                taken
    """


def main_part2():
    """
    The main functionality of the Chess Program begins here

    Initialise the Game
    Display the Board
    Start the Main Loop
    """

    chess = Game()

    chess.fillboard()
    os.system("clear")
    chess.showboard()

    # remove todo
    from_file = None
    from_rank = None
    to_file = None
    to_rank = None

    # Game Loop
    while True:
        play_2_moves(chess,
                     Game.best_from_file,
                     Game.best_from_rank,
                     Game.best_to_file,
                     Game.best_to_rank,
                     Game.evaluation_result)

        # todo - REMOVE
        #  os.system("clear")
        #  chess.showboard()
        Game.evaluation_result = evaluate(chess, 0,
                                          constants.COMPUTER,
                                          constants.EVALUATE_THRESHOLD_SCORE)

        # remove todo
        # from_file = Game.best_from_file
        # from_rank = Game.best_from_rank


def main():
    """
    Main Routine
    Begin Here
    Report any errors
    """

    try:
        main_part2()
    except CustomException as error:
        print(error)
        handle_internal_error()
        quit()
    except Exception as error:
        raise error


if __name__ == "__main__":
    main()
