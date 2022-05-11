import random
import enum
from copy import deepcopy
from time import sleep


class ResultDescription(enum.Enum):
    CYCLE = 'Game is over. State is cycled'
    NO_CELLS = 'Game is over. No alive cells left'
    NO_CHANGES = 'Game is over. No changes are noticed'
    OTHER = 'Something went wrong'
    
    

class Board:
    def __init__(self, size: tuple = (25, 25), alive_cells=100) -> None:
        self.rows = size[0]
        self.cols = size[1]
        self.size = self.rows * self.cols
        self.alive_cells = alive_cells
        self.board = self.populate_board()
        self.next_board = deepcopy(self.board)
        self.insert_alive_cells()
        
        
    def populate_board(self):
        return [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]


    def insert_alive_cells(self):
        if self.alive_cells > self.size:
            raise Exception('Too many alive cells')
        positions = set() 
        while len(positions) < self.alive_cells:
            positions.add((random.randint(0, self.rows-1), random.randint(0, self.cols-1)))
    
        for r, c in positions:
            self.board[r][c] = Cell(r, c, alive=True)
        

    def get_cells_alive_neighbours(self, row, col):
        neighbours = []
        
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if r == row and c == col:
                    continue
                if r < 0:
                    r = self.rows - 1
                elif r > self.rows -1:
                    r = 0 
                if c < 0:
                    c = self.cols - 1
                elif c > self.cols -1:
                    c = 0 
                neighbours.append(self.board[r][c])
        
        return len([n for n in neighbours if n.is_alive])
              
            
    def iterate(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell_old = self.board[r][c]
                cell_next = self.next_board[r][c]
    
                if cell_old.is_alive:
                    if not self.get_cells_alive_neighbours(cell_old.row, cell_old.col) in (2, 3):
                        cell_next.is_alive = False
                        self.alive_cells -= 1
                    else:
                        cell_next.is_alive = True
                else:
                    if self.get_cells_alive_neighbours(cell_old.row, cell_old.col) == 3:
                        cell_next.is_alive = True
                        self.alive_cells += 1
        print(self)
        print()
    
        
    def __str__(self) -> str:
        return  '\n'.join('  '.join(map(str, row)) for row in self.board)
        

class Cell:
    def __init__(self, row, col, alive=False) -> None:
         self.row = row
         self.col = col
         self.is_alive = alive
         
    
    def __eq__(self, other: "Cell") -> bool:
        return self.row == other.row and self.col == other.col and self.is_alive == other.is_alive
        
    
    def __repr__(self) -> str:
        if self.is_alive:
            return '●'
        return ' '
   
   
class Controller:
    def __init__(self) -> None:
        self.board = Board()

    def run_life(self, cycles=10000, consecutive_repeats=10):
        repeating_alive_cells = self.board.alive_cells
        consecutive_alive_qty = 0
        while cycles > 0:
            sleep(0.05)
            
            if consecutive_alive_qty > consecutive_repeats:
                return ResultDescription.CYCLE
            if self.board.alive_cells <= 0:
                return ResultDescription.NO_CELLS
            
            self.board.iterate()
            if self.board.board == self.board.next_board:
                return ResultDescription.NO_CHANGES
            self.board.board = deepcopy(self.board.next_board)
            if self.board.alive_cells == repeating_alive_cells:
                consecutive_alive_qty += 1
            else:
                consecutive_alive_qty = 0
                repeating_alive_cells = self.board.alive_cells
            cycles -= 1
    
    def display_result(self, result: ResultDescription):
        print(result._value_)
    

if __name__ == '__main__':
    game = Controller()
    res = game.run_life()
    game.display_result(res)