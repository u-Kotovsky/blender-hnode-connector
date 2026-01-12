import idprop
import bpy
from bthl.tasks.task import Task
from bthl.api.dmxdata import set_channel_value
from bthl.util.dmx import getColorAsDMX

def handleobjectproperties(object: bpy.types.Object):
    properties = {}
    if len(object.keys()) > 1:
        # First item is _RNA_UI
        for K in object.keys():
            if K not in '_RNA_UI':
                prop_ui = object.id_properties_ui(K)
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
            if properties[p]["description"] != "":
                props = properties[p]
                #check if we can interpret as int
                try:
                    offset = int(props["description"])
                except ValueError:
                    print("Not a float")
                    continue
                finalChannel = globalChannel + offset
                #we now need to interpret it to a value
                #floats should be converted from 0 to 1 to 0 to 255
                #ints should be direct mapping
                subtype = props["subtype"]
                value = props["value"]
                typ = type(value)
                if typ == int:
                    set_channel_value(finalChannel, value)
                elif typ == float:
                    remapped = int(value * 255)
                    print(remapped)
                    set_channel_value(finalChannel, remapped)
                elif type == type(idprop.types.IDPropertyArray) and subtype == "COLOR": #linear color
                    #print(value.typecode)
                    if value.typecode == "f" or value.typecode == "d":
                        coldmx = getColorAsDMX(value)
                        for i in range(len(coldmx)):
                            set_channel_value(finalChannel + i, coldmx[i])

def update_custom_properties(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph):
    bad_obj_types = ['CAMERA','LAMP','ARMATURE']
    for obj in scene.objects:
        if obj.type in bad_obj_types:
            continue
        handleobjectproperties(obj)

class CustomPropertiesTask(Task):
    functions = {
        "depsgraph_update_post": update_custom_properties,
        "frame_change_post": update_custom_properties,
        "load_post": update_custom_properties,
    }
