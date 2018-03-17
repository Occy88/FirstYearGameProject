from SimpleGUICS2Pygame import simpleguics2pygame

from Classes.Settings import *
from Classes.Base.Vector import Vector

from Classes.Super.Camera import Camera
from Handlers.Mouse import Mouse

from Classes.Middle.SpriteControl.SpriteAnimator import SpriteAnimator

from Classes.Super.Player import Player

from GameStates.GameStates import GameState
import configparser

config = configparser.ConfigParser()
# Open file as writeable
config.read_file(open('Classes/config'))

import os
import uuid

# ------------GAME STATES----------------
if('True' == config['CANVAS']['game_state']):
     gameState1 = GameState(True, False)
     gameState2 = GameState(True, False)
else:
     gameState1 = GameState(False, True)
     gameState2 = GameState(False, True)

# ---------------------ANY SETS/LISTS-----------------------
player_list = []
visual_set = set()
visual_set_external=set()
weapon_set = set()
weapon_set_external = set()

env_l1_set = set()
env_l2_list=[]
env_l3_list=[]



monster_set = set()
monster_set_external = set()

# MOUSE HANDLER (PYGAME)(NO RIGHT/MIDDLE CLICKS ON SIMPLEGUI)
mouse = Mouse()
# CONVERSION OF SIMPLE GUI MOUSE LOCATION TO PYGAME LOCATION
adjustment = Vector(250, 25)


def getUid():
    return str(uuid.uuid4())


# ------------------ DICTIONARY OF ALL PICTURES LOCATIONS-----------------
print('LOADING ASSETS')
cwd = os.getcwd()

ch1 = SpriteAnimator(cwd + '/img/Character/1.jpg')
ch2 = SpriteAnimator(cwd + '/img/Character/2.jpg')
print("characters loaded")
env_l1_grass_d_1 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/dark/1.jpg')
env_l1_grass_d_2 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/dark/2.jpg')
env_l1_grass_d_3 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/dark/3.jpg')
env_l1_grass_d_4 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/dark/4.jpg')
env_l1_grass_d_5 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/dark/5.jpg')
env_l1_grass_l_1 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/light/1.jpg')
env_l1_grass_l_2 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/light/2.jpg')
env_l1_grass_l_3 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/light/3.jpg')
env_l1_grass_l_4 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/light/4.jpg')
env_l1_grass_l_5 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/light/5.jpg')
env_l1_grass_m_1 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/med/1.jpg')
env_l1_grass_m_2 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/med/2.jpg')
env_l1_grass_m_3 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/med/3.jpg')
env_l1_grass_m_4 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/med/4.jpg')
env_l1_grass_m_5 = SpriteAnimator(cwd + '/img/Environment/Layer1/Grass/med/5.jpg')
print("grass loaded")
env_l1_ground_1 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/1.jpg')
env_l1_ground_2 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/2.jpg')
env_l1_ground_3 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/3.jpg')
env_l1_ground_4 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/4.jpg')
env_l1_ground_5 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/5.jpg')
env_l1_ground_6 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/6.jpg')
env_l1_ground_7 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/7.jpg')
env_l1_ground_8 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/8.jpg')
env_l1_ground_9 = SpriteAnimator(cwd + '/img/Environment/Layer1/Ground/9.jpg')
print("ground loaded")

env_l2_trees_1x1_1 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/1.jpg')
env_l2_trees_1x1_2 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/2.jpg')
env_l2_trees_1x1_3 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/3.jpg')

env_l2_trees_1x1_4 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/4.jpg')
env_l2_trees_1x1_5 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/5.jpg')
env_l2_trees_1x1_6 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/6.jpg')
env_l2_trees_1x1_7 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/7.jpg')
env_l2_trees_1x1_8 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/8.jpg')
env_l2_trees_1x1_9 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/9.jpg')
env_l2_trees_1x1_10 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/10.jpg')
env_l2_trees_1x1_11 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/11.jpg')
env_l2_trees_1x1_12 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/12.jpg')
env_l2_trees_1x1_13 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/13.jpg')
env_l2_trees_1x1_14 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/14.jpg')
env_l2_trees_1x1_15 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/15.jpg')
env_l2_trees_1x1_16 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/16.jpg')
env_l2_trees_1x1_17 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/17.jpg')
env_l2_trees_1x1_18 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/18.jpg')
env_l2_trees_1x1_19 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/19.jpg')
env_l2_trees_1x1_20 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/20.jpg')
env_l2_trees_1x1_21 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/21.jpg')
env_l2_trees_1x1_22 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/1x1/22.jpg')


