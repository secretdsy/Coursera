"""
Clone of 2048 game.
"""
import poc_2048_gui
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def merge(line):
    """
    This is a docstring for a merge function:
    Return a new merged list.
    """

    # empty list
    answer = []
    tmp_list = []
    
    # append not 0 in list 
    for dummy_i in range(len(line)):
        if line[dummy_i] != 0:
            tmp_list.append(line[dummy_i])
    
    # compare of the numbers
    if len(tmp_list) == 0:
        return line
    elif len(tmp_list) == 1:
        return tmp_list + [0 for dummy_i in range(len(line) - 1)]
    else:
        dummy_i = 0
        while(dummy_i < len(tmp_list) - 1):
            dummy_j = dummy_i + 1
            while(dummy_j < len(tmp_list)):
                if tmp_list[dummy_i] == tmp_list[dummy_j]:
                    answer.append(2 * tmp_list[dummy_i])
                    dummy_i += 2
                    break
                else:
                    answer.append(tmp_list[dummy_i])
                    dummy_i += 1
                    break
            if len(tmp_list) - dummy_i == 1:
                answer.append(tmp_list[-1])
    
    # add 0 elements to the list
    if len(answer) != len(line):
        answer += [0 for dummy_i in range(len(line) - len(answer))]
    
    return answer

def transpose(grid):
    """
    transpose grid list
    """
    return [list(dummy_x) for dummy_x in zip(*grid)]


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        variable initialization
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.grid = [[0 for dummy_row in range(self.get_grid_width())] for dummy_col in range(self.get_grid_height())]
        
    def __str__(self):
        ans = "["
        for dummy_i in range(len(self.grid)):
            if dummy_i < len(self.grid) - 1:
                ans += str(self.grid[dummy_i])
                ans += "\n"
            else:
                ans += str(self.grid[dummy_i])
        return ans + "]"
     
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # Initializes 2 or 4 in up to 2 random positions.
        self.grid = [[0 for dummy_row in range(self.get_grid_width())] for dummy_col in range(self.get_grid_height())]
        for dummy_i in range(2):
            self.new_tile()

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tmp_grid = []
        for dummy_i in range(self.get_grid_height()):
            tmp_row = []
            for dummy_j in range(self.get_grid_width()):
                tmp_row.append(self.grid[dummy_i][dummy_j])
            tmp_grid.append(tmp_row)
        
        if direction == LEFT:
            for dummy_i in range(self.get_grid_height()):
                self.grid[dummy_i] = merge(self.grid[dummy_i])
        elif direction == RIGHT:
            for dummy_i in range(self.get_grid_height()):
                self.grid[dummy_i].reverse()
                self.grid[dummy_i] = merge(self.grid[dummy_i])
                self.grid[dummy_i].reverse()
        elif direction == UP:
            self.grid = transpose(self.grid)
            for dummy_i in range(self.get_grid_width()):
                self.grid[dummy_i] = merge(self.grid[dummy_i])
            self.grid = transpose(self.grid)
        elif direction == DOWN:
            self.grid = transpose(self.grid)
            for dummy_i in range(self.get_grid_width()):
                self.grid[dummy_i].reverse()
                self.grid[dummy_i] = merge(self.grid[dummy_i])
                self.grid[dummy_i].reverse()
            self.grid = transpose(self.grid)
            
        if tmp_grid != self.grid:
            self.new_tile()
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        dummy_k = 0
        while(dummy_k < 1):
            rand_col = random.randrange(self.get_grid_height())
            rand_row = random.randrange(self.get_grid_width())
            zero_cnt = 0
            for dummy_i in range(self.get_grid_height()):
                zero_cnt += self.grid[dummy_i].count(0)
            
            if zero_cnt == 0:
                break
            elif self.grid[rand_col][rand_row] == 0:
                tmp = random.randrange(0, 10)
                if tmp == 9:
                    self.set_tile(rand_col, rand_row, 4)
                else:
                    self.set_tile(rand_col, rand_row, 2)
                dummy_k += 1
                
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]
    

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
