# Kool-AI-Chess
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/cedf65e7-23b2-47a6-beb1-e0b2dc097035)


[Live Link](https://koolai-chess.herokuapp.com/)

**Kool AI Chess - A command line Chess program using Python - Player vs Computer**

## Introduction

For my Code Institute Portfolio Project 3, 
I would like to implement a Chess Program in Python<br> in order to play Chess against a Computer opponent.

In my search for a suitable algorithm I came across this [476-line BASIC PROGRAM by DEAN MENEZES](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

Let me reiterate: the basis of my project is a Chess Program written in<br>**[BASIC](https://en.wikipedia.org/wiki/BASIC) (Beginners' All-purpose Symbolic Instruction Code)** which is available [here](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt).

I found it amazing how Denezes has written such a highly interesting chess playing program in under 500 lines.<br>
My goal then is to convert Denezes' BASIC program to Python; moreover, to add ***[castling](https://en.wikipedia.org/wiki/Castling) and [en passant](https://en.wikipedia.org/wiki/En_passant)*** chess moves so that the user can play a complete game of Chess against their Computer opponent, namely, ***Kool AI***.

## Chess

To quote [Boardgamegeek](https://boardgamegeek.com/boardgame/171/chess)

> Chess is a two-player, abstract strategy board game that represents medieval warfare on an 8x8 board with alternating light and dark squares. Opposing pieces, traditionally designated *White and Black*, are initially lined up on either side. Each type of piece has a unique form of movement and capturing occurs when a piece, via its movement, occupies the square of an opposing piece. Players take turns moving one of their pieces in an attempt to capture, attack, defend, or develop their positions.<br>Chess games can end in **checkmate, resignation, or one of several types of draws.**<br>Chess is one of the most popular games in the world, played by millions of people worldwide at home, in clubs, online, by correspondence, and in tournaments. 

To quote [Wikipedia](https://en.wikipedia.org/wiki/Chess)

> Chess is an abstract strategy game that involves no hidden information and no elements of chance. It is played on a chessboard with 64 squares arranged in an eight-by-eight grid.<br>At the start, each player controls sixteen pieces:<br>
*one king, one queen, two rooks, two bishops, two knights, and eight pawns.*<br>
**White moves first, followed by Black. The game is won by checkmating the opponent's king,<br>i.e. threatening it with inescapable capture.**<br>There are also several ways a game can end in a draw.

For the rules and further information on the game of Chess please refer to the following Wikipedia articles:<br>
1. [Rules of Chess](https://en.wikipedia.org/wiki/Rules_of_chess)
2. [Chess](https://en.wikipedia.org/wiki/Chess)

Thank You.


## User Stories

1.  As a user I want to be able to enjoy a game of Chess against a Computer opponent.
2.  As a user I want to know whether I have entered a correct Chess move. Moreover, if I have not,<br>then an explanation of why a move is incorrect ought to be displayed, if possible.
3.  As a user, I want to know whether I have placed the Computer *in Check*.
4.  As a user, I want to know whether I have placed the Computer *in Checkmate*. That is, have I won?
5.  As a user, I want to know whether I am *in Check*.
6.  As a user, I want to know whether the Computer has placed me *in Checkmate*. That is, have I lost?
7.  As a user, I want the option to *Resign* when realising that I cannot beat my opponent or I no longer want to continue the game.

------

## UX

### Design

#### Logic Flow of the Program

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/04461b56-96b0-444c-b2b2-f716bd0c6fcb)

### Evaluation Algorithm

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/96d70908-f9f3-4309-be9c-b77191987523)

------

## Features

### How To Play Against Kool AI

In the context of this game *the user* is referred to as *The Player*. So I will describe the user in this manner in the following sections.

The Player goes first and is prompted to do so.<br>The Player is designated *White* however seeing that this is a monochrome console game,<br>the Player's pieces are depicted as lowercase letters at the bottom of the board.

*Kool AI, the Computer opponent* will go second. The Computer is designated *Black*.<br>The Computer's pieces are depicted as uppercase letters at the top of the board.

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/848f397e-3704-4e75-8203-53f1b70a8138)

From this point onwards each, that is, *the Player and the Computer*, will play their corresponding moves until one of the following scenarios:

1. **The Player beats *Kool AI* ! That is, [Checkmate!](https://en.wikipedia.org/wiki/Checkmate) The Player has Won!**
2. *Kool AI* recognises it cannot win therefore it resigns. **The Player has Won!**
3. ***Kool AI* beats the Player** and informs the Player that the Player is in **[Checkmate](https://en.wikipedia.org/wiki/Checkmate). Kool AI has Won!**
4. The Player resigns because of one of the following reasons:
* 1. The Player can foresee that *Checkmate* is inevitable.
* 2. The Player realises that the game is *Stalemate*.<br>([Stalemate](https://en.wikipedia.org/wiki/Stalemate) is a situation in Chess where the player whose turn it is to move is not in Check and has no legal move.)
* 3. The Player realises that the game is a [Draw](https://en.wikipedia.org/wiki/Draw_(chess)).
* 4. Or the Player chooses to no longer continue the game.

------

### How to enter a move

The chessboard has the following coordinates:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/4ab1187f-3d85-4d83-9eb4-1d4d3bed8224)

The chessboard at the beginning of the game is shown as:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/848f397e-3704-4e75-8203-53f1b70a8138)

Therefore, the form of how one enters a Chess move is of the form *\<FromSquare\>\<ToSquare\> e.g. d2d4*<br>That is, pawn *(p)* from square *d2* to square *d4*.<br>
Another example, would be *g1f3*<br>That is, knight *(n)* from square *g1* to square *f3*.<br>
If the Player enters a move in UPPERCASE, the input algorithm will *lowercase* the input in order to process the move.<br>
For matching a *Castling move, either O-O or O-O-O*, the input algorithm will *UPPERCASE* the input in order to test for Castling.

From the outset a prompt **(e.g. e2e4)** is displayed reminding the Player of the format of a Chess move.<br>

Please Note: A description of both the Player's and Computer's moves is always shown.
The descriptions will be in these formats:<br>

**Player moves g1-f3 Piece: Pawn**<br>
**Computer moves g7-g6 Piece: Pawn**

Therefore, the description will always show:
* Who played
* The From Square
* The To Square
* The Piece Played

------

### Game Screen

Each piece has a letter. Starting from the top of the board:
* R for Rook
* N for Knight
* B for Bishop
* Q for Queen
* K for King
* P for Pawn

The Computer's pieces (Black) are depicted as *uppercase, capital* letters - R, N, B, Q, K, P

The Player's pieces (White) are depicted as *lowercase* letters - r, n, b, q, k, p

The program will prompt the Player then await the Player's input 

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/2eb31ea3-d3b9-4bd9-953d-b0d4b9985469)

The Player's input needs to be a four-character string which uses *[files-first Chess Algebraic notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))*<br> 
For example, to move one's pawn **from square e2 to e4, enter *e2e4***

The program will then respond with a message such as<br>
*Checking Player move for e2-e4 Piece: Pawn*

Since the Player has moved the pawn from square *e2 to e4* and the move is valid, the program will display the following board:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/cb116eae-8e63-4573-8ca1-742d3230e67f)

*Kool AI* will inform the Player that it is *Thinking* - That is, *it is evaluating its next move*:<br>
**Please note: sometimes Kool AI takes over 20 seconds to respond!** Please Be Patient :)

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d4fdb642-448e-41ef-b9fc-c594edd593e8)

Subsequently, *Kool AI* has responded with *e7e6*<br>That is, Pawn from square *E7* to *E6*<br>
Please Note: A description of both the Player's and Computer's moves is always shown.

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/8292752c-c146-4281-96ba-7202fa115c7d)

------

### Illegal Moves

The Player's input will always be validated. Here are some examples:

1. When it cannot understand the input - that is, it does not fit the Chess move format<br>
In this scenario, the Player entered the word, *hello*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/661a4bb3-aa52-413a-85ab-f60ff3128760)

2. A null entry

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/a3bcae23-a679-41ae-aa2d-9919b1d849f1)