env_l2_trees_6x5_1 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/6x5/1.jpg')
env_l2_trees_15x4_1 = SpriteAnimator(cwd + '/img/Environment/Layer2/Trees/15x4/1.jpg')
print("Trees loaded")
mag_att_5x4_1 = SpriteAnimator(cwd + '/img/Magic/Attack/5x4/1.jpg')
mag_att_5x4_2 = SpriteAnimator(cwd + '/img/Magic/Attack/5x4/2.jpg')
mag_att_5x5_1 = SpriteAnimator(cwd + '/img/Magic/Attack/5x5/1.jpg')
mag_att_5x6_1 = SpriteAnimator(cwd + '/img/Magic/Attack/5x6/1.jpg')
mag_att_5x6_2 = SpriteAnimator(cwd + '/img/Magic/Attack/5x6/2.jpg')
mag_att_5x6_3 = SpriteAnimator(cwd + '/img/Magic/Attack/5x6/3.jpg')
mag_att_5x7_1 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/1.jpg')
mag_att_5x7_2 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/2.jpg')
mag_att_5x7_3 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/3.jpg')
mag_att_5x7_4 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/4.jpg')
mag_att_5x7_5 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/5.jpg')
mag_att_5x7_6 = SpriteAnimator(cwd + '/img/Magic/Attack/5x7/6.jpg')
mag_att_5x11_1 = SpriteAnimator(cwd + '/img/Magic/Attack/5x11/1.jpg')

mag_cas_5x4_1 = SpriteAnimator(cwd + '/img/Magic/Cast/5x4/1.jpg')
mag_cas_5x4_2 = SpriteAnimator(cwd + '/img/Magic/Cast/5x4/2.jpg')
mag_cas_5x4_3 = SpriteAnimator(cwd + '/img/Magic/Cast/5x4/3.jpg')
mag_cas_5x7_1 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/1.jpg')
mag_cas_5x7_2 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/2.jpg')
mag_cas_5x7_3 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/3.jpg')
mag_cas_5x7_4 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/4.jpg')
mag_cas_5x7_5 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/5.jpg')
mag_cas_5x7_6 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/6.jpg')
mag_cas_5x7_7 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/7.jpg')
mag_cas_5x7_8 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/8.jpg')
mag_cas_5x7_9 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/9.jpg')
mag_cas_5x7_10 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/10.jpg')
mag_cas_5x7_11 = SpriteAnimator(cwd + '/img/Magic/Cast/5x7/11.jpg')
mag_cas_5x14_1 = SpriteAnimator(cwd + '/img/Magic/Cast/5x14/1.jpg')
mag_cas_5x14_2 = SpriteAnimator(cwd + '/img/Magic/Cast/5x14/2.jpg')

mag_def_5x4_1 = SpriteAnimator(cwd + '/img/Magic/Defence/5x4/1.jpg')
mag_def_5x4_2 = SpriteAnimator(cwd + '/img/Magic/Defence/5x4/2.jpg')
mag_def_5x4_3 = SpriteAnimator(cwd + '/img/Magic/Defence/5x4/3.jpg')
mag_def_5x4_4 = SpriteAnimator(cwd + '/img/Magic/Defence/5x4/4.jpg')
mag_def_5x5_1 = SpriteAnimator(cwd + '/img/Magic/Defence/5x5/1.jpg')
mag_def_5x5_2 = SpriteAnimator(cwd + '/img/Magic/Defence/5x5/2.jpg')
mag_def_5x6_1 = SpriteAnimator(cwd + '/img/Magic/Defence/5x6/1.jpg')
mag_def_5x6_2 = SpriteAnimator(cwd + '/img/Magic/Defence/5x6/2.jpg')
mag_def_5x7_1 = SpriteAnimator(cwd + '/img/Magic/Defence/5x7/1.jpg')

mag_reg_5x5_1 = SpriteAnimator(cwd + '/img/Magic/Regen/5x5/1.jpg')
mag_reg_5x7_1 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/1.jpg')
mag_reg_5x7_2 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/2.jpg')
mag_reg_5x7_3 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/3.jpg')
mag_reg_5x7_4 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/4.jpg')

