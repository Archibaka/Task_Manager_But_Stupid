# Blackjack-Tkinter

An interactive game of blackjack, with the GUI created using Python's tkinter package.

## Description

This project recreates the popular game of blackjack, using tkinter to create the user interface. The card images are loaded into memory from the [cards directory](https://github.com/mhoward91/blackjack-tkinter/tree/master/cards), and the rest of the GUI is constructed using various tkinter widgets. Elements of the game (such as dealing, scoring, shuffling etc.) are arranged as functions.

The rules are the same as standard blackjack, where a hand 'busts' once it exceeds 21. Additionally:
- The player deals to their hand by selecting the _player_ button
- Once they want to hold their hand, the player should select the _dealer_ button until the dealer wins or busts
- The player has the ability to shuffle the deck at anytime
- A counter to the right of screen shows the number of games the player and dealer have won, and only resets when the program restarts

## Motivation
As Python is primarily a backend language, I was motivated to understand what was possible regarding front-end development, and create an alternative way of showcasing my code (instead of just running programs through the command line). 

## Getting Started

### Dependencies

To clone and run this app on your machine, you'll need [Git](https://git-scm.com) and [Python 3](http://python.org/).

### Installation & running the program 


1. Fork and clone this repository
```
$ git clone https://github.com/mhoward91/blackjack-tkinter.git
```

2. Navigate to the relevant directory and run the program
```
$ python blackjack.py
```

_Note: no further packages are required beyond the python built-in modules_

## Acknowledgements

Guidance on how to use tkinter to create this interface comes from Tim Buchalka's [Python Programming Masterclass](https://www.udemy.com/course/python-the-complete-python-developer-course/) course.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
