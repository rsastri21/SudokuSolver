# The recursive backtracking algorithm for Sudoku

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

# Recursive backtracking algorithm
def solve(board):
    # Base case --> Last position is correct
    find = find_empty(board)
    if find:
        row, col = find 
    else: 
        return True # Every position in the board is filled in.

    # Loop through possible options 1 through 9
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            # Re-assign empty space
            board[row][col] = i

            # Attempt to solve
            if solve(board):
                return True
                
            # Backtrack if solution is not possible with selected i
            board[row][col] = 0
    
    return False


# Check if a given space is valid
def valid(board, num, pos):
    # Checking the row
    for i in range(len(board[0])):
        # Check if a board space in a row is equal to the provided number
        # Skip the position being checked for validity as that will return true.
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    
    # Checking the column
    for j in range(len(board)):
        # Same process with indices flipped for columns
        if board[j][pos[1]] == num and pos[0] != j:
            return False
    
    # Check squares
    # First find the box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # Iterate through the box
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False


    return True




# Prints out the board in a 3x3 segmented grid.
def print_board(board):

    # Loop through number of rows
    for i in range(len(board)):
        # Dividing lines
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        # Loop through columns
        for j in range(len(board[0])):
            # Vertical dividing lines
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")
            
            # Last number and shift to next row
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end = "")

# Returns a tuple (x, y) of the first empty space on the board.
def find_empty(board):
    # i denotes rows
    for i in range(len(board)):
        # j denotes columns
        for j in range(len(board[0])):
            # Check that space is empty
            if board[i][j] == 0:
                return (i, j)
    return None
