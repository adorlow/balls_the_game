#### ############################## ####
#### GENERATED WITH CHAT-GPT HELP   ####
#### ############################## ####

from balls_mechanics import *
from player import *

import pygame
import sys
import pickle

# Initialize pygame
pygame.init()

# Constants for the game window
WIDTH, HEIGHT = 600, 400
ROWS, COLS = 4, 4
CIRCLE_RADIUS = 30
MARGIN = 10  # Space between circles
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 40
BUTTON_X = WIDTH - BUTTON_WIDTH - 20  # Button position (right side)
BUTTON_Y = 20  # Button position (top)
NEW_GAME_BUTTON_Y = BUTTON_Y + BUTTON_HEIGHT + 10  # "New Game" button below "Move" button
COMPUTER_STARTS_BUTTON_Y = NEW_GAME_BUTTON_Y + BUTTON_HEIGHT + 10  # "Computer Starts" button below "New Game" button

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_HOVER_COLOR = (0, 0, 200)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 0, 0)  # Color for "Game ended" message
ILLEGAL_MOVE_COLOR = (255, 0, 255)  # Color for "Move is illegal" message

# Create the screen (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balls")

# 2D list to track the state of each circle (whether it is active on the grid)
grid = np.array([[True for _ in range(COLS)] for _ in range(ROWS)])

# 2D list to track the state of each circle (whether it is highlighted)
highlighted = np.array([[False for _ in range(COLS)] for _ in range(ROWS)])

# Moves that can be performed for actual grid / board
n = ROWS
kernels = np.bool_(spider_flat(grid))
accessible_moves = possible_moves(board=grid.reshape(n*n), kernels=kernels, n=n)

# Global variable to track the turn (0 = player, 1 = computer)
which_player_turn = 0

# Computer Player, greedy one
# no learning implemented in here
player_computer = Player_which_learns(name="1", n=n, epsilon=0)

# importing the policy for playing
with open('action_values_5x5.pkl', 'rb') as fp:
    recipe_for_winning = pickle.load(fp)
player_computer.actions_values = recipe_for_winning
    
# Function to draw the ROWSxCOLS grid of circles
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]:  # Draw only circles that are in the grid (True)
                # Calculate the position for each circle (center of the circle)
                x = col * (2 * CIRCLE_RADIUS + MARGIN) + CIRCLE_RADIUS + MARGIN
                y = row * (2 * CIRCLE_RADIUS + MARGIN) + CIRCLE_RADIUS + MARGIN
                # If the circle is highlighted, draw it in green, otherwise red
                color = GREEN if highlighted[row][col] else RED
                pygame.draw.circle(screen, color, (x, y), CIRCLE_RADIUS)

# Function to check if the mouse click is inside a circle
def check_click(pos):
    mx, my = pos
    for row in range(ROWS):
        for col in range(COLS):
            # Calculate the position of the circle's center
            x = col * (2 * CIRCLE_RADIUS + MARGIN) + CIRCLE_RADIUS + MARGIN
            y = row * (2 * CIRCLE_RADIUS + MARGIN) + CIRCLE_RADIUS + MARGIN
            # Check if the mouse click is inside the circle (distance from center <= radius)
            distance = ((mx - x) ** 2 + (my - y) ** 2) ** 0.5
            if distance <= CIRCLE_RADIUS:
                return row, col  # Return the row and col of the clicked circle
    return None  # Return None if no circle was clicked

# Function to draw a button
def draw_button(text, x, y):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Check if mouse is hovering over the button
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    
    # Draw the button text
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

# Function to reset the grid and highlighted circles (New Game)
def new_game():
    global grid, highlighted
    global accessible_moves
    # Reset all grid cells to True (visible) and highlighted cells to False (non-highlighted)
    grid = np.array([[True for _ in range(COLS)] for _ in range(ROWS)])
    highlighted = np.array([[False for _ in range(COLS)] for _ in range(ROWS)])
    accessible_moves = possible_moves(board=grid.reshape(n*n), kernels=kernels, n=n)

# Function to delete the highlighted circles
def delete_after_move():
    global highlighted
    global grid
    global accessible_moves
    global which_player_turn
    
    grid_after_move = np.uint8(grid) - np.uint8(highlighted)
    grid_after_move_number = np.sum(np.ravel(grid_after_move) * 2 ** np.arange(n**2-1, -1, -1))
    is_move_legal = grid_after_move_number in accessible_moves
        
    if is_move_legal:
        for row in range(ROWS):
            for col in range(COLS):
                if highlighted[row][col]:
                    grid[row][col] = False  # Set it to False in the grid (it disappears)
                    highlighted[row][col] = False  # Reset the highlight (circle goes back to red)
        
        # Updating the accessible_moves which can be made
        accessible_moves = possible_moves(board=grid.reshape(n*n), kernels=kernels, n=n)
        # computer plays, change the round 
        which_player_turn = 1
        
