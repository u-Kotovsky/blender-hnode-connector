import bpy

class OBJECT_OT_add_base_dmx_custom_properties(bpy.types.Operator):
    bl_idname = "object.add_base_dmx_custom_properties"
    bl_label = "Add Base DMX Properties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}

        #Universe
        obj["Universe"] = 1
        ui_universe = obj.id_properties_ui("Universe")
        if ui_universe is not None:
            ui_universe.update(
                description="DMX Universe (1-512)",
                min=1,
                max=512,
                default=1
            )

        #Channel
        obj["Channel"] = 1
        ui_channel = obj.id_properties_ui("Channel")
        if ui_channel is not None:
            ui_channel.update(
                min=1,
                max=512,
                description="DMX Channel (1-512)",
                default=1
            )

        return {'FINISHED'}

    def draw_custom_properties_context_menu(self, context):
        # Only show when an object is active
        if not context.active_object:
            return

        layout = self.layout
        if layout is None:
            return
        layout.separator()
        layout.operator(
            OBJECT_OT_add_base_dmx_custom_properties.bl_idname,
            icon='PRESET'
        )
    
    @staticmethod
    def register():
        """Register the operator"""
        bpy.types.UI_MT_button_context_menu.append(OBJECT_OT_add_base_dmx_custom_properties.draw_custom_properties_context_menu)
    
    @staticmethod
    def unregister():
        """Unregister the operator"""
        bpy.types.UI_MT_button_context_menu.remove(OBJECT_OT_add_base_dmx_custom_properties.draw_custom_properties_context_menu)
