import numpy as np
import time


class TickTackToe():
    def __init__(self, size=3, connection=3):
        self.size = size
        self.connection = connection
        self.board = self.reset_board()
        self.variation_count = 0

    def reset_board(self):
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def show_board(self):
        for row in self.board:
            print(row)

    def _check_column(self, player, board):
        for column in range(self.size):
            if all(board[row][column] == player for row in range(self.size)):
                return True
        return False

    def _check_row(self, player, board):
        for row in range(self.size):
            if all(board[row][column] == player for column in range(self.size)):
                return True
        return False

    def _check_diagonal(self, player, board):
        if all(board[i][i] == player for i in range(self.size)):
            return True
        if all(board[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False

    def check_win(self, player, board):
        if self._check_column(player, board) or self._check_row(player, board) or self._check_diagonal(player, board):
            return True
        return False

    def check_draw(self,board):
        return all(cell != 0 for row in board for cell in row)

    def check_valid_move(self, board):
        valid_moves = []
        for row in range(self.size):
            for column in range(self.size):
                if board[row][column] == 0:
                    valid_moves.append((row, column))
        return valid_moves

    def human_play(self, player=1):
        self.board = self.reset_board()
        self.show_board()

        while not self.check_win(player, self.board) and not self.check_win(-player,
                                                                            self.board) and not self.check_draw(self.board):
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

        self.variation_count += 1

        if self.check_win(player * - 1, current_board):
            return 1 * player * - 1
        if self.check_draw(current_board):
            return 0.5 * player * - 1
        if layer_deep == 0:
            return 0 * player * - 1
        count = []
        for row, column in self.check_valid_move(current_board):
            board = np.copy(current_board)
            board[row][column] = player
            # print(f"\n Layer Deep: {5 - layer_deep}")
            # for row in board:
            #     print(row)
            # time.sleep(0.2)
            count.append(self.min_max(player * - 1, board, layer_deep - 1))
        # if layer_deep >= 0:
        #     print(f"\nLayer Deep: {5 - layer_deep}")
        #     print('\nSolution: Given board configuration and player',player )
        #     board = self.reset_board()
        #     some = 0
        #     for row in range (0,len(current_board)):
        #         print(current_board[row])
        #         for column in range (0,len(current_board[row])):
        #             if current_board[row][column] != 0:
        #                 board[row][column] = 'None'
        #
        #     for row, column in self.check_valid_move(current_board):
        #         board[row][column] = count[some]
        #         some += 1
        #
        #     for row in board:
        #         print(row)

        if player == 1:
            return max(count)
        else:
            return min(count)

    def min_max_best_move(self, player, current_board, layer_deep):

        self.variation_count += 1

        if self.check_win(player * - 1, current_board):
            return 1 * player * - 1, None
        if self.check_draw(current_board):
            return 0.5 * player * - 1, None
        if layer_deep == 0:
            return 0 * player * - 1, None

        best_move = []


        if player == 1:
            best_value = -np.inf
            # return max(count)
            for row, column in self.check_valid_move(current_board):
                board = np.copy(current_board)
                board[row][column] = player
                # print(self.min_max_best_move(player * - 1, board, layer_deep - 1),'max')
                cur_value, _ = self.min_max_best_move(player * - 1, board, layer_deep - 1)
                if cur_value > best_value:
                    best_value = cur_value
                    best_move = [row,column]
            return best_value,best_move

        else:
            # return min(count)
            best_value = np.inf
            for row, column in self.check_valid_move(current_board):
                board = np.copy(current_board)
                board[row][column] = player
                # print(self.min_max_best_move(player * - 1, board, layer_deep - 1),'min')
                cur_value, _ = self.min_max_best_move(player * - 1, board, layer_deep - 1)
                if cur_value < best_value:
                    best_value = cur_value
                    best_move = [row, column]
            return best_value, best_move


    def human_machine(self, player = 1, layer_deep = 9):
        self.board = self.reset_board()
        self.show_board()

        while not self.check_win(player, self.board) and not self.check_win(-player,self.board) and not self.check_draw(self.board):
            if player == 1:
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
                score,[row,column] = self.min_max_best_move(player,self.board, layer_deep)
                print(f"AI has chosen {row,column} The score by it is: {score}")
                print(f'Number of variations is {game.variation_count}')
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
        """For 3 x 3 board"""
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
    game.human_machine()
    # game.show_board()
    # board = [[0, 0, 0],
    #          [0, 0, 0],
    #          [0, 0, 1]]
    # # print(game.min_max(-1, board, 9))
    # print(game.min_max_best_move(1, board, 9))

    # game.human_play()
