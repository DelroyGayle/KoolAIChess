import constants

"""
My coding of piece.py is based somewhat on how
X.S. styled piece.py as shown here
https://github.com/xsanon/chess/blob/main/src/piece.py
"""


class Piece():
    """
    A class to represent a piece in chess

    ...

    Attributes:
    -----------
    piece : str
        Each piece is depicted by a letter which represents
        the name of a piece as following :-
        Pawn -> P
        Rook -> R
        Knight -> N
        Bishop -> B
        Queen -> Q
        King -> K

    sign (colour) : is depicted by a number
        1 if the piece belongs to the Player i.e. white
       -1 if the piece belongs to the Computer i.e. black
    """

    def __init__(self, sign):
        self.letter = ""
        self.sign = sign

    def print_string(self):
        """
        No 'print_string' for the Base Class
        """
        return None


class Rook(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - Rook's value is 500
        """
        super().__init__(sign)
        self.letter = constants.ROOK_LETTER
        self.value = constants.ROOK_VALUE * sign

    def print_string(self):
        """
        String to be outputted for Rooks
        """
        return "Rook"


class Knight(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - Knight's value is 270
        """
        super().__init__(sign)
        self.letter = constants.KNIGHT_LETTER
        self.value = constants.KNIGHT_VALUE * sign

    def print_string(self):
        """
        String to be outputted for Knights
        """
        return "Knight"


class Bishop(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - Bishop's value is 300
        """
        super().__init__(sign)
        self.letter = constants.BISHOP_LETTER
        self.value = constants.BISHOP_VALUE * sign

    def print_string(self):
        """
        String to be outputted for Bishops
        """
        return "Bishop"


class Queen(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - Queen's value is 900
        """
        super().__init__(sign)
        self.letter = constants.QUEEN_LETTER
        self.value = constants.QUEEN_VALUE * sign

    def print_string(self):
        """
        String to be outputted for Queens
        """
        return "Queen"


class King(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece
        Note: The Player's King value is 5000
        and the Computer's King value is -7500
        """
        super().__init__(sign)
        self.letter = constants.KING_LETTER
        self.value = (constants.VALUE_OF_COMPUTER_KING
                      if sign == constants.COMPUTER
                      else constants.VALUE_OF_PLAYER_KING)
        # King piece cannot be 'taken'
        # So no 'print_string'


class Pawn(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece
        Note: Base class Piece - Pawn's value is 100
        """
        super().__init__(sign)
        self.letter = constants.PAWN_LETTER
        self.value = constants.PAWN_VALUE * sign

    def print_string(self):
        """
        String to be outputted for Pawns
        """
        return "Pawn"
