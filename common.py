# From Norvig.
def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a+b for a in A for b in B]


DIGITS = '123456789'
ROWS = 'ABCDEFGHI'
COLS = DIGITS
PLACEHOLDERS = '0.'
CELLS = cross(ROWS, COLS)
UNITS = (
        [cross(ROWS, c) for c in COLS] +
        [cross(r, COLS) for r in ROWS] +
        [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    )
PEERS = {s: set(sum([u for u in UNITS if s in u], [])) - set([s])
         for s in CELLS}
