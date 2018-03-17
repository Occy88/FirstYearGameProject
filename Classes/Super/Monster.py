import time, configparser
from SimpleGUICS2Pygame import simplegui_lib_draw
from Classes.Middle.Particle import Particle
from Classes.Base.Vector import Vector
from Classes.Settings import SHOW_MONSTER_THOUGHTS #this never seems to be used?
config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
import json

#exact copy of player but used for monsters and no preset animations
class Monster:
    def __init__(self, pos, vel, nextPosTime, nextPos, maxVel, angle, radius, spriteKey, spriteDictionary, spriteFps,
                 idObject, hasFired,
                 clickPosition, spriteState, numRows, numColumns, startRow, startColumn, endRow, endColumn,tier,aBack,external,totalLife,operationOrigin,
                 operationRange,attackRange,followDistance):
        # id's
        self.remove = False
        self.idClass = 4
        self.idObject = idObject
        self.external = external
        # non-vectors (attributes)
        self.operationOrigin=operationOrigin
        self.operationRange=operationRange
        self.attackRange=attackRange
        self.followDistance=followDistance
        self.returning=False
        self.hasSelectedReturn=False
        self.tier=tier
        self.life = totalLife
        self.lifePrev=self.life
        self.range = 0
        self.melee = 0
        self.magic = 0
        self.tier = 0
        self.totalLife=totalLife
        self.hitByWeapon=0 #used for when external arrow hits local monster... need to save that arrows id as it can reapear even if removed locally

        # vectors
        self.clickPosition = clickPosition
        # Sprite Attributes
        self.spriteState = spriteState
        self.currentTime = 0
        self.hasFired = hasFired
        self.fireCooldown=0

        self.aBack=aBack


        #sub class
        self.particle = Particle(True, pos, vel, nextPosTime, nextPos, maxVel, 0, angle, radius, spriteKey,
                                 spriteDictionary, spriteFps,
                                 False, False, self.idObject, numRows, numColumns, startRow, startColumn, endRow,
                                 endColumn)

    def recieve(self, hasFired, clickPosition, nextPos, nextPosTime, maxVel, maxRange, angle, updateSprite, spriteKey,
                fps, numRows, numColumns, startRow, startColumn, endRow, endColumn, radius, spriteDictionary,life,range,melee,magic,remove):

        self.life=life
        self.melee=melee
        self.range=range
        self.magic=magic
        self.remove=remove
        self.hasFired = hasFired
        self.clickPosition = clickPosition
        self.particle.recieve(nextPos, nextPosTime, maxVel, maxRange, angle, updateSprite, spriteKey, fps, numRows,
                              numColumns, startRow, startColumn, endRow, endColumn, radius, spriteDictionary)

    def update(self):

        self.particle.update()
        self.setCorrectSpriteState()
        self.checkFireCooldown()
        self.currentTime = time.time()

    def setSpriteState(self,state):
        self.spriteState=state
        if state == 1:    # FIRST HALF OF SPRITE SHEET GOING LEFT

            self.particle.spriteSheet.startRow=1
            self.particle.spriteSheet.endRow=self.particle.spriteSheet.numRows/2
            self.particle.spriteSheet.currentRow -= self.particle.spriteSheet.numRows / 2
        elif state == 2:  # SECOND HALF OF SPRITE SHEET GOING RIGHT

            self.particle.spriteSheet.endRow = self.particle.spriteSheet.numRows
            self.particle.spriteSheet.startRow = self.particle.spriteSheet.numRows / 2 + 1

            self.particle.spriteSheet.currentRow += self.particle.spriteSheet.numRows / 2

        if self.aBack and self.spriteState==1 and self.particle.spriteSheet.startColumn<self.particle.spriteSheet.endColumn:
                self.particle.spriteSheet.startColumn=self.particle.spriteSheet.numColumns
                self.particle.spriteSheet.endColumn=self.particle.spriteSheet.numColumns-self.particle.spriteSheet.endColumn
        elif not self.aBack and self.spriteState==1 and self.particle.spriteSheet.startColumn>self.particle.spriteSheet.endColumn:
            self.particle.spriteSheet.startColumn = 1
            self.particle.spriteSheet.endColumn = self.particle.spriteSheet.numColumns - self.particle.spriteSheet.endColumn
        elif not self.aBack and self.spriteState == 2 and self.particle.spriteSheet.startColumn < self.particle.spriteSheet.endColumn:
            self.particle.spriteSheet.startColumn = self.particle.spriteSheet.numColumns
            self.particle.spriteSheet.endColumn = self.particle.spriteSheet.numColumns - self.particle.spriteSheet.endColumn
        elif self.aBack and self.spriteState == 2 and self.particle.spriteSheet.startColumn > self.particle.spriteSheet.endColumn:
            self.particle.spriteSheet.startColumn = 1
            self.particle.spriteSheet.endColumn = self.particle.spriteSheet.numColumns - self.particle.spriteSheet.endColumn

    def draw(self, canvas, cam):

        self.particle.draw(canvas, cam)
        if SHOW_MONSTER_THOUGHTS:
            ratio = cam.ratioToCam()

            percentage=-self.life/self.totalLife
            simplegui_lib_draw.draw_rect(canvas, self.particle.pos.copy().add(Vector(0,-100)).transformToCam(cam).getP(),
                                         Vector(100,20).multiplyVector(Vector(percentage,0.2)).multiplyVector(ratio).getP(), 1, 'Red', fill_color='red')




        if SHOW_MONSTER_THOUGHTS:
            ratio = cam.ratioToCam()

            radius1 = int(self.attackRange * ratio.getX())
            radius2 = int(self.followDistance * ratio.getX())
            canvas.draw_circle(self.particle.pos.copy().transformToCam(cam).getP(), radius1, 1, 'Red')
            canvas.draw_circle(self.particle.pos.copy().transformToCam(cam).getP(), radius2, 1, 'Pink')
            simplegui_lib_draw.draw_rect(canvas, self.operationOrigin.copy().transformToCam(cam).subtract(
                self.operationRange.copy().multiplyVector(ratio)).getP(),
                                         self.operationRange.copy().add(self.operationRange).multiplyVector(ratio).getP(), 1, 'White', fill_color=None)

    def move(self, pos):
        self.particle.move(pos)

    def checkFireCooldown(self):
        if self.hasFired:
            self.fireCooldown+=time.time()-self.currentTime
            if self.fireCooldown>5:
                self.hasFired=False
                self.fireCooldown=0

    def turn(self, angle):
        self.particle.angle += angle

    def setCorrectSpriteState(self):
        if self.particle.pos.getX()-self.particle.nextPos.getX()<0 and not self.spriteState==2:
            self.setSpriteState(2)
        elif self.particle.pos.getX()-self.particle.nextPos.getX()>0 and not self.spriteState==1:
            self.setSpriteState(1)
    def encode(self):
        data = {'spriteState': self.spriteState,
                'clickPosition': {'x': self.clickPosition.x, 'y': self.clickPosition.y}, 'hasFired': self.hasFired,
                'idObject': self.idObject, 'idClass': self.idClass,
                'pos': {'x': self.particle.pos.x, 'y': self.particle.pos.y},
                'vel': {'x': self.particle.vel.x, 'y': self.particle.vel.y}, 'maxVel': self.particle.maxVel,
                'angle': self.particle.angle, 'radius': self.particle.radius, 'spriteKey': self.particle.spriteKey,
                'currentTime': self.currentTime,
                'nextPos': {'x': self.particle.nextPos.x, 'y': self.particle.nextPos.y},
                'nextPosTime': self.particle.nextPosTime,
                'fps': self.particle.spriteSheet.fps, 'remove': self.remove,
                'updateSprite': self.particle.updateSprite, 'maxRange': self.particle.maxRange,
                'numColumns': self.particle.spriteSheet.numColumns,
                'numRows': self.particle.spriteSheet.numRows, 'startColumn': self.particle.spriteSheet.startColumn,
                'startRow': self.particle.spriteSheet.startRow, 'endRow': self.particle.spriteSheet.endRow,
                'endColumn': self.particle.spriteSheet.endColumn,
                'magic':self.magic,'melee':self.melee,'range':self.range,'life':self.life,'tier':self.tier,'aBack':self.aBack,
                'external':True,'totalLife':self.totalLife,'operationOrigin':{'x':self.operationOrigin.x,'y':self.operationOrigin.y},'operationRange':{'x':self.operationRange.x,'y':self.operationRange.y},
                'attackRange':self.attackRange,'followDistance':self.followDistance}
        b=json.dumps(data)
        return data
