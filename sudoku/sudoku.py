import re
import itertools
import copy

from .common import *
from .renderer import TextRenderer


class Contradiction(Exception):
  pass


class Sudoku:
  renderer = TextRenderer()

  def __init__(self, assignments=None, verbose=False):
    self._verbose = verbose
    self._values = {}
    self._possibilities = {cell: set(DIGITS) for cell in CELLS}
    self._moves = []
    if assignments:
      for cell in assignments:
        self.assign(cell, assignments[cell])
      self._moves = []  # Reset moves.

  def __str__(self):
    return self.to_text()

  def _validate_cell(self, cell):
    if cell not in self._possibilities:
      raise ValueError('Invalid cell: {}'.format(cell))

  def _validate_value(self, value):
    if value not in DIGITS and value not in PLACEHOLDERS:
      raise ValueError('Invalid value: {}'.format(value))

  def set_verbose(self, opt):
    self._verbose = opt

  @property
  def values(self):
    return self._values

  @property
  def moves(self):
    return self._moves

  def try_assign(self, cell, value):
    """
    Assigns `value` to `cell` if possible without raising a contradiction.
    """
    sudoku = self.clone()
    sudoku.set_verbose(False)
    try:
      sudoku.assign(cell, value)
      self.assign(cell, value)  # It's safe.
    except Contradiction:
      return False
    else:
      return True

  def assign(self, cell, value):
    """
    Assigns `value` to `cell` and raises if a contradiction results.
    """
    self._validate_cell(cell)
    self._validate_value(value)
    if value in PLACEHOLDERS:
      # Any value is possible.
      if self._verbose:
        print('Skipping assignment of {} to {}'.format(value, cell))
      return
    self._values[cell] = value
    self._moves.append((cell, value))
    if self._verbose:
      print('Assigned {} to {}'.format(value, cell))
    for p in self._possibilities[cell] - set(value):
      self.eliminate(cell, p)

  def eliminate(self, cell, value):
    """
    Eliminates `value` as a possibility for `cell` and raises if a
    contradiction results.
    """
    possibilities = self._possibilities[cell]
    if value not in possibilities:
      return
    if self._verbose:
      print('Eliminating {} from {}'.format(value, cell), possibilities)
    possibilities.discard(value)
    if len(possibilities) == 0:
      raise Contradiction(
          'No possibilities left for {} after eliminating {}!'.format(cell, value))
    elif len(possibilities) == 1:
      new_value = list(possibilities)[0]
      if self._verbose:
        print('Only possibility is {} for {}, pruning it from peers!'.format(
            new_value, cell))
      # Prune this possibility from peers.
      for peer in PEERS[cell]:
        self.eliminate(peer, new_value)

  def at(self, cell, default='.'):
    self._validate_cell(cell)
    return self._values.get(cell, default)

  def possibilities(self, cell):
    self._validate_cell(cell)
    return sorted(self._possibilities[cell])

  def is_filled(self, cell):
    self._validate_cell(cell)
    return cell in self._values

  def is_solved(self):
    # All cells should have an assignment.
    return all(cell in self._values for cell in CELLS)

  def to_text(self):
    return self.renderer.render(self)

  def clone(self):
    return copy.deepcopy(self)

  @classmethod
  def from_grid(cls, grid):
    if (len(grid) != 9 or
            not all(len(grid[i]) == 9 for i in range(9))):
      raise ValueError('Input must be a 9x9 grid!')
    values = (str(i) for i in itertools.chain(*grid))
    assignments = dict(zip(CELLS, values))
    return Sudoku(assignments)

  @classmethod
  def from_text(cls, text):
    values = re.sub(r'[^0-9.]', '', text.strip())
    if len(values) != 81:
      raise ValueError('Invalid puzzle length!: {}'.format(len(values)))
    assignments = dict(zip(CELLS, values))
    return Sudoku(assignments)