# Function to check if move is legal
def is_move_legal(grid, highlighted):
    grid_after_move = np.uint8(grid) - np.uint8(highlighted)
    grid_after_move_number = np.sum(np.ravel(grid_after_move) * 2 ** np.arange(n**2-1, -1, -1))

    is_move_legal = grid_after_move_number in accessible_moves
    return is_move_legal

# Function to count visible circles on the grid
def count_visible_circles():
    count = 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]:  # Count circles that are still visible
                count += 1
    return count

# Function to display "Game ended" message
def draw_game_ended_message():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game ended", True, GAME_OVER_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(text, text_rect)

# Function to display "Computer woon" message
def computer_won_message():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Computer won", True, GAME_OVER_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))
    screen.blit(text, text_rect)    

# Function to display "You won" message
def you_won_message():
    font = pygame.font.SysFont(None, 50)
    text = font.render("You won", True, GAME_OVER_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))
    screen.blit(text, text_rect)     
    
# Function to display "MOVE IS ILLEGAL" message
def draw_illegal_move_message():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Move is illegal", True, ILLEGAL_MOVE_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(text, text_rect)

# Function to display the current turn (Player or Computer)
def draw_turn_message():
    global which_player_turn
    turn_message = "Player's Turn" if which_player_turn == 0 else "Computer's Turn"
    font = pygame.font.SysFont(None, 30)
    text = font.render(turn_message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(text, text_rect)
    
# Main game loop
def main():
    global which_player_turn
    global grid
    global highlighted
    global accessible_moves
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detect mouse button press (click to toggle highlight on circles)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    clicked_circle = check_click(pos)
                    if clicked_circle:
                        row, col = clicked_circle
                        # Toggle the highlight for the clicked circle
                        if grid[row][col] == True:
                            highlighted[row][col] = not highlighted[row][col]

                    # Check if the "Move" button is clicked
                    button_rect = draw_button("Move", BUTTON_X, BUTTON_Y)
                    if button_rect.collidepoint(pos):
                        delete_after_move()  # Remove all highlighted circles

                    # Check if the "New Game" button is clicked
                    new_game_button_rect = draw_button("New Game", BUTTON_X, NEW_GAME_BUTTON_Y)
                    if new_game_button_rect.collidepoint(pos):
                        new_game()  # Reset the grid and circles
                        which_player_turn = 0
                        
                    # Check if the "Computer Starts" button is clicked
                    computer_starts_button_rect = draw_button("Computer Starts", BUTTON_X, COMPUTER_STARTS_BUTTON_Y)
                    if computer_starts_button_rect.collidepoint(pos):
                        which_player_turn = 1  # Change the turn to computer's turn
                        
        # Fill the screen with a background color
        screen.fill(WHITE)

        # Draw the grid of circles
        draw_grid()

        # Check if the game has ended (only one circle is visible)
        if count_visible_circles() == 1:
            draw_game_ended_message()  # Show the "Game ended" message
            if which_player_turn == 0:
                computer_won_message() # Show the "Computer won" message
            if which_player_turn == 1:
                you_won_message() # Show the "You won" message
            
            
        # Check if the move is legal
        if is_move_legal(grid, highlighted) == 0  and np.sum(highlighted) != 0:
            draw_illegal_move_message()  # Show the "Move is illegal" message
        
        # Check if it is computer round
        if which_player_turn == 1 and count_visible_circles() != 1:
            computer_move = player_computer.make_move(np.array(grid).reshape(n**2))
            grid = number_to_array(computer_move, n).reshape(n,n)
            # reset highlights
            highlighted = np.array([[False for _ in range(COLS)] for _ in range(ROWS)])
            # back to player
            which_player_turn = 0
            accessible_moves = possible_moves(board=grid.reshape(n*n), kernels=kernels, n=n)
            
        draw_button("Move", BUTTON_X, BUTTON_Y)
        draw_button("New Game", BUTTON_X, NEW_GAME_BUTTON_Y)
        draw_button("Computer Starts", BUTTON_X, COMPUTER_STARTS_BUTTON_Y)
        draw_turn_message()
        
        # Update the display
        pygame.display.update()

if __name__ == "__main__":
    main()
