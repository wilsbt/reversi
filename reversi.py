# Reversi

import copy


def new_board():
    """
    resets the board to original state
    :return: none
    """
    global board1
    board1 = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]


def print_board(board):
    """
    converts the board from matrix form to graphical from and prints it in console
    :param board: current board
    :return: none
    """
    for i in range(len(board)):
        print(i + 1, "|", end='')
        for j in range(len(board)):
            if board[i][j] == 0:
                print("_|", end='')
            elif board[i][j] == 2:
                print('W|', end='')
            elif board[i][j] == 1:
                print('B|', end='')
            else:
                print("print error")
        print('\n')
    print("  |a|b|c|d|e|f|g|h|")


def score_board(board):
    """
    calulate scores of back and white by finding the sum respectively
    :param board: board
    :return: score for black, score for white
    """
    B = 0
    W = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[j][i] == 2:
                W = W + 1
            elif board[j][i] == 1:
                B = B + 1
    return B, W


def enclosing(board, player, pos, dr):
    """
    decide whether a position and direction enclose opponents tile(s)
    :param board: a board in matrix form
    :param player: black(1) or white(2)
    :param pos: position in (r, c) form where r is the list and c is the sublist
    :param dr: direction up down, left, right, diagonal expressed (dr, dc) where dr is is up (1),
    down (-1) and dc is right(1), left (-1). e.g. (0,1) is right, (-1,-1) is down left.
    :return: True if it does enclose, false if not
    """
    # test whether player is placing tile on empty square:
    if board[pos[0]][pos[1]] != 0:
        return False

    # test whether player can move in selected direction without leaving board:
    elif (pos[0] + dr[0]) > 7 or (pos[0] + dr[0]) < 0:
        return False
    elif (pos[1] + dr[1]) > 7 or (pos[1] + dr[1]) < 0:
        return False

    # test if neighbouring tile is opposing colour:
    elif board[pos[0] + dr[0]][pos[1] + dr[1]] != player:
        # test next tile in direction dr:
        for i in range(1, len(board)):
            if (pos[0] + i * dr[0]) > 7 or (pos[0] + i * dr[0]) < 0:
                # the opposing tiles go to the edge of the board
                return False
            elif (pos[1] + i * dr[1]) > 7 or (pos[1] + i * dr[1]) < 0:
                # the opposing tiles go to the edge of the board
                return False
            elif board[pos[0] + i * dr[0]][pos[1] + i * dr[1]] == 0:
                # their is no tile of the same colour to enclose the opponents tiles
                return False
            elif board[pos[0] + i * dr[0]][pos[1] + i * dr[1]] != player:
                # tile is opponents tile, check next tile
                continue
            elif board[pos[0] + i * dr[0]][pos[1] + i * dr[1]] == player:
                # at least one opponents tile has been enclosed
                return True

    else:
        return False
        # precaution


def valid_moves(board, player):
    """
    find all valid moves
    :param board:
    :param player:
    :return: list of possible moves
    """
    moves = []

    # test all possible positions in all possible directions:
    for i in range(len(board)):
        for j in range(len(board)):
            # down
            if enclosing(board, player, (i, j), (1, 0)):
                moves.append([i, j])
            # down, right
            if enclosing(board, player, (i, j), (1, 1)):
                moves.append([i, j])
            # right
            if enclosing(board, player, (i, j), (0, 1)):
                moves.append([i, j])
            # up
            if enclosing(board, player, (i, j), (-1, 0)):
                moves.append([i, j])
            # up left
            if enclosing(board, player, (i, j), (-1, -1)):
                moves.append([i, j])
            # left
            if enclosing(board, player, (i, j), (0, -1)):
                moves.append([i, j])
            # up right
            if enclosing(board, player, (i, j), (-1, 1)):
                moves.append([i, j])
            # down left
            if enclosing(board, player, (i, j), (1, -1)):
                moves.append([i, j])
    return moves


def flip_tiles(board, player, pos):
    """
    flip all eclosing tiles from certain move
    :param player:
    :param board:
    :param pos: position of tile (move)
    :return: none
    """
    dr = []
    # work out direction(s) that enclose:
    for i in range(-1, 2):
        for j in range(-1, 2):
            if enclosing(board, player, pos, (i, j)):
                dr.append([i, j])
    print(dr)
    # enclose/ flip tiles:
    for d in range(len(dr)):
        for i in range(1, len(board)):
            if (pos[0] + i * dr[d][0]) > 7 or (pos[0] + i * dr[d][0]) < 0:
                # if goes off board (precaution)
                break
            elif (pos[1] + i * dr[d][1]) > 7 or (pos[1] + i * dr[d][1]) < 0:
                # if goes off board (precaution)
                break
            if board[pos[0] + i * dr[d][0]][pos[1] + i * dr[d][1]] == 0:
                # if a zero is encountered (precaution)
                break
            if board[pos[0] + i * dr[d][0]][pos[1] + i * dr[d][1]] != player:
                # if the stone is not the players stone
                board[pos[0] + i * dr[d][0]][pos[1] + i * dr[d][1]] = player
                # flip stone
                continue
                # iterate alon in the same direction
            if board[pos[0] + i * dr[d][0]][pos[1] + i * dr[d][1]] == player:
                # the other enclosing tile reached, so next direction can be tried
                break


