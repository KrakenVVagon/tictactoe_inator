"""
Module that holds the board and game settings
"""

def reinforcedBestMove():

    return 0

def minMaxBestMove(board,aiTurn=True,marker="X"):
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
        scores.append(minMaxBestMove(board_copy,aiTurn=aiTurn,marker=marker))
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

class Game:
    """
    goes through turns (user input 1-9 for square selected)
    knows which token was used last
    can print rules
    can show an example board
    """
    def __init__(self):
        self.gameboard = Board()

        numberPlayers = int(input("How many players are playing (0-2)? "))
        if numberPlayers == 0:
            self.player1 = Player("PC1","X",ai=True)
            self.player2 = Player("PC2","O",ai=True)
        elif numberPlayers == 1:
            playerName = input("Player 1 (X) please enter your name: ")
            self.player1 = Player(playerName,"X")
            self.player2 = Player("PC2","O",ai=True)
        elif numberPlayers == 2:
            playerName = input("Player 1 (X) please enter your name: ")
            self.player1 = Player(playerName,"X")
            playerName = input("Player 2 (O) please enter your name: ")
            self.player2 = Player(playerName,"O")
        else:
            raise ValueError("Unacceptable number of players")

        self.players = [self.player1,self.player2]
        return None

    def turn(self,player):

        if player.ai:
            n = player.ai_move(self.gameboard,marker=player.token)
            self.gameboard.updateBoard(n,player.token)
            self.gameboard.showBoard()
            return None

        instruction = input("Enter a square to play (1-9) or another command. 'help' for details. ")
        if instruction.lower() == "help":
            self.help()
            self.turn(player)
        elif instruction.lower() == "board":
            self.exampleBoard()
            self.turn(player)
        elif instruction.lower() == "rules":
            self.showRules()
            self.turn(player)
        elif instruction.lower() == "current board":
            self.gameboard.showBoard()
            self.turn(player)
        elif int(instruction) in range(1,10):
            n = int(instruction)
            if self.gameboard.board[n-1] == "-":
                self.gameboard.updateBoard(n,player.token)
                self.gameboard.showBoard()
            else:
                print("Someone is already there!")
                self.turn(player)

#        if self.gameboard.checkWinner():
#            self.endGame()
        return None

    @staticmethod
    def showRules():
        print("It is a game of Tic-Tac-Toe do you really need rules?")
        print("First to 3 in a row wins!")
        print("Alternate placing X and O in squares until someone wins or there are no moves left")
        return None

    @staticmethod
    def exampleBoard():
        board = Board()
        for i,k in enumerate(board.board):
            board.updateBoard(i+1,str(i+1))
        board.showBoard()
        return None

    def endGame(self):
        again = input("Would you like to play again (y/n)? ").lower()
        if again == "y":
            print("Let's go again!")
            return True
        elif again == "n":
            print("Thanks for playing!")
            print("Final results: ")
            for p in self.players:
                p.showStats()
            return False
        else:
            print("Invalid entry!")
            self.endGame()

    @staticmethod
    def help():
        print("Options are: ")
        print("""
        help - shows this message
        board - shows the example board with labeled 1-9 squares
        (1-9) - the square where the player's token will be placed
        rules - prints the rules of Tic-Tac-Toe (lol)
        current board - prints the current state of the board
        """)
        return None

class Board:
    """
    should check for a winner
    shoud know which player wins (X or O)
    should print the current state of the board
    """
    def __init__(self):
        self.board = ["-"]*9
        self._updateRows()
        return None

    def showBoard(self):
        # show the current state of the board
        pstring = ""
        for i,k in enumerate(self.board):
            if (i+1)%3 == 0:
                pstring += f" {k.upper()}\n"
            else:
                pstring += f" {k.upper()}"
        print(pstring)
        return None

    def checkWinner(self,verbose=True):
        # check if any player has 3 in a row
        for r in self._rows:
            if r.count(r[0])==len(r) and (r[0].lower() == "x" or r[0].lower()=="o"):
                if verbose:
                    print("WE HAVE A WINNER!")
                return True
        return False

    def updateBoard(self,n,token):
        self.board[n-1] = token
        self._updateRows()
        return None

    def _updateRows(self):
        # updates the "rows" (anything that can win)
        self._row1 = self.board[0:3]
        self._row2 = self.board[3:6]
        self._row3 = self.board[6:10]
        self._col1 = [k for i,k in enumerate(self.board) if i%3==0]
        self._col2 = [k for i,k in enumerate(self.board) if i%3==1]
        self._col3 = [k for i,k in enumerate(self.board) if i%3==2]
        self._diag1 = [self.board[0],self.board[4],self.board[8]]
        self._diag2 = [self.board[2],self.board[4],self.board[6]]

        self._rows = [
            self._row1,self._row2,self._row3,
            self._col1,self._col2,self._col3,
            self._diag1,self._diag2
        ]

class Player:
    """
    players can be AI or human
    players have names
    players are a token (X or O)
    players keep track of their W/L/T stats
    """
    def __init__(self,name,token,ai=False):
        self.name = name
        self.token = token
        self.ai = ai
        self.stats = {"W":0,"L":0,"T":0}

        # if ai then select what kind of AI you are playing against
        if self.ai:
            self.ai_difficulty = input("Select AI difficulty (E/H): ")
            if self.ai_difficulty.lower() == "e":
                self.ai_move = minMaxBestMove
            elif self.ai_difficulty.lower() == "h":
                self.ai_move = reinforcedBestMove
                raise ValueError("Hard AI not currently implemented")
            else:
                raise ValueError("Invalid AI Difficulty.")

        return None

    def updateStats(self,result):
        self.stats[result] += 1
        return None

    def showStats(self):
        print(f"{self.name} stats: ")
        print(self.stats)
        return None

def main():
    game = Game()
    game.exampleBoard()
    game.turn()

if __name__ == "__main__":
    main()