"""
Unit tests for the TicTacToe GUI functionality.

This module contains test cases that verify the GUI initialization,
component creation, and basic functionality without requiring a display.
"""

import sys  # Import system module for path manipulation
import os  # Import os module for file path operations
import tkinter as tk  # Import Tkinter for GUI testing

# Reason: Add parent directory to path so we can import our modules
# This allows the test to find the main application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to path

from main import TicTacToeGUI  # Import GUI class to test


class TestTicTacToeGUI:
    """Test cases for the TicTacToe GUI functionality."""
    
    def setup_method(self):
        """Setup method called before each test."""
        # Reason: Create a fresh GUI instance for each test to ensure isolation
        # This prevents test interference and provides clean state
        
        try:
            self.app = TicTacToeGUI()  # Create GUI instance for testing
        except tk.TclError:  # Handle case where no display is available (CI/CD environments)
            self.skip_gui_tests = True  # Set flag to skip GUI tests
            return  # Exit early if no display
        
        self.skip_gui_tests = False  # Set flag that GUI tests can run
    
    def teardown_method(self):
        """Cleanup method called after each test."""
        # Reason: Properly clean up GUI resources to prevent memory leaks
        # This ensures each test starts with a clean slate
        
        if hasattr(self, 'app') and self.app.root and not self.skip_gui_tests:  # Check if resources exist
            self.app.root.destroy()  # Destroy the window to free resources
    
    def test_gui_initialization(self):
        """Test that GUI initializes with correct basic properties."""
        # Reason: Verify that the GUI creates all required components
        # This tests the basic setup and initialization of the interface
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        assert self.app.game is not None  # Verify game logic instance exists
        assert self.app.game_active == True  # Verify game starts in active state
        assert self.app.root is not None  # Verify main window was created
        assert self.app.status_label is not None  # Verify status label was created
        assert len(self.app.buttons) == 3  # Verify correct number of button rows
        
        # Check that each row has correct number of buttons
        for row in self.app.buttons:  # Iterate through each row of buttons
            assert len(row) == 3  # Verify each row has exactly 3 buttons
    
    def test_window_properties(self):
        """Test that the main window has correct properties."""
        # Reason: Verify that the window is configured with expected settings
        # This ensures the UI appears correctly to users
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        assert self.app.root.title() == "Smart Tic-Tac-Toe with Minimax AI"  # Check window title
        assert "400x600" in self.app.root.geometry()  # Check window size (updated to 600 height for better layout)
        assert self.app.root.resizable()[0] == False  # Check that width is not resizable
        assert self.app.root.resizable()[1] == False  # Check that height is not resizable
    
    def test_initial_button_states(self):
        """Test that all buttons start in the correct initial state."""
        # Reason: Verify that the game board starts empty and interactive
        # This tests the happy path initial condition
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        for row in range(3):  # Iterate through each row index
            for col in range(3):  # Iterate through each column index
                button = self.app.buttons[row][col]  # Get the button at this position
                assert button['text'] == ''  # Verify button starts empty
                assert button['state'] == 'normal'  # Verify button is enabled
    
    def test_status_label_initial_state(self):
        """Test that status label starts with correct message."""
        # Reason: Verify that the user receives proper initial guidance
        # This tests the user experience at game start
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        initial_text = self.app.status_label.cget('text')  # Get current status text
        assert "Your Turn" in initial_text  # Verify it prompts user to start
        assert self.app.status_label.cget('fg') == 'green'  # Verify positive color is used
    
    def test_update_status_method(self):
        """Test the status update method functionality."""
        # Reason: Verify that status messages can be updated correctly
        # This tests a core functionality for user feedback
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        test_message = "Test Status Message"  # Define test message
        test_color = "blue"  # Define test color
        
        self.app.update_status(test_message, test_color)  # Update status with test values
        
        assert self.app.status_label.cget('text') == test_message  # Verify text was updated
        assert self.app.status_label.cget('fg') == test_color  # Verify color was updated
    
    def test_disable_all_buttons_method(self):
        """Test that all buttons can be disabled correctly."""
        # Reason: Verify that the game can be properly ended by disabling interaction
        # This tests the edge case when the game concludes
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        self.app.disable_all_buttons()  # Disable all game buttons
        
        # Check that every button is disabled
        for row in range(3):  # Iterate through each row index
            for col in range(3):  # Iterate through each column index
                button = self.app.buttons[row][col]  # Get the button at this position
                assert button['state'] == 'disabled'  # Verify button is disabled
    
    def test_restart_game_method(self):
        """Test that the restart functionality works correctly."""
        # Reason: Verify that the game can be reset to initial state
        # This tests the happy path for starting a new game
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        # Simulate a game in progress by modifying some buttons
        self.app.game.board[0][0] = 'X'  # Make a move in game logic
        self.app.buttons[0][0].config(text='X', state='disabled')  # Update button to match
        self.app.game_active = False  # Set game as inactive
        
        self.app.restart_game()  # Reset the game
        
        # Verify everything is reset to initial state
        assert self.app.game_active == True  # Verify game is active again
        assert self.app.game.board[0][0] == ''  # Verify game logic board is empty
        assert self.app.buttons[0][0]['text'] == ''  # Verify button text is empty
        assert self.app.buttons[0][0]['state'] == 'normal'  # Verify button is enabled
        
        # Check status message is reset
        status_text = self.app.status_label.cget('text')  # Get current status
        assert "Your Turn" in status_text  # Verify it shows initial message
    
    def test_player_move_invalid_cell(self):
        """Test player move behavior when clicking occupied cell."""
        # Reason: Verify that the game handles invalid moves gracefully
        # This tests the error condition of clicking an occupied cell
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        # Simulate an occupied cell
        self.app.game.board[1][1] = 'X'  # Mark cell as occupied in game logic
        
        # Attempt to make a move on the occupied cell
        self.app.player_move(1, 1)  # Try to click the occupied cell
        
        # Verify the status shows an error message
        status_text = self.app.status_label.cget('text')  # Get current status
        assert "already taken" in status_text.lower()  # Check for error message
        assert self.app.status_label.cget('fg') == 'orange'  # Verify warning color
    
    def test_player_move_inactive_game(self):
        """Test player move behavior when game is inactive."""
        # Reason: Verify that moves are prevented when the game has ended
        # This tests the error condition of interaction after game end
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        self.app.game_active = False  # Set game as inactive
        original_board = [row[:] for row in self.app.game.board]  # Copy current board state
        
        self.app.player_move(0, 0)  # Attempt to make a move
        
        # Verify that the board state hasn't changed
        assert self.app.game.board == original_board  # Board should remain unchanged
        assert self.app.buttons[0][0]['text'] == ''  # Button should remain empty


