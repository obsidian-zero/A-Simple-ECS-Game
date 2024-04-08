'''
Author: OBSIDIAN_ZERO
Date: 2024-04-07 21:54:27
LastEditors: OBSIDIAN_ZERO
LastEditTime: 2024-04-08 22:43:53
Description: 
'''
import pygame
import GameWorld
from config import *
import keyboard

class BaseSystem:
    def __init__(self):
        self.paused = False
        self.query = None

    def update(self):
        if self.query != None:
            self.onUpdate(self.query['entity'])
        else:
            self.onUpdate([])

    def onUpdate(self, query):
        pass

    def getQuery(self):
        return None

    def setQuery(self, query):
        self.query = query

    def begin(self):
        pass

class RenderSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        
    def begin(self):
        # 创建窗口
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Eat Small Ball")

    def onUpdate(self, query):
        # 绘制背景和小球
        self.win.fill(BLACK)  # 黑色背景

        for entity in query:
            posX = entity.getComponentByName('position').posX
            posy = entity.getComponentByName('position').posY
            size = entity.getComponentByName('size').size
            if entity.getComponentByName('player') != None:
                pygame.draw.circle(self.win, RED, (posX, posy), size)  # 自控为红色圆形
            else:
                pygame.draw.circle(self.win, WHITE, (posX, posy), size)  # 小球为白色圆形

        pygame.display.update()

    def getQuery(self):
        return ['position', 'size']

class EatSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        
    def getQuery(self):
        return ['position', 'size']

    def onUpdate(self, query):
        player_entity = None
        for entity in query:
            if entity.getComponentByName('player') != None:
                player_entity = entity
                break
        
        if not player_entity:
            return
        
        for entity in query:
            if entity == player_entity:
                continue
            
            entity_pos = entity.getComponentByName('position')
            player_pos = player_entity.getComponentByName('position')
            dx = entity_pos.posX - player_pos.posX
            dy = entity_pos.posY - player_pos.posY
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance < player_entity.getComponentByName('size').size + entity.getComponentByName('size').size:
                player_size_com = player_entity.getComponentByName('size')
                entity_size_com = entity.getComponentByName('size')
                if player_size_com.size >= entity_size_com.size:
                    player_size_com.size += (entity_size_com.size ** 0.5)
                    GameWorld.removeEntity(entity.getId())
                
class BallSystem(BaseSystem):
    def __init__(self):
        super().__init__()

    def begin(self):
        GameWorld.createEntity(['position', 'size', 'speed'], 10)
        GameWorld.createEntity(['position', 'size', 'player', 'speed'])

    def onUpdate(self, query):
        frameComponent = GameWorld.getSingleComponents('frame')
        if frameComponent.frame % (CREATE_INTERVAL * FPS) == 0:
            GameWorld.createEntity(['position', 'size', 'speed'])

class MoveSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        
    def getQuery(self):
        return ['position', 'speed']

    def onUpdate(self, query):
        for entity in query:
            speedCom = entity.getComponentByName('speed')
            posCom = entity.getComponentByName('position')

            posX = posCom.posX
            posy = posCom.posY

            speedX = speedCom.speedX
            speedY = speedCom.speedY

            if speedX > MAX_SPEED:
                speedX = MAX_SPEED
            if speedX < -MAX_SPEED:
                speedX = -MAX_SPEED
            if speedY > MAX_SPEED:
                speedY = MAX_SPEED
            if speedY < -MAX_SPEED:
                speedY = -MAX_SPEED
                

            if posX + speedX > WIDTH or posX + speedX < 0:
                speedX = -speedX
            if posy + speedY > HEIGHT or posy + speedY < 0:
                speedY = -speedY

            speedCom.speedX = speedX
            speedCom.speedY = speedY
                
            entity.getComponentByName('position').posX += speedCom.speedX
            entity.getComponentByName('position').posY += speedCom.speedY

            

class SpeedControlSystem(BaseSystem):
    def getQuery(self):
        return ['player', 'speed']

    def onUpdate(self, query):
        com = GameWorld.getSingleComponents('input')
        if len(query) > 0:
            player = query[0]
            X = 0
            Y = 0

            if com.inputW:
                Y = -1  
            if com.inputS:
                Y = 1
            if com.inputA:
                X = -1
            if com.inputD:
                X = 1

            player.getComponentByName('speed').speedX += X
            
            player.getComponentByName('speed').speedY += Y

class InputSystem(BaseSystem):
    def on_key_event(self, event):
        com = GameWorld.getSingleComponents('input')
        if event.name == 'w':
            com.inputW = True
        elif event.name == 's':
            com.inputS = True
        elif event.name == 'a':
            com.inputA = True
        elif event.name == 'd':
            com.inputD = True

    def begin(self):
        keyboard.on_press(self.on_key_event)

    def onUpdate(self, query):
        com = GameWorld.getSingleComponents('input')
        com.inputW = None
        com.inputS = None
        com.inputA = None
        com.inputD = None
class FrameSystem(BaseSystem):
    def __init__(self):
        super().__init__()

    def onUpdate(self, query):
        frameComponent = GameWorld.getSingleComponents('frame')
        frameComponent.frame = frameComponent.frame + 1