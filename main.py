"""
Smart Tic-Tac-Toe GUI Application

This module creates a graphical user interface for the Tic-Tac-Toe game
using Tkinter, allowing players to interact with the AI through button clicks.
"""

import tkinter as tk  # Import the GUI framework for creating the user interface
from tkinter import messagebox  # Import message box for displaying game results
from tictactoe_logic import TicTacToe, find_best_move  # Import our game logic and AI


class TicTacToeGUI:
    """
    Manages the graphical user interface for the Tic-Tac-Toe game.
    
    This class handles all GUI elements, user interactions, and coordinates
    between the visual interface and the underlying game logic.
    """
    
    def __init__(self):
        # Reason: Initialize the GUI components and game state
        # We need both the visual elements and the game logic state
        
        self.game = TicTacToe()  # Create instance of game logic to track board state
        self.game_active = True  # Flag to control whether moves can be made
        
        # Create the main application window
        self.root = tk.Tk()  # Initialize the main window
        self.root.title("Smart Tic-Tac-Toe with Minimax AI")  # Set window title
        self.root.geometry("400x500")  # Set window size (width x height)
        self.root.resizable(False, False)  # Prevent window resizing for consistent layout
        
        # Initialize the UI components
        self.setup_ui()  # Create all visual elements and layout
        
    def setup_ui(self):
        """Create and arrange all UI elements in the main window."""
        # Reason: Organize UI creation into separate method for better code structure
        # This separates initialization from UI layout for maintainability
        
        # Create title label at the top
        title_label = tk.Label(  # Create label widget for game title
            self.root,  # Parent container is the main window
            text="Smart Tic-Tac-Toe",  # Display text for the title
            font=("Arial", 18, "bold"),  # Font family, size, and style
            fg="navy"  # Text color (foreground)
        )
        title_label.pack(pady=10)  # Add title to window with vertical padding
        
        # Create status label to show current game state
        self.status_label = tk.Label(  # Create label for game status messages
            self.root,  # Parent container is the main window
            text="Your Turn! Click any cell to start.",  # Initial status message
            font=("Arial", 12),  # Font family and size
            fg="green"  # Text color for positive messages
        )
        self.status_label.pack(pady=5)  # Add status label with vertical padding
        
        # Create frame to contain the 3x3 game board
        board_frame = tk.Frame(self.root)  # Create container for game buttons
        board_frame.pack(pady=20)  # Add frame to window with vertical padding
        
        # Create 3x3 grid of buttons for the game board
        self.buttons = []  # Initialize list to store button references
        for row in range(3):  # Create each row of buttons
            button_row = []  # Initialize list for current row of buttons
            for col in range(3):  # Create each button in the current row
                button = tk.Button(  # Create individual game cell button
                    board_frame,  # Parent container is the board frame
                    text="",  # Initially empty text
                    width=6,  # Button width in characters
                    height=3,  # Button height in characters
                    font=("Arial", 20, "bold"),  # Large font for X and O symbols
                    command=lambda r=row, c=col: self.player_move(r, c)  # Button click handler
                )
                button.grid(row=row, column=col, padx=2, pady=2)  # Position button in grid
                button_row.append(button)  # Add button to current row list
            self.buttons.append(button_row)  # Add completed row to main button list
        
        # Create control buttons frame
        controls_frame = tk.Frame(self.root)  # Create container for control buttons
        controls_frame.pack(pady=20)  # Add controls frame with vertical padding
        
        # Create restart button
        restart_button = tk.Button(  # Create button to restart the game
            controls_frame,  # Parent container is the controls frame
            text="Restart Game",  # Button label text
            font=("Arial", 12, "bold"),  # Font styling
            bg="lightblue",  # Background color
            command=self.restart_game  # Function to call when clicked
        )
        restart_button.pack(side=tk.LEFT, padx=10)  # Position button on left side
        
        # Create quit button
        quit_button = tk.Button(  # Create button to exit the application
            controls_frame,  # Parent container is the controls frame
            text="Quit",  # Button label text
            font=("Arial", 12, "bold"),  # Font styling
            bg="lightcoral",  # Background color
            command=self.root.quit  # Function to call when clicked (quit app)
        )
        quit_button.pack(side=tk.RIGHT, padx=10)  # Position button on right side
    
    def player_move(self, row, col):
        """
        Handle player's move when a button is clicked.
        
        Args:
            row (int): Row index of the clicked button (0-2)
            col (int): Column index of the clicked button (0-2)
        """
        # Reason: This method coordinates player input with game logic and GUI updates
        # It validates the move, updates the display, and triggers the AI response
        
        if not self.game_active:  # Check if the game is still active
            return  # Exit early if game has ended
        
        if self.game.board[row][col] != '':  # Check if the clicked cell is already occupied
            self.update_status("Cell already taken! Try another cell.", "orange")  # Show error message
            return  # Exit early without making a move
        
        # Make the player's move
        self.game.board[row][col] = 'X'  # Update game logic board state
        self.buttons[row][col].config(text='X', fg='blue')  # Update button display
        
        # Check if player won
        if self.game.check_winner('X'):  # Check if player's move resulted in a win
            self.update_status("Congratulations! You won!", "green")  # Show win message
            self.game_active = False  # Disable further moves
            self.disable_all_buttons()  # Prevent additional button clicks
            return  # Exit since game is over
        
        # Check if game is a draw
        if self.game.is_draw():  # Check if the board is full with no winner
            self.update_status("It's a draw! Good game!", "purple")  # Show draw message
            self.game_active = False  # Disable further moves
            self.disable_all_buttons()  # Prevent additional button clicks
            return  # Exit since game is over
        
        # If game continues, trigger AI move
        self.update_status("AI is thinking...", "orange")  # Show AI thinking message
        self.root.update()  # Force GUI update to show status change immediately
        self.root.after(500, self.ai_move)  # Schedule AI move after 500ms delay for better UX
    
    def ai_move(self):
        """Execute the AI's move using the minimax algorithm."""
        # Reason: This method handles the AI's turn by finding the optimal move
        # and updating both the game state and visual representation
        
        if not self.game_active:  # Check if the game is still active
            return  # Exit early if game has ended
        
        best_move = find_best_move(self.game)  # Get optimal move from AI algorithm
        
        if best_move is None:  # Check if no moves are available (shouldn't happen)
            return  # Exit early if no valid moves
        
        row, col = best_move  # Unpack the AI's chosen move coordinates
        
        # Make the AI's move
        self.game.board[row][col] = 'O'  # Update game logic board state
        self.buttons[row][col].config(text='O', fg='red')  # Update button display
        
        # Check if AI won
        if self.game.check_winner('O'):  # Check if AI's move resulted in a win
            self.update_status("AI wins! Better luck next time!", "red")  # Show AI win message
            self.game_active = False  # Disable further moves
            self.disable_all_buttons()  # Prevent additional button clicks
            return  # Exit since game is over
        
        # Check if game is a draw
        if self.game.is_draw():  # Check if the board is full with no winner
            self.update_status("It's a draw! Good game!", "purple")  # Show draw message
            self.game_active = False  # Disable further moves
            self.disable_all_buttons()  # Prevent additional button clicks
            return  # Exit since game is over
        
        # Game continues - player's turn
        self.update_status("Your turn! Make your move.", "green")  # Prompt player for next move
    
    def update_status(self, message, color="black"):
        """
        Update the status label with a new message and color.
        
        Args:
            message (str): The status message to display
            color (str): The color for the status text (default: "black")
        """
        # Reason: Centralize status updates to ensure consistent formatting
        # and provide visual feedback about the current game state
        
        self.status_label.config(text=message, fg=color)  # Update label text and color
    
    def disable_all_buttons(self):
        """Disable all game board buttons to prevent further moves."""
        # Reason: When the game ends, we need to prevent additional button clicks
        # This provides clear visual feedback that the game is over
        
        for row in range(3):  # Iterate through each row of buttons
            for col in range(3):  # Iterate through each button in the row
                self.buttons[row][col].config(state='disabled')  # Disable the button
    
    def restart_game(self):
        """Reset the game to its initial state for a new game."""
        # Reason: Allow players to start a new game without restarting the application
        # This resets both the game logic and the visual interface
        
        self.game = TicTacToe()  # Create new game instance with empty board
        self.game_active = True  # Re-enable game interactions
        
        # Reset all buttons to their initial state
        for row in range(3):  # Iterate through each row of buttons
            for col in range(3):  # Iterate through each button in the row
                self.buttons[row][col].config(  # Reset button configuration
                    text="",  # Clear button text
                    state='normal',  # Re-enable button
                    fg='black'  # Reset text color
                )
        
        self.update_status("Your Turn! Click any cell to start.", "green")  # Reset status message
    
    def run(self):
        """Start the GUI main event loop."""
        # Reason: This method starts the Tkinter event loop that handles user interactions
        # It should be called last after all GUI setup is complete
        
        self.root.mainloop()  # Start the GUI event loop


# Reason: This block ensures the application only runs when the script is executed directly
# It prevents the GUI from starting if this module is imported elsewhere
if __name__ == "__main__":
    app = TicTacToeGUI()  # Create the GUI application instance
    app.run()  # Start the application 