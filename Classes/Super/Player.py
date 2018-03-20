import time, configparser

from Classes.Middle.Particle import Particle

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
import json

class Player:
    def __init__(self, pos, vel, nextPosTime, nextPos, maxVel, angle, radius, spriteKey, spriteDictionary, spriteFps,
                 idObject, hasFired,
                 clickPosition, spriteState, numRows, numColumns, startRow, startColumn, endRow, endColumn):
        # id's
        self.remove = False
        self.idClass = 3
        self.idObject = idObject

        # vectors
        self.clickPosition = clickPosition
        # Sprite Attributes
        self.spriteState = spriteState
        self.currentTime = 0
        self.hasFired = hasFired

        self.totalLife=10000000000
        self.life = 10000000000
        self.range = 90000
        self.melee = 90000 #OPTIONAL,NOT IMPLEMENTED (REQUIRES SPRITE STATES AND MORE TIME)
        self.magic = 90000
        self.weapon=1
        # sub class
        self.particle = Particle(True, pos, vel, nextPosTime, nextPos, maxVel, 0, angle, radius, spriteKey,
                                 spriteDictionary, spriteFps,
                                 False, False, self.idObject, numRows, numColumns, startRow, startColumn, endRow,
                                 endColumn)

    def recieve(self, hasFired, clickPosition, nextPos, nextPosTime, maxVel, maxRange, angle, updateSprite, spriteKey,
                fps, numRows, numColumns, startRow, startColumn, endRow, endColumn, radius, spriteDictionary, life,
                range, melee, magic):

        self.life = life
        self.melee = melee
        self.range = range
        self.magic = magic
        self.hasFired = hasFired
        self.clickPosition = clickPosition
        self.particle.recieve(nextPos, nextPosTime, maxVel, maxRange, angle, updateSprite, spriteKey, fps, numRows,
                              numColumns, startRow, startColumn, endRow, endColumn, radius, spriteDictionary)



    def update(self):
        self.particle.update()
        self.setCorrectSpriteState()
        self.currentTime = time.time()

    def draw(self, canvas, cam):
        self.particle.draw(canvas, cam)

    def move(self, pos):
        self.particle.move(pos)

    def setCorrectSpriteState(self):
        if self.spriteState == 0:
            self.setCorrectAnimation(1)
        # CORRECT SPRITE ROW AND UPDATE FPS
        if self.hasFired and self.particle.spriteSheet.hasLooped:
            self.hasFired = False
            self.setCorrectAnimation(1)

        if self.particle.vel.getX() == 0 and self.particle.vel.getY() == 0 and not self.hasFired:
            self.particle.spriteSheet.currentColumn = 1



    def setCorrectAnimation(self,action):
        if action==1:
            self.particle.spriteSheet.fps=20
        if action==2:
            self.particle.spriteSheet.fps=30
        if action==3:
            self.particle.spriteSheet.fps=5
        x, y = self.particle.pos.copy().distanceToVector(self.clickPosition)
        if y < 0:
            if action==2:
                self.setSpriteState(6)
            elif action==3:
                self.setSpriteState(11)
            else:
                self.setSpriteState(3)

        if y > 0:
            if action==2:
                self.setSpriteState(8)
            elif action==3:
                self.setSpriteState(9)
            else:
                self.setSpriteState(1)

        if y != 0:
            if (x + y) / y > 2 and y < 0:
                if action==2:
                    self.setSpriteState(5)
                elif action==3:
                    self.setSpriteState(12)
                else:
                    self.setSpriteState(4)

            if (x + y) / y < 0 and y < 0:
                if action==2:
                    self.setSpriteState(7)
                elif action==3:
                    self.setSpriteState(10)

                else:
                    self.setSpriteState(2)

    def walkUp(self):
        self.particle.spriteSheet.setRow(21, 13, 9, 1, 9, 9)

    def walkLeft(self):
        self.particle.spriteSheet.setRow(21, 13, 10, 1, 10, 9)

    def walkDown(self):
        self.particle.spriteSheet.setRow(21, 13, 11, 1, 11, 9)

    def walkRight(self):
        self.particle.spriteSheet.setRow(21, 13, 12, 1, 12, 9)

    def fireRight(self):
        self.particle.spriteSheet.setRow(21, 13, 20, 1, 20, 13)

    def fireDown(self):
        self.particle.spriteSheet.setRow(21, 13, 19, 1, 19, 13)

    def fireLeft(self):
        self.particle.spriteSheet.setRow(21, 13, 18, 1, 18, 13)

    def fireUp(self):
        self.particle.spriteSheet.setRow(21, 13, 17, 1, 17, 13)

    def magicUp(self):
        self.particle.spriteSheet.setRow(21, 13, 1, 1, 1, 7)

    def magicRight(self):
        self.particle.spriteSheet.setRow(21, 13, 4, 1, 4, 7)

    def magicDown(self):
        self.particle.spriteSheet.setRow(21, 13, 3, 1, 3, 7)

    def magicLeft(self):
        self.particle.spriteSheet.setRow(21, 13, 2, 1, 2, 7)

    def setSpriteState(self, id):
        self.spriteState = id
        self.particle.spriteSheet.resetLoop()
        if id == 1:
            self.walkUp()
        elif id == 2:
            self.walkLeft()
        elif id == 3:
            self.walkDown()
        elif id == 4:
            self.walkRight()
        elif id == 5:
            self.fireRight()
        elif id == 6:
            self.fireDown()
        elif id == 7:
            self.fireLeft()
        elif id == 8:
            self.fireUp()
        elif id == 9:
            self.magicUp()
        elif id == 10:
            self.magicLeft()
        elif id == 11:
            self.magicDown()
        elif id == 12:
            self.magicRight()

    def turn(self, angle):
        self.particle.angle += angle

    def encode(self):

        data = {'spriteState': self.spriteState,
                'clickPosition': {'x': self.clickPosition.x, 'y': self.clickPosition.y},
                'hasFired': self.hasFired,
                'idObject': self.idObject,
                'idClass': self.idClass,
                'pos': {'x': self.particle.pos.x, 'y': self.particle.pos.y},
                'vel': {'x': self.particle.vel.x, 'y': self.particle.vel.y},
                'maxVel': self.particle.maxVel,
                'angle': self.particle.angle,
                'radius': self.particle.radius,
                'spriteKey': self.particle.spriteKey,
                'currentTime': self.currentTime,
                'nextPos': {'x': self.particle.nextPos.x, 'y': self.particle.nextPos.y},
                'nextPosTime': self.particle.nextPosTime,
                'fps': self.particle.spriteSheet.fps,
                'remove': self.remove,
                'updateSprite': self.particle.updateSprite,
                'maxRange': self.particle.maxRange,
                'numColumns': self.particle.spriteSheet.numColumns,
                'numRows': self.particle.spriteSheet.numRows,
                'startColumn': self.particle.spriteSheet.startColumn,
                'startRow': self.particle.spriteSheet.startRow,
                'endRow': self.particle.spriteSheet.endRow,
                'endColumn': self.particle.spriteSheet.endColumn,
                'magic': self.magic,
                'melee': self.melee,
                'range': self.range,
                'life': self.life,}
        c=json.dumps(data)
        return data
