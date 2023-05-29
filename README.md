# Kool-AI-Chess

Live Link

GitHub Repository

**Kool AI Chess - A command line Chess program using Python - Player vs Computer**

For my Code Institute Portfolio Project 3, 
I would like to implement a Chess Program in Python.

In my search for a suitable algorithm I came across this [476-line BASIC PROGRAM by DEAN MENEZES](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

Let me reiterate: the basis of my project is a Chess Program written in<br>**[BASIC](https://en.wikipedia.org/wiki/BASIC) (Beginners' All-purpose Symbolic Instruction Code)**
available [here](http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt)

I found it amazing how Denezes has written such an highly interesting chess playing program in under 500 lines.
My goal then is to convert it to Python and add ***castling and en passant*** chess moves to it so that the user can play a complete game of Chess against their Computer opponent, namely, ***Kool A.I.***

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

### Target Audience

### User Stories

------

## Features

------

## Testing

* I tested that the pages work in Chrome

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
    num_moves = -1    
    ...
```

### Unfixed Bugs

No unfixed bugs

------

## Deployment

## Technologies Used

### Languages Used

* Python

### Other tools

* GitHub - for hosting the site
* Gitpod - for editing the files
* Heroku - for the deployment of the site

---


## Future Features

## Deployment

------

## Credits/Acknowledgements

+  I would like to acknowledge Dean Menezes, the author of the BASIC program on which my project is based on.
+  I would like to acknowledge Rod Bird who also adopted Menezes' code. I preferred Bird's display of the Chess Board.
+  I would like to acknowledge the *Pythoneer* [X.S.](https://xsanon.medium.com/)
+  X.S.'s article *[How to Code a Simple Chess Game in Python](https://medium.com/codex/how-to-code-a-simple-chess-game-in-python-9a9cb584f57)* and 
+  X.S.'s *Pythonic* style of coding in the following [Chess Program](https://github.com/xsanon/chess)