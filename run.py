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
import os
import re


class Game:
    """
    A class that represents the status of the Chess Game
    This is the main workspace of the program
    It keeps track of the flags, properties and variables related
    to the state of play of the Game
    """

# Class Variables

    # the number of valid moves found for chosen piece
    num_moves = -1
    # recursion level for evaluate()
    level = 0
    # worth of play
    score = 0
    check_flag = False  # Therefore, True means that one is currently in check
    reading_game_file = None
    writing_game_file = False
    player_first_move = True
    skipped_seven_tag_rosters = False
    tag_pair_count = 0
    output_stream = ""
    whose_move = constants.PLAYER  # WHITE goes first
    move_count = 0
    move_count_incremented = False
    player_castled = False
    computer_castled = False
    player_king_moved = False
    player_king_rook_moved = False
    player_queen_rook_moved = False
    computer_king_moved = False
    computer_king_rook_moved = False
    computer_queen_rook_moved = False
    error_message = ""
    message_printed = False
    inputstream_previous_contents = ""
    player_pawn_2squares_advanced_col = None
    player_pawn_2squares_advanced_row = None
    computer_pawn_2squares_advanced_col = None
    computer_pawn_2squares_advanced_row = None
    en_passant_status = None


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
        You have: The value of each piece followed by its letter
        Zero and Space show the empty squares
        Then White at the bottom has positive values

        I chose not to use a 8X8 array with numerical indices

        In the Chess World,
        A chess board is depicted as eight ranks (rows) numbered
        from the bottom of the board 1 to 8
        Files are columns that are labelled left to right with numbers
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

        Therefore I chose to use a dictionary to reflect the above scheme
        The keys being a string e.g. 'h8' for the square h8
        Then each value would be a Piece Class instance variable
        of the form (PIECE VALUE, LETTER, SIGN)
        Therefore the Dictionary would look like this
        {a8:value, b8:value, ... a1:value, ... h1:value}
        Blank squares will have the value None

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

    def board_sign(self, index, rank=""):
        """
        Determine the sign of the value of the piece on the square
        Blank squares have a 'sign' of 1 i.e. Positive Zero
        """
        if rank:
            index += rank
            
        return getattr(self.board[index], 'sign', 1)

    def board_piece(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted with a space
        """
        if rank:
            index += rank

        space = " "
        return getattr(self.board[index], 'piece', space)

    def showboard(self):
        """
        Display the Chessboard
        """

        space = " "
        left_bracket = " ["
        right_bracket = " ]"

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
                letter = chr(97 + column)  # characters a to h
                number = row
                number = chr(48 + number)  # characters 1 to 8
                thesign = self.board_sign(letter, number)
                if thesign == constants.BLANK:
                    output_string += portion1 + space + portion2
                elif thesign == constants.COMPUTER:
                    output_string += (portion1
                                      + self.board_piece(letter, number)
                                      + portion2)
                else:
                    output_string += (portion1
                                      + self.board_piece(letter, number)
                                      .lower()
                                      + portion2)

            print("{}|".format(output_string))

        # 3 spaces and 26 dashes "-"
        print("{}{}".format(space*3, "-"*26))
        # 5 spaces THEN 2 spaces each
        print("{}A  B  C  D  E  F  G  H".format(space*5))


def goodbye()
    """
    End of Game Message
    """

    print()
    print("Thank You For Playing. Goodbye.")


def determine_generate_move_method(piece_letter):
    """
    Use a dictionary to determine which method to call
    """
    methods_dictionary = {  
        PAWN_LETTER: generate_moves_for_pawn,
    }
    themethod = methods_dictionary.get(piece_letter, "Unknown letter " + piece_letter)

    if isinstance(themethod, str):
        raise Exception("Internal Error: " + themethod)

    return themethod

    
    def file_plus1(file)
    """
    Is the next file plus one
    between a and h
    """
    if file not in ["a", "b", "c", "d", "e", "f", "g"]:
        return None
    return chr(ord(file) + 1)


    def generate_moves(self, piece_sign)
        """
        Generate a list of valid moves for a particular piece
        """
        # todo
        # Capture right?

	...        

def movelist(from_file, from_rank, piece_sign, evaluating= False)
    """
    get a list of valid moves for a particular piece
    """
    all_the_moves = chess.board[from_files + from_rank].generate_moves(piece_sign)
    num_moves = - 1

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
                  print("EL/Castle", evaluating, level)  # todo
                  evaluate_castle(x, y, piece_sign)


def is_player_move_legal(from_file, from_rank, to_file, to_rank, taken, illegal)

    """
    validate that the PLAYER'S move is legal
    and that it does not put the PLAYER in check
    """

    piece_sign = constants.PLAYER  # white piece
    illegal = True
    all_the_moves = movelist(from_file, from_rank, piece_sign, False)

    ...

def output_attacking_move(who_are_you, from_file, from_rank, to_file, to_rank)

    print_string = from_file + from_file + "-" + to_file + to_rank + " Piece: " + board_piece(from_file, from_rank)

    if who_are_you == constants.PLAYER:
          return "Checking Player move for " + print_string
    else:
          return "Computer moves " + print_string



def process_computer_move(from_file, from_rank, to_file, to_rank)


    just_performed_castling = False
    computer_move_finalised = False

    ...    

def player_move_validation_loop(from_file, from_rank ,to_file, to_rank, just_performed_castling, attacking_piece, taken)
    """
    Input Validation of the Player's Move
    Main Validation Loop
    """

    while True:
        
        print()

        # fetch the next move from the player from keyboard
        input_string = trim(input("YOUR MOVE (e.g. e2e4): "))

        if input_string == "R":
            print("Player Resigned")
            output_all_chess_moves(chess.COMPUTER_WON)
            goodbye()  # Player Resigned
            # *** END ***
            

        """
        *** CASTLING ***
        This is denoted by using capital 'O
        that is O-O and O-O-O
        It is not PGN notation to use ZEROS - However will cater for 0-0 and 0-0-0
        """
        if constants.castling_pattern.match(input_string):
            # \A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z"
            chess.general_string_result = input_string
            print("Castling Is Not Implemented")
            continue

        # General User Input Validation
        if input_string == "":
            print("Null Input! Enter 'R' to Resign")
            continue

        lower_string = input_string.lower()
        if len(lower_string) != 4 or 
            not constants.chess_move_pattern.match(lower_string):  # ([a-h][1-8]){2}
            os.system("clear")
            chess.showboard()
            print()
            print("I do not understand this input ", input_string)
            print("Format of chess moves ought to be 4 characters e.g. e2e4")
            print("Files should be a letter from a to h")
            print("Ranks should be a number from 1 to 8")
            continue
            
        # Determine the file and rank of each board name e.g. e2 ==> file 'e', rank '2'
        from_file = lower_string[0]
        from_rank = lower_string[1]
        to_file = lower_string[2]
        to_rank = lower_string[3]

        attacking_piece = chess.board_piece(from_file, from_rank)

        print_string = output_attacking_move(chess.PLAYER, from_file, from_rank, to_file, to_rank)
        # print() todo
        print(print_string)

        piece_value = chess.board_piece(from_file,from_rank)

        if piece_value < 0: # negative numbers are the Computer's Pieces
             print("This is not your piece to move")
             ...
             continue
        
        if  piece_value =- constants.BLANK: # BLANK SQUARE
             print("There is no piece to be played, instead a Blank Square")
             ...
             continue
        
        illegal = is_player_move_legal(from_file, from_rank, to_file, to_rank, taken, illegal)
        if illegal ISTRUE THEN
            PRINT "Illegal move"
            ...
            continue

        else

            # Has the king been moved?
            # Has a rook been moved
            record_if_king_or_rook_have_moved(%PLAYER, from_file, from_rank, to_file, to_rank)

            # As the opponent advanced a pawn two squares? if yes, record the pawn's position
            record_pawn_that_advanced_by2(%PLAYER, from_file, from_rank, to_file, to_rank)

            # Increment the move count
            # Convert player's chess move for output
            # Output the chess move
            finalise_player_move(from_file, from_rank, to_file, to_rank, just_performed_castling, attacking_piece, taken)
            return
        

    # Validation Loop ends here                             


def player_move(from_file, from_rank, to_file, to_rank)
    """
    Firstly show the result of the computer move
    Then get and validate the player's move
    """


    if chess.player_first_move:
        # Player goes first so on the first iteration there is no processing of Computer Moves 
        chess.player_first_move = False
        return

    # From this point onwards, process computer moves
    just_performed_castling, attacking_piece, taken = 
        process_computer_move(from_file, from_rank, to_file, to_rank)
    #                               just_performed_castling, attacking_piece, taken)
    
    player_move_validation_loop(from_file, from_rank, to_file, to_rank, 
                                just_performed_castling,
                                attacking_piece,
                                taken)



def main_part2():
    """
    The main functionality of the Chess Program begins here
    """

    """
    Initialise the Game
    Display the Board
    """
    chess = Game()
    chess.fillboard()
    chess.showboard()

    from_file = None
    from_rank = None
    to_file = None
    to_rank = None
    result = None
    # Game Loop
    while True:
        player_move(from_file, from_rank, to_file, to_rank, result)
        chess.showboard()
        break

def main():
    try:
        main_part2()
    except Exception as error:
        print(error)
        print("This Program Will Now End")
        quit()

if __name__ == "__main__":
    main()
