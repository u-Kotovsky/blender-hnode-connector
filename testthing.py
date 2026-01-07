import bpy
from bthl.api.callbacks import add_callback
from bthl.api.dmxdata import set_channel_value
from bthl.util.dmx import *
import mathutils
import math

def gen_truss_data(start_channel, object):
    if object == None:
        return
    base_channel = start_channel
    loc = object.matrix_world.to_translation()
    #loc.z *= -1
    loc.y, loc.x = loc.x, loc.y
    loc.y *= -1
    loc.y, loc.z = loc.z, loc.y
    combined = getPositionAsDMX(loc, range=50, bytesPerAxis=2)
    rot = object.matrix_world.to_quaternion()
    #works but flipped across Y??????
    unityrot = mathutils.Quaternion((rot.w, rot.x, rot.y, rot.z))
    eulrot = unityrot.to_euler("XYZ")
    combined += getRotationAsDMX(eulrot, range=math.radians(540 / 2), bytesPerAxis=2)
    #write them starting at channel 0
    for i in range(12):
        set_channel_value(i + base_channel, combined[i])

def dothings():
    gen_truss_data(0, bpy.data.objects["Cube"])

add_callback(dothings)
