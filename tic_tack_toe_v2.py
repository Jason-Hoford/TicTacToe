import numpy as np

class TickTockToe():
    def __init__(self, row_length=3, column_length=3, connection=3):
        self.row_length = row_length
        self.column_length = column_length
        self.connection = connection
        self.variation_count = 0

    def rest_board(self):
        """Reset the board to an empty state."""
        return [[0 for _ in range(self.column_length)] for _ in range(self.row_length)]

    def check_column(self, board, player):
        """Check if a player has won by filling any column."""
        count = [0] * self.column_length
        for row in range(self.row_length):
            for column in range(self.column_length):
                if board[row][column] == player:
                    count[column] += 1
                    if max(count) == self.connection:
                        return True
                elif count[column] != 0:
                    count[column] = 0
        return max(count) == self.connection

    def check_row(self, board, player):
        """Check if a player has won by filling any row."""
        count = [0] * self.row_length
        for row in range(self.row_length):
            for column in range(self.column_length):
                if board[row][column] == player:
                    count[row] += 1
                    if max(count) == self.connection:
                        return True
                elif count[row] != 0:
                    count[row] = 0
        return max(count) == self.connection

    def _run_down_positive_diagonal(self, board, player, row, column):
        """Check for a win on the positive diagonal."""
        cur_row = row
        cur_column = column
        count = 0
        while cur_row < self.row_length and cur_column < self.column_length:
            if board[cur_row][cur_column] == player:
                count += 1
            elif count != 0:
                count = 0
            if count == self.connection:
                return True
            cur_row += 1
            cur_column += 1
        return False

    def _run_down_negative_diagonal(self, board, player, row, column):
        """Check for a win on the negative diagonal."""
        cur_row = row
        cur_column = column
        count = 0
        while cur_row < self.row_length and cur_column >= 0:
            if board[cur_row][cur_column] == player:
                count += 1
            elif count != 0:
                count = 0
            if count == self.connection:
                return True
            cur_row += 1
            cur_column -= 1
        return False

    def check_diagonals(self, board, player):
        """Check if a player has won by filling any diagonal."""
        possible_row = self.row_length - self.connection + 1
        possible_column = self.column_length - self.connection + 1

        # positive diagonal
        for row in range(possible_row):
            for column in range(possible_column):
                if self._run_down_positive_diagonal(board, player, row, column):
                    return True

        # negative diagonal
        for row in range(possible_row):
            for column in range(possible_column):
                if self._run_down_negative_diagonal(board, player, row, self.column_length - column - 1):
                    return True
        return False

    def check_win(self, board, player):
        """Check if the player has won the game."""
        return self.check_column(board, player) or self.check_row(board, player) or self.check_diagonals(board, player)

    def check_draw(self, board):
        """Check if the game is a draw."""
        for row in range(self.row_length):
            if 0 in board[row]:
                return False
        return True

    def show_board(self, board):
        """Print the current state of the board."""
        for row in range(self.row_length):
            print(board[row])

    def check_valid_moves(self, board):
        """Return a list of valid moves."""
        valid_moves = []
        for row in range(self.row_length):
            for column in range(self.column_length):
                if board[row][column] == 0:
                    valid_moves.append((row, column))
        return valid_moves

    def human_play_game(self, player=1):
        """Allow a human to play against another human."""
        board = self.rest_board()
        while not (self.check_win(board, 1) or self.check_win(board, -1) or self.check_draw(board)):
            self.show_board(board)
            valid_moves = self.check_valid_moves(board)
            print(f'Possible positions: {valid_moves}')
            try:
                row = int(input('Enter the row number: '))
                column = int(input('Enter the column number: '))
                if (row, column) not in valid_moves:
                    raise ValueError("Invalid move")
            except ValueError as e:
                print(e)
                print('You have not entered a valid position. Please enter again.')
                continue
            board[row][column] = player
            if self.check_win(board, player):
                self.show_board(board)
                print(f'Player {player} wins!')
                return
            if self.check_draw(board):
                self.show_board(board)
                print('It\'s a draw!')
                return
            player *= -1
        self.show_board(board)

    def min_max(self, cur_board, cur_player, layer_deep):
        """Minimax algorithm to determine the best move for the AI."""
        self.variation_count += 1
        player_of_last_move = cur_player * -1
        if self.check_win(cur_board, player_of_last_move):
            return 1 * player_of_last_move, None
        if self.check_draw(cur_board):
            return 0.5 * player_of_last_move, None
        if layer_deep == 0:
            return 0, None

        if cur_player == 1:
            # maximize
            best_move = None
            best_val = -np.inf
            for row, column in self.check_valid_moves(cur_board):
                new_board = np.copy(cur_board)
                new_board[row][column] = cur_player
                val, move = self.min_max(new_board, cur_player * -1, layer_deep - 1)
                if val > best_val:
                    best_val = val
                    best_move = [row, column]
        else:
            # minimize
            best_move = None
            best_val = np.inf
            for row, column in self.check_valid_moves(cur_board):
                new_board = np.copy(cur_board)
                new_board[row][column] = cur_player
                val, move = self.min_max(new_board, cur_player * -1, layer_deep - 1)
                if val < best_val:
                    best_val = val
                    best_move = [row, column]

        return best_val, best_move

    def human_ai(self, human_player, layer_deep):
        """Allow a human to play against the AI."""
        player = 1
        board = self.rest_board()
        while not (self.check_win(board, 1) or self.check_win(board, -1) or self.check_draw(board)):
            if human_player == player:
                self.show_board(board)
                valid_moves = self.check_valid_moves(board)
                print(f'Possible positions: {valid_moves}')
                try:
                    row = int(input('Enter the row number: '))
                    column = int(input('Enter the column number: '))
                    if (row, column) not in valid_moves:
                        raise ValueError("Invalid move")
                except ValueError as e:
                    print(e)
                    print('You have not entered a valid position. Please enter again.')
                    continue
                board[row][column] = player
            else:
                score, best_move = self.min_max(board, player, layer_deep)
                row, column = best_move
                print(f"Number of variations gone through: {self.variation_count}")
                print(f"AI has chosen {row, column}. The score by it is: {score}")
                board[row][column] = player

            if self.check_win(board, player):
                self.show_board(board)
                print(f'Player {player} wins!')
                return
            if self.check_draw(board):
                self.show_board(board)
                print('It\'s a draw!')
                return
            player *= -1
        self.show_board(board)

    def test(self):
        """Run tests to verify game logic."""
        # check diagonals
        board = [[1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0]]
        print('Expected Answer: True', 'got', self.check_diagonals(board, 1))

        # check rows
        board = [[0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0],
                 [1, 1, 1, 0, 0]]
        print('Expected Answer: True', 'got', self.check_row(board, 1))

        # check columns
        board = [[1, 1, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 1, 0, 0]]
        print('Expected Answer: True', 'got', self.check_column(board, 1))

if __name__ == '__main__':
    game = TickTockToe(row_length=3, column_length=5, connection=3)
    game.human_ai(human_player=-1, layer_deep=7)