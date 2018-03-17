from Classes.Settings import MAP_WIDTH, MAP_HEIGHT,SHOW_COLLISION_TECH
from Loading.Objects import monster_set, monster_set_external, player_list, playerId, env_l2_list,weapon_set,weapon_set_external
from Classes.Functions.Collisions.Collisions import doCirclesIntersect

# CLASS DESCRIPTION:
# Takes care of any action that contains any sort of collisions, this means drawing objects as they collide with trees radius and drawing is decided upon who hits who...
# perhaps not the best structure as i'm writing this on the fly and don't have time to thing about better structuring.
# AS WE HAVE TWO PLAYERS ON DIFFERENT MACHINES WE HAVE TO DECIDE WHO CALCULATES WHAT COLLISIONS...

# PREDIFINED RULES THAT I HAVE NO TIME TO CHECK BUT HOPE THEY WORKOUT :D
# ACTIONS TAKEN ON ONLY LOCAL OBJECTS (MODIFICATIONS)
# ALL LOCAL AND EXTERNAL PROJECTILES CHECKED AGAINST LOCAL MONSTERS ONLY, LOCAL MONSTERS AND PROJECTILES TO BE MODIFIED
# ALL LOCAL AND EXTERNAL PARTICLE CONAINING OBJECTS ARE TO BE CHECKED AGAINST ENVIRONMENT FOR DECIDING WHAT IS DRAWN FIRST :D THIS WILL BE FUN
# DAMAGE ONLY APPLIED ON LOCAL ITEMS AS EXTERNAL ONES WILL BE TAKEN CARE OF BY OTHER MACHINE. THIS INCLUDES PLAYER AND LOCAL MONSTERS.

# CLASS BROKEN INTO THREE FUNCTIONS FOR COLLISIONS:
# FUNCTION FOR DECISION ON WHAT IS DRAWN FIRST
# FUNCTION FOR DECISION OF WHAT COLLIDES WITH MONSTERS AND PLAYER TO APPLY RELEVANT DAMADGE AND ANIMATION
# PERHAPS ANOTHER FUNCTION FOR HOUSE, HOWEVER THIS CAN BE THOUGHT OF AFTER WE FINISH IF FPS IS A PROBLEM OR NOT.

