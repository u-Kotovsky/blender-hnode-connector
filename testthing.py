import bpy
from bthl.api.callbacks import add_callback
from bthl.api.dmxdata import set_channel_value
from bthl.util.dmx import *
import mathutils
import math
import itertools
import time
from bpy_extras.io_utils import axis_conversion

def gen_truss_data(start_channel, object):
    if object == None:
        return
    base_channel = start_channel
    loc = object.matrix_world.to_translation()
    
    loc.y, loc.x = loc.x, loc.y
    loc.y *= -1
    loc.y, loc.z = loc.z, loc.y
    
    combined = getPositionAsDMX(loc, range=50, bytesPerAxis=2)
    mat = object.matrix_world.copy()
    eul = mat.to_euler("ZXY")
    eul.x = 0
    #eul.y = 0
    eul.z = 0
    
    combined += getRotationAsDMX(eul, range=math.radians(540 / 2), bytesPerAxis=2)
    #hardcoded additional info
    combined.append(0) #fixture offset
    combined.append(0) #FX Selector
    #write them starting at channel 0
    for i in range(14):
        set_channel_value(i + base_channel, combined[i])

def dothings():
    for t in range(12):
        gen_truss_data(6 + (14 * t), bpy.data.objects["Truss " + str(t + 1)])
    
    #version
    set_channel_value(0,0)
    set_channel_value(1,0)
    set_channel_value(2,0)
    set_channel_value(3,0)
    
    set_channel_value(4,255) #speed
    
    set_channel_value(5,255) #custom truss

add_callback(dothings)
