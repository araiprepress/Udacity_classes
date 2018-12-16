#===================Coding: Building a Game Class============
xlim, ylim = 3, 2  # board dimension constants

class GameState:
    def __init__(self):
        self._board = [[0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self._parity = 0
        self._player_locations = [None, None]

if __name__ == "__main__":
    emptyState = GameState()  # create an instance of the object

#===================== Game Class Functionality=====================
# player(): return the active player in the current state
# actions(): return a list of the legal actions in the current state
# result(action): return a new state that results from applying the given action in the current state
# terminal_test(): return True if the current state is terminal, and False otherwise
# utility(player): 
#  return +inf if the game is terminal and the specified player wins, 
#  return -inf if the game is terminal and the specified player loses, and
#  return 0 if the game is not terminal (NOTE: You do not need to implement this function now)
# liberties(loc): return a list of cells in the neighborhood of the specified location that are open

from copy import deepcopy

xlim, ylim = 3, 2  # board dimensions

# The eight movement directions possible for a chess queen
RAYS = [(1, 0), (1, -1), (0, -1), (-1, -1),
        (-1, 0), (-1, 1), (0, 1), (1, 1)]


class GameState:
    """
    Attributes
    ----------
    _board: list(list)
        Represent the board with a 2d array _board[x][y]
        where open spaces are 0 and closed spaces are 1
    
    _parity: bool
        Keep track of active player initiative (which
        player has control to move) where 0 indicates that
        player one has initiative and 1 indicates player 2
    
    _player_locations: list(tuple)
        Keep track of the current location of each player
        on the board where position is encoded by the
        board indices of their last move, e.g., [(0, 0), (1, 0)]
        means player 1 is at (0, 0) and player 2 is at (1, 0)
    """
    def __init__(self):
        self._board = [[0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self._parity = 0
        self._player_locations = [None, None]
        
    def actions(self):
        """ Return a list of legal actions for the active player """
        return self.liberties(self._player_locations[self._parity])
    
    def player(self):
        """ Return the id of the active player """
        return self._parity
    
    def result(self, action):
        """ Return a new state that results from applying the given
        action in the current state
        """
        assert action in self.actions(), "Attempted forecast of illegal move"
        newBoard = deepcopy(self)
        newBoard._board[action[0]][action[1]] = 1
        newBoard._player_locations[self._parity] = action
        newBoard._parity ^= 1
        return newBoard
    
    def terminal_test(self):
        """ return True if the current state is terminal,
        and False otherwise
        
        Hint: an Isolation state is terminal if _either_
        player has no remaining liberties (even if the
        player is not active in the current state)
        """
        return (not self._has_liberties(self._parity)
            or not self._has_liberties(1 - self._parity))
    
    def liberties(self, loc):
        """ Return a list of all open cells in the
        neighborhood of the specified location.  The list 
        should include all open spaces in a straight line
        along any row, column or diagonal from the current
        position. (Tokens CANNOT move through obstacles
        or blocked squares in queens Isolation.)
        """
        if loc is None: return self._get_blank_spaces()
        moves = []
        for dx, dy in RAYS:  # check each movement direction
            _x, _y = loc
            while 0 <= _x + dx < xlim and 0 <= _y + dy < ylim:
                _x, _y = _x + dx, _y + dy
                if self._board[_x][_y]:  # stop at any blocked cell
                    break
                moves.append((_x, _y))
        return moves
    
    def _has_liberties(self, player_id):
        """ Check to see if the specified player has any liberties """
        return any(self.liberties(self._player_locations[player_id]))

    def _get_blank_spaces(self):
        """ Return a list of blank spaces on the board."""
        return [(x, y) for y in range(ylim) for x in range(xlim)
                if self._board[x][y] == 0]

#==========================Scoring Min & Max Levels====================

def min_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the minimum value over all legal successors
    """
    if gameState.terminal_test():
        return gameState.utility(0)
    v = float("inf")
    for a in gameState.actions():
        v = min(v, max_value(gameState.result(a)))
    return v


def max_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the maximum value over all legal successors
    """
    if gameState.terminal_test():
        return gameState.utility(0)
    v = float("-inf")
    for a in gameState.actions():
        v = max(v, min_value(gameState.result(a)))
    return v

#====================Minimax Search======================
def minimax_decision(gameState):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """
    # TODO: Finish this function!
    best_score = float("-inf")
    best_move = None
    
    for m in gameState.actions():
        v = min_value(gameState.result(m))
        if v > best_score:
            best_score = v
            best_move = m
    return best_move