3. Trying to play a *Blank Square*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/15fc2286-4912-4379-bf7e-0621f7d1772d)

4. Trying to play *an opponent's piece*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/17368a9f-5f2c-4b43-9bdf-3d9a72cd773a)

5. Trying to play an illegal move for a piece

This is the general *catchall* response.
*Kool AI's algorithm* will examine the Player's move against all the possible moves for the chosen piece.
If the Player's move does not appear in the list of all possible moves it will display **an Illegal Move** message.
In such a scenario it would be up to the Player to determine why such a move cannot be played.
For example:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/324873df-a696-4269-a2fa-a96475a774b0)

In this case, a rook cannot *pass through pieces*. It is blocked by a pawn.

------

### Check
Here is an example of Check:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/94a31e76-2d33-4567-8273-100521b6ee9c)

Here are a couple of examples of illegal moves whilst **in Check**

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/a58df4fb-eccd-4d45-a117-9808e13035d6)

That is, the king cannot move towards an attacking piece whilst being attacked!<br>A king however, can *take an attacking piece* if the king is in a position to do so.

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/a35e7c33-c9ad-4449-a09b-d1a78765839b)

The only *legal moves when in Check* is to protect your king, whether by
1. Taking the attacking piece
2. Moving a piece to block the attacking piece
3. Or moving the king out of its position where it is currently under attack

