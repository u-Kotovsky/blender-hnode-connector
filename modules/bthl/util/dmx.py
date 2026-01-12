import math
from bthl.util.general import scale_number
import struct
from mathutils import Vector, Quaternion, Euler

def getPositionAsDMX(loc: Vector, range: int, bytesPerAxis: int = 1) -> bytearray:
    xscale = int(scale_number(loc.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(loc.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(loc.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = struct.pack('>I', xscale)[-bytesPerAxis:]
    ybytes = struct.pack('>I', yscale)[-bytesPerAxis:]
    zbytes = struct.pack('>I', zscale)[-bytesPerAxis:]
    return bytearray(xbytes + ybytes + zbytes)

def getRotationAsDMX(rot: Euler, range: int, bytesPerAxis: int = 1) -> bytearray:
    #constrict to 360 degrees as theres no point going beyond
    rot.x = rot.x % math.radians(360)
    rot.y = rot.y % math.radians(360)
    rot.z = rot.z % math.radians(360)
    #0 is the valid start for this range in this case
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, 0, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, 0, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, 0, range))
    #now convert to bytes
    xbytes = struct.pack('>I', xscale)[-bytesPerAxis:]
    ybytes = struct.pack('>I', yscale)[-bytesPerAxis:]
    zbytes = struct.pack('>I', zscale)[-bytesPerAxis:]
    return bytearray(xbytes + ybytes + zbytes)

def getQuaternionAsDMX(rot: Quaternion, range: int, bytesPerAxis: int = 1) -> bytearray:
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    wscale = int(scale_number(rot.w, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = struct.pack('>I', xscale)[-bytesPerAxis:]
    ybytes = struct.pack('>I', yscale)[-bytesPerAxis:]
    zbytes = struct.pack('>I', zscale)[-bytesPerAxis:]
    wbytes = struct.pack('>I', wscale)[-bytesPerAxis:]
    return bytearray(xbytes + ybytes + zbytes + wbytes)

def getColorAsDMX(color: tuple[float, float, float]) -> bytes:
    return getTupleAsDMX(color)

def getTupleAsDMX(tup: tuple) -> bytes:
    barray = bytearray()
    for val in tup:
        if isinstance(val, float):
            scaled = int(scale_number(val, 0,255,0,1))
            barray.append(scaled)
        elif isinstance(val, int):
            barray.append(val)
    return bytes(barray)