import time
class BroadPhaseCollision:

    def __init__(self, gridWidth, gridHeight):
        # CREATE A LIST REPRESENTING A GRID EACH CELL 200X200PX,EACH ENTRY IS A POINT
        self.grid = []
        self.cam=0
        self.canvas=0
        self.rangeX = MAP_WIDTH // gridWidth
        self.rangeY = MAP_HEIGHT // gridHeight
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.imunity=0 # make local monsters temporarily imune (like 0.2 seconds, in order to make sure arrow/magic is cleared after being used...
        # initialisation
        for i in range(0, self.rangeX + 2):
            x = []
            self.grid.append(x)
            for j in range(0, self.rangeY + 2):
                y = []
                self.grid[i].append(y)
        # populate with permanent env_l2_list

    def update(self,canvas,cam):
        self.cam=cam
        self.canvas=canvas
        # LOAD SETS WHICH WILL HAVE COLLISIONS INTO THE LIST VIA THEIR CLASS TYPES I.E. SUPER OR MIDDLE
        self.populate()
        self.checkCollision()
        self.clear()


    def populate(self):
        for player in player_list:
            if player.idObject==playerId:
                self.addToRelevant(player,player.particle.pos,player.particle.radius)
        self.populateGridSuper(monster_set)
        self.populateGridSuper(monster_set_external)
        self.populateGridSuper(weapon_set_external)
        self.populateGridSuper(weapon_set)
        self.populateGridBase(env_l2_list)

    def checkInteractionBaseRemoved(self,object,i,j): #this is a collision between an Env object and anything else, we are only checking which to draw first :D, so no need for checking details in collision, we just want to know if they are close or not
        for object2 in self.grid[i][j]:
            if object2.idClass==2:
                if object2.pos.getY()>object.pos.getY():
                    object.drawn=True
            else:
                if SHOW_COLLISION_TECH:
                    ratio = self.cam.ratioToCam()
                    radius = object2.particle.radius * ratio.getX()
                    self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(), radius, 1, 'White')
                    radius = object.radius * ratio.getX()
                    self.canvas.draw_circle(object.pos.copy().transformToCam(self.cam).getP(), radius, 1,
                                            'white')

                if doCirclesIntersect(object2.particle.pos,object2.particle.radius,object.pos,object.radius):
                    object.drawn=True
                    if SHOW_COLLISION_TECH:
                        ratio = self.cam.ratioToCam()
                        radius = object.radius * ratio.getX()
                        self.canvas.draw_circle(object.pos.copy().transformToCam(self.cam).getP(), radius, 1, 'Red')


    def checkInteractionBase(self,object,i,j):
        #is the length of that array position still greater than 1?
        idObject=object.idObject
        if self.grid[i][j+1].__len__()>1:
            for object2 in self.grid[i][j+1]:
                if object2.idObject==idObject:
                    self.grid[i][j+1].remove(object2)
                    self.checkInteractionBaseRemoved(object,i,j+1)

        if self.grid[i+1][j].__len__() > 1:
            for object2 in self.grid[i+1][j]:
                if object2.idObject==idObject:
                    self.grid[i+1][j].remove(object2)
                    self.checkInteractionBaseRemoved(object,i+1,j)

        if self.grid[i+1][j + 1].__len__() > 1:
            for object2 in self.grid[i+1][j+1]:
                if object2.idObject==idObject:
                    self.grid[i+1][j+1].remove(object2)
                    self.checkInteractionBaseRemoved(object,i+1,j+1)

        if self.grid[i][j].__len__()>1: #check the following locations for collisions if the len is greater than 1: y,x  y+1,x   y,x+1   x+1,y+1, if object is present check all colisions, and remove object
            for object2 in self.grid[i][j]:
                if object2.idObject==idObject:
                    self.grid[i][j].remove(object2)
                    self.checkInteractionBaseRemoved(object,i,j)

    def checkInteractionSuperRemoved(self,object,i,j):# here we only recieve super classes, if it's weapon, check against player, monster external and internal and if there is a collision apply appropriate action only on internal (not recieved from ohter player), mark the weapon as used
        #idClass:
        # 5=weapon
        # 4=monster
        # 3=player
        if not object.applied:# if the weapon has already damaged pass
            for object2 in self.grid[i][j]:
                if object2.idClass==2:
                    pass
                elif object2.idClass==3: # a weapon hits a player
                    if object2.idObject==playerId:#local player close to projectile:
                        if doCirclesIntersect(object.particle.pos,object.particle.radius,object2.particle.pos,object2.particle.radius): #weapon hit local player: ig
                            object2.life-=object.damage #adjust life of player
                            object.particle.vel.multiply(0)#terminate velocity if projectile
                            object.particle.nextPos=object.particle.pos
                            object.particle.nextPosTime=time.time()
                            object.applied=True #terminate damage of weapon in case of future collisions

                            if SHOW_COLLISION_TECH: #draw collision for visual confirmation
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius,
                                                        1, 'red')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius, 1,
                                                        'red')

                        else:
                            if SHOW_COLLISION_TECH:
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(), radius,
                                                        1, 'White')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(), radius, 1,
                                                        'white')
                    else: #object hits enemy player (remember to remove it lol :D
                        if doCirclesIntersect(object.particle.pos, object.particle.radius, object2.particle.pos,
                                              object2.particle.radius):  # weapon hit local player: ig
                            object2.life -= object.damage  # adjust life of player (pretend)
                            object.particle.vel.multiply(0)  # terminate velocity if projectile
                            object.particle.nextPos = object.particle.pos
                            object.particle.nextPosTime = time.time()

                            object.applied = True  # terminate damage of weapon in case of future collisions
                            if SHOW_COLLISION_TECH:  # draw collision for visual confirmation
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius,
                                                        1, 'red')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius, 1,
                                                        'red')
                        else:
                            if SHOW_COLLISION_TECH:
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius,
                                                        1, 'White')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius, 1,
                                                        'white')

                elif object2.idClass==4:# a weapon hits a monster:
                    if not object2.external: # if the monster is local
                        if doCirclesIntersect(object2.particle.pos,object2.particle.radius,object.particle.pos,object.particle.radius): #weapon hit local monster

                            object2.life -= object.damage  # adjust life of monster
                            object.particle.vel.multiply(0)  # terminate velocity if projectile
                            object.particle.nextPos = object.particle.pos
                            object.particle.nextPosTime = time.time()
                            object.applied = True  # terminate damage of weapon in case of future collisions
                            for player in player_list:
                                if player.idObject==playerId:

                                    if object.idPlayer==playerId:#the collision happened with local players weapon

                                        if object2.life<0:
                                            object2.remove=True
                                            player.magic+=object2.magic/10
                                            player.melee+=object2.melee/10
                                            player.totalLife+=object2.totalLife/10
                                            player.range+=object2.range/10
                                    else:# if collision happened with other player: just check for monsters life and remove if necesary
                                        if object2.life<0:
                                            object2.remove=True
                    else:   # if it is external: assume the other party has detected collision, so remove object if intersection and life <0
                        if doCirclesIntersect(object2.particle.pos, object2.particle.radius, object.particle.pos, object.particle.radius):
                            #remove weapon otherwise it will keep hitting our poor monster:D
                            object.particle.vel.multiply(0)  # terminate velocity if projectile
                            object.particle.nextPos = object.particle.pos
                            object.particle.nextPosTime = time.time()
                            object.applied = True # place an applied marker
                            object2.life -= object.damage # apply a pretend damage in case it hasent been removed ( not updated by other party, this way things are 100% removed)
                            for player in player_list:# if local player kills external monster give him the stats, may have buggs, but at this point whatever.
                                if player.idObject == playerId:
                                    if object.idPlayer==playerId:  # the collision happened with this players weapon
                                        if object2.life < 0:
                                            object2.remove = True
                                            player.magic += object2.magic / 10
                                            player.melee += object2.melee / 10
                                            player.totalLife += object2.totalLife / 10
                                            player.range += object2.range / 10
                            if SHOW_COLLISION_TECH:  # draw collision for visual confirmation
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius,
                                                        1, 'red')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius, 1,
                                                        'red')
                        else:
                            if SHOW_COLLISION_TECH:
                                ratio = self.cam.ratioToCam()
                                radius = object2.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object2.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius,
                                                        1, 'White')
                                radius = object.particle.radius * ratio.getX()
                                self.canvas.draw_circle(object.particle.pos.copy().transformToCam(self.cam).getP(),
                                                        radius, 1,
                                                        'white')

    def checkInteractionSuper(self,object,i,j):
        # is the length of that array position still greater than 1?
        idObject = object.idObject
        if self.grid[i][j + 1].__len__() > 1:
            for object2 in self.grid[i][j + 1]:
                if object2.idClass ==5:                         # only check for interactions with weapons and other stuff
                    if object2.particle.idObject == idObject:
                        self.grid[i][j + 1].remove(object2)
                        self.checkInteractionSuperRemoved(object, i, j + 1)

        if self.grid[i + 1][j].__len__() > 1:
            for object2 in self.grid[i + 1][j]:
                if object2.idClass == 5:
                    if object2.particle.idObject == idObject:
                        self.grid[i + 1][j].remove(object2)
                        self.checkInteractionSuperRemoved(object, i + 1, j)

        if self.grid[i + 1][j + 1].__len__() > 1:
            for object2 in self.grid[i + 1][j + 1]:
                if object2.idClass ==5:
                    if object2.particle.idObject == idObject:
                        self.grid[i + 1][j + 1].remove(object2)
                        self.checkInteractionSuperRemoved(object, i + 1, j + 1)

        if self.grid[i][j].__len__() > 1:  # check the following locations for collisions if the len is greater than 1: y,x  y+1,x   y,x+1   x+1,y+1, if object is present check all colisions, and remove object
            for object2 in self.grid[i][j]:
                if object2.idClass ==5 :
                    if object2.particle.idObject == idObject:
                        self.grid[i][j].remove(object2)
                        self.checkInteractionSuperRemoved(object, i, j)
    def checkCollision(self):
        for i in range(0,self.rangeX):
            for j in range(0,self.rangeY):
                if self.grid[i][j].__len__()>1:
                    for object in self.grid[i][j]:
                        if object.idClass==2:           #a particle
                            self.checkInteractionBase(object,i,j)
                        elif object.idClass==5:                            # only require collisions between weapon and other objects as there are flying monsters and those are random so we shall avoid extra trouble
                            self.checkInteractionSuper(object,i,j)

    def clear(self):
        for monster in monster_set_external:
            monster.hitByWeapon=0
        for i in range(0, self.rangeX):
            for j in range(0, self.rangeY):
                self.grid[i][j].clear()

    def checkInside(self, x, y):
        if x > MAP_WIDTH or x < 0 or y > MAP_HEIGHT or y < 0:
            return False
        return True

    def populateGridSuper(self,super):  # takes a super class of particle so to get position by which we populate we do super.particle.pos.getX()//self.gridWidth
        for object in super:
            if self.checkInside(object.particle.pos.getX(), object.particle.pos.getY()):
                self.addToRelevant(object,object.particle.pos,object.particle.radius)
                # place in relevant location of array.

    def populateGridBase(self, base):
        for object in base:
            if self.checkInside(object.pos.getX(), object.pos.getY()):
                self.addToRelevant(object,object.pos,object.radius)

    def addToRelevant(self, object, origin, radius):
        x = origin.getX()
        y = origin.getY()
        x1 = int((x - radius) // self.gridWidth)
        x2 = int((x + radius) // self.gridWidth)
        y1 = int((y - radius) // self.gridHeight)
        y2 = int((y + radius) // self.gridHeight)
        if y1> self.rangeY or x1>self.rangeX or y1<0 or x1<0:

            pass
        else:

            if (x1 != x2 and y1 != y2):
                self.grid[x1][y1].append(object)
                self.grid[x1][y2].append(object)
                self.grid[x2][y1].append(object)
                self.grid[x2][y2].append(object)

            elif (x1 == x2 and y1 != y2):
                self.grid[x1][y1].append(object)
                self.grid[x1][y2].append(object)

            elif (x1 != x2 and y1 == y2):
                self.grid[x1][y1].append(object)
                self.grid[x2][y1].append(object)

            else:
                self.grid[x2][y2].append(object)