So, in this example, the Knight move does none of the above, **therefore, it is an illegal move!**

------

### Checkmate

When Checkmate occurs, this signifies **a win**.<br>
The game is won by checkmating the opponent's king, i.e. threatening it with inescapable capture.<br>
The program will print a message declaring the victor and **all the moves played are output to the screen.**<br>
(They are also outputted to *output.pgn for testing purposes only!* See [TESTING.md](https://github.com/DelroyGayle/KoolAIChess/blob/main/TESTING.md) for details.)<br>
The moves are outputted in **Long algebraic notation (LAN)**.<br>(See [Resignation](https://github.com/DelroyGayle/KoolAIChess/blob/main/README.md#resignation) 
 below for details)<p> 
Here is an example of Checkmate:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/5fd730fc-8748-42f0-bff8-80f350405743)

*Kool AI* first declares that the Player is *in Check*.
Seeing this is the case, *Kool AI* does a *further test to see whether it is Checkmate?*
In the above scenario, this is indeed the case. Therefore, *Kool AI* declares itself the Victor!<br>
However, for reasons explained below, the Game **will continue until the Player resigns!**

By the way, the above chessboard Checkmate configuration, is known in the Chess world, as

**Fool's Mate - Checkmate in two moves! 1. f2f3 e7e5 2. g2g4 Qd8h4# 0-1**

The Computer Chess algorithm as designed by *Dean Menezes is clever enough* to make these moves and to Checkmate the opponent.

------

### Resignation
Here is an example of Resignation:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/394a8189-1cd2-4227-b9a2-1727683ae128)

Resignation in Chess is the player conceding the game to their opponent, that is, to acknowledge defeat.<br>
Resignation immediately ends the game.<br>
To resign, the Player has to enter **either R or r to resign.**<br>
Please note however:
1.  *Kool AI's algorithm* will score each of **its own** potential moves before its play and if the score is *too low, Kool AI* will resign.<br>That is, if the score is below the constant **STALEMATE_THRESHOLD_SCORE which is equal to -2500**;<br>*Kool AI* will deem that it cannot possibly win the game; therefore, *Kool AI will resign!*
2.  Unfortunately, the program is not *smart enough* to determine whether a game is [Stalemate](https://en.wikipedia.org/wiki/Stalemate) or a [Draw](https://en.wikipedia.org/wiki/Draw_(chess));<br>so it relies on the human user to end the game by *entering 'r' to resign*.
3.  I am a novice chess player. So in writing this program, there is the possibility that my program may declare **Checkmate** against the human opponent when in fact, it is not! (Although personally, throughout my testing I have not come across such a scenario!)<br>
Therefore, in regards to this: even after *Kool AI* declares **Checkmate**, I leave it up to the Player to resign.<br>That is, this program does **not** force the end of the game - *the Player can play on!*  


When either the Player or *Kool AI* resigns or if *Kool AI checkmates its opponent*; **all the moves played are output to the screen.**<br>
(They are also outputted to *output.pgn for testing purposes only!* See [TESTING.md](https://github.com/DelroyGayle/KoolAIChess/blob/main/TESTING.md) for details.)<br>
The moves are outputted in **Long algebraic notation (LAN)**.<p> 
To quote [Wikipedia](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)), 
   > **In long algebraic notation (LAN), also known as full/fully expanded algebraic notation,<br> 
   both the starting and ending squares are specified**,<br>
   for example: e2e4. Sometimes these are separated by a hyphen, e.g. Nb1-c3, while captures are indicated by an "x", e.g. Rd3xd7.<br>
   Long algebraic notation takes more space and is no longer commonly used in print; however, it has the advantage of clarity. 
   
   Therefore, this program produces the output of all moves in LAN *without hyphens* so that an user such as I,<br> can read the moves clearly without too much difficulty;<br>that is,
   *what moves were made from what square to which square, and what piece was moved.*<p>
   The Player can then copy these moves from the console terminal for further study!

---
### Pawn Promotion
When it comes to Pawn Promotion, *Kool AI* solely promotes *its Pawns* to Queens.<br>The Player, however, has the option to promote a White Pawn to another piece besides Queen.<br>
Here is an example of Pawn Promotion - The Player's pawn has reached **c8**:  
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/b4b88f91-c750-46fe-9d11-75276cb044a1)  

The Player has the option to enter either *r for Rook, b for Bishop, n for Knight or q for Queen.*<br>
Note: the default is Queen. So, the Player can just hit *Enter!*<br>
When the Player enters their choice, the Pawn in question is promoted to the requested piece.<br>
A message will be printed of the form: **Pawn promoted to** *\<whichever piece was chosen\>*.<br>
For example:  
     ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/6a746c09-3418-49da-8ee1-db4dfc5b5412)


In the above scenario, the result of the promotion of the Player's Pawn to Queen resulted in a win for *the Player!*<br>
Here is the full response:  
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/ffd7a43b-21ed-4716-b3d5-95bc16c9bcd6)


