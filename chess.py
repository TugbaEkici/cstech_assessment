import sys

class board:
    def __init__(self, pieces):
        self.pieces = pieces

    def add_piece(self, piece):
        self.pieces.append(piece)

    def get_piece_on_coordinate(self, x, y):
        """
        :param x: x value of coordinate
        :param y: y value of coordinate
        :return: piece on coordinate if no piece exists on this coordinate returns False
        """

        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return False

    def get_black_bishop_coordinates(self):
        """
        :return: list which includes black bishop coordinates as tuple
        """

        bishop_coordinates = []

        for piece in self.pieces:
            if piece.is_black and piece.acronym == "f":
                bishop_coordinates.append((piece.x, piece.y))
        return bishop_coordinates

    def get_white_bishop_coordinates(self):
        """
        :return: list which includes white bishop coordinates as tuple
        """

        bishop_coordinates = []

        for piece in self.pieces:
            if not piece.is_black and piece.acronym == "f":
                bishop_coordinates.append((piece.x, piece.y))
        return bishop_coordinates

    def is_any_piece_between(self, c1, c2):
        """
        Since bishop cannot jump over other pieces to attack, we must sure whether any
        piece exists between bishop and piece which is attacked by bishop
        :param c1: coordinate of piece as tuple
        :param c2: coordinate of bishop as tuple
        :return: True if any other piece exists between them, False otherwise
        """

        slope = (c2[1] - c1[1]) / (c2[0] - c1[0])

        if slope == 1:
            if c2[1] > c1[1]:
                max_y = c2[1]
                for i in range(1, max_y - c1[1]):
                    coordinate = (c1[0] + i, c1[1] + i)
                    if self.get_piece_on_coordinate(coordinate[0], coordinate[1]):
                        return True
            else:
                max_y = c1[1]
                for i in range(1, max_y - c2[1]):
                    coordinate = (c2[0] + i, c2[1] + i)
                    if self.get_piece_on_coordinate(coordinate[0], coordinate[1]):
                        return True
        elif slope == -1:
            if c1[1] > c2[1]:
                max_y = c1[1]
                for i in range(1, max_y - c2[1]):
                    coordinate = (c1[0] + i, c1[1] - i)
                    if self.get_piece_on_coordinate(coordinate[0], coordinate[1]):
                        return True
            else:
                max_y = c2[1]
                for i in range(1, max_y - c1[1]):
                    coordinate = (c2[0] + i, c2[1] - i)
                    if self.get_piece_on_coordinate(coordinate[0], coordinate[1]):
                        return True
        return False


    def calculate_score(self):
        """
        :return: white's score and black's score
        """
        white_score = 139.0
        black_score = 139.0

        white_bishops = self.get_white_bishop_coordinates()
        black_bishops = self.get_black_bishop_coordinates()

        for piece in self.pieces:
            if piece.is_black:
                if piece.acronym != "a":
                    attack_positions = piece.knight_attack_positions()
                    for pos in attack_positions:
                        i = self.get_piece_on_coordinate(pos[0], pos[1])
                        if i and i.acronym == "a" and not i.is_black:
                            black_score -= (piece.score / 2)
                if piece.acronym != "f":
                    bishop_coordinate = piece.is_aligned_with_bishop(white_bishops)

                    if bishop_coordinate:

                        if not self.is_any_piece_between((piece.x, piece.y), bishop_coordinate):
                            black_score -= (piece.score / 2)
            else:
                if piece.acronym != "a":
                    attack_positions = piece.knight_attack_positions()
                    for pos in attack_positions:
                        i = self.get_piece_on_coordinate(pos[0], pos[1])
                        if i and i.acronym == "a" and i.is_black:
                            white_score -= (piece.score / 2)
                if piece.acronym != "f":
                    bishop_coordinate = piece.is_aligned_with_bishop(black_bishops)
                    if bishop_coordinate:
                        if not self.is_any_piece_between((piece.x, piece.y), bishop_coordinate):
                            white_score -= (piece.score / 2)

        return white_score, black_score


