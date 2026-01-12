import bpy

class OBJECT_OT_copy_custom_property_to_selected(bpy.types.Operator):
    bl_idname = "object.copy_custom_property_to_selected"
    bl_label = "Copy Custom Property to Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    property_name: bpy.props.StringProperty()

    def execute(self, context):
        active = context.active_object
        if not active:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}

        if self.property_name not in active.keys():
            self.report({'ERROR'}, "Property not found on active object")
            return {'CANCELLED'}

        value = active[self.property_name]

        # UI metadata (if any)
        ui_data = active.id_properties_ui(self.property_name)
        ui_settings = {}
        for attr in (
            "min", "max",
            "soft_min", "soft_max",
            "description",
            "default",
            "subtype"
        ):
            try:
                ui_settings[attr] = getattr(ui_data, attr)
            except Exception:
                pass

        for obj in context.selected_objects:
            if obj == active:
                continue

            obj[self.property_name] = value

            ui = obj.id_properties_ui(self.property_name)
            for key, val in ui_settings.items():
                try:
                    setattr(ui, key, val)
                except Exception:
                    pass

        return {'FINISHED'}

    def draw_custom_property_context_menu(self, context):
        prop = context.button_prop
        if not prop:
            return

        #owner = context.button_owner
        #if not isinstance(owner, bpy.types.Object):
        #    return

        layout = self.layout
        if layout is None:
            return
        op = layout.operator(
            OBJECT_OT_copy_custom_property_to_selected.bl_idname,
            text="Copy Custom Property to Selected Objects",
            icon='DUPLICATE'
        )
        op.property_name = context.button_prop.identifier

    @staticmethod
    def register():
        bpy.types.UI_MT_button_context_menu.append(OBJECT_OT_copy_custom_property_to_selected.draw_custom_property_context_menu)

    @staticmethod
    def unregister():
        bpy.types.UI_MT_button_context_menu.remove(OBJECT_OT_copy_custom_property_to_selected.draw_custom_property_context_menu)