mag_rev_5x5_1 = SpriteAnimator(cwd + '/img/Magic/Regen/5x5/1.jpg')
mag_rev_5x7_1 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/1.jpg')
mag_rev_5x7_2 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/2.jpg')
mag_rev_5x7_3 = SpriteAnimator(cwd + '/img/Magic/Regen/5x7/3.jpg')
print("Magic loaded")
mag_sho_5x4_1 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x4/1.jpg')
mag_sho_5x4_2 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x4/2.jpg')
mag_sho_5x4_3 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x4/3.jpg')
mag_sho_5x4_4 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x4/4.jpg')
mag_sho_5x6_1 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x6/1.jpg')
mag_sho_5x6_2 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x6/2.jpg')
mag_sho_5x6_3 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x6/3.jpg')
mag_sho_5x7_1 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/1.jpg')
mag_sho_5x7_2 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/2.jpg')
mag_sho_5x7_3 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/3.jpg')
mag_sho_5x7_4 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/4.jpg')
mag_sho_5x7_5 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/5.jpg')
mag_sho_5x7_6 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/6.jpg')
mag_sho_5x7_7 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x7/7.jpg')
mag_sho_5x20_1 = SpriteAnimator(cwd + '/img/Magic/ShowOff/5x20/1.jpg')

# num rows num columns, end row,end column, id
mon_t1_20_6_10_4_1 = SpriteAnimator(cwd + '/img/Monsters/Tier1/1.jpg')
mon_t1_14_3_7_3_2 = SpriteAnimator(cwd + '/img/Monsters/Tier1/2.jpg')
mon_t1_4_6_2_6_3 = SpriteAnimator(cwd + '/img/Monsters/Tier1/3.jpg')
mon_t1_2_4_1_4_4 = SpriteAnimator(cwd + '/img/Monsters/Tier1/4.jpg')
mon_t1_2_10_1_10_5 = SpriteAnimator(cwd + '/img/Monsters/Tier1/5.jpg')
mon_t1_8_3_4_3_6 = SpriteAnimator(cwd + '/img/Monsters/Tier1/6.jpg')
mon_t2_4_4_2_4_1 = SpriteAnimator(cwd + '/img/Monsters/Tier2/1.jpg')
mon_t2_16_10_8_9_2 = SpriteAnimator(cwd + '/img/Monsters/Tier2/2.jpg')
mon_t2_2_8_1_8_3 = SpriteAnimator(cwd + '/img/Monsters/Tier2/3.jpg')
mon_t2_4_4_2_4_4 = SpriteAnimator(cwd + '/img/Monsters/Tier2/4.jpg')
mon_t3_8_2_4_2_1 = SpriteAnimator(cwd + '/img/Monsters/Tier3/1.jpg')
mon_t3_10_4_5_4_2 = SpriteAnimator(cwd + '/img/Monsters/Tier3/2.jpg')
mon_t3_10_4_5_4_3 = SpriteAnimator(cwd + '/img/Monsters/Tier3/3.jpg')
mon_t3_6_2_3_2_4 = SpriteAnimator(cwd + '/img/Monsters/Tier3/4.jpg')
mon_t3_6_2_3_2_5 = SpriteAnimator(cwd + '/img/Monsters/Tier3/5.jpg')
mon_t3_8_8_4_2_6 = SpriteAnimator(cwd + '/img/Monsters/Tier3/6.jpg')
print("Monsters Loaded")
pro_t1_1 = SpriteAnimator(cwd + '/img/Projectiles/Tier1/1.jpg')
pro_t2_1 = SpriteAnimator(cwd + '/img/Projectiles/Tier2/1.jpg')
pro_t2_2 = SpriteAnimator(cwd + '/img/Projectiles/Tier2/2.jpg')
pro_t2_3 = SpriteAnimator(cwd + '/img/Projectiles/Tier2/3.jpg')
pro_t2_4 = SpriteAnimator(cwd + '/img/Projectiles/Tier2/4.jpg')
pro_t3_1 = SpriteAnimator(cwd + '/img/Projectiles/Tier3/1.jpg')
pro_t3_2 = SpriteAnimator(cwd + '/img/Projectiles/Tier3/2.jpg')
pro_t3_3 = SpriteAnimator(cwd + '/img/Projectiles/Tier3/3.jpg')
pro_t4_1 = SpriteAnimator(cwd + '/img/Projectiles/Tier4/1.jpg')
pro_t4_2 = SpriteAnimator(cwd + '/img/Projectiles/Tier4/2.jpg')
print("Projectiles Loaded")
spriteDictionary = {'ch_1': ch1,
                    'ch_2': ch2,
                    'en_l1_gs_d_1': env_l1_grass_d_1,
                    'en_l1_gs_d_2': env_l1_grass_d_2,
                    'en_l1_gs_d_3': env_l1_grass_d_3,
                    'en_l1_gs_d_4': env_l1_grass_d_4,
                    'en_l1_gs_d_5': env_l1_grass_d_5,

                    'en_l1_gs_l_1': env_l1_grass_l_1,
                    'en_l1_gs_l_2': env_l1_grass_l_2,
                    'en_l1_gs_l_3': env_l1_grass_l_3,
                    'en_l1_gs_l_4': env_l1_grass_l_4,
                    'en_l1_gs_l_5': env_l1_grass_l_5,

                    'en_l1_gs_m_1': env_l1_grass_m_1,
                    'en_l1_gs_m_2': env_l1_grass_m_2,
                    'en_l1_gs_m_3': env_l1_grass_m_3,
                    'en_l1_gs_m_4': env_l1_grass_m_4,
                    'en_l1_gs_m_5': env_l1_grass_m_5,

                    'en_l1_gd_1': env_l1_ground_1,
                    'en_l1_gd_2': env_l1_ground_2,
                    'en_l1_gd_3': env_l1_ground_3,
                    'en_l1_gd_4': env_l1_ground_4,
                    'en_l1_gd_5': env_l1_ground_5,
                    'en_l1_gd_6': env_l1_ground_6,
                    'en_l1_gd_7': env_l1_ground_7,
                    'en_l1_gd_8': env_l1_ground_8,
                    'en_l1_gd_9': env_l1_ground_9,


                    'en_l2_ts_1x1_1': env_l2_trees_1x1_1,
                    'en_l2_ts_1x1_2': env_l2_trees_1x1_2,
                    'en_l2_ts_1x1_3': env_l2_trees_1x1_3,
                    'en_l2_ts_1x1_4': env_l2_trees_1x1_4,
                    'en_l2_ts_1x1_5': env_l2_trees_1x1_5,
                    'en_l2_ts_1x1_6': env_l2_trees_1x1_6,
                    'en_l2_ts_1x1_7': env_l2_trees_1x1_7,
                    'en_l2_ts_1x1_8': env_l2_trees_1x1_8,
                    'en_l2_ts_1x1_9': env_l2_trees_1x1_9,
                    'en_l2_ts_1x1_10': env_l2_trees_1x1_10,
                    'en_l2_ts_1x1_11': env_l2_trees_1x1_11,
                    'en_l2_ts_1x1_12': env_l2_trees_1x1_12,
                    'en_l2_ts_1x1_13': env_l2_trees_1x1_13,
                    'en_l2_ts_1x1_14': env_l2_trees_1x1_14,
                    'en_l2_ts_1x1_15': env_l2_trees_1x1_15,
                    'en_l2_ts_1x1_16': env_l2_trees_1x1_16,
                    'en_l2_ts_1x1_17': env_l2_trees_1x1_17,
                    'en_l2_ts_1x1_18': env_l2_trees_1x1_18,
                    'en_l2_ts_1x1_19': env_l2_trees_1x1_19,
                    'en_l2_ts_1x1_20': env_l2_trees_1x1_20,
                    'en_l2_ts_1x1_21': env_l2_trees_1x1_21,
                    'en_l2_ts_1x1_22': env_l2_trees_1x1_22,
                    'en_l2_ts_6x5_1': env_l2_trees_6x5_1,
                    'en_l2_ts_15x4_1': env_l2_trees_15x4_1,

                    'ma_at_5x4_1': mag_att_5x4_1,
                    'ma_at_5x4_2': mag_att_5x4_2,
                    'ma_at_5x5_1': mag_att_5x5_1,
                    'ma_at_5x6_1': mag_att_5x6_1,
                    'ma_at_5x6_2': mag_att_5x6_2,
                    'ma_at_5x6_3': mag_att_5x6_3,
                    'ma_at_5x7_1': mag_att_5x7_1,
                    'ma_at_5x7_2': mag_att_5x7_2,
                    'ma_at_5x7_3': mag_att_5x7_3,
                    'ma_at_5x7_4': mag_att_5x7_4,
                    'ma_at_5x7_5': mag_att_5x7_5,
                    'ma_at_5x7_6': mag_att_5x7_6,
                    'ma_at_5x11_1': mag_att_5x11_1,

                    'ma_ca_5x4_1': mag_cas_5x4_1,
                    'ma_ca_5x4_2': mag_cas_5x4_2,
                    'ma_ca_5x4_3': mag_cas_5x4_3,
                    'ma_ca_5x7_1': mag_cas_5x7_1,
                    'ma_ca_5x7_2': mag_cas_5x7_2,
                    'ma_ca_5x7_3': mag_cas_5x7_3,
                    'ma_ca_5x7_4': mag_cas_5x7_4,
                    'ma_ca_5x7_5': mag_cas_5x7_5,
                    'ma_ca_5x7_6': mag_cas_5x7_6,
                    'ma_ca_5x7_7': mag_cas_5x7_7,
                    'ma_ca_5x7_8': mag_cas_5x7_8,
                    'ma_ca_5x7_9': mag_cas_5x7_9,
                    'ma_ca_5x7_10': mag_cas_5x7_10,
                    'ma_ca_5x7_11': mag_cas_5x7_11,
                    'ma_ca_5x14_1': mag_cas_5x14_1,
                    'ma_ca_5x14_2': mag_cas_5x14_2,

                    'ma_de_5x4_1': mag_def_5x4_1,
                    'ma_de_5x4_2': mag_def_5x4_2,
                    'ma_de_5x4_3': mag_def_5x4_3,
                    'ma_de_5x4_4': mag_def_5x4_4,
                    'ma_de_5x5_1': mag_def_5x5_1,
                    'ma_de_5x5_2': mag_def_5x5_2,
                    'ma_de_5x6_1': mag_def_5x6_1,
                    'ma_de_5x6_2': mag_def_5x6_2,
                    'ma_de_5x7_1': mag_def_5x7_1,

                    'ma_re_5x5_1': mag_reg_5x5_1,
                    'ma_re_5x7_1': mag_reg_5x7_1,
                    'ma_re_5x7_2': mag_reg_5x7_2,
                    'ma_re_5x7_3': mag_reg_5x7_3,
                    'ma_re_5x7_4': mag_reg_5x7_4,

                    'ma_rv_5x4_1': mag_rev_5x5_1,
                    'ma_rv_5x7_1': mag_rev_5x7_1,
                    'ma_rv_5x7_2': mag_rev_5x7_2,
                    'ma_rv_5x7_3': mag_rev_5x7_3,

                    'ma_sh_5x4_1': mag_sho_5x4_1,
                    'ma_sh_5x4_2': mag_sho_5x4_2,
                    'ma_sh_5x4_3': mag_sho_5x4_3,
                    'ma_sh_5x4_4': mag_sho_5x4_4,
                    'ma_sh_5x6_1': mag_sho_5x6_1,
                    'ma_sh_5x6_2': mag_sho_5x6_2,
                    'ma_sh_5x6_3': mag_sho_5x6_3,
                    'ma_sh_5x7_1': mag_sho_5x7_1,
                    'ma_sh_5x7_2': mag_sho_5x7_2,
                    'ma_sh_5x7_3': mag_sho_5x7_3,
                    'ma_sh_5x7_4': mag_sho_5x7_4,
                    'ma_sh_5x7_5': mag_sho_5x7_5,
                    'ma_sh_5x7_6': mag_sho_5x7_6,
                    'ma_sh_5x7_8': mag_sho_5x7_7,
                    'ma_sh_5x20_1': mag_sho_5x20_1,

                    'mo_t1_1': mon_t1_20_6_10_4_1,
                    'mo_t1_2': mon_t1_14_3_7_3_2,
                    'mo_t1_3': mon_t1_4_6_2_6_3,
                    'mo_t1_4': mon_t1_2_4_1_4_4,
                    'mo_t1_5': mon_t1_2_10_1_10_5,
                    'mo_t1_6': mon_t1_8_3_4_3_6,
                    'mo_t2_1': mon_t2_4_4_2_4_1,
                    'mo_t2_2': mon_t2_16_10_8_9_2,
                    'mo_t2_3': mon_t2_2_8_1_8_3,
                    'mo_t2_4': mon_t2_4_4_2_4_4,
                    'mo_t3_1': mon_t3_8_2_4_2_1,
                    'mo_t3_2': mon_t3_10_4_5_4_2,
                    'mo_t3_3': mon_t3_10_4_5_4_3,
                    'mo_t3_4': mon_t3_6_2_3_2_4,
                    'mo_t3_5': mon_t3_6_2_3_2_5,
                    'mo_t3_6': mon_t3_8_8_4_2_6,

                    'pr_t1_1': pro_t1_1,
                    'pr_t2_1': pro_t2_1,
                    'pr_t2_2': pro_t2_2,
                    'pr_t2_3': pro_t2_3,
                    'pr_t2_4': pro_t2_4,
                    'pr_t3_1': pro_t3_1,
                    'pr_t3_2': pro_t3_1,
                    'pr_t3_3': pro_t3_2,
                    'pr_t3_4': pro_t3_3,
                    'pr_t4_1': pro_t4_1,
                    'pr_t4_2': pro_t4_2}
