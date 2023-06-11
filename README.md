# Kool-AI-Chess
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/cedf65e7-23b2-47a6-beb1-e0b2dc097035)


[Live Link](https://koolai-chess.herokuapp.com/)

**Kool AI Chess - A command line Chess program using Python - Player vs Computer**

## Introduction

For my Code Institute Portfolio Project 3, 
I would like to implement a Chess Program in Python<br> in order to play Chess against a Computer opponent.

In my search for a suitable algorithm I came across this [476-line BASIC PROGRAM by DEAN MENEZES](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

Let me reiterate: the basis of my project is a Chess Program written in<br>**[BASIC](https://en.wikipedia.org/wiki/BASIC) (Beginners' All-purpose Symbolic Instruction Code)** which is available [here](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt).

I found it amazing how Denezes has written such an highly interesting chess playing program in under 500 lines.<br>
My goal then is to convert Denezes' BASIC program to Python; moreover, to add ***castling and en passant*** chess moves so that the user can play a complete game of Chess against their Computer opponent, namely, ***Kool AI***.

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

## How To Play Against Kool AI

In the context of this game *the user* is referred to as *The Player*. So I will describe the user in this manner in the following sections.

The Player goes first and is prompted to do so.<br>The Player is designated *White* however seeing that this is a monochrome console game,<br>the Player's pieces are depicted as lowercase letters at the bottom of the board.

*Kool AI, the Computer opponent* will go second. The Computer is designated *Black*.<br>The Computer's pieces are depicted as uppercase letters at the top of the board.

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/848f397e-3704-4e75-8203-53f1b70a8138)

From this point onwards each, that is, *the Player and the Computer*, will play their corresponding moves until one of the following scenarios:

* **The Player beats *Kool AI* ! That is, [Checkmate!](https://en.wikipedia.org/wiki/Checkmate) The Player has Won!**
* *Kool AI* recognises it cannot win therefore it resigns. **The Player has Won!**
* ***Kool AI* beats the Player** and informs the Player that the Player is in **[Checkmate](https://en.wikipedia.org/wiki/Checkmate). Kool AI has Won!**
* The Player resigns because of one of the following reasons:
* 1. The Player can foresee that *Checkmate* is inevitable.
* 2. The Player realises that the game is *Stalemate*.<br>([Stalemate](https://en.wikipedia.org/wiki/Stalemate) is a situation in Chess where the player whose turn it is to move is not in Check and has no legal move.)
* 3. The Player realises that the game is a [Draw](https://en.wikipedia.org/wiki/Draw_(chess)).
* 4. Or the Player chooses to no longer continue the game.

### How to enter a move

The chessboard has the following coordinates:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/4ab1187f-3d85-4d83-9eb4-1d4d3bed8224)

The chessboard at the beginning of the game is shown as:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/848f397e-3704-4e75-8203-53f1b70a8138)

Therefore, the form of how one enters a Chess move is of the form *\<FromSquare\>\<ToSquare\> e.g. d2d4*<br>That is, pawn *(p)* from square *d2* to square *d4*.<br>
Another example, would be *g1f3*<br>That is, knight *(n)* from square *g1* to square *f3*.<br>

From the outset a prompt **(e.g. e2e4)** is displayed reminding the Player of the format of a Chess move.<br>

Each piece has a letter. Starting from the top of the board:
* R for Rook
* N for Knight
* B for Bishop
* Q for Queen
* K for King
* P for Pawn

The Computer's pieces (Black) are depicted as *uppercase, capital* letters - R, N, B, Q, K, P

The Player's pieces (White) are depicted as *lowercase* letters - r, n, b, q, k, p

Please Note: A description of both the Player's and Computer's moves is always shown.
The descriptions will be in these formats:<br>

**Player moves g1-f3 Piece: Pawn**<br>
**Computer moves g7-g6 Piece: Pawn**

Therefore, the description will always show:
* Who played
* The From Square
* The To Square
* The Piece Played

### Game Screen

The program will prompt the Player then await the Player's input 

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/2eb31ea3-d3b9-4bd9-953d-b0d4b9985469)

The Player's input needs to be a four-character string which uses *[files-first Chess Algebraic notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))*<br> 
For example, to move one's pawn **from square e2 to e4, enter *e2e4***

The program will then respond with a message such as<br>
*Checking Player move for e2-e4 Piece: Pawn*

Since the Player has moved the pawn from square *e2 to e4* and the move is valid, the program will display the following board:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/cb116eae-8e63-4573-8ca1-742d3230e67f)

*Kool AI* will inform the Player that it is *Thinking* - That is, *it is evaluating its next move*:<br>
**Please note: sometimes Kool AI takes up to 10 seconds to respond!** Please Be Patient :)

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d4fdb642-448e-41ef-b9fc-c594edd593e8)

Subsequently, *Kool AI* has responded with *e7e6*<br>That is, Pawn from square *E7* to *E6*<br>
Please Note: A description of both the Player's and Computer's moves is always shown.

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/8292752c-c146-4281-96ba-7202fa115c7d)

