'''
Created on May 30, 2017

@author: Andrew
'''
import bpy
import bgl
import blf
import os

ICON_WIDTH = 128
ICON_HEIGHT = 128

TARGET_ITEM_WIDTH = 400
TARGET_ITEM_HEIGHT = 128
ITEM_MARGIN_X = 5
ITEM_MARGIN_Y = 5
ITEM_PADDING_X = 5

class Node:
    """ This is a single node in the library 
    """
    
    NODE_TYPE = "LIBRARY" #LIBRARY, CATEGORY, ITEM
    
    x = 0
    y = 0
    
    width = 150
    height = 60
    
    x_location = 0
    y_location = 0
    
    icon_margin_x = 4
    icon_margin_y = 4
    text_margin_x = 6

    text_height = 16
    text_width = 72
    
    def __init__(self,x,y,width,height,module="",class_name=""):
        """ x = x location of the library node in px
            y = y location of the library node in px
            width = width of the library node in px
            height = height of the library node in px
            loc = location of the library node in px from bottom left
            module = module to store item logic
            class_name = class name to store item logic
        """
        pass
    
    def draw_node(self):
        """ Draws the Node onto the interface
        """
        bgl.glEnable(bgl.GL_BLEND)
#         if highlighted:
#             bgl.glColor4f(0.555, 0.555, 0.555, 0.8)
#         else:
        bgl.glColor4f(0.447, 0.447, 0.447, 0.8)

        bgl.glRectf(self.x, self.y, self.x + self.width, self.y + self.height)

        texture = bpy.data.images.load(filepath=os.path.join(os.path.dirname(__file__),"folder.png")) 
        err = texture.gl_load(filter=bgl.GL_NEAREST, mag=bgl.GL_NEAREST)
        assert not err, 'OpenGL error: %i' % err

        bgl.glColor4f(0.0, 0.0, 1.0, 0.5)
        # bgl.glLineWidth(1.5)

        # ------ TEXTURE ---------#
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture.bindcode[0])
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

        bgl.glColor4f(1, 1, 1, 1)
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glTexCoord2d(0, 0)
        bgl.glVertex2d(self.x + self.icon_margin_x, self.y)
        bgl.glTexCoord2d(0, 1)
        bgl.glVertex2d(self.x + self.icon_margin_x, self.y + ICON_HEIGHT)
        bgl.glTexCoord2d(1, 1)
        bgl.glVertex2d(self.x + self.icon_margin_x + ICON_WIDTH, self.y + ICON_HEIGHT)
        bgl.glTexCoord2d(1, 0)
        bgl.glVertex2d(self.x + self.icon_margin_x + ICON_WIDTH, self.y)
        bgl.glEnd()
        bgl.glDisable(bgl.GL_TEXTURE_2D)
        bgl.glDisable(bgl.GL_BLEND)

        texture.gl_free()
        
        # draw some text
        font_id = 0
        blf.position(font_id,
                     self.x + self.icon_margin_x + ICON_WIDTH + self.text_margin_x,
                     self.y + ICON_HEIGHT * 0.5 - 0.25 * self.text_height, 0)
        blf.size(font_id, self.text_height, self.text_width)
        blf.draw(font_id, "Library Folder")
    
    def highlighted(self):
        """ Determines if the mouse is over the node
        """
        pass
    
    def clicked(self):
        """ This is called when the node is clicked
        """
        pass
    
class Button:
    
    command = None
    
    width = 150
    height = 60
    
    x_location = 0
    y_location = 350
    
    def __init__(self,):
        pass
    
    def draw(self, highlighted: bool):
        bgl.glEnable(bgl.GL_BLEND)

        if highlighted:
            bgl.glColor4f(0.555, 0.555, 0.555, 0.8)
        else:
            bgl.glColor4f(0.447, 0.447, 0.447, 0.8)   

        #HEADER
        bgl.glColor4f(0.1, 0.1, 0.1, 1)
        bgl.glRectf(self.x_location, self.y_location, self.width, self.height)  
        
        bgl.glDisable(bgl.GL_BLEND)             
    
    def highlighted(self, mouse_x: int, mouse_y: int) -> bool:
        """ Determines if the mouse is over the node
        """
        print(self.x_location < mouse_x < self.x_location + self.width and self.y_location < mouse_y < self.y_location + self.height)
        return self.x_location < mouse_x < self.x_location + self.width and self.y_location < mouse_y < self.y_location + self.height
    
    def clicked(self):
        """ This is called when the node is clicked
        """
        pass
    
    
