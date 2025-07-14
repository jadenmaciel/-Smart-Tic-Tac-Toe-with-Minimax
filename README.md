# Smart Tic-Tac-Toe with Minimax AI 🤖

This project is a Python implementation of the classic Tic-Tac-Toe game, featuring a graphical user interface (GUI) and an unbeatable AI opponent powered by the Minimax algorithm.

-----

## 🌟 Features

  - **Graphical User Interface:** A clean and intuitive UI built with Tkinter where you can play by clicking on the grid.
  - **Unbeatable AI:** Play against a "perfect" AI that will never lose. It uses the Minimax algorithm to determine the optimal move in any scenario.
  - **Game Status Display:** Real-time feedback on the game's state (e.g., "Your Turn," "AI Wins," "It's a Draw").
  - **Restart Functionality:** A "Restart" button to easily start a new game at any time.

-----

## 🧠 How It Works

The core of the AI opponent is the **Minimax algorithm**. Minimax is a recursive decision-making algorithm used in two-player, zero-sum games. It works by:

1.  Creating a tree of all possible moves from the current state.
2.  Assigning a score to the terminal states (win, lose, or draw).
      - AI Win: +1
      - Player Win: -1
      - Draw: 0
3.  Recursively working its way back up the tree, choosing the move that maximizes its own score while assuming the opponent (the player) will always choose the move that minimizes the AI's score.

This ensures the AI always makes the move that leads to the best possible outcome for itself, making it impossible to defeat.

-----

## 📋 Prerequisites

To run this game, you only need to have Python installed on your system. The `Tkinter` library is included in the standard Python installation.

  - Python 3.x

-----

## 🚀 Installation & Usage

1.  **Clone the repository (or download the files):**

    ```sh
    git clone [https://github.com/jadenmaciel/-Smart-Tic-Tac-Toe-with-Minimax](https://github.com/jadenmaciel/-Smart-Tic-Tac-Toe-with-Minimax)
    cd tictactoe-minimax
    ```

    *Alternatively, just place `main.py` and `tictactoe_logic.py` in the same directory.*

2.  **Run the application:**

    ```sh
    python main.py
    ```

3.  The game window will appear. Click on any empty cell to make your move and play against the AI\!

-----

## 📂 File Structure

The project is organized into two main files:

  - `tictactoe_logic.py`: Contains the core game logic, including the `TicTacToe` class for managing the board state and the `minimax` algorithm for the AI's decision-making.
  - `main.py`: Contains the GUI code built with `Tkinter`. It handles the game window, user input (clicks), and the main game loop, connecting the UI to the game logic.

<!-- end list -->