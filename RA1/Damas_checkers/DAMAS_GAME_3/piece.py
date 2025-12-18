class Piece:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color[0].upper() 
