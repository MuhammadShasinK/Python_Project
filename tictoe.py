def display_board(board):
    print()
    print("-------------")
    print("|", board[0], "|", board[1], "|", board[2], "|")
    print("-------------")
    print("|", board[3], "|", board[4], "|", board[5], "|")
    print("-------------")
    print("|", board[6], "|", board[7], "|", board[8], "|")
    print("-------------")
    print()


def check_winner(board, player):
    if (board[0] == player and board[1] == player and board[2] == player):
        return True

    if (board[3] == player and board[4] == player and board[5] == player):
        return True

    if (board[6] == player and board[7] == player and board[8] == player):
        return True

    if (board[0] == player and board[3] == player and board[6] == player):
        return True

    if (board[1] == player and board[4] == player and board[7] == player):
        return True

    if (board[2] == player and board[5] == player and board[8] == player):
        return True

    if (board[0] == player and board[4] == player and board[8] == player):
        return True

    if (board[2] == player and board[4] == player and board[6] == player):
        return True

    return False


def check_draw(board):
    return " " not in board


def play_game():
    board = [" ", " ", " ",
             " ", " ", " ",
             " ", " ", " "]

    current_player = "X"

    print("\nTIC-TAC-TOE")
    print("Player 1 = X")
    print("Player 2 = O")

    display_board(board)

    while True:
        print("Player", current_player, "'s turn")

        while True:
            position = input("Enter a position (1-9): ").strip()

            if position == "":
                print("Input cannot be empty. Please try again.")
                continue

            if not position.isdigit():
                print("Please enter a number from 1 to 9.")
                continue

            position = int(position)

            if position < 1 or position > 9:
                print("Invalid position. Please enter a number from 1 to 9.")
                continue

            index = position - 1

            if board[index] != " ":
                print("That position is already occupied. Please choose another.")
                continue

            break

        board[index] = current_player

        display_board(board)

        if check_winner(board, current_player):
            if current_player == "X":
                print("Player 1 (X) wins!")
            else:
                print("Player 2 (O) wins!")

            break

        if check_draw(board):
            print("The game is a draw!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


while True:
    play_game()

    while True:
        again = input("Do you want to play again? (yes/no): ").strip().lower()

        if again == "yes" or again == "y":
            break
        elif again == "no" or again == "n":
            print("Thank you for playing Tic-Tac-Toe!")
            exit()
        else:
            print("Please enter yes or no.")