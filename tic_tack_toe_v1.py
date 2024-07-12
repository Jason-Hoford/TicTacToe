import numpy as np

class TickTackToe():
    def __init__(self, size=3, connection=3):
        self.size = size
        self.connection = connection
        self.board = self.reset_board()
        self.variation_count = 0

    def reset_board(self):
        """Reset the board to an empty state."""
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def show_board(self):
        """Print the current state of the board."""
        for row in self.board:
            print(row)

    def _check_column(self, player, board):
        """Check if a player has won by filling any column."""
        for column in range(self.size):
            if all(board[row][column] == player for row in range(self.size)):
                return True
        return False

    def _check_row(self, player, board):
        """Check if a player has won by filling any row."""
        for row in range(self.size):
            if all(board[row][column] == player for column in range(self.size)):
                return True
        return False

    def _check_diagonal(self, player, board):
        """Check if a player has won by filling any diagonal."""
        if all(board[i][i] == player for i in range(self.size)):
            return True
        if all(board[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False

    def check_win(self, player, board):
        """Check if the player has won the game."""
        if self._check_column(player, board) or self._check_row(player, board) or self._check_diagonal(player, board):
            return True
        return False

    def check_draw(self, board):
        """Check if the game is a draw."""
        return all(cell != 0 for row in board for cell in row)

    def check_valid_move(self, board):
        """Return a list of valid moves."""
        valid_moves = []
        for row in range(self.size):
            for column in range(self.size):
                if board[row][column] == 0:
                    valid_moves.append((row, column))
        return valid_moves

    def human_play(self, player=1):
        """Allow a human to play against another human."""
        self.board = self.reset_board()
        self.show_board()

        while not self.check_win(player, self.board) and not self.check_win(-player, self.board) and not self.check_draw(self.board):
            valid_moves = self.check_valid_move(self.board)
            print("Valid moves:", valid_moves)

            row = int(input('Which row (0-2): '))
            column = int(input('Which column (0-2): '))
            while (row, column) not in valid_moves:
                print('Invalid move. Try again.')
                row = int(input('Which row (0-2): '))
                column = int(input('Which column (0-2): '))

            self.board[row][column] = player
            self.show_board()
            if self.check_win(player, self.board):
                print(f'Player {player} wins!')
                return
            if self.check_draw(self.board):
                print('It\'s a draw!')
                return
            player *= -1

    def min_max(self, player, current_board, layer_deep):
        """Minimax algorithm to determine the best move for the AI."""
        self.variation_count += 1

        if self.check_win(player * -1, current_board):
            return 1 * player * -1
        if self.check_draw(current_board):
            return 0.5 * player * -1
        if layer_deep == 0:
            return 0 * player * -1

        count = []
        for row, column in self.check_valid_move(current_board):
            board = np.copy(current_board)
            board[row][column] = player
            count.append(self.min_max(player * -1, board, layer_deep - 1))

        if player == 1:
            return max(count)
        else:
            return min(count)

    def min_max_best_move(self, player, current_board, layer_deep):
        """Minimax algorithm to determine the best move for the AI with the best move selection."""
        self.variation_count += 1

        if self.check_win(player * -1, current_board):
            return 1 * player * -1, None
        if self.check_draw(current_board):
            return 0.5 * player * -1, None
        if layer_deep == 0:
            return 0 * player * -1, None

        best_move = []

        if player == 1:
            best_value = -np.inf
            for row, column in self.check_valid_move(current_board):
                board = np.copy(current_board)
                board[row][column] = player
                cur_value, _ = self.min_max_best_move(player * -1, board, layer_deep - 1)
                if cur_value > best_value:
                    best_value = cur_value
                    best_move = [row, column]
            return best_value, best_move
        else:
            best_value = np.inf
            for row, column in self.check_valid_move(current_board):
                board = np.copy(current_board)
                board[row][column] = player
                cur_value, _ = self.min_max_best_move(player * -1, board, layer_deep - 1)
                if cur_value < best_value:
                    best_value = cur_value
                    best_move = [row, column]
            return best_value, best_move

    def human_machine(self, human_player=1, layer_deep=9):
        """Play a game against the AI."""
        player = 1
        self.board = self.reset_board()
        self.show_board()

        while not self.check_win(player, self.board) and not self.check_win(-player, self.board) and not self.check_draw(self.board):
            if human_player == player:
                valid_moves = self.check_valid_move(self.board)
                print("Valid moves:", valid_moves)

                row = int(input('Which row (0-2): '))
                column = int(input('Which column (0-2): '))
                while (row, column) not in valid_moves:
                    print('Invalid move. Try again.')
                    row = int(input('Which row (0-2): '))
                    column = int(input('Which column (0-2): '))

                self.board[row][column] = player
                self.show_board()
            else:
                score, [row, column] = self.min_max_best_move(player, self.board, layer_deep)
                print(f"AI has chosen {row,column}. The score by it is: {score}")
                print(f'Number of variations is {self.variation_count}')
                self.variation_count = 0
                self.board[row][column] = player
                self.show_board()
            if self.check_win(player, self.board):
                print(f'Player {player} wins!')
                return
            if self.check_draw(self.board):
                print('It\'s a draw!')
                return
            player *= -1

    def tests(self):
        """Run tests for the game logic."""
        # Column tests
        self.board = [[1, 0, 0],
                      [1, 0, 0],
                      [1, 0, 0]]
        print('\nColumn test:')
        print('Expected: True', 'Got:', self._check_column(player=1, board=self.board))
        self.board = [[1, 0, 0],
                      [0, 0, 0],
                      [1, 0, 0]]
        print('Expected: False', 'Got:', self._check_column(player=1, board=self.board))
        self.board = [[0, 0, 1],
                      [0, 0, 1],
                      [0, 0, 1]]
        print('Expected: True', 'Got:', self._check_column(player=1, board=self.board))

        # Row tests
        print('\nRow test:')
        self.board = [[1, 1, 1],
                      [0, 0, 0],
                      [0, 0, 0]]
        print('Expected: True', 'Got:', self._check_row(player=1, board=self.board))
        self.board = [[1, 0, 1],
                      [0, 0, 0],
                      [0, 0, 0]]
        print('Expected: False', 'Got:', self._check_row(player=1, board=self.board))
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [1, 1, 1]]
        print('Expected: True', 'Got:', self._check_row(player=1, board=self.board))

        # Diagonal tests
        print('\nDiagonal testing')
        self.board = [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]]
        print('Expected: True', 'Got:', self._check_diagonal(player=1, board=self.board))
        self.board = [[0, 0, 1],
                      [0, 1, 0],
                      [1, 0, 0]]
        print('Expected: True', 'Got:', self._check_diagonal(player=1, board=self.board))

if __name__ == '__main__':
    game = TickTackToe()
    game.human_machine(human_player=1)

    # Uncomment the following lines to run additional tests or play a human vs human game
    # game.show_board()
    # board = [[0, 0, 0],
    #          [0, 0, 0],
    #          [0, 0, 1]]
    # print(game.min_max_best_move(1, board, 9))
    # game.human_play()
