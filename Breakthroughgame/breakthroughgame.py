import sys, os, math
from minimax_agent import *
from model import *
from alpha_beta_agent import *
import time

class BreakthroughGame:
    def __init__(self):
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.winner = 0
        self.computer = None

        # status 0: origin;  1: ready to move; 2: end
        # turn 1: black 2: white
        self.status = 0
        self.turn = 1
        # Variable for moving
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece_1 = 0
        self.eat_piece_2 = 0
        self.game_over = False  # checks whether a winner has been found

    def run(self, status):

        if self.game_over:  # check if the game is over
            return True

        self.status = status

        if self.status in [5,6,7,9,9,10]:
            """
            5. Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
            6. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)\n"
            7. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)\n"
            8. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)\n"
            9. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)\n"
            10. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)\n")
            
            the default search type is set to alpha-beta
            """
            blacksearch = 2
            whitesearch = 2
            blackheuristic = 0
            whiteheuristic = 0

            match (self.status):

                case 5:
                    blacksearch = 1 # the black pieces to minimax
                    blackheuristic = 1
                    whiteheuristic = 1
                case 6:
                    blackheuristic = 3
                    whiteheuristic = 2
                case 7:
                    blackheuristic = 4
                    whiteheuristic = 1
                case 8:
                    blackheuristic = 3
                    whiteheuristic = 1
                case 9:
                    blackheuristic = 4
                    whiteheuristic = 2
                case 10:
                    blackheuristic = 3
                    whiteheuristic = 4
            # Black
            if self.turn == 1:
                start = time.process_time()
                self.ai_move(blacksearch, blackheuristic)
                self.total_time_1 += (time.process_time() - start)
                self.total_step_1 += 1
                print('total_step_1 = ', self.total_step_1,
                      'total_nodes_1 = ', self.total_nodes_1,
                      'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
                      'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
                      'have_eaten = ', self.eat_piece_1)
            elif self.turn == 2:
                start = time.process_time()
                self.ai_move(whitesearch, whiteheuristic)
                self.total_time_2 += (time.process_time() - start)
                self.total_step_2 += 1
                print('total_step_2 = ', self.total_step_2,
                      'total_nodes_2 = ', self.total_nodes_2,
                      'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
                      'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
                      'have_eaten: ', self.eat_piece_2)
        if self.status == 3 or self.isgoalstate():
            self.game_over = True
            winner = "Black" if self.turn == 2 else "White"
            print(f"\nGame Over: {winner} wins!")
            black_dist = []
            white_dist = []

            for row in range(8):
                for col in range(8):
                    if self.boardmatrix[row][col] == 1:
                        black_dist.append(7 - row)
                    elif self.boardmatrix[row][col] == 2:
                        white_dist.append(row)

            black_min = min(black_dist) if black_dist else float('inf')
            white_min = min(white_dist) if white_dist else float('inf')

            # Print final statistics
            print("\nFinal Statistics:")
            print(f"Black moves: {self.total_step_1}")
            print(f"Black average nodes per move: {self.total_nodes_1 / self.total_step_1}")
            print(f"Black average time per move: {self.total_time_1 / self.total_step_1}")
            print(f"Black moves needed to win: {black_min}")
            print(f"White moves: {self.total_step_2}")
            print(f"White average nodes per move: {self.total_nodes_2 / self.total_step_2}")
            print(f"White average time per move: {self.total_time_2 / self.total_step_2}")
            print(f"White moves needed to win: {white_min}")
            print(f"White pieces eaten: {self.eat_piece_1}")
            print(f"Black pieces eaten: {self.eat_piece_2}")

            print(f"Final board:")
            for row in self.boardmatrix:
                print(row)
            return True



        return False

    def isabletomove(self):
        if (self.boardmatrix[self.ori_x][self.ori_y] == 1
            and self.boardmatrix[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2)) \
            or (self.boardmatrix[self.ori_x][self.ori_y] == 2
                and self.boardmatrix[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1)):
            return 1
        return 0

    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        for row in self.boardmatrix:    # print the current board state
            print(row)
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.eat_piece_1 = 16 - piece
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        if self.isgoalstate():
            self.status = 3
            #print(self.boardmatrix)

    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
        self.boardmatrix = board.getMatrix()
        for row in self.boardmatrix:    # print the current board state
            print(row)
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.eat_piece_2 = 16 - piece
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        if self.isgoalstate():
            self.status = 3

    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

def main():

    num_dict = {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 9, 'F': 10}
    status = input("Breakthrough!:\n"
                   "Choose a matchup:\n"
                   "A. Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)\n"
                   "B. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)\n"
                   "C. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)\n"
                   "D. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)\n"
                   "E. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)\n"
                   "F. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)\n")
    print("Now loading...")

    status = num_dict[status]
    game = BreakthroughGame()
    while True:
        if game.run(status): # game is over once run returns True
            break


if __name__ == '__main__':
    main()

