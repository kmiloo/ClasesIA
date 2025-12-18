class Move:
    def __init__(self, start_row, start_col, end_row, end_col, captured_pieces=None):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.captured_pieces = captured_pieces or []

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.start_row == other.start_row and
                self.start_col == other.start_col and
                self.end_row == other.end_row and
                self.end_col == other.end_col)

    def __repr__(self):
        return f"Move from ({self.start_row}, {self.start_col}) to ({self.end_row}, {self.end_col})"