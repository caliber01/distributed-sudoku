import itertools

product = lambda a, b: list(''.join(i) for i in itertools.product(a, b))

rows = 'ABCDEFGHI'
digits = '123456789'
cols = digits
squares = product(rows, digits)
unitlist = ([product(row, digits) for row in rows] +
            [product(rows, col) for col in digits] +
            [product(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']])

units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - {s})
             for s in squares)


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = {s: digits for s in squares}
    for s, d in grid_values(grid).items():
        values[s] = d
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def display(values):
    "Display these values as a 2-D grid."
    print(values)
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print
