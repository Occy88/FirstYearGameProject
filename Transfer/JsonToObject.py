# to read data into dictionary: data = json.loads(<json File>, object_hook=lambda d: namedtuple('<Object Name For Reference>', d.keys())(*d.values()))
from Classes.Super.Camera import Camera
from Classes.Base.Vector import Vector
from Classes.Middle.Particle import Particle
from Classes.Super.Player import Player
from Classes.Super.Monster import Monster
from Classes.Super.Weapon import Weapon
from Loading.Objects import weapon_set_external, player_list,monster_set_external,spriteDictionary, playerId,gameState2,visual_set_external
from Loading.Objects import cam
import configparser

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))

import json


### If exists local: update   if does not exist local: add      if boolean: remove  and on local then set boolean to False


def getCam(arr):
    obj = Camera(Vector(arr['origin']['x'], arr['origin']['y']), Vector(arr['dim']['x'], arr['dim']['y']))
    cam.recieve(obj)
def getWeapon(arr):
    exists=False
    for weapon in weapon_set_external:
        if weapon.idObject== arr['idObject']:
            exists=True

    if not exists:

        weapon_set_external.add(Weapon(Vector(arr['pos']['x'],arr['pos']['y']),Vector(arr['vel']['x'],arr['vel']['y']),
                                         arr['nextPosTime'],Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['maxVel'],
                                         arr['angle'], arr['radius'],arr['spriteKey'],spriteDictionary,arr['fps'],arr['idObject'],arr['numRows'],arr['numColumns'],arr['startRow'],
                                         arr['startColumn'],arr['endRow'],arr['endColumn'],arr['removeOnVelocity0'],
                                         arr['removeOnAnimationLoop'],arr['damage']))


    for weapon in weapon_set_external:
        if weapon.idObject==arr['idObject']:

            weapon.recieve(Vector(arr['nextPos']['x'], arr['nextPos']['y']),
                             arr['nextPosTime'],arr['maxVel'],arr['angle'],arr['spriteKey'],arr['fps'],arr['numRows'],
                             arr['numColumns'],arr['startRow'],arr['startColumn'],
                             arr['endRow'],arr['endColumn'],arr['radius'],spriteDictionary,arr['applied'])

def getVisual(arr):
    exists=False
    for particle in visual_set_external:
        if particle.idObject== arr['idObject']:
            exists=True
    if not exists:
        visual_set_external.add(Particle(arr['updateSprite'],Vector(arr['pos']['x'],arr['pos']['y']),Vector(arr['vel']['x'],arr['vel']['y']),
                                         arr['nextPosTime'],Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['maxVel'],arr['maxRange'],
                                         arr['angle'], arr['radius'],arr['spriteKey'],spriteDictionary,arr['fps'],arr['removeOnVelocity0'],
                                         arr['removeOnAnimationLoop'],arr['idObject'],arr['numRows'],arr['numColumns'],arr['startRow'],
                                         arr['startColumn'],arr['endRow'],arr['endColumn']))

    for particle in visual_set_external:
        if particle.idObject==arr['idObject']:
            particle.recieve(Vector(arr['nextPos']['x'], arr['nextPos']['y']),
                             arr['nextPosTime'],arr['maxVel'],arr['maxRange'],arr['angle'],
                             arr['updateSprite'],arr['spriteKey'],arr['fps'],arr['numRows'],
                             arr['numColumns'],arr['startRow'],arr['startColumn'],
                             arr['endRow'],arr['endColumn'],arr['radius'],spriteDictionary)
def getMonster(arr):
    exists = False
    for monster in monster_set_external:

        if monster.idObject == arr['idObject']:
            exists = True
    if not exists:
        monster_set_external.add(
            Monster(Vector(arr['pos']['x'], arr['pos']['y']), Vector(arr['vel']['x'], arr['vel']['y']),
                   arr['nextPosTime'], Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['maxVel'],
                   arr['angle'], arr['radius'], arr['spriteKey'], spriteDictionary,
                   arr['fps'], arr['idObject'], arr['hasFired'],
                   Vector(arr['clickPosition']['x'], arr['clickPosition']['y']),
                   arr['spriteState'], arr['numRows'], arr['numColumns'], arr['startRow'], arr['startColumn'],
                   arr['endRow'], arr['endColumn'],arr['tier'],arr['aBack'],arr['external'],arr['totalLife'],
                   Vector(arr['operationOrigin']['x'],arr['operationOrigin']['y']),
                   Vector(arr['operationRange']['x'],arr['operationRange']['y']),
                    arr['attackRange'],
                    arr['followDistance']))


    for monster in monster_set_external:
        if monster.idObject == arr['idObject'] :
            monster.recieve(arr['hasFired'], Vector(arr['clickPosition']['x'], arr['clickPosition']['y']),
                           Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['nextPosTime'], arr['maxVel'],
                           arr['maxRange'], arr['angle'], arr['updateSprite'], arr['spriteKey'],
                           arr['fps'], arr['numRows'], arr['numColumns'], arr['startRow'], arr['startColumn'],
                           arr['endRow'], arr['endColumn'], arr['radius'], spriteDictionary,arr['life'],arr['range'],arr['melee'],arr['magic'],arr['remove'])

def getGameState(arr):
    if arr['main']:
        gameState2.main=True

    else:
        gameState2.main=False
    if arr['intro']:
        gameState2.intro=True

    else:
        gameState2.intro=False

def getPlayer(arr):
    exists=False
    for player in player_list:

        if player.idObject == arr['idObject']:
            exists = True
    if not exists:

        player_list.append(

            Player(Vector(arr['pos']['x'],arr['pos']['y']),Vector(arr['vel']['x'],arr['vel']['y']),
                           arr['nextPosTime'],Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['maxVel'],
                           arr['angle'], arr['radius'], arr['spriteKey'], spriteDictionary,
                           arr['fps'],arr['idObject'], arr['hasFired'],
                           Vector(arr['clickPosition']['x'], arr['clickPosition']['y']),
                           arr['spriteState'],arr['numRows'],arr['numColumns'],arr['startRow'],arr['startColumn'],
                           arr['endRow'],arr['endColumn']))

    for player in player_list:
        if player.idObject == arr['idObject'] and arr['idObject'] != playerId:
            player.recieve(arr['hasFired'],Vector(arr['clickPosition']['x'], arr['clickPosition']['y']),Vector(arr['nextPos']['x'], arr['nextPos']['y']), arr['nextPosTime'],arr['maxVel'],
                           arr['maxRange'], arr['angle'], arr['updateSprite'], arr['spriteKey'],
                arr['fps'], arr['numRows'], arr['numColumns'], arr['startRow'], arr['startColumn'], arr['endRow'], arr['endColumn'], arr['radius'], spriteDictionary,arr['life'],arr['range'],arr['melee'],arr['magic'])


def getObject(j):
    arr = j

    if(bool(int(config['DEVELOPER']['DEVELOPER_OPTIONS']))): print("Class ID:" + str(arr['idClass']))
    if(bool(int(config['DEVELOPER']['DEVELOPER_OPTIONS'])) and bool( config['NETWORKING']['LOGGING_LEVEL'] == "high")): print(arr)

    if arr['idClass'] == 1:
        getCam(arr)
        getCam(arr)
    elif arr['idClass'] == 2:
        getVisual(arr)
    elif arr['idClass']== 3:
        getPlayer(arr)
    elif arr['idClass'] == 4:
        getMonster(arr)
    elif arr['idClass']==5:#get weapons
        getWeapon(arr)
    elif arr['idClass']==10:#game states
        getGameState(arr)
    else:
        return "No class for ID"
