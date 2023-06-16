"""
extras.py
To assist in the modularising of this project
I have introduced this module to resolve any circular import issues
Will place any other miscellaneous routines here
"""

from game import Game


def append_to_output_stream(astring):
    """
    append string to Game.output_stream
    """
    Game.output_stream += astring

    # debugging TODO
    print("OS", Game.output_stream, Game.output_chess_move)
