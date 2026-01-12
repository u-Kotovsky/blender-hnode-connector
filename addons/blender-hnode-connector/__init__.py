bl_info = {
    "name": "Blender to HNode link",
    "blender": (4, 5, 0),
    "category": "Object",
}

import bpy
import inspect
import sys
from bthl.panel.global_control import GlobalControlPanel
from bthl.operator.sender_modal import UDPClientToggleModal
from bthl.operator.copy_property import OBJECT_OT_copy_custom_property_to_selected
from bthl.operator.setup_dmx_properties import OBJECT_OT_add_base_dmx_custom_properties
from bthl.operator.duplicate_property import OBJECT_OT_duplicate_custom_property
from bthl.tasks.sender import UDPClientTasks
from bthl.tasks.customproperties import CustomPropertiesTask
from bthl.tasks.receiver import receive

classes = {
    GlobalControlPanel,
    UDPClientToggleModal,
    OBJECT_OT_copy_custom_property_to_selected,
    OBJECT_OT_add_base_dmx_custom_properties,
    OBJECT_OT_duplicate_custom_property,
}

tasks = {
    UDPClientTasks,
    CustomPropertiesTask,
}

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    for task in tasks:
        task.register(task)
    
    bpy.app.timers.register(receive, persistent=True)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for task in tasks:
        task.unregister(task)
    
    bpy.app.timers.unregister(receive)
