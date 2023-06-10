# Kool-AI-Chess

[Live Link](https://koolai-chess.herokuapp.com/)

[GitHub Repository](https://github.com/DelroyGayle/KoolAIChess/)

**Kool AI Chess - A command line Chess program using Python - Player vs Computer**

## Introduction

For my Code Institute Portfolio Project 3, 
I would like to implement a Chess Program in Python<br> in order to play Chess with a Computer opponent.

In my search for a suitable algorithm I came across this [476-line BASIC PROGRAM by DEAN MENEZES](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

Let me reiterate: the basis of my project is a Chess Program written in<br>**[BASIC](https://en.wikipedia.org/wiki/BASIC) (Beginners' All-purpose Symbolic Instruction Code)** which is available [here](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt).

I found it amazing how Denezes has written such an highly interesting chess playing program in under 500 lines.
My goal then is to convert Denezes' BASIC program to Python; moreover, to add ***castling and en passant*** chess moves so that the user can play a complete game of Chess against their Computer opponent, namely, ***Kool A.I.***

## Chess

To quote [Boardgamegeek](https://boardgamegeek.com/boardgame/171/chess)

> Chess is a two-player, abstract strategy board game that represents medieval warfare on an 8x8 board with alternating light and dark squares. Opposing pieces, traditionally designated *White and Black*, are initially lined up on either side. Each type of piece has a unique form of movement and capturing occurs when a piece, via its movement, occupies the square of an opposing piece. Players take turns moving one of their pieces in an attempt to capture, attack, defend, or develop their positions.<br>Chess games can end in **checkmate, resignation, or one of several types of draws.**<br>Chess is one of the most popular games in the world, played by millions of people worldwide at home, in clubs, online, by correspondence, and in tournaments. 

To quote [Wikipedia](https://en.wikipedia.org/wiki/Chess)

> Chess is an abstract strategy game that involves no hidden information and no elements of chance. It is played on a chessboard with 64 squares arranged in an eight-by-eight grid.<br>At the start, each player controls sixteen pieces:<br>
*one king, one queen, two rooks, two bishops, two knights, and eight pawns.*<br>
**White moves first, followed by Black. The game is won by checkmating the opponent's king, i.e. threatening it with inescapable capture.**<br>There are also several ways a game can end in a draw.

For the rules and further information on the game of Chess please refer to the following Wikipedia articles:<br>
1. [Rules of Chess](https://en.wikipedia.org/wiki/Rules_of_chess)
2. [Chess](https://en.wikipedia.org/wiki/Chess)

Thank You.

## How To Play Against Kool A.I.

The user goes first. The user is designated *White* however seeing that this is a monochrome game,<br>the user's pieces are depicted as the lowercase letters at the bottom of the board.

*Kool A.I., your Computer opponent* will go second. The computer is designated *Black*.<br>The computer's pieces are depicted as the uppercase letters at the top of the board.

From this point onwards each will play their move until either

* The user beats *Kool A.I.*! That is, **[Checkmate!](https://en.wikipedia.org/wiki/Checkmate) The user has Won!**
* *Kool A.I.* recognises it cannot win therefore it resigns. **The user has Won!**
* ***Kool A.I.* beats the user** and informs the user that they are in **[Checkmate](https://en.wikipedia.org/wiki/Checkmate)**
* The user resigns because of one of the following reasons:
* 1. The user can foresee that they will be in *Checkmate*.
* 2. The user realises that the game is *Stalemate*.<br>([Stalemate](https://en.wikipedia.org/wiki/Stalemate) is a situation in Chess where the player whose turn it is to move is not in Check and has no legal move.)
* 3. The user realises that the game is a [Draw](https://en.wikipedia.org/wiki/Draw_(chess)).
* 4. Or the user chooses to no longer continue with the game.

### Resignation

Resignation in Chess is the player conceding the game to their opponent. To acknowledge defeat.<br>
Resignation immediately ends the game.<br>
Please note however:
1.  Kool A.I.'s algorithm will score each of its potential moves before its play and if the score of a move is *too low* it will resign.
2.  Unfortunately, my program is not *smart enough* to determine whether a game is [Stalemate](https://en.wikipedia.org/wiki/Stalemate) or a [Draw](https://en.wikipedia.org/wiki/Draw_(chess));<br>so it relies on the human user to end the game by *entering 'R' to resign*.
3. Also, I am a novice chess player. So in writing this program, there is the distinct possibility that my program may declare **Checkmate** when in fact, it is not!<br>(Personally, throughout my testing I have not come across such a scenario!)<br>
Therefore, in considering the possibility of such a scenario; even after declaring **Checkmate** I leave it up to the user to resign.<br>That is, my program does **not** force the end of the game - *the player can play on!*

### Game Screen

The program will prompt the User then await the User's input 

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/2eb31ea3-d3b9-4bd9-953d-b0d4b9985469)

The User's input needs to be a four-character string which uses *files-first Chess Algebraic notation*<br> 
For example, to move one's pawn **from square e2 to e4, enter *e2-e4***

The program will then respond with a message such as<br>
*Checking Player move for e2-e4 Piece: Pawn*
* Thereby showing the Player's move. That is:
* Showing the From Square
* Showing the To Square
* Showing the Piece being played

Since the User has moved the pawn from square *e2 to e4* the program will display the following board:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/cb116eae-8e63-4573-8ca1-742d3230e67f)

### Check

### Checkmate

### Resignation

## User Stories

1.  As a user I want to be welcomed by a start screen with the name of the game.
2.  As a user I want to be able to enjoy a game of Chess against a Computer Opponent
3.  As a user I want to know whether I am entering correct Chess moves. Moreover, if not,<br>then an explanation of why a move is incorrect.
4.  As a user, I want to know whether I have placed the Computer *in Check*.
5.  As a user, I want to know whether I have placed the Computer *in Checkmate*. That is, have I won?
6.  As a user, I want to know whether I am *in Check*.
7.  As a user, I want to know whether the Computer has placed me *in Checkmate*. That is, have I lost?
8.  As a user, I want the option to *Resign* when realising that I cannot beat my opponent.

------

## UX

### Design

#### Logic Flow of the program

![Flowchart](https://github.com/DelroyGayle/Kool-AI-Chess/assets/91061592/218a8f5e-38ef-4fba-bf27-4c577cfb9e83)

#### A Mock-up of how the game will look like

The game begins with this view

![image](https://github.com/DelroyGayle/Kool-AI-Chess/assets/91061592/4e782939-b475-4b30-b69f-31b6c79bb39b)

If for example, the user plays **e2e4**

![image](https://github.com/DelroyGayle/Kool-AI-Chess/assets/91061592/61e63c94-30e0-46c6-adb7-96da1f43da2c)

Then the computer may respond with **e7e5**

![image](https://github.com/DelroyGayle/Kool-AI-Chess/assets/91061592/0aa858fb-a6d4-43c0-a15e-f9e5d03fea16)

------

## Features

------

## Future Features
* The ability to switch sides
* Undo/Redo ability when playing moves
* Saving board positions during the game
* A Colour Chessboard using a libary such as [Colorama](https://pypi.org/project/colorama/)

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
Thereby if a variable for example *board* represents the chessboard, each square can be accessed using a *string index*.<br>
For example to refer to square *"h3* I can use the code
*square = board["h3"]*

### Overview of Classes

In order to incorporate Object Oriented programming I have used three classes in this program.

1. Piece
2. Game
3. CustomException(Exception)

#### 1) Class: Piece

This is the Class that is the Base Classes for all the Chess Pieces.

As a basis I adopted the way that X.S. had implemented the Pieces' Class in [this code](https://github.com/xsanon/chess/blob/main/src/piece.py)

In my version the rationale is as follows:
```
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

* **print_string(self)**: This method returns a string description of each piece to describe which piece has been *taken* in a game
* * "Pawn"
* * "Rook"
* * "Knight"
* * "Bishop"
* * "Queen"
* * Note: King piece cannot be *taken* - So no 'print_string'

#### 2. Game

This class represents the status of the Chess Game.
It is the main workspace of the program containing all the *global* flags, properties and variables related to the state of play of the Game.

So instead of *global* variables I use *Class Variables* of this Class to hold important values.

#### 3. CustomException(Exception)

I have tested my program to the best of my ability however I am a novice Chess Player.
So just in case my program does some absurd illegal move such as *trying to take a king or capturing a piece of its own colour*;<br>
I have added a Try-Except method to catch a Custom Exception which will be generated if some *strange* chess move occurs.<br>
*Hopefully this will never happen! :)*

### constants.py

In order to avoid the usage of *magic numbers* I created this file to hold all the constants needed for this program.
So if this program needs to be amended, this would me the main place to look at for making adjustments of major values.

The exception is that the function *showboard* in *run.py* uses numbers and strings specific to usage on the ANSI terminal used for this project.
So I suggest an entire new function will need to be written if displaying the chessboard on a different display media.

## Testing

+ Passed the code through the PEP8 linter and confirmed there are no problems

+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal

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

Solution:

I know the error has something to do with scoping however to resolve this issue, I removed the function 'initialise_class_variables' and defined all my Class Variables 
directly beneath the 'Game' Class definition
```
class Game:
    player_first_move = True   
    ...
    ...
```

### Unfixed Bugs

No unfixed bugs.

------

## Deployment

The project is deployed on Heroku. These are the steps in order to deploy on Heroku

1. Create Heroku account.
2. Create new project.
3. Go into settings -> Config Var and add the fallowing:
    +  key by the name of *PORT* with the value of *8000*.<p>

4. Include the following buildpacks:
    + Heroku/python
    + Heroku/nodejs
    + Please note: the order is significant - the Python buildpack **must** appear before the NodeJs buildback.<br>One can use the mouse to drag the buildpacks into the correct order.<p>


5. Regarding your project:
    + create a Procfile with the following one line entry
    ```
    web: node index.js
    ```

6. Then Deploy the project to GitHub with the following files included.
7. On Heroku for Deployment Method pick Github and find the repo with the project you want to deploy.
8. Pick which branch you want to deploy -- Generally this would be **main**
9. Click **deploy** and wait until the project is built.
10. Ensure there are no errors.

## Languages, Libraries and Technologies

### Languages
* Python3

### Libraries

* os - I use this library for the *clear* function in order to clear the console before displaying an updated chessboard.
* re - I use *regular expressions* in order to validate user input of chess moves.

### Other tools

* GitHub - for hosting the site
* Gitpod - for editing the files
* Heroku - for the deployment of the site
* Code Institute's GitHub full template - in order to run Python on Heroku

------

## Credits/Acknowledgements

+  I would like to acknowledge Dean Menezes, the author of [the BASIC program](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt) on which my project is based on.
+  I would like to acknowledge [Rod Bird](https://justbasiccom.proboards.com/thread/258/chess?page=2) who also adopted Menezes' code. I preferred and adopted Bird's display of the Chess Board.
+  I would like to acknowledge the *Pythoneer* [X.S.](https://xsanon.medium.com/).
+  X.S.'s article *[How to Code a Simple Chess Game in Python](https://medium.com/codex/how-to-code-a-simple-chess-game-in-python-9a9cb584f57)*
+  X.S.'s *Pythonic* style of coding can be seen in the following [Chess Program](https://github.com/xsanon/chess).

+  Background image photo by [Chris Burns](https://unsplash.com/@chris_burns ) on [Unsplash](https://unsplash.com/).
+  I would like to acknowledge [asiask97's CLI Battleship game](https://github.com/asiask97/Battleship-cli-game/) which shows how to present a Python program against a background image.
+  Thanks to [Code Institute](https://codeinstitute.net/) for [the template](https://github.com/Code-Institute-Org/python-essentials-template) by which a terminal could be created; in order that my game could be displayed on a webpage.
+  Thanks to [Code Institute](https://codeinstitute.net/) for [the CI Python Linter](https://pep8ci.herokuapp.com/) which ensures that Python code complies with [PEP 8](https://peps.python.org/pep-0008/)
+ [Boardgamegeek](https://boardgamegeek.com/boardgame/171/chess) for the explanation of the game of Chess
+ [Wikipedia](https://en.wikipedia.org/wiki/Chess) for the explanation of the game of Chess
+  The depiction of the chessboard with letters and numbers is from [Naming Ranks and Files in Chess](https://www.dummies.com/article/home-auto-hobbies/games/board-games/chess/naming-ranks-and-files-in-chess-186935/)