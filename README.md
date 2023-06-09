# Kool-AI-Chess

[Live Link](https://koolai-chess.herokuapp.com/)

[GitHub Repository](https://github.com/DelroyGayle/KoolAIChess/)

**Kool AI Chess - A command line Chess program using Python - Player vs Computer**

## Introduction

For my Code Institute Portfolio Project 3, 
I would like to implement a Chess Program in Python<br> in order to play Chess with a Computer opponent.

In my search for a suitable algorithm I came across this [476-line BASIC PROGRAM by DEAN MENEZES](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

Let me reiterate: the basis of my project is a Chess Program written in<br>**[BASIC](https://en.wikipedia.org/wiki/BASIC) (Beginners' All-purpose Symbolic Instruction Code)**
available [here](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

I found it amazing how Denezes has written such an highly interesting chess playing program in under 500 lines.
My goal then is to convert it to Python and add ***castling and en passant*** chess moves to it so that the user can play a complete game of Chess against their Computer opponent, namely, ***Kool A.I.***

## How To Play

### Ready To Play

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

## Target Audience

## User Stories

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

No unfixed bugs

------

## Deployment

## Libraries and Technologies Used

### os
I use this library for the *clear* function in order to clear the console before displaying an updated chessboard

### Languages Used

* Python

### Other tools

* GitHub - for hosting the site
* Gitpod - for editing the files
* Heroku - for the deployment of the site

------

## Credits/Acknowledgements

+ The depiction of the chessboard with letters and numbers is from [Naming Ranks and Files in Chess](https://www.dummies.com/article/home-auto-hobbies/games/board-games/chess/naming-ranks-and-files-in-chess-186935/)
+  I would like to acknowledge Dean Menezes, the author of the BASIC program on which my project is based on.
+  I would like to acknowledge [Rod Bird](https://justbasiccom.proboards.com/thread/258/chess?page=2) who also adopted Menezes' code. I preferred Bird's display of the Chess Board.
+  I would like to acknowledge the *Pythoneer* [X.S.](https://xsanon.medium.com/).
+  X.S.'s article *[How to Code a Simple Chess Game in Python](https://medium.com/codex/how-to-code-a-simple-chess-game-in-python-9a9cb584f57)* and 
+  X.S.'s *Pythonic* style of coding in the following [Chess Program](https://github.com/xsanon/chess).
+  Background image by [Chris Burns](https://unsplash.com/@chris_burns ) at [Unsplash](https://unsplash.com/).
+  I would like to acknowledge [asiask97's CLI Battleship game](https://github.com/asiask97/Battleship-cli-game/) which shows how to present a Python program against a background image.
