'''
Created on May 30, 2017

@author: Andrew
'''
import bpy
import bgl
import blf
import os
from . import room_builder

ICON_WIDTH = 64
ICON_HEIGHT = 64

TARGET_ITEM_WIDTH = 400
TARGET_ITEM_HEIGHT = 128
ITEM_MARGIN_X = 5
ITEM_MARGIN_Y = 5
ITEM_PADDING_X = 5

ICON_MARGIN_X = 5

FOLDER_ICON = os.path.join(os.path.dirname(__file__),"icons","folder.png")
DRAW_NEW_WALL_ICON = os.path.join(os.path.dirname(__file__),"icons","draw_new_wall_64.png")

class Button:
    
    command = None
    
    icon = ""
    text = ""
    
    width = 200
    height = 50
    
    x_location = 100
    y_location = 350
    
    text_height = 16
    text_width = 72    
    
    def __init__(self,x_location,y_location,width,height):
        self.width = width
        self.height = height        
        self.x_location = x_location
        self.y_location = y_location

    def draw_button_boarder(self,highlighted: bool):
        bgl.glEnable(bgl.GL_BLEND)
        if highlighted:
            bgl.glColor4f(0.555, 0.555, 0.555, 0.8)
        else:
            bgl.glColor4f(0.447, 0.447, 0.447, 0.8)   
        bgl.glRectf(self.x_location, self.y_location, self.width + self.x_location, self.height + self.y_location)  
        bgl.glDisable(bgl.GL_BLEND)

    def draw_button_icon(self):
        if self.icon != "":
            bgl.glEnable(bgl.GL_BLEND)
            texture = bpy.data.images.load(filepath=self.icon) 
            err = texture.gl_load(filter=bgl.GL_NEAREST, mag=bgl.GL_NEAREST)
            assert not err, 'OpenGL error: %i' % err
    
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture.bindcode[0])
            bgl.glEnable(bgl.GL_TEXTURE_2D)
            bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
    
            bgl.glColor4f(1, 1, 1, 1)
            bgl.glBegin(bgl.GL_QUADS)
            bgl.glTexCoord2d(0, 0)
            bgl.glVertex2d(self.x_location + ICON_MARGIN_X, self.y_location)
            bgl.glTexCoord2d(0, 1)
            bgl.glVertex2d(self.x_location + ICON_MARGIN_X, self.y_location + ICON_HEIGHT)
            bgl.glTexCoord2d(1, 1)
            bgl.glVertex2d(self.x_location + ICON_MARGIN_X + ICON_WIDTH, self.y_location + ICON_HEIGHT)
            bgl.glTexCoord2d(1, 0)
            bgl.glVertex2d(self.x_location + ICON_MARGIN_X + ICON_WIDTH, self.y_location)
            bgl.glEnd()
            bgl.glDisable(bgl.GL_TEXTURE_2D)
            bgl.glDisable(bgl.GL_BLEND)
    
            texture.gl_free()
    
    def draw(self, highlighted: bool):
        self.draw_button_boarder(highlighted)
        self.draw_button_icon()
        
        # draw some text
        font_id = 0
        blf.position(font_id,
                     self.x_location + ICON_MARGIN_X + ICON_WIDTH + ICON_MARGIN_X,
                     self.y_location + ICON_HEIGHT * 0.5 - 0.25 * self.text_height, 0)
        blf.size(font_id, self.text_height, self.text_width)
        blf.draw(font_id, self.text)
    
    def is_hightlighted(self,mouse_x,mouse_y):
        #TODO: THIS COMMAND NEEDS TO ACCOUNT FOR REGION POSITION
        inside_x = False
        inside_y = False
        if self.x_location < mouse_x and self.x_location + self.width > mouse_x:
            inside_x = True
        if self.y_location < mouse_y and self.y_location + self.height > mouse_y:
            inside_y = True
        return True if inside_x and inside_y else False

#QUESTION:
#I am not sure why the highlighted command is wrtten this way
#     def highlighted(self, mouse_x: int, mouse_y: int) -> bool:
#         """ Determines if the mouse is over the node
#         """
#         print(self.x_location < mouse_x < self.x_location + self.width and self.y_location < mouse_y < self.y_location + self.height)
#         return self.x_location < mouse_x < self.x_location + self.width and self.y_location < mouse_y < self.y_location + self.height
    
    def clicked(self,context,event):
        """ This is called when the node is clicked
        """
        self.command(context,event)
    
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
    event = None
    
    active_button = None
    
    loaded_images = set()
    current_buttons = []
    
    def clear_images(self):
        """Removes all images we loaded from Blender's memory."""

        for image in bpy.data.images:
            if image.filepath_raw not in self.loaded_images:
                continue

            image.user_clear()
            bpy.data.images.remove(image)

        self.loaded_images.clear()    
    
    def finish(self,context):
        self.clear_images()
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
        
        button_height = 64
        button_width = 250
        button_spacing = 20
        
        button = Button(10,window_region.height-library.header_height-(button_spacing+button_height),button_width,button_height)
        button.text = "Draw New Wall"
        button.command = room_builder.draw_new_wall
        button.icon = DRAW_NEW_WALL_ICON
        button.draw(highlighted=button.is_hightlighted(self.mouse_x,self.mouse_y))
        self.store_button(button)
        
#         for i in range(1,10):
#             button = Button(20,window_region.height-library.header_height-(button_spacing+button_height)*i,button_width,button_height)
#             button.text = "Draw Walls"
#             button.command = room_builder.draw_wall
#             button.icon = FOLDER_ICON
#             button.draw(highlighted=button.is_hightlighted(self.mouse_x,self.mouse_y))
#             self.store_button(button)

    def store_button(self,button):
        """ keep button so we can remove image
            and keep track of state
        """
        if button.icon != "":
            self.loaded_images.add(button.icon)
        self.current_buttons.append(button)

    def get_clicked(self):
        for item in self.current_buttons:
            if item.is_hightlighted(self.mouse_x, self.mouse_y):
                return item
        return None

    def invoke(self, context, event):
        self.event = event
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        
        self._draw_handle = context.space_data.draw_handler_add(
            self.draw_menu, (context,), 'WINDOW', 'POST_PIXEL')
        
        self.current_display_content = []
        self.loaded_images = set()
        
        context.window.cursor_modal_set('DEFAULT')
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        self.event = event
        
        if 'MOUSE' in event.type:
            context.area.tag_redraw()
            self.mouse_x = event.mouse_x
            self.mouse_y = event.mouse_y

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}        
        
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            button = self.get_clicked()
            if button:
                button.clicked(context,event)
            else:
                print("NO BUTTON") 
        
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