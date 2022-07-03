import pygame
import time
from solver import *
pygame.font.init()

# A class managing the overarching grid
class GameBoard:
    # 2d Array represents a Sudoku board with zeros taking empty places.
    game_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    # Constructor initializes properties of the GUI window
    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window

        # Create cube array
        # Passes the value from the game_board field
        self.cubes = [[Cube(self.game_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

        self.model = None
        self.update_model()

        self.selected = None
    
    # Update a model to be tested for validity later
    # 2D Array with current solutions
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    # Puts a value in an empty space
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            # Return true if the entered value yields a solvable board
            # Return false if the guess is unsolvable
            # Updates the appropriate parameters in both cases
            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
    # Temporary guess before confirming
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # Creates the visual grid
    def draw(self):
        spacing = self.width / 9
        for i in range(self.rows + 1):
            # Creates bolded lines around each 3x3 sub-grid
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            # Horizontal lines
            pygame.draw.line(self.window, (0, 0, 0), (0, i * spacing), (self.width, i * spacing), thick)
            # Verticle Lines
            pygame.draw.line(self.window, (0, 0, 0), (i * spacing, 0), (i * spacing, self.height), thick)
        # Draw cubes in appropriate locations
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw_cube(self.window)

    # Select a cube on the grid   
    def select(self, row, col):
        # Deselect all others
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        
        # Update selected cube
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # Clears a cube
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # Gives the current box depending on mouse position
    def click(self, pos):
        # Only returns if mouse pointer is within the grid window
        if pos[0] < self.width and pos[1] < self.height:
            spacing = self.width / 9
            x = pos[1] // spacing
            y = pos[0] // spacing
            return (int(x), int(y))
        else:
            return None
    
    # Returns true if every cube has a value (solved)
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    # Solve the current board
    # Based on the algorithm in solver.py
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
            
                if self.solve():
                    return True

            self.model[row][col] = 0

        return False

    # A modified solve to update the gui and provide visual progress
    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                # Update the corresponding cube element on screen
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.window, True)
                
                # Update model and delay for user 
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve_gui():
                    return True

                # Backtracking if the attempt fails
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(50)
        return False


# A class managing the individual spaces of the grid
class Cube:
    # Fields 
    rows = 9
    cols = 9

    # Constructor initializes properties of the cube
    def __init__(self, value, row, col, width, height):
        # Value held by the cube
        self.value = value
        # Temporary value if the cube is not solved
        self.temp = 0

        # Position on the grid
        self.row = row 
        self.col = col

        # Size according to game window dimensions
        self.width = width
        self.height = height

        # Field representing if the current cube is selected by the user
        self.selected = False

    # Draws a cube according to the window size
    def draw_cube(self, window):
        font = pygame.font.SysFont('Helvetica', 40)

        spacing = self.width / 9
        # Makes each cube 1/9 of the total grid in both dimensions
        x = self.col * spacing
        y = self.row * spacing

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128)) # Writes the temp value in black
            window.blit(text, (x+5, y+5)) # Places temp value in top left of box
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0)) # Writes the actual value in black
            # Places the value in the middle of the box
            window.blit(text, (x + (spacing/2 - text.get_width()/2), y + (spacing/2 - text.get_height()/2)))
        
        if self.selected:
            # Draws a red square around the selected cube
            pygame.draw.rect(window, (255, 0, 0), (x, y, spacing, spacing), 3)
    
    def draw_change(self, window, g=True):
        font = pygame.font.SysFont('Helvetica', 40)

        spacing = self.width / 9
        x = self.col * spacing
        y = self.row * spacing
        
        # Draws a filled white rectangle with the appropriate value
        pygame.draw.rect(window, (255, 255, 255), (x, y, spacing, spacing), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (spacing/2 - text.get_width()/2), y + (spacing/2 - text.get_height()/2)))
        # Draws either a green or red border depending on the input parameter.
        # Green by default
        if g:
            pygame.draw.rect(window, (0, 255, 0), (x, y, spacing, spacing), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, spacing, spacing), 3)
    
    # Two setter methods that update either the value or temporary value
    def set(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val

# Game management
def redraw_window(window, board, time, strikes):
    window.fill((255, 255, 255))
    # Create time component
    font = pygame.font.SysFont("Helvetica", 20)
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    window.blit(text, (540 - 160, 560))
    # Draw X's for strikes
    text = font.render("X " * strikes, 1, (255, 0, 0))
    window.blit(text, (20, 560))
    # Create game space
    board.draw()

# Create a friendly to read time
def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Solver")
    board = GameBoard(9, 9, 540, 540, window)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        # Event handlers for key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                
                # Solve the board automatically with space press
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                
                # Update board when a new guess is submitted
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            # Select the appropriate cube on the board            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
            
        if board.selected and key != None:
            board.sketch(key)
        
        redraw_window(window, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()            