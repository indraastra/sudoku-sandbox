from common import *
from renderer import TextRenderer


class Solver:
    renderer = TextRenderer(draw_possibilities=True)

    def __init__(self, sudoku, verbose=False):
        self._sudoku = sudoku.clone()
        self._sudoku.verbose = verbose
        self._verbose = verbose
        
    def __str__(self):
        return self.renderer.render(self._sudoku)
    
    def _find_singleton_in_cell(self):
        for cell in CELLS:
            if self._sudoku.is_filled(cell):
                continue
            possibilities = self._sudoku.possibilities(cell)
            if len(possibilities) == 1:
                value = list(possibilities)[0]
                yield (cell, value)
    
    def _find_singleton_in_unit(self):
        for unit in UNITS:
            needed = set(DIGITS) - set(self._sudoku.at(cell) for cell in unit)
            value_cells = {value: [cell for cell in unit 
                                   if value in self._sudoku.possibilities(cell)]
                           for value in needed}
            for value, cells in value_cells.items():
                if len(cells) == 1:
                    yield (cells[0], value)
    
    @property
    def sudoku(self):
        return self._sudoku
    
    def _chained_strategies(self):
        yield from self._find_singleton_in_cell()
        yield from self._find_singleton_in_unit()
    
    def steps(self):
        while not self._sudoku.is_solved():
            found_move = False
            for move in self._chained_strategies():
                found_move = True
                yield move
            # Terminate if we found no moves!
            if not found_move:
                if self._verbose:
                    print('No more moves!')
                break
    
    def solve(self):
        for move in self.steps():
            self._sudoku.assign(*move)
            if self._verbose:
                print('Found move: ', move)
                print(self._sudoku)

        if self._sudoku.is_solved():
            if self._verbose:
                print('Solved!')
            return True
        else:
            if self._verbose:
                print('Remaining possibilities:')
                print(self)
            return False