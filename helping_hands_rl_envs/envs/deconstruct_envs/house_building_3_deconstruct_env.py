import time
from copy import deepcopy
import numpy.random as npr
import numpy as np
import pybullet as pb
from itertools import combinations
from helping_hands_rl_envs.envs.deconstruct_envs.deconstruct_env import DeconstructEnv
from helping_hands_rl_envs.pybullet.utils import constants

class HouseBuilding3DeconstructEnv(DeconstructEnv):
  ''''''
  def __init__(self, config):
    # env specific parameters
    if 'object_scale_range' not in config:
      config['object_scale_range'] = [0.6, 0.6]
    if 'num_objects' not in config:
      config['num_objects'] = 4
    if 'max_steps' not in config:
      config['max_steps'] = 10
    super(HouseBuilding3DeconstructEnv, self).__init__(config)

  def checkStructure(self):
    blocks = list(filter(lambda x: self.object_types[x] == constants.CUBE, self.objects))
    bricks = list(filter(lambda x: self.object_types[x] == constants.BRICK, self.objects))
    roofs = list(filter(lambda x: self.object_types[x] == constants.ROOF, self.objects))

    return self._checkOnTop(blocks[0], bricks[0]) and \
           self._checkOnTop(blocks[1], bricks[0]) and \
           self._checkOnTop(bricks[0], roofs[0]) and \
           self._checkInBetween(bricks[0], blocks[0], blocks[1]) and \
           self._checkInBetween(roofs[0], blocks[0], blocks[1])

  def generateStructure(self):
    padding = self.max_block_size * 1.5
    min_dist = 2.1 * self.max_block_size
    max_dist = 2.2 * self.max_block_size
    pos1, pos2 = self.get2BaseXY(padding, min_dist, max_dist)
    rot1 = self._getValidOrientation(self.random_orientation)
    rot2 = self._getValidOrientation(self.random_orientation)
    self.generateStructureShape((pos1[0], pos1[1], self.max_block_size / 2), rot1, constants.CUBE)
    self.generateStructureShape((pos2[0], pos2[1], self.max_block_size / 2), rot2, constants.CUBE)

    x, y, r = self.getXYRFrom2BasePos(pos1, pos2)
    self.generateStructureShape([x, y, self.max_block_size * 1.5], pb.getQuaternionFromEuler([0., 0., r]),
                                constants.BRICK)

    self.generateStructureShape([x, y, self.max_block_size * 2.5], pb.getQuaternionFromEuler([0., 0., r]),
                                constants.ROOF)

    self.wait(50)

  def isSimValid(self):
    roofs = list(filter(lambda x: self.object_types[x] == constants.ROOF, self.objects))
    return self._checkObjUpright(roofs[0]) and super(HouseBuilding3DeconstructEnv, self).isSimValid()

def createHouseBuilding3DeconstructEnv(config):
  return HouseBuilding3DeconstructEnv(config)
