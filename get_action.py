import gc
import os

import numpy as np
import tensorflow as tf
# noinspection PyUnresolvedReferences
import unreal_engine as ue
# noinspection PyUnresolvedReferences
from TFPluginAPI import TFPluginAPI

from MCTS import MCTS
from td2020.TD2020Game import TD2020Game
from td2020.keras.NNet import NNetWrapper as NNet
from td2020.src.config import ACTS_REV, NUM_ACTS
from utils import dotdict


class TD2020LearnAPI(TFPluginAPI):
    def __init__(self):
        # gc.enable()
        self.recommended_act = None
        self.owning_player = None
        self.initial_board_config = None

    def onSetup(self):
        pass

    def onJsonInput(self, jsonInput):
        if self.recommended_act:
            act1 = self.recommended_act
            self.recommended_act = None
            # collecting garbage - this causes stutter in game
            # gc.collect()
            # print("collecting garbage - this causes stutter in game - but it cleans the most")  # TODO
            return act1

        encoded_actors = jsonInput['data']
        initial_board_config = []
        for encoded_actor in encoded_actors:
            initial_board_config.append(
                dotdict({
                    'x': encoded_actor['x'],
                    'y': encoded_actor['y'],
                    'player': encoded_actor['player'],
                    'a_type': encoded_actor['actorType'],
                    'health': encoded_actor['health'],
                    'carry': encoded_actor['carry'],
                    'gold': encoded_actor['money'],
                    'timeout': encoded_actor['remaining']
                })
            )
        self.initial_board_config = initial_board_config
        self.owning_player = jsonInput['player']

    def onBeginTraining(self):
        with tf.Session() as sess:
            current_directory = os.path.join(os.path.dirname(__file__), 'temp/')
            g = TD2020Game(8)
            n1 = NNet(g)
            n1.load_checkpoint(current_directory, 'temp.pth.tar')
            args = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
            mcts = MCTS(g, n1, args)
            g.setInitBoard(self.initial_board_config)
            b = g.getInitBoard()
            n1p = lambda x: np.argmax(mcts.getActionProb(x, temp=0))

            print("todo - check if this 'owning player' is ok")
            # canonical_board = g.getCanonicalForm(b, 1)
            canonical_board = g.getCanonicalForm(b, self.owning_player)

            recommended_act = n1p(canonical_board)
            y, x, action_index = np.unravel_index(recommended_act, [b.shape[0], b.shape[0], NUM_ACTS])

            # gc.collect()  # TODO
            act = {"x": str(x), "y": str(y), "action": ACTS_REV[action_index]}
            # self.recommended_act = {"x": str(x), "y": str(y), "action": ACTS_REV[action_index]}
            print("Printing recommended action", self.recommended_act)
            sess.close()
            # TODO
            print("Todo There still are some memory problems")
        # gc.collect()
        self.recommended_act = act
        return ""

    def run(self, args):
        pass


# required function to get our api
def getApi():
    return TD2020LearnAPI.getInstance()