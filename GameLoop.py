#    mmm   mmmm  mmm     mmmm   mmmm   mmmm
#  m"   " #"   "   #    #    # "   "# m"  "m
#  #      "#mmm    #    "mmmm"   mmm" #  m #
#  #          "#   #    #   "#     "# #    #
#   "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm#

#LOADING LIBRARIES

import sys, configparser
from SimpleGUICS2Pygame import simplegui_lib_fps
from SimpleGUICS2Pygame import simpleguics2pygame
#LOADING SETTINGS
config = configparser.ConfigParser()
#Open file as writeable
config.read_file(open('Classes/config'))


#Override settings when testing (to make it easier to run multiple instances)
if(len(sys.argv) > 1):
    print("OVERIDING SETTINGS_________________________")
    config['NETWORKING']['CONFIG_TYPE'] = sys.argv[1]

    config.set('NETWORKING', 'CONFIG_TYPE', sys.argv[1])
    with open('Classes/config', "w") as conf:

        config.write(conf) 

#reopen
#config.read_file(open('Classes/config'))

#LOAD INTERNAL CLASSES
from Transfer.comms import communicate, recieve, ping
from Handlers.KeyHandler import keydown, keyup
from Handlers.ClickHandler import checkClick
from Classes.Functions.Collisions.CollisionHandler import BroadPhaseCollision
from Loading.Objects import *
from GameStates.intro import introLoop, waitingLoop
from Loading.MonsterAi import MonsterAi

#-----START----GAME----CLOCK
fps = simplegui_lib_fps.FPS()
fps.start()
collHandler=BroadPhaseCollision(200,200)
#initiate Ai
monsterAi=MonsterAi(0)
print("INITIALISING MONSTER CONTROLLER")
monsterAi=MonsterAi(10)
monsterAi.spawnMonsters()

print("MONSTERS LOADED AND SPAWNED")
# music.play()
# music.rewind()
# music.set_volume(1)

#--------------GAME-----LOOP-------------------
def draw(canvas):


#========== GAME LOOPS NON MAIN =====================

    if(gameState1.intro):
        introLoop(canvas)

    if gameState1.main and not gameState2.main:
        waitingLoop(canvas)


#================= NETWORKING ==============================

#-----------------CLIENT PING-----------------------
   # if (config['NETWORKING']['CONFIG_TYPE'] == 'client'):
    ping()
#--------------RECIEVE ALL OBJECTS-------------------------
    for a in range(0,100):
        recieve()
#-----------------SEND GAME STATES------------------------



    if(gameState1.main and gameState2.main):

    # communicate objects just before garbage collection at end of game loop to ensure all most current
    #data is sent before removal

#================ NETWORKING END ================================

#===================================================================

#================ CLICK HANDLER =================================

        checkClick()

#================ CLICK HANDLER END =================================

#===================================================================

#================ DRAW AND UPDATES =================================

    #  -------UPDATE-AND-DRAW---OBJECTS---BY---LAYER---PRIORITY
        monsterAi.update()
        for pbot in env_l1_set:
            pbot.update()
            pbot.draw(canvas,cam)
        for pbot in env_l3_list:
            pbot.update()
            pbot.draw(canvas,cam)
        for v in visual_set:
            v.update()
            v.draw(canvas,cam)
        for ve in visual_set_external:
            ve.update()
            ve.draw(canvas,cam)

        # ------------place all objects into list to choose which to draw first, not sure if this is expensive, but we shall try-----------



        for en2 in env_l2_list: #draw unmarked objects
            if not en2.drawn:
                en2.draw(canvas, cam)
        for pp in player_list:
            if pp.idObject == playerId:
                cam.origin = pp.particle.pos.copy()
            pp.draw(canvas, cam)
            pp.update()
        # UPDATE those left then reset updates for all
        for w in weapon_set:
            w.draw(canvas,cam)
            w.update()

        for w in weapon_set_external:
            w.draw(canvas,cam)
            w.update()

        for pm in monster_set_external:
            pm.draw(canvas,cam)
            pm.update()

        for pm in monster_set:
            pm.draw(canvas,cam)
            pm.update()

        for en2 in env_l2_list: #draw marked objects and unmark
            if en2.drawn:
                en2.draw(canvas, cam)
                en2.drawn=False
            en2.update()
        fps.draw_fct(canvas)
        collHandler.update(canvas,cam)