# -----------------------MOVING OBJECTS-------------------
print("ASSETS LOADED")
print("LOADING OBJECTS")
# CAMERA
cam = Camera(Vector(PLAYER_INITIAL_POSITION_X, PLAYER_INITIAL_POSITION_Y), Vector(int(config['CANVAS']['CANVAS_WIDTH'])*4,int(config['CANVAS']['CANVAS_HEIGHT'])*4))

# PLAYER


player1 = Player(
    Vector(int(MAP_WIDTH//2), int(MAP_HEIGHT//2)),
    Vector(int(config['PLAYER']['PLAYER_INITIAL_VELOCITY_X']), int(config['PLAYER']['PLAYER_INITIAL_VELOCITY_Y'])),
    0, Vector(int(MAP_WIDTH//2), int(MAP_HEIGHT//2)),
    int(config['PLAYER']['PLAYER_MAX_VELOCITY']),
    int(config['PLAYER']['PLAYER_INITIAL_ANGLE']),20,
    config['PLAYER']['PLAYER_SPRITE'],
    spriteDictionary,
    int(config['PLAYER']['PLAYER_SPRITE_FPS']),
    str(getUid()),

    False, Vector(0, 0), 1, 21, 13, 11, 1, 9, 9)
player1.setSpriteState(3)
player_list.append(player1)
playerId = player1.idObject

# if (bool(config['NETWORKING']['CONFIG_TYPE'] == "server")):
#     dragon = Monster(Vector(0, 2500), Vector(100, 0), 0, Vector(0, 2500), 150, 0, 0, 'whiteDragon', spriteDictionary,
#                      25, getUid(), False, Vector(0, 0), 1, 5, 4, 1, 1, 5, 4)
#     dragon.move(Vector(10000, 2500))
#     monster_set.add(dragon)
#
# elif bool((config['NETWORKING']['CONFIG_TYPE'] == "client")):
#     dragon2 = Monster(Vector(0, 3000), Vector(100, 0), 0, Vector(0, 3000), 150, 0, 0, 'greenDragon', spriteDictionary,
#                       25, getUid(), False, Vector(0, 0), 1, 5, 4, 1, 1, 5, 4)
#     dragon2.move(Vector(10000, 2500))
#     monster_set.add(dragon2)

# -----------------------NON-MOVING OBJECTS------------------
print("OBJECTS LOADED")
from Loading.RandomGen import randomGrass, randomTrees
print("GENERATING RANDOM ENVIRONMENT")
randomGrass()
randomTrees()
print("ENVIRONMENT GENERATED")
# t1=Particle(False, Vector(2500,2500), Vector(0, 0), 0, Vector(2500,2500), 0, 0, 0, 0,
#                             'en_l2_ts_1x1_19', spriteDictionary, 0.0001, False, False, getUid(), 1, 1, 1, 1, 1, 1)
# t1.radius/=3
# env_l2_list.append(t1)


# tree = Particle(True, Vector(2500, 2500), Vector(0, 0), 0, Vector(2500, 2500), 200, 0, 0, 0, 'en_l1_tr', spriteDictionary,
#                 1, False, False, getUid(), 4, 15, 1, 1, 4, 15)
#
# music = simpleguics2pygame._load_local_sound('Music/main.ogg')
# music.play()