### Illegal Moves

The Player's input will always be validated. Here are some examples:

1. When it cannot understand the input - that is, it does not fit the Chess move format<br>
In this scenario, the Player entered the word, *hello*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/acbd33e1-d39c-465b-bc2c-68b8e579b59e)

2. A null entry

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/4c2ff854-55ce-47d6-bda7-09e780231ae7)

3. Trying to play a *Blank Square*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/15fc2286-4912-4379-bf7e-0621f7d1772d)

4. Trying to play *an opponent's piece*

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/17368a9f-5f2c-4b43-9bdf-3d9a72cd773a)

5. Trying to play an illegal move for a piece

This is the general catchall response.
Kool AI's algorithm will examine the Player's move against all the possible moves for the chosen piece.
If the Player's move does not appear in the list of all possible moves it will display **an Illegal Move** message.
In such a scenario it would be up to the user to determine why such a move cannot be played.
For example:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/324873df-a696-4269-a2fa-a96475a774b0)

In this case, a rook cannot *pass through pieces*. It is blocked by a pawn.

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

So, in the above scenario, the Knight move does none of the above, **therefore, an illegal move!

### Checkmate
Here is an example of Checkmate:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/5fd730fc-8748-42f0-bff8-80f350405743)

*Kool AI* first declares that the Player is *in Check*.
Seeing this is the case, *Kool AI* does a *further test to see whether it is Checkmate?*
In the above scenario, this is indeed the case. Therefore, *Kool AI* declares itself the Victor!<br>
However, for reasons explained below, the Game **will continue until the Player resigns!**

By the way, the above chessboard Checkmate configuration, is known in the Chess world, as<br>
**Fool's Mate - Checkmate in two moves! 1. f2f3 e7e5 2. g2g4 Qd8h4# 0-1**

The Computer algorithm as designed by *Dean Menezes is clever enough* to make these moves and to checkmate the opponent.

### Resignation
Here is an example of Resignation:

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d7bf8bf7-83cc-41ab-b3fd-f5ca4be4e07e)

Resignation in Chess is the player conceding the game to their opponent, that is, to acknowledge defeat.<br>
Resignation immediately ends the game.<br>
Please note however:
1.  Kool AI's algorithm will score each of **its own** potential moves before its play and if the score of a move is *too low Kool AI* will resign.
2.  Unfortunately, my program is not *smart enough* to determine whether a game is [Stalemate](https://en.wikipedia.org/wiki/Stalemate) or a [Draw](https://en.wikipedia.org/wiki/Draw_(chess));<br>so it relies on the human user to end the game by *entering 'R' to resign*.
3. Also, I am a novice chess player. So in writing this program, there is the distinct possibility that my program may declare **Checkmate** against the human opponent when in fact, it is not!<br>(Personally, throughout my testing I have not come across such a scenario!)<br>
Therefore, in considering the possibility of such a scenario; even after declaring **Checkmate**; I leave it up to the user to resign.<br>That is, my program does **not** force the end of the game - *the player can play on!*

## User Stories

1.  As a user I want to be welcomed by a start screen with the name of the game.
2.  As a user I want to be able to enjoy a game of Chess against a Computer opponent.
3.  As a user I want to know whether I am have entered a correct Chess move. Moreover, if I have not,<br>then an explanation of why a move is incorrect ought to be displayed, if possible.
4.  As a user, I want to know whether I have placed the Computer *in Check*.
5.  As a user, I want to know whether I have placed the Computer *in Checkmate*. That is, have I won?
6.  As a user, I want to know whether I am *in Check*.
7.  As a user, I want to know whether the Computer has placed me *in Checkmate*. That is, have I lost?
8.  As a user, I want the option to *Resign* when realising that I cannot beat my opponent or I no longer want to continue the game.

------

## UX

### Design

#### Logic Flow of the Program

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/04461b56-96b0-444c-b2b2-f716bd0c6fcb)

