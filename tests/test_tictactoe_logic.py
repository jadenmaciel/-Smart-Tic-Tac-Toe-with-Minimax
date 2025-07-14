"""
Unit tests for the TicTacToe game logic and Minimax AI algorithm.

This module contains comprehensive test cases that verify the correctness
of the game logic, win detection, and AI decision-making functionality.
"""

import sys  # Import system module for path manipulation
import os  # Import os module for file path operations

# Reason: Add parent directory to path so we can import our modules
# This allows the test to find the main application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to path

from tictactoe_logic import TicTacToe, minimax, find_best_move  # Import modules to test


class TestTicTacToe:
    """Test cases for the TicTacToe class functionality."""
    
    def test_init_creates_empty_board(self):
        """Test that initialization creates a 3x3 empty board."""
        # Reason: Verify the basic initialization works correctly
        # This is the foundation for all other game functionality
        
        game = TicTacToe()  # Create new game instance
        
        # Check that board is 3x3
        assert len(game.board) == 3  # Verify board has 3 rows
        for row in game.board:  # Check each row in the board
            assert len(row) == 3  # Verify each row has 3 columns
        
        # Check that all cells are empty
        for row in range(3):  # Iterate through all row indices
            for col in range(3):  # Iterate through all column indices
                assert game.board[row][col] == ''  # Verify each cell is empty string
    
    def test_get_available_moves_empty_board(self):
        """Test getting available moves on an empty board."""
        # Reason: Verify that all 9 positions are available on a fresh board
        # This tests the happy path scenario at game start
        
        game = TicTacToe()  # Create new game with empty board
        moves = game.get_available_moves()  # Get list of available positions
        
        assert len(moves) == 9  # Verify all 9 positions are available
        
        # Check that all positions (0,0) through (2,2) are included
        expected_moves = [(r, c) for r in range(3) for c in range(3)]  # Generate all possible positions
        assert set(moves) == set(expected_moves)  # Verify all positions are present (order doesn't matter)
    
    def test_get_available_moves_partial_board(self):
        """Test getting available moves on a partially filled board."""
        # Reason: Verify that only empty positions are returned as available
        # This tests the edge case of a board with some moves already made
        
        game = TicTacToe()  # Create new game instance
        
        # Make some moves to fill specific positions
        game.board[0][0] = 'X'  # Place X in top-left corner
        game.board[1][1] = 'O'  # Place O in center position
        game.board[2][2] = 'X'  # Place X in bottom-right corner
        
        moves = game.get_available_moves()  # Get remaining available positions
        
        assert len(moves) == 6  # Verify 6 positions remain available (9 - 3 = 6)
        
        # Verify that occupied positions are not in available moves
        assert (0, 0) not in moves  # Top-left should not be available
        assert (1, 1) not in moves  # Center should not be available
        assert (2, 2) not in moves  # Bottom-right should not be available
        
        # Verify that empty positions are in available moves
        assert (0, 1) in moves  # This position should be available
        assert (1, 0) in moves  # This position should be available
    
    def test_check_winner_row_victory(self):
        """Test winning condition detection for row victories."""
        # Reason: Verify that horizontal wins are detected correctly
        # This tests one of the three main win conditions in Tic-Tac-Toe
        
        game = TicTacToe()  # Create new game instance
        
        # Test row 0 victory for X
        game.board[0][0] = 'X'  # Place X in first position of top row
        game.board[0][1] = 'X'  # Place X in second position of top row
        game.board[0][2] = 'X'  # Place X in third position of top row
        
        assert game.check_winner('X') == True  # Verify X is detected as winner
        assert game.check_winner('O') == False  # Verify O is not detected as winner
    
    def test_check_winner_column_victory(self):
        """Test winning condition detection for column victories."""
        # Reason: Verify that vertical wins are detected correctly
        # This tests the second main win condition in Tic-Tac-Toe
        
        game = TicTacToe()  # Create new game instance
        
        # Test column 1 victory for O
        game.board[0][1] = 'O'  # Place O in top position of middle column
        game.board[1][1] = 'O'  # Place O in center position of middle column
        game.board[2][1] = 'O'  # Place O in bottom position of middle column
        
        assert game.check_winner('O') == True  # Verify O is detected as winner
        assert game.check_winner('X') == False  # Verify X is not detected as winner
    
    def test_check_winner_diagonal_victory(self):
        """Test winning condition detection for diagonal victories."""
        # Reason: Verify that diagonal wins are detected correctly
        # This tests the third main win condition in Tic-Tac-Toe
        
        game = TicTacToe()  # Create new game instance
        
        # Test main diagonal victory for X
        game.board[0][0] = 'X'  # Place X in top-left corner
        game.board[1][1] = 'X'  # Place X in center position
        game.board[2][2] = 'X'  # Place X in bottom-right corner
        
        assert game.check_winner('X') == True  # Verify X is detected as winner
        assert game.check_winner('O') == False  # Verify O is not detected as winner
    
    def test_check_winner_anti_diagonal_victory(self):
        """Test winning condition detection for anti-diagonal victories."""
        # Reason: Verify that anti-diagonal wins are detected correctly
        # This tests the fourth win condition (other diagonal) in Tic-Tac-Toe
        
        game = TicTacToe()  # Create new game instance
        
        # Test anti-diagonal victory for O
        game.board[0][2] = 'O'  # Place O in top-right corner
        game.board[1][1] = 'O'  # Place O in center position
        game.board[2][0] = 'O'  # Place O in bottom-left corner
        
        assert game.check_winner('O') == True  # Verify O is detected as winner
        assert game.check_winner('X') == False  # Verify X is not detected as winner
    
    def test_check_winner_no_winner(self):
        """Test that no winner is detected when there isn't one."""
        # Reason: Verify that false positives don't occur
        # This tests the error condition where no win exists
        
        game = TicTacToe()  # Create new game instance
        
        # Create a board state with no winner
        game.board[0][0] = 'X'  # Place some moves that don't form a line
        game.board[0][1] = 'O'  # Mixed positions that don't create wins
        game.board[1][1] = 'X'  # Scattered placement
        game.board[2][0] = 'O'  # No three in a row
        
        assert game.check_winner('X') == False  # Verify X is not detected as winner
        assert game.check_winner('O') == False  # Verify O is not detected as winner
    
    def test_is_draw_with_full_board_no_winner(self):
        """Test draw detection with a full board and no winner."""
        # Reason: Verify that draw conditions are detected correctly
        # This tests the specific case where the board is full but no one won
        
        game = TicTacToe()  # Create new game instance
        
        # Create a full board with no winner
        game.board[0] = ['X', 'O', 'X']  # Fill first row with mixed symbols
        game.board[1] = ['O', 'X', 'O']  # Fill second row with mixed symbols
        game.board[2] = ['O', 'X', 'O']  # Fill third row with mixed symbols
        
        assert game.is_draw() == True  # Verify draw is detected
    
    def test_is_draw_with_winner_present(self):
        """Test that draw is not detected when there's a winner."""
        # Reason: Verify that draw detection doesn't trigger when someone has won
        # This tests the error condition where a win exists
        
        game = TicTacToe()  # Create new game instance
        
        # Create a board with a winner
        game.board[0] = ['X', 'X', 'X']  # Create winning row for X
        game.board[1] = ['O', 'O', '']  # Add some other moves
        game.board[2] = ['', '', '']  # Leave some positions empty
        
        assert game.is_draw() == False  # Verify draw is not detected when winner exists
    
    def test_is_draw_with_empty_board(self):
        """Test that draw is not detected on an empty board."""
        # Reason: Verify that draw detection only occurs when appropriate
        # This tests the error condition of calling draw check too early
        
        game = TicTacToe()  # Create new game with empty board
        
        assert game.is_draw() == False  # Verify draw is not detected on empty board


