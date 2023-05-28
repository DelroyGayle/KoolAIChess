"""

This Python Program is Based on 
'How To Write A Chess Program in QBASIC By Dean Menezes.'

To quote Rod Bird who also adopted Menezes' program :-
    "Qudos to Mr Menezes for such a stunningly short and powerful Chess AI."

Menezes' QBASIC program can be found at
 http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt  

"""

import constants

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
    check_flag = False # Therefore, True means that one is currently in check     
    reading_game_file = None
    writing_game_file = False
    player_first_move = True
    skipped_seven_tag_rosters = False
    tag_pair_count = 0
    output_stream = ""
    whose_move = constants.PLAYER # WHITE goes first
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
    
    # The Chess Board
    board = {}
    
    def __init__(self):
        pass
    
def fillboard():
    """
    The Chess Board as depicted by Dean Menezes with the following values

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
    
    A chess board is depicted as eight ranks (rows) numbered from the bottom of the board 1 to 8
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
    The keys being a tuple such as ('h',8) for square h8
    Then each value would be a tuple of the form (PIECE VALUE, LETTER, SIGN)

    """

def main():
    """
    The main functionality of the Chess Program begins here
    """
    # Ignore for now - this is test code to ensure that the program is running properly

    print("Hello World")
    print(constants.PLAYER)
    e = Game()
    print(Game.whose_move)
    print(Game.num_moves)
    print(Game.score)
    #print(whose_move,player_first_move)
    print(e.whose_move,e.score)
    Game.whose_move = 2000
    Game.score = 3000
    print(e.whose_move,e.score)

if __name__ == "__main__":
    main()