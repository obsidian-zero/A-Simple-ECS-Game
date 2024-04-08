'''
Author: OBSIDIAN_ZERO
Date: 2024-04-07 21:48:49
LastEditors: OBSIDIAN_ZERO
LastEditTime: 2024-04-08 22:28:01
Description: 
'''
import Entity
from components import *
import pygame
system_list = []
priority_list = []
system_query = []

query_list = {}
singleton_list = {}
entityID_list = []
entityID = 1

remove_entity_list = []
# 初始化pygame
pygame.init()
clock = pygame.time.Clock()


DIRTY_REMOVE = False

def begin():
    for system in system_list:
        system.begin()

def update():
    # 控制帧率
    clock.tick(FPS)

    global DIRTY_REMOVE
    
    if DIRTY_REMOVE:
        dirtyRemove()
        DIRTY_REMOVE = False
    
    for system in system_list:
        system.update()

def addSystems(system, priority=0):
    index = len(priority_list)
    for i, p in enumerate(priority_list):
        if priority > p:
            index = i
            break
    priority_list.insert(index, priority)
    system_list.insert(index, system)

    query = system.getQuery()
    if query:
        query_str = ''

        for entity in query:
            query_str += '_' + entity
        
        if query and not query_str in query_list:
            query_list[query_str] = {
                'components': query,
                'entity': [],
            }

        system.setQuery(query_list[query_str])

def addEntity(componentList):
    global entityID
    newEntity = Entity.Entity(entityID)

    for component in componentList:
        name = component
        className = component + "Component"
        obj = globals()[className]()
        newEntity.addComponent(name, obj)

    for query in query_list.values():
        satisfy = True
        for component in query['components']:
            if not component in componentList:
                satisfy = False
                break
        
        if satisfy:
            query['entity'].append(newEntity)

    entityID_list.append(entityID)
    entityID += 1

def removeEntity(entityID):
    if entityID in entityID_list and not entityID in remove_entity_list:
        global DIRTY_REMOVE
        DIRTY_REMOVE = True
        remove_entity_list.append(entityID)
        entityID_list.remove(entityID)
    

def createEntity(componentList, num = 1):
    for i in range(num):
        addEntity(componentList)

def addSingleComponents(component):
    className = component + "Component"
    
    if not component in singleton_list:
        obj = globals()[className]()
        singleton_list[component] = obj

def getSingleComponents(component):
    if component in singleton_list:
        return singleton_list[component]
    else:
        return None

def dirtyRemove():
    global remove_entity_list
    for entityID in remove_entity_list:
        for query in query_list.values():
            if any(entity.id== entityID for entity in query['entity']):
                query['entity'] = [entity for entity in query['entity'] if entity.id != entityID]

    remove_entity_list = []