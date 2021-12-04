class Board:
    Rows = []

    def __init__(self, size):
        for i in range(0, size):
            new_list = [0 for x in range(0, size)]
            self.Rows.append(new_list)


joc = Board(7)
print(joc.Rows)