class TestMinimaxAlgorithm:
    """Test cases for the Minimax algorithm functionality."""
    
    def test_minimax_ai_win_scenario(self):
        """Test minimax returns +1 when AI wins."""
        # Reason: Verify that the algorithm correctly evaluates AI win conditions
        # This tests the base case where the maximizing player (AI) has won
        
        game = TicTacToe()  # Create new game instance
        
        # Create a winning position for AI (O)
        game.board[0] = ['O', 'O', 'O']  # AI wins with top row
        game.board[1] = ['X', 'X', '']  # Add some player moves
        game.board[2] = ['', '', '']  # Leave rest empty
        
        score = minimax(game, 0, True)  # Evaluate this position for AI
        assert score == 1  # Verify AI win returns score of +1
    
    def test_minimax_player_win_scenario(self):
        """Test minimax returns -1 when player wins."""
        # Reason: Verify that the algorithm correctly evaluates player win conditions
        # This tests the base case where the minimizing player (human) has won
        
        game = TicTacToe()  # Create new game instance
        
        # Create a winning position for player (X)
        game.board[0] = ['X', 'X', 'X']  # Player wins with top row
        game.board[1] = ['O', 'O', '']  # Add some AI moves
        game.board[2] = ['', '', '']  # Leave rest empty
        
        score = minimax(game, 0, False)  # Evaluate this position for player
        assert score == -1  # Verify player win returns score of -1
    
    def test_minimax_draw_scenario(self):
        """Test minimax returns 0 for draw scenarios."""
        # Reason: Verify that the algorithm correctly evaluates draw conditions
        # This tests the base case where neither player can win
        
        game = TicTacToe()  # Create new game instance
        
        # Create a draw position
        game.board[0] = ['X', 'O', 'X']  # Create full board with no winner
        game.board[1] = ['O', 'X', 'O']  # Mixed symbols throughout
        game.board[2] = ['O', 'X', 'O']  # No three in a row for either player
        
        score = minimax(game, 0, True)  # Evaluate this position
        assert score == 0  # Verify draw returns score of 0
    
    def test_minimax_ai_blocks_player_win(self):
        """Test that minimax recognizes when AI should block player win."""
        # Reason: Verify that the algorithm makes defensive moves when necessary
        # This tests the strategic decision-making capability of the AI
        
        game = TicTacToe()  # Create new game instance
        
        # Create situation where player is about to win
        game.board[0] = ['X', 'X', '']  # Player has two in top row
        game.board[1] = ['O', '', '']  # AI has one move in middle row
        game.board[2] = ['', '', '']  # Bottom row is empty
        
        best_move = find_best_move(game)  # Get AI's optimal move
        assert best_move == (0, 2)  # AI should block at position (0,2)


