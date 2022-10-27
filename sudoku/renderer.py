from .common import COLS, ROWS
from termcolor import colored


class TextRenderer:
  def __init__(self, placeholder='.', draw_possibilities=False, colorize=False):
    self.set_placeholder(placeholder)
    self.set_draw_possibilities(draw_possibilities)
    self.set_colorize(colorize)

  def set_draw_possibilities(self, opt):
    self._draw_possibilities = opt

  def set_placeholder(self, opt):
    self._placeholder = opt

  def set_colorize(self, opt):
    self._colorize = opt

  def render_cell(self, sudoku, cell):
    if self._draw_possibilities:
      return ''.join(sudoku.possibilities(cell)) or 'X'
    else:
      value = sudoku.at(cell, self._placeholder)
      if self._colorize:
        if sudoku.moves and (cell, value) == sudoku.moves[-1]:
          return colored(value, 'green', attrs=['bold'])
        elif (cell, value) in sudoku.moves:
          return colored(value, attrs=['bold'])
        else:
          return colored(value, attrs=['dark'])
      return value

  def render_header(self, cell_size):
    return '   ' + ' '.join(''.join(c.center(cell_size) for c in cols)
                            for cols in ('123', '456', '789'))

  def render_separator(self, cell_size):
    return '  +' + '+'.join(['-' * cell_size * 3] * 3) + '+'

  def render_row(self, row, cells, cell_size):
    line = []
    for j, cell in enumerate(cells):
      if j == 0:
        line.append(row + ' ')
      if j % 3 == 0:
        line.append('|')
      line.append(f' {cell} ')
    line.append('|')
    return ''.join(line)

  def render(self, sudoku):
    """Returns a Sudoku puzzle rendered as a string."""
    rows = [[self.render_cell(sudoku, r+c) for c in COLS]
            for r in ROWS]
    cell_size = (9 if self._draw_possibilities else 1) + 2
    lines = []
    for i, row in enumerate(rows):
      if i == 0:
        lines.append(self.render_header(cell_size))
      if i % 3 == 0:
        lines.append(self.render_separator(cell_size))
      lines.append(self.render_row(ROWS[i], row, cell_size))
    lines.append(self.render_separator(cell_size))
    return '\n'.join(lines)
