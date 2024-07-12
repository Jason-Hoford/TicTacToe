# Tic-Tac-Toe Game

This Python project implements a Tic-Tac-Toe game with both human vs. human and human vs. AI modes. The AI uses the Minimax algorithm to determine the best moves. The project includes two versions, each offering different functionalities and improvements.

## Features
- Play Tic-Tac-Toe against another human.
- Play Tic-Tac-Toe against an AI.
- AI uses the Minimax algorithm to decide the best move.
- Customizable board size and connection length (default is 3x3).

## Requirements
- Python 3.x
- NumPy

## Installation
1. Clone the repository or download the `tic_tac_toe_v1.py` and `tic_tac_toe_v2.py` files.
2. Install the required package:
    ```bash
    pip install numpy
    ```
## Usage

### Version 1
Run the game by executing the `tic_tac_toe_v1.py` file:
```bash
python tic_tac_toe_v1.py
```

### Section: Version 1 Human vs. Human
#### Human vs. Human
To play against another human in version 1, call the `human_play` method:
```python
game = TickTackToe()
game.human_play()
```

### Section: Version 1 Human vs. AI
#### Human vs. AI
To play against the AI in version 1, call the `human_machine` method:
```python
game = TickTackToe()
game.human_machine(human_player=1)
```


### Section: Version 2
### Version 2
Run the game by executing the `tic_tac_toe_v2.py` file:
```bash
python tic_tac_toe_v2.py
```

### Section: Version 2 Human vs. Human
#### Human vs. Human
To play against another human in version 2, call the `human_play_game` method:
```python
game = TickTockToe()
game.human_play_game()
```

### Section: Version 2 Human vs. AI
#### Human vs. AI
To play against the AI in version 2, call the `human_ai` method:
```python
game = TickTockToe()
game.human_ai(human_player=1, layer_deep=7)
```


### Section: Customization
## Customization
You can customize the board size and connection length by modifying the `row_length`, `column_length`, and `connection` parameters in the `TickTackToe` or `TickTockToe` class constructor:
```python
game = TickTackToe(row_length=4, column_length=4, connection=3)
```

### Section: Tests
## Tests
Run the tests to verify the game logic:
```python
game = TickTockToe()
game.test()
```
## License
This project is licensed under the MIT License.