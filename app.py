import tictactoeinator.game
import random

def main():
    game = tictactoeinator.game.Game()
    game.showRules()
    player1 = game.player1
    player2 = game.player2
    game.exampleBoard()

    win = game.gameboard.checkWinner()

    turn = int(random.choice([True, False]))
    while not win:

        if turn%2 == 1:
            currentPlayer = player1
            lastPlayer = player2
        if turn%2 == 0:
            currentPlayer = player2
            lastPlayer = player1

        print(f"{currentPlayer.name}'s turn!")
        game.turn(currentPlayer)
        turn += 1
        win = game.gameboard.checkWinner()

        if win:
            currentPlayer.updateStats("W")
            lastPlayer.updateStats("L")
            if game.endGame():
                win=False
                turn=int(random.choice([True, False]))
                game.gameboard = tictactoeinator.game.Board()
                continue
            break
        if ("-" not in game.gameboard.board) and not win:
            print("TIE GAME!")
            for p in game.players:
                p.updateStats("T")
            if game.endGame():
                win=False
                turn=int(random.choice([True, False]))
                game.gameboard = tictactoeinator.game.Board()
                continue
            break

if __name__ == "__main__":
    main()