class Library_Panel:
    """ This is the library panel
    """
    
    mouse_x = 0
    mouse_y = 0
    
    width = 400
    height = 0
    
    x_location = 0
    y_location = 0
    
    text_height = 16
    text_width = 72    
    
    icon_margin_x = 4
    icon_margin_y = 4
    text_margin_x = 6
    
    header_height = 45
    
    def __init__(self,window_region):
        content_width = window_region.width
        content_height = window_region.height
        self.height = content_height
    
    def draw_back_button(self):
        pass
    
    def draw_libraries(self):
        pass
    
    def draw_categories(self):
        pass
    
    def draw_panel(self):
        bgl.glEnable(bgl.GL_BLEND)
        #PANEL
        bgl.glColor4f(0.0, 0.0, 0.0, 0.1)
        bgl.glRectf(self.x_location, self.y_location, self.width, self.height)
        #HEADER
        bgl.glColor4f(0.1, 0.1, 0.1, 1)
        bgl.glRectf(self.x_location, self.height-self.header_height, self.width, self.height)  
              
        bgl.glDisable(bgl.GL_BLEND)
        
        #HEADER TEXT
        bgl.glColor4f(1, 1, 1, 1)
        font_id = 0
        blf.position(font_id,20,self.height-self.text_height-self.icon_margin_y, 0)
        blf.size(font_id, self.text_height, self.text_width)
        blf.draw(font_id, "hAndy Tool Library")
    
    def draw_library(self,mouse_x,mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.draw_panel()
    
class OPERATOR_Show_Library(bpy.types.Operator):    
    bl_idname = "handy.show_library"
    bl_label = "Show Library" 
     
    _draw_handle = None
     
    mouse_x = 0
    mouse_y = 0
    
    def finish(self,context):
        context.space_data.draw_handler_remove(self._draw_handle, 'WINDOW')
        context.window.cursor_modal_restore()        
        context.area.tag_redraw()    

#QUESTION: I AM NOT SURE WHY THIS IS NEEDED 
#     @staticmethod
#     def _window_region(context):
#         window_regions = [region
#                           for region in context.area.regions
#                           if region.type == 'WINDOW']
#         return window_regions[0]

    def draw_menu(self,context):
        window_region = [region
                          for region in context.area.regions
                          if region.type == 'WINDOW'][0]   
                    
        library = Library_Panel(window_region)
        library.draw_library(mouse_x=self.mouse_x,mouse_y=self.mouse_y)
        
        button = Button()
        button.draw(highlighted=button.highlighted(self.mouse_x, self.mouse_y))        
        
#         node = Node(x=100,y=0,width=300,height=100)
#         node.draw_node()

    def invoke(self, context, event):
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        
        self._draw_handle = context.space_data.draw_handler_add(
            self.draw_menu, (context,), 'WINDOW', 'POST_PIXEL')
        
        self.current_display_content = []
        
        context.window.cursor_modal_set('DEFAULT')
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):

        if 'MOUSE' in event.type:
            context.area.tag_redraw()
            self.mouse_x = event.mouse_x
            self.mouse_y = event.mouse_y

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}        
        
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.finish(context)
            return {'FINISHED'}        
        
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.finish(context)
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        print("EXECUTE")
        return {'FINISHED'}    
    
    
class PANEL_Library(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "hAndy Tools"
    bl_category = "Fluid Designer"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("handy.show_library")

bpy.utils.register_class(PANEL_Library)
bpy.utils.register_class(OPERATOR_Show_Library)    