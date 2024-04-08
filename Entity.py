'''
Author: OBSIDIAN_ZERO
Date: 2024-04-07 21:52:27
LastEditors: OBSIDIAN_ZERO
LastEditTime: 2024-04-08 22:33:31
Description: 
'''

class Entity:
    def __init__(self, id):
        self.id = id
        self.components = {}

    def addComponent(self, name, component):
        self.components[name] = component

    def getComponentByName(self, name):
        if name in self.components.keys():
            return self.components[name]
        else:
            return None

    def getId(self):
        return self.id
