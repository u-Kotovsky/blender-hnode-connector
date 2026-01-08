import bpy
from bthl.api.callbacks import add_callback
from bthl.api.dmxdata import set_channel_value
from bthl.util.dmx import *
import mathutils
import math
import itertools
import time
from bpy_extras.io_utils import axis_conversion

CONV_MATRIX = mathutils.Matrix((
(1,0,0,0),
(0,0,1,0),
(0,1,0,0),
(0,0,0,1)))

def getQuaternionAsDMX(rot, range, bytesPerAxis=1) -> bytearray:
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    wscale = int(scale_number(rot.w, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    wbytes = wscale.to_bytes(bytesPerAxis, byteorder='big')
    return bytearray(xbytes + ybytes + zbytes + wbytes)

def gen_truss_data(start_channel, object):
    if object == None:
        return
    base_channel = start_channel
    
    #POSITION
    loc = object.matrix_world.to_translation()
    
    loc.y, loc.x = loc.x, loc.y
    loc.y *= -1
    loc.y, loc.z = loc.z, loc.y
    
    combined = getPositionAsDMX(loc, range=50, bytesPerAxis=2)
    
    #ROTATION
    mat = object.matrix_world.copy()
    #mat = CONV_MATRIX @ mat # @ CONV_MATRIX.inverse()
    oq = mat.to_quaternion()
    #rotate around the Z axis in blender first
    initialfixrot = mathutils.Euler((math.radians(0),math.radians(0),math.radians(90)))
    oq = initialfixrot.to_quaternion() @ oq
    
    
    baserot = mathutils.Euler((math.radians(-90),math.radians(0),math.radians(0)))
    oq = baserot.to_quaternion() @ mathutils.Quaternion((oq.w, oq.x, -oq.y, -oq.z))
    
    combined += getRotationAsDMX(oq.to_euler("ZXY"), range=math.radians(540 / 2), bytesPerAxis=2)
    #combined += getQuaternionAsDMX(oq, range=1,bytesPerAxis=2)
    
    #hardcoded additional info
    combined.append(0) #fixture offset
    combined.append(0) #FX Selector
    #write them starting at channel 0
    for i in range(14):
        set_channel_value(i + base_channel, combined[i])

def dothings():
    #for t in range(12):
    #    gen_truss_data(0 + (14 * t), bpy.data.objects["Truss " + str(t + 1)])
    
    gen_truss_data(0, bpy.data.objects["Truss 1"])
    
    #version
    #set_channel_value(0,0)
    #set_channel_value(1,0)
    #set_channel_value(2,0)
    #set_channel_value(3,0)
    
    #set_channel_value(4,255) #speed
    
    #set_channel_value(5,255) #custom truss

add_callback(dothings)
set_channel_value(7, 255)
