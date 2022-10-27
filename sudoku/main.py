from . import solver
from .sudoku import Sudoku
from .renderer import TextRenderer


def main():
  r = TextRenderer(colorize=True)

  print('Example puzzle: 5...8...3|1..3...5.|836.....2|..423....|...7.1...|....983..|6.....721|.1...9..8|2...7...9')
  raw_puzzle = input('Input puzzle > ')
  sudoku = Sudoku.from_text(raw_puzzle)
  sudoku.set_verbose(True)
  print()

  s = solver.Solver(sudoku, verbose=True)
  s.solve(renderer=r)