def player_turn(board, player):
    """
    check whether opposing player can move, if not, check if player can move, if not no moves
    :param board:
    :param player:
    :return: whose turn it is (player/opponent/false: no available turns)
    """
    opponent = 0
    players = (1, 2)
    if player == players[0]:
        opponent = players[1]
    if player == players[1]:
        opponent = players[0]
    if opponent == 0:
        return False
    if len(valid_moves(board, opponent)) > 0:
        return opponent
    if len(valid_moves(board, opponent)) == 0:
        if len(valid_moves(board, player)) > 0:
            return player
    if len(valid_moves(board, opponent)) == 0:
        if len(valid_moves(board, player)) == 0:
            return 0


def next_state(board, player, pos):
    """
    checks if move is valid, flips tiles, puts tile down on chosen position, find who next player is
    :param board:
    :param player:
    :param pos:
    :return: none if move is invalid, so as not to be confused with false output of player_turn,
    players turn, or false if no player can move
    """
    # check if move is valid
    if [pos[0], pos[1]] not in valid_moves(board, player):
        # precaution
        return None
    # set enclosing tiles to players tiles
    flip_tiles(board, player, pos)
    # set pos to players tiles
    board[pos[0]][pos[1]] = player
    # print new board
    # print_board(board)
    # next players turn
    return player_turn(board, player)


def position(string):
    """
    takes position as string e.g. a3 and converts it to (row, column) format
    :param string: string to convert
    :return: position in row column format
    """
    letters = 'abcdefgh'
    numbers = '12345678'
    letter = list(string)[0]
    number = list(string)[1]
    if len(string) > 2:
        # the input can only be 2 characters long
        return None
    elif letter not in letters:
        # the letter must be in letter
        return None
    elif number not in numbers:
        # the number must be in numbers
        return None
    c = letters.index(letter)
    r = int(number) - 1

    return r, c


def reverse_position(r, c):
    """
    turns position int0 human readable move form
    :param r: row
    :param c: column
    :return:
    """
    letters = 'abcdefgh'
    numbers = '12345678'
    letter = letters[c]
    number = numbers[r]
    return letter, number


def run_two_players():
    """

    :param board:
    :return:
    """
    new_board()
    print_board(board1)
    player = 1
    while True:
        if player == 0:
            # game cant have player 0, only 1 and 2
            break
        # user type in their move:
        move = str(input("player {} where would you like to move [e.g. 'a3']? ('q' to quit) ".format(player)))
        # check if input is correct lenght
        if len(move) > 2:
            print_board(board1)
            print('invalid move')
        # check if user wants to quit:
        elif move == 'q':
            break
        # check if move is valid:
        elif [position(move)[0], position(move)[1]] in valid_moves(board1, player):
            # play move
            player = next_state(board1, player, position(move))
            print_board(board1)
        else:
            # if move was not valid:
            print_board(board1)
            print('invalid move')
    print("thanks for playing")
    print("SCORES:")
    print("black:", score_board(board1)[0], "\nwhite:", score_board(board1)[1])


def max_index(lst):
    """
    find index of max value of list
    :param lst:
    :return: index for max value
    """
    mx = lst[0][0]
    mi = 0
    for i in range(len(lst)):
        if lst[i][0] > mx:
            mx = lst[i][0]
            mi = i
    return mi


def selection_sort(lst):
    """
    sort from index i onwards
    :param lst:
    :return: lst in order from highest to lowest
    """
    for i in range(len(lst)):
        j = max_index(lst[i:]) + i
        lst[i], lst[j] = lst[j], lst[i]


