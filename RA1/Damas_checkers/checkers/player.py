class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.kings = 0

    def add_piece(self, piece):
        self.pieces.append(piece)
        if piece.king:
            self.kings += 1

    def remove_piece(self, piece):
        self.pieces.remove(piece)
        if piece.king:
            self.kings -= 1

    def get_pieces(self):
        return self.pieces

    def __repr__(self):
        return f"Player {self.color} with {len(self.pieces)} pieces ({self.kings} kings)"