"""
Smart Tic-Tac-Toe Game Logic with Minimax AI Algorithm

This module contains the core game logic for a Tic-Tac-Toe game featuring
an unbeatable AI opponent powered by the Minimax algorithm.
"""


class TicTacToe:
    """
    Handles the core game state and logic for Tic-Tac-Toe.
    
    The board is represented as a 3x3 grid where:
    - Empty cells contain ''
    - Player moves are marked with 'X' 
    - AI moves are marked with 'O'
    """
    
    def __init__(self):
        # Reason: Initialize empty 3x3 board using list comprehension for clean structure
        # Each inner list represents a row, outer list represents the full board
        self.board = [['' for _ in range(3)] for _ in range(3)]  # Create 3x3 empty board grid
        
    def print_board(self):
        """Print the current board state to console for debugging purposes."""
        print("Current Board State:")  # Header for debugging output
        for i, row in enumerate(self.board):  # Iterate through each row with index
            row_display = []  # Create list to hold formatted cell values for this row
            for j, cell in enumerate(row):  # Iterate through each cell in the row
                display_value = cell if cell != '' else f'({i},{j})'  # Show coordinates for empty cells
                row_display.append(display_value)  # Add formatted cell to row display
            print(' | '.join(row_display))  # Join cells with separators and print row
            if i < 2:  # Don't print separator after the last row
                print('-' * 15)  # Print horizontal separator between rows
    
    def get_available_moves(self):
        """
        Get all empty cells on the board.
        
        Returns:
            list: List of (row, col) tuples representing empty board positions
        """
        available_moves = []  # Initialize empty list to store available positions
        for row in range(3):  # Iterate through all row indices (0, 1, 2)
            for col in range(3):  # Iterate through all column indices (0, 1, 2)
                if self.board[row][col] == '':  # Check if the cell is empty
                    available_moves.append((row, col))  # Add empty position to available moves
        return available_moves  # Return list of all empty positions
    
    def check_winner(self, player):
        """
        Check if the specified player has won the game.
        
        Args:
            player (str): The player symbol to check ('X' or 'O')
            
        Returns:
            bool: True if the player has won, False otherwise
        """
        # Reason: Check all possible winning conditions - rows, columns, and diagonals
        # This implements the complete win detection logic for Tic-Tac-Toe
        
        # Check all three rows for a win
        for row in range(3):  # Iterate through each row index
            if all(self.board[row][col] == player for col in range(3)):  # Check if all cells in row match player
                return True  # Player has won with this row
        
        # Check all three columns for a win  
        for col in range(3):  # Iterate through each column index
            if all(self.board[row][col] == player for row in range(3)):  # Check if all cells in column match player
                return True  # Player has won with this column
        
        # Check main diagonal (top-left to bottom-right)
        if all(self.board[i][i] == player for i in range(3)):  # Check diagonal from (0,0) to (2,2)
            return True  # Player has won with main diagonal
        
        # Check anti-diagonal (top-right to bottom-left)
        if all(self.board[i][2-i] == player for i in range(3)):  # Check diagonal from (0,2) to (2,0)
            return True  # Player has won with anti-diagonal
        
        return False  # No winning condition found for this player
    
    def is_draw(self):
        """
        Check if the game is a draw (board full with no winner).
        
        Returns:
            bool: True if the game is a draw, False otherwise
        """
        # Reason: A draw occurs when the board is completely filled and neither player has won
        # We need to verify both conditions: no winner exists and no empty spaces remain
        
        if self.check_winner('X') or self.check_winner('O'):  # Check if either player has won
            return False  # Game has a winner, so it's not a draw
        
        return len(self.get_available_moves()) == 0  # Draw if no empty moves remain


def minimax(board, depth, is_maximizing):
    """
    Minimax algorithm implementation for optimal AI decision making.
    
    This recursive algorithm evaluates all possible game states to find the optimal move.
    It assumes both players play optimally.
    
    Args:
        board (TicTacToe): Current game board state
        depth (int): Current recursion depth (used for optimization)
        is_maximizing (bool): True if it's AI's turn (maximizing), False if player's turn (minimizing)
        
    Returns:
        int: Score of the current board state (+1 for AI win, -1 for player win, 0 for draw)
    """
    # Reason: Base cases check if the game has ended in the current state
    # These terminal conditions stop the recursion and return immediate scores
    
    if board.check_winner('O'):  # Check if AI (O) has won
        return 1  # Return positive score for AI win
    
    if board.check_winner('X'):  # Check if player (X) has won  
        return -1  # Return negative score for player win
    
    if board.is_draw():  # Check if the game is a draw
        return 0  # Return neutral score for draw
    
    if is_maximizing:  # AI's turn - trying to maximize score
        best_score = -float('inf')  # Start with worst possible score for maximizing player
        for row, col in board.get_available_moves():  # Try each available move
            board.board[row][col] = 'O'  # Make AI move on the board
            score = minimax(board, depth + 1, False)  # Recursively evaluate this move
            board.board[row][col] = ''  # Undo the move to restore board state
            best_score = max(best_score, score)  # Keep track of the highest score found
        return best_score  # Return the best score AI can achieve
    
    else:  # Player's turn - trying to minimize AI's score
        best_score = float('inf')  # Start with worst possible score for minimizing player
        for row, col in board.get_available_moves():  # Try each available move
            board.board[row][col] = 'X'  # Make player move on the board
            score = minimax(board, depth + 1, True)  # Recursively evaluate this move
            board.board[row][col] = ''  # Undo the move to restore board state
            best_score = min(best_score, score)  # Keep track of the lowest score found
        return best_score  # Return the best score player can achieve (worst for AI)


def find_best_move(board):
    """
    Find the optimal move for the AI using the minimax algorithm.
    
    Args:
        board (TicTacToe): Current game board state
        
    Returns:
        tuple: (row, col) coordinates of the best move, or None if no moves available
    """
    # Reason: This function serves as a wrapper for minimax, evaluating all possible moves
    # and selecting the one that leads to the best outcome for the AI
    
    available_moves = board.get_available_moves()  # Get all possible moves
    if not available_moves:  # Check if there are no available moves
        return None  # Return None if no moves are possible
    
    best_move = None  # Initialize variable to store the optimal move
    best_score = -float('inf')  # Start with worst possible score for maximizing AI
    
    for row, col in available_moves:  # Evaluate each possible move
        board.board[row][col] = 'O'  # Temporarily make the AI move
        score = minimax(board, 0, False)  # Get score for this move (next turn is player's)
        board.board[row][col] = ''  # Undo the move to restore board state
        
        if score > best_score:  # Check if this move is better than current best
            best_score = score  # Update best score
            best_move = (row, col)  # Update best move coordinates
    
    return best_move  # Return the coordinates of the optimal move 