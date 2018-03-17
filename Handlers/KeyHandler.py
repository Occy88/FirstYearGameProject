from SimpleGUICS2Pygame import simpleguics2pygame
from Loading.Objects import gameState1
from Transfer.comms import communicate
from Loading.Objects import cam,player_list,playerId

def keyup(key):
    if key == simpleguics2pygame.KEY_MAP['r']:
        cam.zoomOut = False
    elif key == simpleguics2pygame.KEY_MAP['e']:
        cam.zoomIn = False
    elif key == simpleguics2pygame.KEY_MAP['right']:
        cam.moveRight = False
    elif key == simpleguics2pygame.KEY_MAP['left']:
        cam.moveLeft = False
    elif key == simpleguics2pygame.KEY_MAP['up']:
        cam.moveUp = False
    elif key == simpleguics2pygame.KEY_MAP['down']:
        cam.moveDown = False


def keydown(key):

    if key == simpleguics2pygame.KEY_MAP['r']:
        cam.zoomOut = True
    elif key == simpleguics2pygame.KEY_MAP['e']:
        cam.zoomIn = True
    elif key == simpleguics2pygame.KEY_MAP['1']:
        for player in player_list:
            if player.idObject==playerId:
                player.weapon=1
    elif key == simpleguics2pygame.KEY_MAP['2']:
        for player in player_list:
            if player.idObject==playerId:
                player.weapon=2
    elif key == simpleguics2pygame.KEY_MAP['3']:
        for player in player_list:
            if player.idObject == playerId:
                player.weapon = 3
    elif key == simpleguics2pygame.KEY_MAP['right'] :
        cam.moveRight = True
    elif key == simpleguics2pygame.KEY_MAP['left']:
        cam.moveLeft = True
    elif key == simpleguics2pygame.KEY_MAP['up']:
        cam.moveUp = True
    elif key == simpleguics2pygame.KEY_MAP['down']:
        cam.moveDown = True
    elif key == simpleguics2pygame.KEY_MAP['space']:
        communicate(gameState1)

