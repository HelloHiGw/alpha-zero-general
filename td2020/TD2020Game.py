import sys
from typing import Tuple

import numpy as np

from td2020.src.config_class import CONFIG

sys.path.append('..')
from td2020.src.Board import Board
from td2020.src.config import NUM_ENCODERS, NUM_ACTS, P_NAME_IDX, A_TYPE_IDX, TIME_IDX, FPS

""" USE_TIMEOUT, MAX_TIME, d_a_type, a_max_health, INITIAL_GOLD, TIMEOUT, visibility"""

"""
TD2020Game.py

Defined rules for RTS game TD2020
Includes: 
- init - contains board configuration
- getGameEnded - contains end game checking
"""


# noinspection PyPep8Naming,PyMethodMayBeStatic
class TD2020Game:

    def __init__(self) -> None:
        self.n = CONFIG.grid_size

        self.initial_board_config = CONFIG.initial_board_config

    def setInitBoard(self, board_config) -> None:
        self.initial_board_config = board_config

    def getInitBoard(self) -> np.ndarray:
        b = Board(self.n)
        remaining_time = None  # when setting initial board, remaining time might be different
        for e in self.initial_board_config:
            b.pieces[e.x, e.y] = [e.player, e.a_type, e.health, e.carry, e.gold, e.timeout]
            remaining_time = e.timeout
        # remaining time is stored in all squares
        b.pieces[:, :, TIME_IDX] = remaining_time
        return np.array(b.pieces)

    def getBoardSize(self) -> Tuple[int, int, int]:
        # (a,b) tuple
        return self.n, self.n, NUM_ENCODERS

    def getActionSize(self) -> int:
        return self.n * self.n * NUM_ACTS + 1

    def getNextState(self, board: np.ndarray, player: int, action: int) -> Tuple[np.ndarray, int]:

        b = Board(self.n)
        b.pieces = np.copy(board)

        y, x, action_index = np.unravel_index(action, [self.n, self.n, NUM_ACTS])
        move = (x, y, action_index)

        # first execute move, then run time function to destroy any actors if needed
        b.execute_move(move, player)

        # get config for timeout
        if player == 1:
            USE_TIMEOUT = CONFIG.player1_config.USE_TIMEOUT
        else:
            USE_TIMEOUT = CONFIG.player2_config.USE_TIMEOUT

        # update timer on every tile:
        if USE_TIMEOUT:
            b.pieces[:, :, TIME_IDX] -= 1
        else:
            b.pieces[:, :, TIME_IDX] += 1
            b.time_killer(player)

        return b.pieces, -player

    def getValidMoves(self, board: np.ndarray, player: int):

        valids = []
        b = Board(self.n)
        b.pieces = np.copy(board)

        if player == 1:
            config = CONFIG.player1_config
        else:
            config = CONFIG.player2_config

        for y in range(self.n):
            for x in range(self.n):
                if b[x][y][P_NAME_IDX] == player and b[x][y][A_TYPE_IDX] != 1:  # for this player and not Gold
                    valids.extend(b.get_moves_for_square(x, y, config=config))
                else:
                    valids.extend([0] * NUM_ACTS)
        valids.append(0)  # because of that +1 in action Size

        return np.array(valids)

    # noinspection PyUnusedLocal
    def getGameEnded(self, board: np.ndarray, player) -> float:

        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        n = board.shape[0]

        # detect timeout
        if player == 1:
            USE_TIMEOUT = CONFIG.player1_config.USE_TIMEOUT
        else:
            USE_TIMEOUT = CONFIG.player2_config.USE_TIMEOUT

        if USE_TIMEOUT:
            if board[0, 0, TIME_IDX] < 1:

                score_player1 = self.getScore(board, player)
                score_player2 = self.getScore(board, -player)

                if score_player1 == score_player2:

                    if CONFIG.visibility:
                        print("#################### TIMEOUT Tie #######################")
                    return 0.001
                better_player = 1 if score_player1 > score_player2 else -1
                if CONFIG.visibility:
                    print("#################### TIMEOUT", better_player, score_player1, score_player2, "#######################")
                return better_player
        else:
            if player == 1:
                MAX_TIME = CONFIG.player1_config.MAX_TIME
            else:
                MAX_TIME = CONFIG.player2_config.MAX_TIME

            if board[0, 0, TIME_IDX] >= MAX_TIME:
                print("######################################## ERROR ####################################")
                print("################ YOU HAVE TIMEOUTED BECAUSE NO PLAYER HAS LOST YET #################")
                print("###################################### END ERROR ##################################")

                return 0.001

        # detect win condition
        sum_p1 = 0
        sum_p2 = 0
        for y in range(n):
            for x in range(n):
                if board[x][y][P_NAME_IDX] == 1:
                    sum_p1 += 1
                if board[x][y][P_NAME_IDX] == -1:
                    sum_p2 += 1

        if sum_p1 < 2:  # SUM IS 1 WHEN PLAYER ONLY HAS MINERALS LEFT
            if CONFIG.visibility:
                print("################ game end player -1, tick", board[0, 0, TIME_IDX], "################")

            return -1
        if sum_p2 < 2:  # SUM IS 1 WHEN PLAYER ONLY HAS MINERALS LEFT
            if CONFIG.visibility:
                print("################ game end player +1,tick", board[0, 0, TIME_IDX], "################")

            return +1

        # detect no valid actions - possible tie by overpopulating on non-attacking units and buildings - all fields are full or one player is surrounded:
        if sum(self.getValidMoves(board, 1)) == 0:
            if CONFIG.visibility:
                print("################ game end player +1,tick", board[0, 0, TIME_IDX], "No valid moves for player", 1, "################")

            return -1

        if sum(self.getValidMoves(board, -1)) == 0:
            if CONFIG.visibility:
                print("################ game end player +1,tick", board[0, 0, TIME_IDX], "No valid moves for player", - 1, "################")

            return 1
        # continue game
        return 0

    def getCanonicalForm(self, board: np.ndarray, player: int):

        b = np.copy(board)
        b[:, :, P_NAME_IDX] = b[:, :, P_NAME_IDX] * player

        return b

    def getSymmetries(self, board: np.ndarray, pi):
        # mirror, rotational
        assert (len(pi) == self.n * self.n * NUM_ACTS + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n, NUM_ACTS))
        return_list = []
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                return_list += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return return_list

    def stringRepresentation(self, board: np.ndarray):
        return board.tostring()

    def getScore(self, board: np.array, player: int):
        b = Board(self.n)
        b.pieces = np.copy(board)

        # can use different score functions for each player
        if player == 1:
            score_function = CONFIG.player1_config.score_function
        else:
            score_function = CONFIG.player2_config.score_function

        if score_function == 1:
            return b.get_health_score(player)
        elif score_function == 2:
            return b.get_money_score(player)
        else:
            return b.get_combined_score(player)


def display(board):
    from td2020.visualization.Graphics import init_visuals, update_graphics

    if not CONFIG.visibility:
        return

    n = board.shape[0]
    if CONFIG.visibility > 3:
        game_display, clock = init_visuals(n, n, CONFIG.visibility)
        update_graphics(board, game_display, clock, FPS)
    else:
        for y in range(n):
            print('-' * (n * 8 + 1))
            for x in range(n):
                a_player = board[x][y][P_NAME_IDX]
                if a_player == 1:
                    a_player = '+1'
                if a_player == -1:
                    a_player = '-1'
                if a_player == 0:
                    a_player = ' 0'
                print("|" + a_player + " " + str(board[x][y][A_TYPE_IDX]) + " ", end="")
            print("|")
        print('-' * (n * 8 + 1))
