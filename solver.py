from common import *
from renderer import TextRenderer
from sudoku import Contradiction


class Solver:
    renderer = TextRenderer(draw_possibilities=True)

    def __init__(self, sudoku, verbose=False):
        self._sudoku = sudoku.clone()
        self._sudoku.verbose = verbose
        self._verbose = verbose
        self._checkpoints = []
        
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
    
    def _deterministic_strategies(self):
        yield from self._find_singleton_in_cell()
        yield from self._find_singleton_in_unit()
        
    def _guess(self):
        # Start a new checkpoint by finding the cell with the fewest possibilities.
        while True:
            cell = min((c for c in CELLS if not self._sudoku.is_filled(c)), 
                       key=lambda c: len(self._sudoku.possibilities(c)))
            possibilities = self._sudoku.possibilities(cell)
            # If no guesses were found, we should try to backtrack.
            if cell and possibilities:
                break
            elif not self.backtrack():
                if self._verbose:
                    print('End of the line, no more possibilities!')
                return None

        # Take the first possibility as a guess.
        move = (cell, possibilities.pop())
        if self._verbose:
            print('Guessing: ', move)
        self._checkpoints.append((self._sudoku.clone(), move))
        return move
    
    def backtrack(self, last_move=None):
        # Backtrack to the last valid checkpoint that doesn't lead to an immediate contradiction.
        while True:
            try:
                if not last_move:
                    self._sudoku, last_move = self._checkpoints.pop()
                if self._verbose:
                    print('Backtracking from', last_move)
                self._sudoku.eliminate(*last_move)
                return True
            except Contradiction:
                # Keep backtracking further.
                continue
            except IndexError:
                return False
    
    def moves(self):
        while not self._sudoku.is_solved():
            found_move = False
            for move in self._deterministic_strategies():
                found_move = True
                yield move
            if found_move: continue
            # Only make a guess if we exhausted deterministic strategies.
            move = self._guess()
            if move:
                yield move
            else:
                break
    
    def solve(self):
        for move in self.moves():
            ok = self._sudoku.try_assign(*move)
            if not ok:
                self.backtrack(move)
            if self._verbose:
                if ok:
                    print('Found move: ', move)
                    print(self._sudoku)
                else:
                    print('Made bad move: ', move)

        if self._sudoku.is_solved():
            if self._verbose:
                print('Solved!')
            return True
        else:
            if self._verbose:
                print('Remaining possibilities:')
                print(self)
            return False