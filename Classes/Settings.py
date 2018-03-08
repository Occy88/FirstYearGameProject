'''
Class Id's:
1: Camera
2: particle
3: Player
4: Vector
'''
#FOR MULTIPLAYER MAKE SURE EACH PLAYER ID IS DIFFERENT, 1-4

#DEVELOPER OPTIONS
DEVELOPER_OPTIONS = False


#CANVAS
CANVAS_WIDTH = 720
CANVAS_HEIGHT = 480

#NETWORKING
CONFIG_TYPE = 'client'
CLIENT_IP = '10.2.76.93'

#CAMERA
CAM_MOVE_SENSITIVITY=60
CAM_ZOOM_SENSITIVITY=0.03
CAM_MIN_DIST=200

#PARTICLE
PARTICLE_VELOCITY= 300
PARTICLE_RADIUS=20
PARTICLE_MAX_RANGE=2000
#SPRITE
SPRITE_FPS=1/20

#PLAYER
PLAYER_ID=1
PLAYER_RADIUS=40
PLAYER_MAX_VELOCITY=100
PLAYER_INITIAL_ANGLE=0
PLAYER_DIMENSIONS_X=50
PLAYER_DIMENSIONS_Y=100
PLAYER_INITIAL_VELOCITY_X=0
PLAYER_INITIAL_VELOCITY_Y=0
PLAYER_INITIAL_POSITION_X=2500
PLAYER_INITIAL_POSITION_Y=2500
PLAYER_SPRITE_FPS=10
PLAYER_SPRITE='elf_demo'