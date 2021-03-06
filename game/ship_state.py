# -*- coding: utf-8 -*-

"""Class to keep track of spaceship position."""


class Spaceship(object):
    """
    Spaceship state.

    Use it to disable stars that are behind spaceship or detect collisions.
    """

    def __init__(self, row: int, column: int, rows: int, cols: int, sizes: tuple):  # noqa: Z211
        """
        New ship of given size and at given position.

        :param row: Start row.
        :param column: Start column.
        :param sizes: (start, size) tuple for each row as by utils.get_frame_shape.
        """
        self.row = row
        self.col = column
        self.rows = rows
        self.cols = cols
        self.sizes = sizes
        self.occupied_positions = set()

    def __setattr__(self, key, value):  # noqa: Z110, Z210
        """Update occupied positions on every position update or sizes update."""
        try:
            # use try except instead of hasattr as
            # AttributeError will be risen only at initialization
            if key in ('row', 'col', 'sizes'):
                old_row, old_col = self.row, self.col
                new_row = (key == 'row' and value) or old_row
                new_col = (key == 'col' and value) or old_col
                new_sizes = (key == 'sizes' and value) or None
                new_positions = set()
                for n_line, line in enumerate(self.sizes):
                    # add positions occupied by n-th line
                    [new_positions.add((new_row + n_line, new_col + shift))
                     for shift in range(1, line[1] + 1)]  # noqa: Z319
                self.occupied_positions = new_positions
                self.__dict__['row'] = new_row
                self.__dict__['col'] = new_col
                if new_sizes:
                    self.__dict__['sizes'] = new_sizes
            else:
                super().__setattr__(key, value)
        except AttributeError:
            # __init__ call
            super().__setattr__(key, value)

    def __str__(self):
        """Position of spaceship."""
        return 'Spaceship at row={0}, col={1}'.format(self.row, self.col)