------

### Minimax/Negamax
The Computer Chess algorithm as designed by *Dean Menezes* uses what is known as **negamax** to determine its next move.  
To quote Rod Bird as he describes the *evaluate* function:  
> *This function checks all squares for players to move then recursively test plays.<br>
  It plays its own move then plays the opponent's best move, recursively over four moves.<br>
  So getting the potential net worth of each moveable player on the board.<br>
  The highest scored determines the computer's next move.<br>
  It is **a classic mini max evaluation shortened to its a negamax form with pruning**<br>
  i.e. it does not waste time on lower value plays.*
    
I will not pretend that I understand the mathematics involved. I can only verify that it indeed works!<br>
Nonetheless, for more information please see the following Wikipedia articles: [minimax](https://en.wikipedia.org/wiki/Minimax) and [negamax](https://en.wikipedia.org/wiki/Negamax).

## Limitations
* When it comes to Pawn Promotion, *Kool AI* solely promotes its Pawns to Queens.<br>Nonetheless, the Player is given the option to promote a White Pawn to another piece besides Queen.
* The program is not *smart enough* to determine whether a game is [Stalemate](https://en.wikipedia.org/wiki/Stalemate) or a [Draw](https://en.wikipedia.org/wiki/Draw_(chess));<br>so it relies on the Player to end the game by *entering 'r' to resign*.<br>*Kool AI* will designate such an ending as a Draw i.e. *1/2-1/2*.
* Unfortunately, this program is slow. Sometimes, it takes over 20 seconds for *Kool AI* to respond with its move!
* To speed up this process, the constant **MAXLEVEL which is currently equal to 5**, can be lowered to 4 or 3.<br>This will indeed quicken the Computer's response, however, it will play a *dumber* game!

## Future Features
* Attempt to speed up the program by using a library such as [itertools](https://docs.python.org/3/library/itertools.html)
* The ability to switch sides
* Undo/Redo ability when playing moves
* Saving board positions during the game
* Loading of saved positions
* Explore further the possibilities of **Chess-Playing Automation** using the existing functionality
* Loading and playing of [PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation) chess files
* A Colour Chessboard using a library such as [Colorama](https://pypi.org/project/colorama/)
* Better Graphics for the Chess Pieces and the Chessboard

------

## Data Model

### The Chessboard

The Chessboard and Pieces as designed by [Dean Menezes](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt) had the following values:
```
        -500,"R",-270,"N",-300,"B",-900,"Q",-7500,"K",-300,"B",-270,"N",-500,"R"
        -100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P"
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P"
        500,"R",270,"N",300,"B",900,"Q",5000,"K",300,"B",270,"N",500,"R"
```

* Black Pieces at the top have negative values
* Each piece has a value followed by its letter
* Zero and Space show the empty squares
* Then the White Pieces are at the bottom with corresponding positive values

I chose not to use a 8X8 array with numerical indices for the following reason.<br>
In the Chess World, this is how a chessboard is depicted:
        
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/4ab1187f-3d85-4d83-9eb4-1d4d3bed8224)

The chessboard consists of eight files and eight ranks.<br>
Columns are known as ***files*** and are labelled left to right with letters, ***a*** to ***h***.<br>
Rows are known as ***ranks*** and are numbered from the bottom of the board upwards, ***1*** to ***8***.<br>
Therefore, rather than a 8X8 array with numerical indices; instead I chose to use a Python dictionary to reflect the above scheme.<br>
The keys being a string e.g. *"h8" for the square h8*<br>
Then each value would be a *Piece Class* instance of the form *Piece(VALUE, LETTER, SIGN)*<br>
        
Therefore the Dictionary would look like this:<br>
*{a8:value, b8:value, ..., d1:None, ..., e1:None, a1:value, ..., h1:value}*<br>
Blank squares have the value None<br> 
Thereby if a variable for example *board* represents the chessboard, each square can be accessed using a *string key*.<br>
For example to refer to square *"h3"* I can use the code
*square = board["h3"]*

### Overview of Classes

In order to incorporate Object Oriented programming I have used three classes in this program.

1. Piece
2. Game
3. CustomException(Exception)

#### 1) Class: Piece

This Class is the Base Class for all the Chess Pieces.

As a basis I adopted the way that X.S. had implemented the Piece Class in [this code](https://github.com/xsanon/chess/blob/main/src/piece.py)

In my version the rationale is as follows:
```
    Attributes:
    -----------
    piece : string
        Each piece is depicted by a letter which represents
        the name of a piece as following :-
        Pawn -> P
        Rook -> R
        Knight -> N
        Bishop -> B
        Queen -> Q
        King -> K

    sign (represents the colour) : it is depicted by a number
        1 if the piece belongs to the Player i.e. white
       -1 if the piece belongs to the Computer i.e. black
  ```

Each piece has
* **self.sign**: **-1** for the Computer (Black Pieces); **1** for the Player (White Pieces)

* **self.letter**: P R N B Q K

* **self.value**:
* * Player:
* * Pawn's value is 100
* * Rook's value is 500
* * Knight's value is 270
* * Bishop's value is 300
* * Queen's value is 900
* * **Note: The Player's King value is 5000 and the Computer's King value is -7500**
* * The Computer's values of each of the above is the negative equivalent i.e. **-100, -500, -270, -300, -900**
* * **The Kings' values differ as shown above**
* Note: Blank squares have a value and a sign of ZERO

* **piece_string(self)**: This method returns a string description of each piece to describe which piece had been *taken* in a Chess move.
* * "Pawn"
* * "Rook"
* * "Knight"
* * "Bishop"
* * "Queen"
* * Note: King piece cannot be *taken* - So no 'piece_string'

* **promote(self)**: This method handles Pawn Promotion.<br>When a Pawn is promoted, two new attributes are added to the Pawn object.
* 1. **self.promoted_letter**: the letter of the piece that the Pawn was promoted to.
* 2. **self.promoted_value**: the corresponding value of the piece that the Pawn was promoted to.



#### 2. Class: Game

This class represents the status of the Chess Game.
It is the main workspace of the program containing all the *global* flags, properties and variables related to the state of play of the Game.

So instead of *global* variables I use *Class Variables* belonging to this Class to hold important values.

#### 3. Class: CustomException(Exception)

I have tested my program to the best of my ability however I am a novice Chess Player.
So just in case this program does some absurd illegal move such as *trying to take a king or capturing a piece of its own colour*;<br>
I have added a Try-Except method to catch a Custom Exception which will be generated if some *strange* chess move occurs.<br>
*Hopefully this will never happen! :)*

### constants.py

In order to avoid the usage of *magic numbers* I created this file to hold all the constants needed for this program.
So if this program needs to be amended, this would be the main place to look at for making adjustments of major values.

The exception is that the function *showboard* in *run.py* uses numbers and strings specific to usage on the ANSI terminal used for this project.
So I suggest an entire new function will need to be written if displaying the chessboard on a different display media.

## Modules

This program was originally one file - *run.py*<br>As this project began to grow I realised that *run.py* was getting unwieldy<br> 
Therefore, I split it up into different modules:
* **constants.py** - Holds all the major constants used in this program
* **extras.py** - I moved the routines that manage how piece moves are generated - Pawn/Rook/Knight/Bishop/Queen/King - into this module<br>
Also any routines that caused *import circular issues* with the Python interpreter are placed in extras.py
* **fileio.py** - This program can *essentially perform Chess-Playing Automation* by playing chess moves read from the *input.pgn* file<br>
All routines related to this process are placed in fileio.py<br>(see [TESTING.md](https://github.com/DelroyGayle/KoolAIChess/blob/main/TESTING.md) for more details)
* **game.py** - The *Game Class* and its related routines
* **moves.py** - The functionality for the chess moves: *[Castling](https://en.wikipedia.org/wiki/Castling) and [En Passant](https://en.wikipedia.org/wiki/En_passant)*
* **piece.py** - The *Piece Class* and its related routines
* **run.py** - the main module of the program

## Testing

+ Passed the code through the PEP8 linter and confirmed there are no problems.
+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal.
+ Added functionality so that this program could read Chess moves from a [PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation) file, namely, *input.pgn*.<br>
My rationale is that if my program can play *recorded chess games **identically*** then the chess-playing algorithm works correctly.<br>
See [TESTING.md](https://github.com/DelroyGayle/KoolAIChess/blob/main/TESTING.md) for further details.

### Internal Errors

At the top level of the program I have added the following *try-except* :- 

```
def main():
    try:
        main_part2()
    except CustomException as error:
        print(error)
        handle_internal_error()
        quit()
    except Exception as error:
        raise error
```

That way, if there is some *logic error that I have not anticipated or some internal error occurs*;<br>
it would be caught here and a suitable message would be printed.

The message will be of the form:<br>

<strong>Internal Error: \<The Error Message\><br>
Computer resigns due to an internal error<br>
Please investigate<br>
<br>
Thank You For Playing<br>
Goodbye<br>
</strong>

## Code Validation

## Bugs

### Solved Bugs

#### Class Bug
Initially when I defined my 'Game' class
I thought I could call the following ***'initialise_class_variables'*** function
to initialise all the relevant Class Variables
```
class Game:
    """
    """
    def initialise_class_variables():
        print("Initialise")
        # the number of valid moves found for chosen piece
        num_moves = -1    
        ...
```

However when I tried to access a Class Variable defined that way
I got
```
    print(Game.num_moves)
          ^^^^^^^^^^^^^^
AttributeError: type object 'Game' has no attribute 'num_moves'
```

##### Solution

I know the error has something to do with scoping, however to resolve this issue, I removed the function *'initialise_class_variables'* and defined all my Class Variables directly beneath the 'Game' Class definition.
```
class Game:
    player_first_move = True   
    ...
    ...
```
------

#### Pawn Promotion Bug

*Kool AI* determines its next move by calling the *evaluate* function recursively over four moves.<br>
The highest scored move is *Kool AI's* next move.<br>The evaluation process involves moving the chess pieces then scoring the resultant chessboard configuration.<br>Therefore, before calling *evaluate* a copy of the original pieces are saved in order to be restored after the function call is completed.<br>As shown:
```
    # store From and To data so that it may be restored
    save_from_square = chess.board[from_square]
    save_to_square = chess.board[to_square]
```

*If during evaluation*, a piece happens to be **a Black Pawn that is moved to rank 8** this will result in a promotion of the Pawn to a Queen in accordance with the rules of Chess and *Kool AI's* handling of its own Pawns.

##### The Bug
However, when the *evaluate* function call was returned, any Pawns that happened to be promoted to Queens **were remaining Queens!**<br>*Pawns-to-Queens* ought to have been restored back to Pawns!<p>See for example:  
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/c6cc0b4b-c796-4b2a-8ccb-2f0fc1740d3d)  
*There are two Black Queens - two capital Qs - when there should only be one!*  
Despite the fact, that I was restoring the original pieces as shown in this code:
```
        # Restore previous squares
        chess.board[from_square] = save_from_square
        chess.board[to_square] = save_to_square
```
Nonetheless, **two Black Queens - capital Qs** appeared!

##### Deepcopy Solution

Therefore, I concluded that I needed to make *a **deep** copy of chess.board[from_square] and chess.board[to_square]* to be used to restore their contents when the function *evaluate* returned.<br>I used **copy.deepcopy** from the [copy](https://docs.python.org/3/library/copy.html) library.  
Unfortunately, my program is not fast as it stands, and *deepcopy appeared to be taking a very long time* - so using this option was not viable. 

##### Alternative Solution

I therefore chose  to use a *List of Sets to act as a Stack* that grows and shrinks with the calls of *evaluate*. That is, at each function call level, an empty Set is added to the *undo_stack*.
```
Game.undo_stack.append(set())
```
If any Pawn Promotion happens, the coordinates of the square in question is added to the current set at the top of the Stack.
```
Game.undo_stack[-1].add(to_square)
```
When the function call is over, the following two operations take place.  

1) If the current set at the top of the Stack is not empty; then each coordinate in the Set has their Pawn Promotion attributes removed; which in effect, *undoes the Pawn Promotion* of each Pawn in question.

```
    if not Game.undo_stack[-1]:
        return

    undo_set = Game.undo_stack[-1]
    for index in undo_set:
        # Remove the Pawn Promotion attributes
        # i.e. Undo them!
        del chess.board[index].promoted_value
        del chess.board[index].promoted_letter
        # empty the set
    Game.undo_stack[-1].clear()
```

2) The current set is popped of from the top of the Stack.
```
    # Regardless of whether the current set was empty or not
    # Pop the stack
    Game.undo_stack.pop()
```
------

## Deployment

The project is deployed on Heroku. These are the steps in order to deploy on Heroku:
1. Regarding your project:
    + create a Procfile with the following one line entry
    ```
    web: node index.js
    ```

2. Then ensure that you have pushed your latest version including Procfile to GitHub

3. Create a Heroku account. You will need to enter 
* first name
* last name
* email address,  
* role e.g. *student*
* location
* primary development language i.e. *Python*

4. Click *Create free account*

5. Proceed with confirmation via email

6. Log into Heroku

7. Create a new application by clicking the *Create New App* button.<br>
You will need to enter
* The *App name*
* The region
* Then click the *Create app* button

8. Go into settings -> Config Var and add the following:
    +  key by the name of *PORT* with the value of *8000*.<p>

9. The next step is to add a couple of  buildpacks to your application.<br>Then click the *Add buildpack* button

10. Include the following buildpacks:
    + The first buildpack is *heroku/python* - then click "Save changes"
    + The second buildpack is *heroku/nodejs* - then click "Save changes"
    + Please note: the order is significant - the Python buildpack **must** appear on top before the NodeJs buildpack.<br>One can use the mouse to drag the buildpacks into the correct order<p>

11. Then click the *Deploy* option. This is where you choose the deployment method of *GitHub*

12. Find the repo with the project you want to deploy

13. Confirm that you want to connect to GitHub by clicking the *Connect* button

14. Scroll down to the two options, *Automatic deploys - Manual deploy*

15. In this section, you can click *Enable Automatic deploys* - Heroku will rebuild your app every time you push a new change  
to your code to GitHub

16. Or you can choose to *manually deploy* using the *Deploy Branch* option here 

17. Pick which branch you want to deploy -- Generally this would be **main**

18. Click **Deploy Branch** and wait until the project is built

19. Ensure there are no errors. Heroku will display the message **Your app was successfully deployed**

20. Click the *View* button and you will be taken to an URL of the form *https:\/\/\<project-name>.herokuapp.com/*<br>
This is your deployed app in operation

## Languages, Libraries and Technologies

### Languages
* Python3

### Python Libraries

* os - I use this library for the *clear* function in order to clear the console before displaying an updated chessboard.
* re - I use *regular expressions* in order to validate user input of chess moves.
* time - I use the *sleep* function to cause the program to delay for a few seconds, in order so that the user can see the updated chessboard.

### Other tools

* [GitHub](https://github.com/) - for hosting the site
* [Gitpod](https://www.gitpod.io/) - for editing the files
* [Heroku](https://heroku.com) - for the deployment of the site
* [Code Institute's GitHub full template](https://github.com/Code-Institute-Org/python-essentials-template) - in order to run Python on Heroku

------

## Credits
+  Background image photo by [Chris Burns](https://unsplash.com/@chris_burns ) on [Unsplash](https://unsplash.com/)
+  I would like to credit [asiask97's CLI Battleship game](https://github.com/asiask97/Battleship-cli-game/) which shows how to present a Python program against a background image
+  Thanks to [Code Institute](https://codeinstitute.net/) for [the template](https://github.com/Code-Institute-Org/python-essentials-template) by which a terminal could be created; in order that my game could be displayed on a webpage.
+  Thanks to [Code Institute](https://codeinstitute.net/) for [the CI Python Linter](https://pep8ci.herokuapp.com/) which ensures that Python code complies with [PEP 8](https://peps.python.org/pep-0008/)
+ [Boardgamegeek](https://boardgamegeek.com/boardgame/171/chess) for the explanation of the game of Chess
+ [Wikipedia](https://en.wikipedia.org/wiki/Chess) for the explanation of the game of Chess
+  The depiction of the chessboard with letters and numbers is from [Naming Ranks and Files in Chess](https://www.dummies.com/article/home-auto-hobbies/games/board-games/chess/naming-ranks-and-files-in-chess-186935/)
+ [Flowchart Fun](https://flowchart.fun/) was used to create the flowchart for the Logic Flow of the Program
+ [Miro](https://miro.com/) was used to create the flowchart for the Evaluation Algorithm
        
## Acknowledgements    
+  I would like to thank my mentor Derek McAuley for his advice and guidance.
+  I would like to acknowledge Dean Menezes, the author of [the BASIC program](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt) on which my project is based on.
+  I would like to acknowledge [Rod Bird](https://justbasiccom.proboards.com/thread/258/chess?page=2) who also adopted Menezes' code.<br>I preferred and adopted Bird's display of the Chessboard.
+  I would like to acknowledge the *Pythoneer* [X.S.](https://xsanon.medium.com/)
+  X.S.'s article *[How to Code a Simple Chess Game in Python](https://medium.com/codex/how-to-code-a-simple-chess-game-in-python-9a9cb584f57)*
+  X.S.'s *Pythonic* style of coding can be seen in the following [Chess Program](https://github.com/xsanon/chess).
+ I would like to acknowledge Steven J. Edwards who designed [Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation) in order to record chess games
