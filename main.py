'''
Author: OBSIDIAN_ZERO
Date: 2024-04-08 22:22:39
LastEditors: OBSIDIAN_ZERO
LastEditTime: 2024-04-08 22:42:10
Description: 
'''
import sys
import random
import GameWorld
from config import *
from systems import *

GameWorld.addSingleComponents('frame')
GameWorld.addSingleComponents('input')

GameWorld.addSystems(FrameSystem(), 2)
GameWorld.addSystems(SpeedControlSystem(), 1)
GameWorld.addSystems(BallSystem())
GameWorld.addSystems(MoveSystem())
GameWorld.addSystems(InputSystem())
GameWorld.addSystems(EatSystem(), -1)
GameWorld.addSystems(RenderSystem(), -2)

GameWorld.begin()

while True:
    GameWorld.update()