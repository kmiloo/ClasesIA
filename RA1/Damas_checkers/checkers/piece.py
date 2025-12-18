class Piece:
    def __init__(self, color, row, col):
        self.color = color  # 'white' or 'black'
        self.row = row
        self.col = col
        self.king = False
        self.direction = 1 if color == 'black' else -1  # black moves down, white moves up

    def make_king(self):
        self.king = True

    def __repr__(self):
        if self.color == 'white':
            return 'W' if not self.king else 'WK'
        else:
            return 'B' if not self.king else 'BK'