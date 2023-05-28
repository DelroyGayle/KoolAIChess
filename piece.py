import constants

"""
My coding of piece.py is based somewhat on how X.S. styled piece.py as shown here
https://github.com/xsanon/chess/blob/main/src/piece.py 
"""
class Piece():
    """
    A class to represent a piece in chess
    
    ...

    Attributes:
    -----------
    name : str
        Represents the name of a piece as following - 
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
        self.name = ""
        self.sign = sign

class Rook(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - however differ in value    
        """
        super().__init__(sign)
        self.name = "R"
        self.value = constants.ROOK_VALUE

class Knight(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - however differ in value    
        """
        super().__init__(sign)
        self.name = "N"
        self.value = constants.KNIGHT_VALUE

class Bishop(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - however differ in value    
        """
        super().__init__(sign)
        self.name = "B"
        self.value = constants.BISHOP_VALUE

class Queen(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece - however differ in value    
        """
        super().__init__(sign)
        self.name = "Q"
        self.value = constants.QUEEN_VALUE

class King(Piece):
    def __init__(self, value, sign):
        """
        Base class Piece
        Note: The Player's King and the Computer's King have different values
        """
        super().__init__(sign)
        self.name = "K"
        self.value = constants.VALUE_OF_COMPUTER_KING if sign == constants.COMPUTER else constants.VALUE_OF_PLAYER_KING 
