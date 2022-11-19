"""
Module for min-max algorithm for AI opponent

Min-max algorithm goes through all possible states down a series of decision trees until there are no more
Winning states are given +1, losing states are given -1 and neutral states are given 0.
The highest total value for the initial action is the one that should be chosen
"""
from game import Board

def getBestMove(board,aiTurn=True,marker="X"):
    """
    Gets the best move for the computer should make
    Will be recursive (each move generates new possible moves)
    Should return 1,-1 or 0 and the according square that is being played

    board   the current state of the board (board object)
    aiTurn  whether it is the AI turn or the other player's turn
    """

    win = board.checkWinner(verbose=False)
    if win and aiTurn:
        return 1
    elif win and not aiTurn:
        return -1

    # make a copy of the board to iterate through
    board_copy = Board()
    board_copy.board = board.board[:]

    possible_moves = getPossibleMoves(board.board)

    # if there are no moves and no one has won then it is a draw
    if possible_moves == []:
        return 0

    # each move needs to get the next set of possible moves
    # need to update the game board and send the new state to the function
    scores = []
    moves = []
    for move in possible_moves:
        board_copy.updateBoard(move,marker)

        aiTurn = not aiTurn
        if marker.lower() == "x":
            marker = "O"
        elif marker.lower() == "o":
            marker = "X"

        moves.append(move)
        scores.append(getBestMove(board_copy,aiTurn=aiTurn,marker=marker))
        board_copy.board = board.board[:]

    return moves[scores.index(max(scores))]

def getPossibleMoves(state):
    """
    Checks which spots in the board are currently empty
    These are the possible moves that we need to get the best one for
    This will be in square numbers not in indices
    """

    possible_spots = [1,2,3,4,5,6,7,8,9]
    empty_spots = [possible_spots[i] for i,k in enumerate(state) if k == "-"]

    return empty_spots

if __name__ == "__main__":
    board = Board()

    board.updateBoard(1,"O")
    board.updateBoard(6,"O")
    board.updateBoard(8,"O")
    board.updateBoard(2,"X")
    board.updateBoard(5,"X")
    board.updateBoard(9,"X")
    board.showBoard()

    # prints the first winning move
    print(getBestMove(board))