class TestFindBestMove:
    """Test cases for the find_best_move function."""
    
    def test_find_best_move_winning_opportunity(self):
        """Test that AI takes a winning move when available."""
        # Reason: Verify that the AI prioritizes winning over other moves
        # This tests the happy path where AI can win immediately
        
        game = TicTacToe()  # Create new game instance
        
        # Create situation where AI can win
        game.board[0] = ['O', 'O', '']  # AI has two in top row
        game.board[1] = ['X', 'X', 'O']  # Mixed middle row
        game.board[2] = ['', '', '']  # Bottom row empty
        
        best_move = find_best_move(game)  # Get AI's optimal move
        assert best_move == (0, 2)  # AI should win by completing top row
    
    def test_find_best_move_blocking_priority(self):
        """Test that AI blocks player win when no winning move available."""
        # Reason: Verify that the AI makes defensive moves when it can't win
        # This tests the edge case where blocking is the optimal strategy
        
        game = TicTacToe()  # Create new game instance
        
        # Create situation where player is about to win and AI can't win
        game.board[0] = ['X', 'X', '']  # Player about to win top row
        game.board[1] = ['O', '', '']  # AI has one piece in middle
        game.board[2] = ['', '', '']  # Bottom row empty
        
        best_move = find_best_move(game)  # Get AI's optimal move
        assert best_move == (0, 2)  # AI should block player's winning move
    
    def test_find_best_move_empty_board(self):
        """Test that AI makes a reasonable first move on empty board."""
        # Reason: Verify that the AI can start the game appropriately
        # This tests the edge case of the very first move
        
        game = TicTacToe()  # Create new game with empty board
        
        best_move = find_best_move(game)  # Get AI's optimal first move
        assert best_move is not None  # Verify a move is returned
        assert isinstance(best_move, tuple)  # Verify return type is tuple
        assert len(best_move) == 2  # Verify tuple has exactly 2 elements
        
        row, col = best_move  # Unpack the move coordinates
        assert 0 <= row <= 2  # Verify row is within valid range
        assert 0 <= col <= 2  # Verify column is within valid range
    
    def test_find_best_move_no_moves_available(self):
        """Test behavior when no moves are available."""
        # Reason: Verify graceful handling of edge case with full board
        # This tests the error condition where no moves are possible
        
        game = TicTacToe()  # Create new game instance
        
        # Fill the entire board
        game.board[0] = ['X', 'O', 'X']  # Fill first row
        game.board[1] = ['O', 'X', 'O']  # Fill second row
        game.board[2] = ['O', 'X', 'O']  # Fill third row
        
        best_move = find_best_move(game)  # Attempt to find a move
        assert best_move is None  # Verify None is returned when no moves available


# Reason: Run tests when this file is executed directly
# This allows developers to run the test suite easily
if __name__ == "__main__":
    import unittest  # Import unittest for basic test running
    
    # Create a test suite and run all test methods
    loader = unittest.TestLoader()  # Create test loader
    suite = unittest.TestSuite()  # Create test suite
    
    # Add all test classes to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestTicTacToe))  # Add TicTacToe tests
    suite.addTests(loader.loadTestsFromTestCase(TestMinimaxAlgorithm))  # Add Minimax tests
    suite.addTests(loader.loadTestsFromTestCase(TestFindBestMove))  # Add find_best_move tests
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)  # Create test runner with verbose output
    runner.run(suite)  # Execute all tests 