class TestGUIIntegration:
    """Test cases for GUI integration with game logic."""
    
    def setup_method(self):
        """Setup method called before each test."""
        # Reason: Create fresh instances for integration testing
        # This ensures clean state for testing GUI-logic interaction
        
        try:
            self.app = TicTacToeGUI()  # Create GUI instance for testing
        except tk.TclError:  # Handle case where no display is available
            self.skip_gui_tests = True  # Set flag to skip GUI tests
            return  # Exit early if no display
        
        self.skip_gui_tests = False  # Set flag that GUI tests can run
    
    def teardown_method(self):
        """Cleanup method called after each test."""
        # Reason: Clean up resources after each integration test
        # This prevents resource leaks in test environments
        
        if hasattr(self, 'app') and self.app.root and not self.skip_gui_tests:  # Check if resources exist
            self.app.root.destroy()  # Clean up GUI window
    
    def test_game_logic_gui_synchronization(self):
        """Test that GUI and game logic stay synchronized."""
        # Reason: Verify that the visual interface reflects the actual game state
        # This tests the critical integration between logic and display
        
        if self.skip_gui_tests:  # Check if GUI tests should be skipped
            return  # Skip test if no display available
        
        # Make a move through the GUI
        self.app.player_move(1, 1)  # Click center cell
        
        # Verify both GUI and logic are updated
        assert self.app.game.board[1][1] == 'X'  # Logic should show X
        assert self.app.buttons[1][1]['text'] == 'X'  # GUI should show X
        
        # Verify game continues to be active (no immediate win)
        assert self.app.game_active == True  # Game should still be active


# Reason: Run tests when this file is executed directly
# This allows developers to run GUI tests independently
if __name__ == "__main__":
    import unittest  # Import unittest for basic test running
    
    # Create a test suite and run all test methods
    loader = unittest.TestLoader()  # Create test loader
    suite = unittest.TestSuite()  # Create test suite
    
    # Add all test classes to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestTicTacToeGUI))  # Add GUI tests
    suite.addTests(loader.loadTestsFromTestCase(TestGUIIntegration))  # Add integration tests
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)  # Create test runner with verbose output
    runner.run(suite)  # Execute all tests 