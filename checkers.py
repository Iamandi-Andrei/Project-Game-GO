import random


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
    previousMove = []
    skippedRecently = 0
    previousCaptureCount = 0

    def __init__(self, size):
        self.scoreWhite = 0
        self.scoreBlack = 0
        self.board = Board(size)
        self.playerTurn = 1
        self.previousMove = []
        self.skippedRecently = 0
        self.previousCaptureCount = 0


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


def get_group_positions(game, position):
    """
    :param game:
    :param position:
    :return: the list of all the positions connected to the given position that have the same color
    """
    color = game.board.Rows[position[0]][position[1]]
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
    """
    :param game:
    :param positions:
    :return: all the positions marked -1 that are around the given position's group
    """
    liberties = []
    total_positions = []
    for pos in positions:
        for elem in get_group_positions(game, pos):
            if elem not in total_positions:
                total_positions.append(elem)
    for pos in total_positions:
        for liberty in get_neighbours(game, -1, pos):
            if liberty not in liberties:
                liberties.append(liberty)
    return liberties


def capture_pieces(game, previous_move):
    """
    Called after ending a turn.
    :param game:
    :param previous_move:
    :return:  Based on the previous move, it captures the pieces that have no remaining liberties
    """
    game.previousCaptureCount = 0
    for neighbour in get_neighbour_group(game, get_group_positions(game, previous_move)):
        group = get_group_positions(game, neighbour)
        if not get_liberties_pos(game, group):
            for elem in group:
                if game.board.Rows[elem[0]][elem[1]] == 1:
                    print("WhiteScored at " + str(elem[0]) + " " + str(elem[1]))
                    game.scoreWhite += 1
                    game.previousCaptureCount += 1
                else:
                    print("BlackScored at " + str(elem[0]) + " " + str(elem[1]))
                    game.scoreBlack += 1
                    game.previousCaptureCount += 1
                game.board.Rows[elem[0]][elem[1]] = -1


def validate_move(game, position):
    """
    Three main rules to check if the move is valid.
    1) Cant place pieces on an already occupied spot
    2) You can't capture the piece that was placed right beore your turn if that piece only captured one piece ( Simple 2-turn loop prevention)
    3) You can't "suicide" unless by doing so, you capture enemy pieces and the "suicide" is undone
    :param game:
    :param position:
    :return: True or False if the move is valid based on the rules above
    """
    if game.board.Rows[position[0]][position[1]] != -1:
        return False
    previous = game.board.Rows[position[0]][position[1]]
    game.board.Rows[position[0]][position[1]] = game.playerTurn
    total_positions = get_group_positions(game, position)
    if game.previousMove:
        if not get_liberties_pos(game, [game.previousMove]):
            if game.previousCaptureCount == 1:
                game.board.Rows[position[0]][position[1]] = previous
                return False
    if not get_liberties_pos(game, total_positions):
        neighbours = get_neighbour_group(game, total_positions)
        for neighbour in neighbours:
            if not get_liberties_pos(game, [neighbour]):
                game.board.Rows[position[0]][position[1]] = previous
                return True
        game.board.Rows[position[0]][position[1]] = previous
        return False

    game.board.Rows[position[0]][position[1]] = previous
    return True


def move_piece(game, position):
    """
    During a turn, the first step is to validate the move, modify the board and capture enemy pieces afterwards
    :param game:
    :param position:
    :return: True or False if the move was succesfull
    """
    if validate_move(game, position):
        game.board.Rows[position[0]][position[1]] = game.playerTurn
        game.playerTurn = (game.playerTurn + 1) % 2
        capture_pieces(game, position)
        game.previousMove = position
        game.skippedRecently = 0
        return True
    print("Failed to move: " + str(game.playerTurn) + " at " + str(position[0]) + " " + str(position[1]))
    return False


def pass_turn(game):
    """
    Skips a turn. Changes the game.playerTurn variable from 1 to 0 or 0 to 1
    :param game:
    :return:
    """
    game.playerTurn = (game.playerTurn + 1) % 2
    game.skippedRecently += 1
    game.previousMove = []
    game.previousCaptureCount = 0


def random_ai(game, tries):
    """
    The AI generates random positions, tries to make the move and skips if it fails too many items
    :param game:
    :param tries:  Max number of times the AI can fail to find an available move before skipping turn
    :return:
    """
    failed = True
    iterations = 0
    while failed:
        random_pos_x = random.randint(0, len(game.board.Rows) - 1)
        random_pos_y = random.randint(0, len(game.board.Rows) - 1)
        if move_piece(game, [random_pos_x, random_pos_y]):
            print("Moved: " + str((game.playerTurn + 1) % 2) + " to " + str(random_pos_x) + " " + str(random_pos_y))
            failed = False
        iterations += 1
        if iterations > tries:
            pass_turn(game)
            print("Skipped")
            break


def is_final(game):
    if game.skippedRecently >= 2:
        return True
    return False


def get_neighbour_colors(game, position):
    """

    :param game:
    :param position:
    :return: All the colors of the up-down-right-left neighbours of the given position
    """
    colors = []
    if position[0] > 0:
        colors.append(game.board.Rows[position[0] - 1][position[1]])
    if position[0] < len(game.board.Rows) - 1:
        colors.append(game.board.Rows[position[0] + 1][position[1]])
    if position[1] > 0:
        colors.append(game.board.Rows[position[0]][position[1] - 1])
    if position[1] < len(game.board.Rows[0]) - 1:
        colors.append(game.board.Rows[position[0]][position[1] + 1])
    return colors


def group_surrounded_by(game, positions):
    """
    Checks if the pieces group of the given position is fully surrounded by a single color
    :param game:
    :param positions:
    :return: -1 if the group is surrounded by both "1" and "0" pieces and 0 or 1 otherwise
    """
    total_colors = []
    for pos in positions:
        total_colors.extend(get_neighbour_colors(game, pos))
    if 1 in total_colors and 0 in total_colors:
        return -1
    elif 1 in total_colors:
        return 1
    else:
        return 0


def print_game(game):
    for row in game.board.Rows:
        print(row)


def compute_scores(game):
    """
    Computes the total scores of the game.
    Score formula = amount of captured pieces during the whole game + territory owned only by you
    ( groups of unoccupied territory surrounded by only one color)
    :param game:
    :return:
    """
    white_pieces = 0
    black_pieces = 0
    uncaptured_spaces = []
    for i in range(0, len(game.board.Rows)):
        for j in range(0, len(game.board.Rows[0])):
            if game.board.Rows[i][j] == 0:
                white_pieces += 1
            elif game.board.Rows[i][j] == 1:
                black_pieces += 1
            else:
                uncaptured_spaces.append([i, j])
    surrounded_white = 0
    surrounded_black = 0
    while uncaptured_spaces:
        elem = uncaptured_spaces[0]
        group = get_group_positions(game, elem)
        captor = group_surrounded_by(game, group)
        if captor != -1:
            if captor == 0:
                surrounded_white += len(group)
            else:
                surrounded_black += len(group)
        uncaptured_spaces = list(filter(lambda x: x not in group, uncaptured_spaces))
    print("Pieces on board -- pieces captured -- free spaces under control")
    print("Black")
    print(str(black_pieces) + " -- " + str(game.scoreBlack) + " -- " + str(surrounded_black))
    print("White")
    print(str(white_pieces) + " -- " + str(game.scoreWhite) + " -- " + str(surrounded_white))
    return [surrounded_black + game.scoreBlack, surrounded_white + game.scoreWhite]
