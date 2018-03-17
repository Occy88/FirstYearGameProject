# REMEMBER: SIMULATE YOUR SHOT AGAINST MONSTER TO CHECK IF KILLED, IF SO, ADD STATS TO PLAYER, THE MONSTER WILL BE REMOVED ON THE OTHER SIDE

import time
import random
from Classes.Base.Vector import Vector
from Loading.RandomGen import getRandomMagicWeapon, getRandomMagicCast, getRandomMonster
from Classes.Super.Weapon import Weapon
from Classes.Middle.Particle import Particle
from Classes.Super.Monster import Monster
from Loading.Objects import weapon_set, visual_set, spriteDictionary, getUid, playerId
from Classes.Settings import MAP_WIDTH, MAP_HEIGHT

# monsters spawned based on how far away from the map they are.
# respawn by tier time

from Loading.Objects import monster_set, player_list
from Classes.Functions.Collisions.Collisions import doCirclesIntersect, isPointInRect, isCircleInRect


class MonsterAi:
    def __init__(self, numMonsters):
        self.tier1Total = int(numMonsters * 1)
        self.tier2Total = int(numMonsters * 0.4)
        self.tier3Total = int(numMonsters * 0.3)
        self.tier1Current = 0
        self.tier2Current = 0
        self.tier3Current = 0
        self.tier1SpawnRate = 60
        self.tier2SpawnRate = 200
        self.tier3SpawnRate = 500
        self.tier3Respawn = 0
        self.tier2Respawn = 0
        self.tier1Respawn = 0
        self.timeElapsed = 0
        self.currentTime = time.time()
        self.updateStatsTime = 0
        self.moveMonstersTime = 20

        self.updateTime = 0.1

    def update(self):
        self.updateCountdowns()
        if self.updateTime > 0.1:
            self.moveMonsters()
            self.attack()
            self.respawn()
            self.updateTime = 0

        if self.updateStatsTime > 100:
            self.updateNum()
            self.updateStatsTime = 0
        self.currentTime = time.time()

    def respawn(self):
        if self.tier1Respawn > self.tier1SpawnRate and self.tier1Current < self.tier1Total:
            self.tier1Respawn = 0
            self.spawnT1()
        if self.tier2Respawn > self.tier2SpawnRate and self.tier2Current < self.tier2Total:
            self.tier2Respawn = 0
            self.spawnT2()
        if self.tier3Respawn > self.tier3SpawnRate and self.tier3Current < self.tier3Total:
            self.tier3Respawn = 0
            self.spawnT3()

    def spawnMonsters(self):
        t1 = self.tier1Total
        t2 = self.tier2Total
        t3 = self.tier3Total
        for a in range(0, t1):
            self.spawnT1()
        for a in range(0, t2):
            self.spawnT2()
        for a in range(0, t3):
            self.spawnT3()

        #  print(monster.spriteState)

    def updateCountdowns(self):
        difference = time.time() - self.currentTime

        self.updateStatsTime += difference
        self.moveMonstersTime += difference
        self.tier1Respawn += difference
        self.tier2Respawn += difference
        self.tier3Respawn += difference
        self.updateTime += difference

    def returnMonster(self, monster):
        px = random.randrange(int(monster.operationOrigin.getX() - monster.operationRange.getX()),
                              int(monster.operationOrigin.getX() + monster.operationRange.getX()))
        py = random.randrange(int(monster.operationOrigin.getY() - monster.operationRange.getY()),
                              int(monster.operationOrigin.getY() + monster.operationRange.getY()))
        if px > MAP_WIDTH:
            px = MAP_WIDTH
        if px < 0:
            px = 0
        if py > MAP_HEIGHT:
            py = MAP_HEIGHT
        if py < 0:
            py = 0
        monster.particle.move(Vector(px, py))

    def moveMonsters(self):
        # CHOOSE A RANDOM POINT WITHIN OPERATING RANGE OF MONSTER AND MOVE THE MONSTER TO THAT LOCATION IF THE VELOCITY IS 0 and not fierin
        if self.moveMonstersTime > 5:
            for monster in monster_set:
                num = random.randrange(1, 3)
                if num == 1 and not monster.hasFired and monster.particle.vel.getX() == 0 and monster.particle.vel.getY() == 0:
                    px = random.randrange(int(monster.operationOrigin.getX() - monster.operationRange.getX()),
                                          int(monster.operationOrigin.getX() + monster.operationRange.getX()))
                    py = random.randrange(int(monster.operationOrigin.getY() - monster.operationRange.getY()),
                                          int(monster.operationOrigin.getY() + monster.operationRange.getY()))
                    if px > MAP_WIDTH:
                        px = MAP_WIDTH
                    if px < 0:
                        px = 0
                    if py > MAP_HEIGHT:
                        py = MAP_HEIGHT
                    if py < 0:
                        py = 0
                    monster.particle.move(Vector(px, py))
            self.moveMonstersTime = 0

    def updateNum(self):
        self.tier1Current = 0
        self.tier2Current = 0
        self.tier3Current = 0
        for monster in monster_set:

            if monster.tier == 1:
                self.tier1Current += 1
            elif monster.tier == 2:
                self.tier2Current += 1
            elif monster.tier == 3:
                self.tier3Current += 1

    def attack(self):
        # VERY SIMPLE AI, IF MONSTER WITHIN OPERATION RANGE AND WITHIN ATTACK RANGE ATTACK AND KEEP RANGE IF MONSTER OUT OF OPERATION RANGE ==> IGNORE
        # ONLY TAKE CARE OF LOCAL MONSTER SET, NOT EXTERNAL, BUT ATTACK BOTH PLAYERS

        for monster in monster_set:
            if not monster.hasFired:
                # SLIGHTLY LONG, JUST CHECKING IF WITHIN BOUNDARY OF OPERATION RECT
                if isCircleInRect(monster.particle.pos, monster.followDistance, monster.operationOrigin,
                                  monster.operationRange) and not monster.returning:
                    # print("within rect")
                    # CHECK IF PLAYEisCircleInRectR WITHIN ATTACK RANGE:
                    for player in player_list:
                        # CHECK IF SELF FOLLOW DISTANCE IS IN RANGE OF PLAYER AND IF SELF MAGIC IS GREATER (WEAKER DON'T ATTACK BUT DO RETALIATE)
                        #THEN CHECK FOR WITHIN ATTACK RANGE

                        if doCirclesIntersect(monster.particle.pos, monster.followDistance, player.particle.pos,
                                              player.particle.radius) and monster.magic>player.magic:
                            monster.particle.keepRange(player.particle.pos,
                                                       monster.attackRange)  # artbitrary distance at which to keep range by monster tier
                            print("intercection follow ",monster.particle.pos," , ", monster.followDistance," , ", player.particle.pos," , ",
                                              player.particle.radius)
                            monster.particle.keepRange(player.particle.pos,
                                                       monster.attackRange)
                            if doCirclesIntersect(monster.particle.pos, monster.attackRange, player.particle.pos,
                                                  player.particle.radius):
                                self.fire(player, monster)
                                print("intercection attack ", monster.particle.pos, " , ", monster.attackRange,
                                      " , ", player.particle.pos, " , ",
                                      player.particle.radius)

                else:
                    monster.returning = True
                    if not monster.hasSelectedReturn:
                        self.returnMonster(monster)

                    print("monster returning")
                    if isPointInRect(monster.particle.pos, monster.operationOrigin, monster.operationRange):
                        print("monstere returned")
                        monster.returning = False
                        monster.hasSelectedReturn = False

                # IF HEALTH IS LOWER THAN PREVIOUS GENERATION I.E. ATTACKED, THEN RETALIATE ON CLOSEST OPPONENT
                d1 = 0
                d2 = 0
                if monster.lifePrev > monster.life:
                    monster.lifePrev=monster.life
                    for player in player_list:
                        if player.idObject == playerId:

                            d1 = monster.particle.pos.copy().distanceTo(player.particle.pos)
                        else:

                            d2 = monster.particle.pos.copy().distanceTo(player.particle.pos)
                    for player in player_list:
                        if player.idObject == playerId and d1 < d2:

                            monster.particle.keepRange(player.particle.pos, monster.followDistance)
                            self.fire(player, monster)
                        elif player.idObject != playerId and d2 < d1:
                            self.fire(player, monster)

                            monster.particle.keepRange(player.particle.pos, monster.followDistance)

    def fire(self, player, monster):
        # THIS IS ESSENTIALLY COPPIED FROM CLICK HANDLER AND IMPLEMENTED FOR MONSTER ONCE IT CHOOSES A TARGET :d, NO TIME TO MAKE IT NICER ON BOTH ENDS AND OPTIMIZE UNFORTUNATELY
        # SET MAGIC SPRITE ATTACK ANIMATION
        numRows, numCol, startRow, startCol, endRow, endCol, key = getRandomMagicWeapon(monster.magic)
        # SET MAGIC SPRITE WEAPON WITH The above
        precisionX = random.randrange(0, 90)
        precisionY = random.randrange(0, 90)
        precisionY -= 45
        precisionX -= 45
        pos = player.particle.pos.copy().add(Vector(precisionX, precisionY))
        radius = 0
        if monster.magic < 500:
            radius = 15
        if monster.magic < 1000 and radius == 0:
            radius = 20
        if monster.magic < 5000 and radius == 0:
            radius = 25
        if monster.magic < 20000 and radius == 0:
            radius = 30
        if monster.magic < 50000 and radius == 0:
            radius = 35
        if monster.magic > 50000 and radius == 0:
            radius = 40

        weapon = Weapon(pos, Vector(0, 0), 0,
                        pos, 0, 0, radius, key, spriteDictionary,
                        20, getUid(), numRows, numCol, startRow, startCol, endRow, endCol, False, True, monster.magic)
        # BIND SPRITE TO MONSTER and MONSTER TO SPRITE to remember who kills who
        weapon.idPlayer = monster.idObject
        weapon_set.add(weapon)

        # SET MAGIC SPRITE CASTING ANIMATION USE PARTICLE CLASS ADD TO VISUAL SET
        # SHIFT ALL MAGIC SPRITES UP FOR MONSTER IF SMALL
        pos = monster.particle.pos.copy()
        if monster.particle.dim.getY() < 120:
            pos.y -= 30
        numRows, numCol, startRow, startCol, endRow, endCol, key = getRandomMagicCast(monster.magic)
        particle = Particle(True, pos, Vector(0, 0), 0, pos, 0, 0, 0, 0, key, spriteDictionary, 15, False, True,
                            getUid(), numRows, numCol, startRow, startCol, endRow, endCol)
        visual_set.add(particle)

        monster.particle.vel.multiply(0)
        monster.particle.nextPosTime = time.time()
        monster.particle.nextPos = monster.particle.pos
        monster.hasFired = True

    def spawnT1(
            self):  # WITHIN 25% OF MAP CENTER, OPERATION RANGE OF 1000, ATTACK RANGE OF 500 t1, 1500,t2, 2500 t3? for lols
        # the following locations on the map X axis and y axis randomly:   \_________XXXXXX___________\
        pos = Vector(random.randint(int(MAP_WIDTH / 2 - MAP_WIDTH / 3), int(MAP_WIDTH / 2 + MAP_WIDTH / 3)),
                     random.randint(int(MAP_HEIGHT / 2 - MAP_HEIGHT / 3), int(MAP_HEIGHT / 2 + MAP_HEIGHT / 3)))
        vel = Vector(0, 0)
        maxVel = 100  # why not

        aBack, numRows, numCol, startRow, startCol, endRow, endCol, key = getRandomMonster(1)
        monster = Monster(pos, vel, 0, pos, maxVel, 0, 50, key, spriteDictionary, 15, getUid(), False, Vector(0, 0), 1,
                          numRows, numCol, startRow, startCol, endRow, endCol, 1, aBack, False,
                          random.randrange(6000, 10000), pos.copy(),
                          pos.copy().normalize().multiply(1000), 200, 500)

        monster.setSpriteState(2)

        monster.totalLife = monster.life
        monster.magic = random.randrange(200, 1000)
        monster.range = random.randrange(200, 1000)
        monster_set.add(monster)

    def spawnT2(
            self):  # WITHIN 25-75% OF MAP CENTER, OPERATION RANGE OF 3000, ATTACK RANGE OF 500 t1, 1500,t2, 2500 t3? for lols
        topBand = Vector(random.randrange(0, int(MAP_WIDTH)),
                         random.randrange(int(MAP_HEIGHT * 0.1), int(MAP_HEIGHT * 0.25)))  # bottom 25% of map

        bottomBand = Vector(random.randrange(0, int(MAP_WIDTH)),
                            random.randrange(int(MAP_HEIGHT * 0.75), int(MAP_HEIGHT * 0.9)))  # top 25% of map

        leftBand = Vector(random.randrange(int(MAP_WIDTH * 0.1), int(MAP_WIDTH * 0.25)),
                          random.randrange(0, int(MAP_HEIGHT)))  # left 25% of map

        rightBand = Vector(random.randrange(int(MAP_WIDTH * 0.75), int(MAP_WIDTH * 0.9)),
                           random.randrange(0, int(MAP_HEIGHT)))  # right 25% of map

        num = random.randrange(0, 400)
        if num > 300:
            pos = topBand
        elif num > 200:
            pos = bottomBand
        elif num > 100:
            pos = leftBand
        else:
            pos = rightBand

        maxVel = 120  # why not
        vel = Vector(0, 0)

        aBack, numRows, numCol, startRow, startCol, endRow, endCol, key = getRandomMonster(2)
        monster = Monster(pos, vel, 0, pos, maxVel, 0, 75, key, spriteDictionary, 15, getUid(), False, Vector(0, 0), 1,
                          numRows, numCol, startRow, startCol, endRow, endCol, 2, aBack, False,
                          random.randrange(50000, 300000),pos.copy(),pos.copy().normalize().multiply(1000), 300, 700 )
        monster.setSpriteState(2)

        monster.totalLife = monster.life
        monster.magic = random.randrange(10000, 30000)
        monster.range = random.randrange(10000, 30000)

        monster_set.add(monster)

    def spawnT3(
            self):  # WITHIN 25% OF MAP CENTER, OPERATION RANGE OF 1000, ATTACK RANGE OF 500 t1, 1500,t2, 2500 t3? for lols

        topBand = Vector(random.randrange(0, int(MAP_WIDTH)),
                         random.randrange(0, int(MAP_HEIGHT * 0.15)))  # bottom 25% of map

        bottomBand = Vector(random.randrange(0, int(MAP_WIDTH)),
                            random.randrange(int(MAP_HEIGHT * 0.85), int(MAP_HEIGHT)))  # top 25% of map

        leftBand = Vector(random.randrange(0, int(MAP_WIDTH * 0.15)),
                          random.randrange(0, int(MAP_HEIGHT)))  # left 25% of map

        rightBand = Vector(random.randrange(int(MAP_WIDTH * 0.85), int(MAP_WIDTH)),
                           random.randrange(0, int(MAP_HEIGHT)))  # right 25% of map

        num = random.randrange(0, 400)
        if num > 300:
            pos = topBand
        elif num > 200:
            pos = bottomBand
        elif num > 100:
            pos = leftBand
        else:
            pos = rightBand

        # the following locations on the map X axis and y axis randomly:   \XXXXX______________________XXXXX\
        vel = Vector(0, 0)
        maxVel = 200  # why not
        aBack, numRows, numCol, startRow, startCol, endRow, endCol, key = getRandomMonster(3)
        monster = Monster(pos, vel, 0, pos, maxVel, 0, 100, key, spriteDictionary, 15, getUid(), False, Vector(0, 0), 1,
                          numRows, numCol, startRow, startCol, endRow, endCol, 3, aBack, False,
                          random.randrange(500000, 1000000),pos.copy(),pos.copy().normalize().multiply(1000), 500, 1000
                          )
        monster.setSpriteState(2)

        monster.life = random.randrange(500000, 1000000)
        monster.totalLife = monster.life
        monster.magic = random.randrange(50000, 100000)

        monster.operationOrigin = pos.copy()

        monster_set.add(monster)
