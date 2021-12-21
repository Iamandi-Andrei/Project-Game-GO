class Board:
    Rows = []

    def __init__(self, size):
        self.Rows = []
        for i in range(0, size):
            new_list = [-1 for x in range(0, size)]
            self.Rows.append(new_list)


class Game:
    board = []
    playerTurn = 0
    scoreWhite = 0
    scoreBlack = 0

    def __init__(self, size):
        self.scoreWhite = 0
        self.scoreBlack = 0
        self.board = Board(size)
        self.playerTurn = 1


def compare_colors(game, color, position):
    if game.board.Rows[position[0]][position[1]] == color:
        return True
    return False


def get_neighbours(game, color, position):
    """
    :param game:
    :param color:
    :param position:
    :return: all the neighbours of "position" of the given "color"
    """
    positions = []
    if position[0] > 0:
        if compare_colors(game, color, [position[0] - 1, position[1]]):
            positions.append([position[0] - 1, position[1]])
    if position[0] < len(game.board.Rows) - 1:
        if compare_colors(game, color, [position[0] + 1, position[1]]):
            positions.append([position[0] + 1, position[1]])
    if position[1] > 0:
        if compare_colors(game, color, [position[0], position[1] - 1]):
            positions.append([position[0], position[1] - 1])
    if position[1] < len(game.board.Rows[0]) - 1:
        if compare_colors(game, color, [position[0], position[1] + 1]):
            positions.append([position[0], position[1] + 1])
    return positions


def get_neighbour_group(game, positions):
    """
    :param game:
    :param positions:
    :return: all the coordinates of the enemy pieces surrounding the given piece group (positions)
    """
    total_positions = []
    color = (game.board.Rows[positions[0][0]][positions[0][1]] + 1) % 2
    for pos in positions:
        for vecin in get_neighbours(game, color, pos):
            if vecin not in total_positions:
                total_positions.append(vecin)
    return total_positions


def get_group_positions(game, color, position):
    """
    :param game:
    :param color:
    :param position:
    :return:
    """
    positions = [position]
    total_positions = [position]
    while positions:
        current_pos = positions[0]
        positions.remove(current_pos)
        for vecin in get_neighbours(game, color, current_pos):
            if vecin not in total_positions:
                positions.append(vecin)
                total_positions.append(vecin)
    return total_positions


def get_liberties_pos(game, positions):
    liberties = []
    for pos in positions:
        for liberty in get_neighbours(game, -1, pos):
            liberties.append(liberty)
    return liberties


def capture_pieces(game, previous_move):
    for neighbour in get_neighbours(game, game.playerTurn, previous_move):
        group = get_group_positions(game, game.playerTurn, neighbour)
        if not get_liberties_pos(game, group):
            for elem in group:
                game.board.Rows[elem[0]][elem[1]] = -1
                if game.playerTurn == 1:
                    game.scoreWhite += 1
                else:
                    game.scoreBlack += 1


def validate_move(game, position):
    if game.board.Rows[position[0]][position[1]] != -1:
        return False
    total_positions = get_group_positions(game, game.playerTurn, position)

    previous = game.board.Rows[position[0]][position[1]]
    game.board.Rows[position[0]][position[1]] = game.playerTurn

    if not get_liberties_pos(game, total_positions):
        neighbours = get_neighbour_group(game, total_positions)
        if get_liberties_pos(game, neighbours):
            game.board.Rows[position[0]][position[1]] = previous
            return False
        return True
    return True


def move_piece(game, position):
    if validate_move(game, position):
        game.board.Rows[position[0]][position[1]] = game.playerTurn
        game.playerTurn = (game.playerTurn + 1) % 2
        capture_pieces(game, position)


def pass_turn(game):
    game.playerTurn = (game.playerTurn + 1) % 2


joc = Game(12)
while True:
    pos1 = int(input("00: "))
    pos2 = int(input("11: "))
    move_piece(joc, [pos1, pos2])
    for row in joc.board.Rows:
        print(row)

# move_piece(joc, [0, 0])
# pass_turn(joc)
# move_piece(joc, [1, 1])
# pass_turn(joc)
# move_piece(joc, [1, 2])
# pass_turn(joc)
# move_piece(joc, [0, 3])
# move_piece(joc, [0, 1])
# pass_turn(joc)
# move_piece(joc, [0, 2])
# move_piece(joc, [0, 0])
# move_piece(joc, [0, 1])
# move_piece(joc, [1, 1])
# pass_turn(joc)
# move_piece(joc,[1,3])
# pass_turn(joc)
# move_piece(joc,[0,2])
# pass_turn(joc)
# move_piece(joc,[2,2])
# move_piece(joc,[1,2])
