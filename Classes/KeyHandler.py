import SimpleGUICS2Pygame
from SimpleGUICS2Pygame import simpleguics2pygame

from Classes.Objects import cam

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

    elif key == simpleguics2pygame.KEY_MAP['right']:
        cam.moveRight = True
    elif key == simpleguics2pygame.KEY_MAP['left']:
        cam.moveLeft = True
    elif key == simpleguics2pygame.KEY_MAP['up']:
        cam.moveUp = True
    elif key == simpleguics2pygame.KEY_MAP['down']:
        cam.moveDown = True