def run_single_players():
    """

    :param board:
    :return:
    """
    new_board()
    print_board(board1)
    player = 1
    while True:
        if player == 0:
            break
        if player == 1:
            move = str(input("Where would you like to move [e.g. 'a3']? ('q' to quit) ".format(player)))
            print(valid_moves(board1, player))
            if len(move) > 2:
                print_board(board1)
                print('invalid move')
            elif move == 'q':
                break
            elif [position(move)[0], position(move)[1]] in valid_moves(board1, player):
                player = next_state(board1, player, position(move))
                print_board(board1)
            else:
                print_board(board1)
                print('invalid move')
        if player == 2:
            # find points for all moves by simulation:
            scores = []
            # create copy of board to test moves on:
            tmp = copy.deepcopy(board1)
            moves = valid_moves(tmp, player)

            for m in range(len(moves)):
                next_state(tmp, player, (moves[m][0], moves[m][1]))
                score = score_board(tmp)[1]
                scores.append((score, moves[m]))
                tmp = copy.deepcopy(board1)
            # sort from best move to worst move:
            selection_sort(scores)
            # play best move:
            player = next_state(board1, player, (scores[0][1][0], scores[0][1][1]))
            print_board(board1)
            move = reverse_position(scores[0][1][0], scores[0][1][1])
            # print the computers move so the player knows where the computer moved
            print("computer: ", move[0], move[1], sep='')

    print("thanks for playing")
    print("SCORES:")
    print("black:", score_board(board1)[0], "\nwhite:", score_board(board1)[1])


def menu():
    """
    menu for game, choose to play single player, multi player or quit
    :return: none
    """
    while True:
        mode = input("type 1 for single player or 2 for multiplayer [q to quit]: ")
        if mode == "q":
            print("goodbye")
            break

        if mode == "1":
            print("single player")
            run_single_players()
        if mode == "2":
            print("multi-player")
            run_two_players()


menu()

"""
------ bugs (all solved):
the 2 player game mostly functions as it should however there are some bugs
bugs:
potential moves were invalid:
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) f7
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|_|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) f7
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|_|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) f6
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|_|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) f5
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|_|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) c6
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|_|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) c3
[[1, 0]]
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|W|B|_|W|_|_|

4 |_|_|W|B|B|B|_|_|

5 |_|_|W|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) f7
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|W|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|B|B|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
player 2 where would you like to move [e.g. 'a3']? ('q' to quit) c6
1 |_|_|_|B|_|_|_|_|

2 |_|_|_|B|_|_|_|_|

3 |_|B|W|B|_|W|_|_|

4 |_|_|B|B|B|B|_|_|

5 |_|B|B|B|B|B|_|_|

6 |_|_|_|B|_|B|_|_|

7 |_|_|_|_|_|_|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
"""

"""
[6, 5] in valid_moves(board1, player)
valid moves is wrong.


get rid of elif and replace with if
"""

"""
new bug {in single player}:
Where would you like to move [e.g. 'a3']? ('q' to quit) f8
[[1, 2], [1, 5], [2, 2], [2, 2], [2, 4], [3, 1], [6, 2], [6, 4]]
[[1, 2], [1, 5], [2, 2], [2, 2], [2, 4], [3, 1], [6, 2], [6, 4]]
[[1, 2], [1, 5], [2, 2], [2, 2], [2, 4], [3, 1], [6, 2], [6, 4]]
1 |_|_|_|W|_|_|_|_|

2 |_|_|_|W|_|_|W|_|

3 |_|W|_|W|_|W|_|_|

4 |_|_|W|W|W|B|_|_|

5 |_|_|B|W|W|B|_|_|

6 |_|_|_|W|_|B|_|_|

7 |_|_|_|_|_|B|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
invalid move
"""

"""
1 |_|_|_|W|_|_|_|_|

2 |_|_|_|W|_|_|W|_|

3 |W|W|_|W|_|W|_|_|

4 |_|W|B|B|B|B|_|_|

5 |_|_|W|W|W|B|_|_|

6 |_|_|_|W|_|B|_|_|

7 |_|_|_|_|_|B|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
Where would you like to move [e.g. 'a3']? ('q' to quit) h1
[[0, 7], [1, 0], [1, 2], [1, 4], [1, 5], [3, 0], [4, 1], [5, 1], [5, 2], [5, 2], [5, 4], [5, 4], [6, 2], [6, 3]]
1 |_|_|_|W|_|_|_|B|

2 |_|_|_|W|_|_|W|_|

3 |W|W|_|W|_|W|_|_|

4 |_|W|B|B|B|B|_|_|

5 |_|_|W|W|W|B|_|_|

6 |_|_|_|W|_|B|_|_|

7 |_|_|_|_|_|B|_|_|

8 |_|_|_|_|_|_|_|_|

  |a|b|c|d|e|f|g|h|
1 |_|_|_|W|_|_|_|B|

2 |_|_|_|W|_|_|W|_|

3 |W|W|W|W|_|W|_|_|

4 |_|W|W|W|B|B|_|_|

5 |_|_|W|W|W|B|_|_|

6 |_|_|_|W|_|B|_|_|

7 |_|_|_|_|_|B|_|_|

8 |_|_|_|_|_|_|_|_|
"""
