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
            if liberty not in liberties:
                liberties.append(liberty)
    return liberties


def capture_pieces(game, previous_move):
    game.previousCaptureCount = 0
    for i in range(0, len(game.board.Rows)):
        for j in range(0, len(game.board.Rows[0])):
            if game.board.Rows[i][j] != -1:
                group = get_group_positions(game,game.board.Rows[i][j],[i,j])
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
    # for neighbour in get_neighbour_group(game,get_group_positions(game,(game.playerTurn+1)%2,previous_move)):
    #     group = get_group_positions(game, game.playerTurn, neighbour)
    #     if not get_liberties_pos(game, group):
    #         for elem in group:
    #             game.board.Rows[elem[0]][elem[1]] = -1
    #             if game.board.Rows[elem[0]][elem[1]] == 1:
    #                 print("WhiteScored at " + str(elem[0]) + " " + str(elem[1]))
    #                 game.scoreWhite += 1
    #                 game.previousCaptureCount += 1
    #             else:
    #                 print("BlackScored at " + str(elem[0]) + " " + str(elem[1]))
    #                 game.scoreBlack += 1
    #                 game.previousCaptureCount +=1


def validate_move(game, position):
    if game.board.Rows[position[0]][position[1]] != -1:
        return False
    previous = game.board.Rows[position[0]][position[1]]
    game.board.Rows[position[0]][position[1]] = game.playerTurn
    total_positions = get_group_positions(game, game.playerTurn, position)
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
    if validate_move(game, position):
        game.board.Rows[position[0]][position[1]] = game.playerTurn
        game.playerTurn = (game.playerTurn + 1) % 2
        capture_pieces(game, position)
        game.previousMove = position
        game.skippedRecently = 0
        return True
    return False


def pass_turn(game):
    game.playerTurn = (game.playerTurn + 1) % 2
    game.skippedRecently += 1


def available_positions(game):
    moves = []
    for i in range(0, len(game.board.Rows)):
        for j in range(0, len(game.board.Rows[0])):
            if validate_move(game, [i, j]):
                moves.append([i, j])

    return moves


def random_ai(game,tries):
    # failed = True
    # iterations = 0
    # while failed:
    #     random_pos_x = random.randint(0, len(game.board.Rows) - 1)
    #     random_pos_y = random.randint(0, len(game.board.Rows) - 1)
    #     if move_piece(game, [random_pos_x, random_pos_y]):
    #         print("Moved: " + str((game.playerTurn+1)%2) + " to " + str(random_pos_x) + " " + str(random_pos_y))
    #         failed = False
    #     iterations += 1
    #     if iterations > tries:
    #         pass_turn(game)
    #         break
    available = available_positions(game)
    if len(available) > 0:
        move = random.choice(available)
        move_piece(game, move)
        print("Moved: " + str((game.playerTurn + 1) % 2) + " to " + str(move[0]) + " " + str(move[1]))
    else:
        pass_turn(game)
        print("Skipped")


def isFinal(game):
    if game.skippedRecently >= 2:
        return True
    return False

def compute_scores(game):
    whitePieces = 0
    blackPieces = 0
    for i in range(0, len(game.board.Rows)):
        for j in range(0, len(game.board.Rows[0])):
            if game.board.Rows[i][j] == 0:
                whitePieces +=1
            if game.board.Rows[i][j] == 1:
                blackPieces +=1
    return [blackPieces + game.scoreBlack , whitePieces + game.scoreWhite]


joc = Game(9)


while not isFinal(joc):
    # failed = True
    # while failed:
    #     pos1 = int(input("00: "))
    #     pos2 = int(input("11: "))
    #     if pos1 == 69:
    #         running = False
    #         pass_turn(joc)
    #         break
    #     if move_piece(joc, [pos1, pos2]):
    #         failed = False
    #         for row in joc.board.Rows:
    #             print(row)
    random_ai(joc,300)
    print("AI moved -------")
    for row in joc.board.Rows:
        print(row)
    print("AI moved -------")
    random_ai(joc,300)
    for row in joc.board.Rows:
        print(row)



print("blackScore: " + str(compute_scores(joc)[0]))
print("whiteScore: " + str(compute_scores(joc)[1]))


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
