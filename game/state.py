"""Game state."""
from itertools import product


class Spaceship:
    """
    Spaceship state.

    Use it to disable stars that are behind spaceship or detect collisions.
    """
    def __init__(self, row: int, column: int, row_size: int, col_size: int):
        """
        :param row: Start row.
        :param column: Start column.
        :param max_rows: Total rows occupied.
        :param max_cols: Total columns occupied.
        """
        self.row = row
        self.col = column
        self.rows = row_size
        self.cols = col_size
        self.occupied_positions = set()

    def is_occupied(self, row, column):
        return (row, column) in self.occupied_positions

    def __setattr__(self, key, value):
        """Update occupied positions on every position update."""
        try:
            # use try except instead of hasattr as
            # AttributeError will be risen only at initialization
            if key in ('row', 'col', 'rows', 'cols'):
                old_row, old_col = self.row, self.col
                old_rows, old_cols = self.rows, self.cols
                new_row = (key == 'row' and value) or old_row
                new_col = (key == 'col' and value) or old_col
                new_rows = (key == 'rows' and value) or old_rows
                new_cols = (key == 'cols' and value) or old_cols
                self.occupied_positions = set(product(
                    range(new_row, new_row+new_rows+1),
                    range(new_col, new_col+new_cols+1))
                )
                self.__dict__['row'] = new_row
                self.__dict__['col'] = new_col
                self.__dict__['cols'] = new_cols
                self.__dict__['rows'] = new_rows
            else:
                super().__setattr__(key, value)
        except AttributeError:
            # __init__ call
            super().__setattr__(key, value)