### Evaluation Algorithm

![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/96d70908-f9f3-4309-be9c-b77191987523)




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
Thereby if a variable for example *board* represents the chessboard, each square can be accessed using a *string key*.<br>
For example to refer to square *"h3* I can use the code
*square = board["h3"]*

### Overview of Classes

In order to incorporate Object Oriented programming I have used three classes in this program.

1. Piece
2. Game
3. CustomException(Exception)

#### 1) Class: Piece

This Class is the Base Class for all the Chess Pieces.

As a basis I adopted the way that X.S. had implemented the Pieces' Class in [this code](https://github.com/xsanon/chess/blob/main/src/piece.py)

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

* **print_string(self)**: This method returns a string description of each piece to describe which piece had been *taken* in a Chess move.
* * "Pawn"
* * "Rook"
* * "Knight"
* * "Bishop"
* * "Queen"
* * Note: King piece cannot be *taken* - So no 'print_string'

#### 2. Class: Game

This class represents the status of the Chess Game.
It is the main workspace of the program containing all the *global* flags, properties and variables related to the state of play of the Game.

So instead of *global* variables I use *Class Variables* belonging to this Class to hold important values.

#### 3. Class: CustomException(Exception)

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

I know the error has something to do with scoping however to resolve this issue, I removed the function 'initialise_class_variables' and defined all my Class Variables directly beneath the 'Game' Class definition.
```
class Game:
    player_first_move = True   
    ...
    ...
```

### Unfixed Bugs

When I played the following moves
```
1. e2e4
2. d2d4
3. c1h6
```
After I played my Bishop move c1h6, **the Computer took 40 seconds to respond with g7h6**!<br>
So, the Computer algorithm can sometimes be *very slow* to evaluate its next move.<br>
Whether this is *a bug* or whether it is related to the speed of the Python interpreter.<br>
At this stage, I cannot tell.
    

------

## Deployment

The project is deployed on Heroku. These are the steps in order to deploy on Heroku

1. Create Heroku account.
2. Create new project.
3. Go into settings -> Config Var and add the following:
    +  key by the name of *PORT* with the value of *8000*.<p>

4. Include the following buildpacks:
    + Heroku/python
    + Heroku/nodejs
    + Please note: the order is significant - the Python buildpack **must** appear before the NodeJs buildpack.<br>One can use the mouse to drag the buildpacks into the correct order.<p>


5. Regarding your project:
    + create a Procfile with the following one line entry
    ```
    web: node index.js
    ```

6. Then ensure that you have pushed your latest version including Procfile to GitHub.
7. On Heroku for Deployment Method pick Github and find the repo with the project you want to deploy.
8. Pick which branch you want to deploy -- Generally this would be **main**
9. Click **deploy** and wait until the project is built.
10. Ensure there are no errors.

## Languages, Libraries and Technologies

### Languages
* Python3

### Python Libraries

* os - I use this library for the *clear* function in order to clear the console before displaying an updated chessboard.
* re - I use *regular expressions* in order to validate user input of chess moves.
* time - I use the *sleep* function to cause the program to delay for a few seconds.

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
