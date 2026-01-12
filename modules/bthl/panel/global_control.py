from bpy.types import Panel, Context
import bthl.operator.sender_modal as sender_modal

class GlobalControlPanel(Panel):
    bl_label = "HNode Connector"
    bl_idname = "OBJECT_PT_main_panel"

    #Specific controls for the sidebar in the 3d view
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HNode Connector'

    def draw(self, context: Context):
        layout = self.layout
        if layout is None:
            return
        #scene = context.scene

        #render udp client
        layout.operator(sender_modal.UDPClientToggleModal.bl_idname, text=sender_modal.UDPClientToggleModal.dynamic_text(context))
