"""
Tic Tac Toe Player
"""

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    if board == initial_state():
        return X
    
    xs = 0
    os = 0
    for row in board:
        xs += row.count(X)
        os += row.count(O)
    if xs > os:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i, _ in enumerate(board):
        for j, col in enumerate(board[i]):
            if col == EMPTY:
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    plyr = player(board)
    # validate action
    row, col = action
    if row not in [0,1,2] or col not in [0,1,2] or board[row][col] != EMPTY:
        raise Exception('not valid move')
    
    new_board = deepcopy(board)
    new_board[row][col] = plyr
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    size = len(board)
    while not winner:
        # check straights
        for row in board:
            if row == [X] * 3:
                winner = X
                break
            elif row == [O] * 3:
                winner = O
                break
        for col in zip(*board):
            if list(col) == [X] * 3:
                winner = X
                break
            elif list(col) == [O] * 3:
                winner = O
                break
             
        # check diagonals 
        right_diag = []
        left_diag = []
        for i in range(size):
            for j in range(size):
                if i == j and board[i][j] != EMPTY:
                    right_diag.append(board[i][j])             
                if (i == 0 and j == size - 1) and board[i][j] != EMPTY:
                    left_diag.append(board[i][j])
                if (i == j == 1) and board[i][j] != EMPTY:
                    left_diag.append(board[i][j])
                if (i == size - 1 and j == 0) and board[i][j] != EMPTY:
                    left_diag.append(board[i][j])
        if right_diag == [X] * 3:
            winner = X
        elif right_diag == [O] * 3:
            winner = O

        if left_diag == [X] * 3:
            winner = X
        elif left_diag == [O] * 3:
            winner = O
        

        break

    # no winner
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for row in board:
        if EMPTY in row:
            return False
    return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board) 
    if w == X:
        return 1
    elif w == O:
        return -1 
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def algo(board):
        scores = {}
        plyr = player(board)
        actns = actions(board)
        
        for action in actns:
            new_board = result(board, action)
            
            if terminal(new_board):
                scores[utility(new_board)] = action
            else:
                score, _ = algo(new_board)
                scores[score] = action
        
        if plyr == X:
            return max(scores.keys()), scores[max(scores.keys())]
        else:
            return min(scores.keys()), scores[min(scores.keys())]
    
    _, action = algo(board)
    return action