class piece:
    """
    All pieces have a acronym, coordinate(x,y) and are belong to white or black.
    """
    is_black = None
    acronym = ""
    x = 0
    y = 0

    def __init__(self, acr, x, y, is_black):
        self.acronym = acr
        self.x = x
        self.y = y
        self.is_black = is_black

    def knight_attack_positions(self):
        """
        :return: list of coordinate which are attackable positions by knight according to piece coordinate
        """
        x = self.x
        y = self.y
        positions = [(x - 1, y - 2), (x - 2, y - 1),
                     (x + 1, y - 2), (x + 2, y - 1),
                     (x - 2, y + 1), (x - 1, y + 2),
                     (x + 1, y + 2), (x + 2, y + 1)]

        for (i, j) in positions:
            if i < 1 or i > 8 or j < 1 or j > 8:
                positions = list(filter(lambda x: x[0] != i or x[1] != j, positions))

        return positions

    def is_aligned_with_bishop(self, bishop_coordinates):
        """
        Since bishop can move crosswise only, slope of piece to bishop must be 1 or -1 to be aligned.
        :param bishop_coordinates: list of coordinate tuples
        :return: True if they are aligned, False otherwise
        """
        bishop_coordinate1 = bishop_coordinates[0]
        bishop_coordinate2 = bishop_coordinates[1]

        if (bishop_coordinate1[0] - self.x) == 0:
            return False
        if (bishop_coordinate2[0] - self.x) == 0:
            return False

        slope1 = (bishop_coordinate1[1] - self.y) / (bishop_coordinate1[0] - self.x)
        slope2 = (bishop_coordinate2[1] - self.y) / (bishop_coordinate2[0] - self.x)

        if slope1 == 1 or slope1 == -1:
            return bishop_coordinate1
        elif slope2 == 1 or slope2 == -1:
            return bishop_coordinate2
        else:
            return False


class p(piece):
    """
    For "piyon" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 1.0
        super().__init__(acr, x, y, is_black)


class a(piece):
    """
    For "at" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 3.0
        super().__init__(acr, x, y, is_black)


class f(piece):
    """
    For "fil" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 3.0
        super().__init__(acr, x, y, is_black)


class k(piece):
    """
    For "kale" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 5.0
        super().__init__(acr, x, y, is_black)


class v(piece):
    """
    For "vezir" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 9.0
        super().__init__(acr, x, y, is_black)


class s(piece):
    """
    For "şah" piece
    """
    def __init__(self, acr, x, y, is_black):
        self.score = 100.0
        super().__init__(acr, x, y, is_black)


def main():
    """
    reads input file
    create board and then adds all pieces to board.
    :param input_path: string of input file's name
    :return: -
    """
    input_path = sys.argv[-1]
    pieces = []
    global board
    board = board(pieces)
    row_number = 8
    with open(input_path, 'r') as data:
        rows = data.readlines()
        for row in rows:
            row = row.split()
            col_number = 1
            for item in row:
                if item == "xx":
                    pass
                else:
                    if item == "ks":
                        new_piece = k("k", col_number, row_number, True)
                    elif item == "as":
                        new_piece = a("a", col_number, row_number, True)
                    elif item == "fs":
                        new_piece = f("f", col_number, row_number, True)
                    elif item == "vs":
                        new_piece = v("v", col_number, row_number, True)
                    elif item == "ss":
                        new_piece = s("s", col_number, row_number, True)
                    elif item == "ps":
                        new_piece = p("p", col_number, row_number, True)
                    elif item == "kb":
                        new_piece = k("k", col_number, row_number, False)
                    elif item == "ab":
                        new_piece = a("a", col_number, row_number, False)
                    elif item == "fb":
                        new_piece = f("f", col_number, row_number, False)
                    elif item == "vb":
                        new_piece = v("v", col_number, row_number, False)
                    elif item == "sb":
                        new_piece = s("s", col_number, row_number, False)
                    elif item == "pb":
                        new_piece = p("p", col_number, row_number, False)

                    board.add_piece(new_piece)
                col_number = col_number + 1
            row_number = row_number - 1

    scores = board.calculate_score()
    white_score = scores[0]
    black_score = scores[1]

    print("White's score is", white_score)
    print("Black's score is", black_score)
    return

if __name__ == '__main__':
    main()
