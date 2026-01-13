import idprop
import bpy
from bthl.tasks.task import Task
from bthl.api.dmxdata import set_channel_value
from bthl.util.dmx import getColorAsDMX, getTupleAsDMX
import mathutils
import math

def handleobjectproperties(object: bpy.types.Object):
    print("Handling properties for object:", object.name)
    properties = {}
    if len(object.keys()) > 1:
        # First item is _RNA_UI
        for K in object.keys():
            if K not in '_RNA_UI':
                try:
                    prop_ui = object.id_properties_ui(K)
                except TypeError: # does not support ui data
                    print("No UI data for property:", K)
                    continue
                dict = prop_ui.as_dict()
                dict["value"] = object[K]
                properties[K] = dict
    
    #check if universe and channel are defined
    if "Universe" in properties and "Channel" in properties:
        #store these and convert to a global index
        universe = properties["Universe"]["value"]
        channel = properties["Channel"]["value"]
        globalChannel = (universe - 1) * 512 + (channel - 1)
        
        #now that we have the global channel index, interpret all custom props that have descriptions as offsets to the base channel
        for p in properties:
            #print("Processing property:", p)
            #ignore universe and channel props
            if p in ["Universe","Channel"]:
                continue
            #check if description field exists
            if "description" in properties[p]:
                if properties[p]["description"] != "":
                    props = properties[p]
                    #check if we can interpret as int
                    try:
                        offset = int(props["description"])
                    except ValueError:
                        print("Not a valid offset:", props["description"])
                        continue
                    finalChannel = globalChannel + offset
                    #we now need to interpret it to a value
                    #floats should be converted from 0 to 1 to 0 to 255
                    #ints should be direct mapping
                    subtype = props["subtype"]
                    value = props["value"]
                    typ = type(value)
                    # if object.name == "Clouds":
                    #     print(typ)
                    if typ == int:
                        set_channel_value(finalChannel, value)
                    elif typ == float:
                        remapped = int(value * 255)
                        #print(remapped)
                        set_channel_value(finalChannel, remapped)
                    elif typ == bool:
                        #TODO: Allow defining this via description standard
                        set_channel_value(finalChannel, 255 if value else 0)
                    elif typ == idprop.types.IDPropertyArray:
                        #print(value.typecode)
                        dmx = getTupleAsDMX(value)
                        for i in range(len(dmx)):
                            set_channel_value(finalChannel + i, dmx[i])
                    #handle data blocks
                    #Text os executed as python code with finalChannel passed in
                    elif typ == bpy.types.Text:
                        #print("detected text")
                        #exec the text block as python
                        textblock: bpy.types.Text = value
                        local_dict = {}
                        #pass in the channel index
                        local_dict["finalChannel"] = finalChannel
                        #pass along the object we are referencing
                        local_dict["object"] = object
                        exec(textblock.as_string(), {}, local_dict)
                    #objects are treated as directional pointers for pan/tilt
                    elif typ == bpy.types.Object:
                        target_obj: bpy.types.Object = value
                        direction = target_obj.location - object.location
                        #calculate pan/tilt from direction vector
                        direction.normalize()
                        #pan is rotation around z axis
                        pan = mathutils.Vector((direction.x, direction.y)).angle_signed(mathutils.Vector((1,0)))
                        #tilt is rotation around x axis
                        tilt = math.asin(direction.z)
                        #remap pan from -pi to pi to 0-255
                        #TODO: determine a format to define the range here instead of hardcoding pi as this is based on the vrchat fixture side
                        pan_remapped = int((pan + math.pi) / (2 * math.pi) * 255)
                        tilt_remapped = int((tilt + (math.pi/2)) / math.pi * 255)
                        set_channel_value(finalChannel, pan_remapped)
                        set_channel_value(finalChannel + 1, tilt_remapped)

def update_custom_properties(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph):
    bad_obj_types = ['CAMERA','LAMP','ARMATURE']
    for obj in bpy.data.objects:
        if obj.type in bad_obj_types:
            continue
        handleobjectproperties(obj)

class CustomPropertiesTask(Task):
    functions = {
        "depsgraph_update_post": update_custom_properties,
        "frame_change_post": update_custom_properties,
        "load_post": update_custom_properties,
    }
