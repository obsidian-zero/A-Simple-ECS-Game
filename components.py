'''
Author: OBSIDIAN_ZERO
Date: 2024-04-07 21:52:53
LastEditors: OBSIDIAN_ZERO
LastEditTime: 2024-04-08 22:32:07
Description: 
'''
from config import *
import random

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        
        return instances[cls]

    return get_instance

class positionComponent:
    def __init__(self):
        self.posX = random.randint(0, WIDTH)
        self.posY = random.randint(0, HEIGHT)

class sizeComponent:
    def __init__(self):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)

class speedComponent:
    def __init__(self):
        self.speedX = random.randint(1, 5)
        self.speedY = random.randint(1, 5)

class playerComponent:
    pass

@singleton
class frameComponent:
    def __init__(self):
        self.frame = 0

@singleton
class inputComponent:
    def __init__(self):
        self.inputW = None
        self.inputS = None
        self.inputA = None
        self.inputD = None