#====================== UPDATES DRAWING END =============================================

#===========================SENDING STATES BEFORE GARBAGE COLLECTION=============================================================
        # -----------IN MAIN LOOP NETWORKING-------------------------
        for object in weapon_set:
            # don't communicate it if it has been applied lol otherwise it's like continuous aoe damage good luck with that
            if not object.applied and not object.sent:
                communicate(object)
                object.sent=True
        for monster in monster_set:
            communicate(monster)
        for object in visual_set:
            communicate(object)

        # we don't to thread this as it is a small set
        for player in player_list:
            if player.idObject == playerId:
                communicate(player)


# ===================== GARBAGE REMOVAL =================================================
        removal_set=set()

        #WEAPON CLEANUP (MAGIC, ARROWS)
        for weapon in weapon_set:

            if weapon.particle.pos == weapon.particle.nextPos and weapon.particle.removeOnVelocity0:
                removal_set.add(weapon)

            if weapon.particle.spriteSheet.hasLooped and weapon.particle.removeOnAnimationLoop:
                removal_set.add(weapon)
        weapon_set.difference_update(removal_set)
        removal_set.clear()

        for weapon in weapon_set_external:
            if weapon.particle.pos == weapon.particle.nextPos and weapon.particle.removeOnVelocity0:
                removal_set.add(weapon)
            if weapon.particle.spriteSheet.hasLooped and weapon.particle.removeOnAnimationLoop:
                removal_set.add(weapon)
        weapon_set_external.difference_update(removal_set)
        removal_set.clear()

        #MONSTER_CLEANUP
        for monster in monster_set_external:
            if monster.particle.pos == monster.particle.nextPos and monster.particle.removeOnVelocity0 or monster.remove:
                removal_set.add(monster)
            if monster.particle.spriteSheet.hasLooped and monster.particle.removeOnAnimationLoop:
                removal_set.add(monster)
        monster_set_external.difference_update(removal_set)

        removal_set.clear()
        for monster in monster_set:
            if monster.particle.pos == monster.particle.nextPos and monster.particle.removeOnVelocity0 or monster.remove:
                removal_set.add(monster)
            if monster.particle.spriteSheet.hasLooped and monster.particle.removeOnAnimationLoop:
                removal_set.add(monster)
        monster_set.difference_update(removal_set)
        removal_set.clear()

        #VISUAL SET CLEANUP
        for v in visual_set:
            if v.pos == v.nextPos and v.removeOnVelocity0:
                removal_set.add(v)
            if v.spriteSheet.hasLooped and v.removeOnAnimationLoop:
                removal_set.add(v)
        visual_set.difference_update(removal_set)
        removal_set.clear()

        for v in visual_set_external:
            if v.pos == v.nextPos and v.removeOnVelocity0:
                removal_set.add(v)
            if v.spriteSheet.hasLooped and v.removeOnAnimationLoop:
                removal_set.add(v)
        visual_set_external.difference_update(removal_set)
        removal_set.clear()

# ========================= GARBAGE REMOVAL END ===============================================================

 # ========================================================================================

#  ======================== CAMERA UPDATE ===============================================================

        cam.zoom()
        cam.move(playerId, player_list)

# ========================== CAMERA UPDATE END==============================================================

# ========================================================================================

# ========================== STATS DISPLAY ==============================================================

        #DISPLAY STATS:
        for player in player_list:
            if player.idObject==playerId:
                p1Life=player.life
                p1Magic=player.magic
                p1Range=player.range

                p1Arrows=1
                p1Spells=(p1Magic//3000+3)*2
                if p1Range > 1000:
                    p1Arrows=2
                if p1Range > 10000:
                    p1Arrows=3

                if p1Range > 50000:
                    p1Arrows=4

        canvas.draw_text('Life: '+str(p1Life)+"     Magic: "+str(p1Magic)+"     Range: "+str(p1Range)+"     Arrows: "+str(p1Arrows)+"  Spells: "+str(p1Spells), (0,int(config['CANVAS']['CANVAS_HEIGHT'])-10), 23, "Black")

frame = simpleguics2pygame.create_frame('Game', int(config['CANVAS']['CANVAS_WIDTH']), int(config['CANVAS']['CANVAS_HEIGHT']))
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()