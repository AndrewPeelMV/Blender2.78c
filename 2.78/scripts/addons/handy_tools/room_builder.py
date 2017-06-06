import bpy
import bmesh
import math
from . import unit
from . import handy_types, handy_utils

def delete_obj_list(obj_list):
    """ This function deletes every object in the list
    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in obj_list:
        if obj.animation_data:
            for driver in obj.animation_data.drivers:
                if driver.data_path in {'hide','hide_select'}: # THESE DRIVERS MUST BE REMOVED TO DELETE OBJECTS
                    obj.driver_remove(driver.data_path) 
        
        obj.parent = None
        obj.hide_select = False
        obj.hide = False
        obj.select = True
        
        if obj.name in bpy.context.scene.objects:
            bpy.context.scene.objects.unlink(obj)

#   I HAVE HAD PROBLEMS WITH THIS CRASHING BLENDER
#   HOPEFULLY THE do_unlink PARAMETER WORKS
    for obj in obj_list:
        bpy.data.objects.remove(obj,do_unlink=True)

def delete_object_and_children(obj_bp):
    """ Deletes a object and all it's children
    """
    obj_list = []
    obj_list.append(obj_bp)
    for child in obj_bp.children:
        if len(child.children) > 0:
            delete_object_and_children(child)
        else:
            obj_list.append(child)
    delete_obj_list(obj_list)

class OPS_draw_walls(bpy.types.Operator):
    bl_idname = "fd_assembly.draw_wall"
    bl_label = "Draws Walls"
    bl_options = {'UNDO'}
    
    #READONLY
    drawing_plane = None
    wall = None
    previous_wall = None
    is_disconnected = False
    
    typed_value = ""
    
    starting_point = (0,0,0)
    header_text = "(Esc, Right Click) = Cancel Command  :  (Left Click) = Place Wall  :  (Ctrl) = Disconnect/Move Wall"
    
    def cancel_drop(self,context,event):
        delete_object_and_children(self.wall.obj_bp)
        context.window.cursor_set('DEFAULT')
        delete_obj_list([self.drawing_plane])
        return {'FINISHED'}
        
    def __del__(self):
        bpy.context.area.header_text_set()
        
    def create_wall(self):
        con = None
        if self.previous_wall:
            con = self.previous_wall.obj_x
            
        self.wall = fd_types.Wall()
        self.wall.create_wall()
        obj_mesh = self.wall.build_wall_mesh()
        self.wall.obj_bp.location = self.starting_point
        obj_mesh.draw_type = 'WIRE'
        self.wall.obj_z.location.z = bpy.context.scene.mv.default_wall_height
        self.wall.obj_y.location.y = bpy.context.scene.mv.default_wall_depth
        self.wall.obj_bp.mv.item_number = self.get_wall_count()
        if con:
            constraint = self.wall.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = con
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = True
            
        width = self.wall.get_var("dim_x","width")
        height = self.wall.get_var("dim_z","height")
        depth = self.wall.get_var("dim_y","depth")
             
        dim = fd_types.Dimension()
        dim.parent(self.wall.obj_bp)
        dim.start_y('depth+INCH(5)',[depth])
        dim.start_z('height+INCH(5)',[height])
        dim.end_x('width',[width])
        dim.anchor.hide = True
        
    def position_wall(self,p):
        x = p[0] - self.starting_point[0]
        y = p[1] - self.starting_point[1]
        
        if math.fabs(x) > math.fabs(y):
            if x > 0:
                self.wall.obj_bp.rotation_euler.z = math.radians(0)
            else:
                self.wall.obj_bp.rotation_euler.z = math.radians(180)
            if self.typed_value == "":
                self.wall.obj_x.location.x = math.fabs(x)
            else:
                value = eval(self.typed_value)
                if bpy.context.scene.unit_settings.system == 'METRIC':
                    self.wall.obj_x.location.x = unit.millimeter(float(value))
                else:
                    self.wall.obj_x.location.x = unit.inch(float(value))
            
        if math.fabs(y) > math.fabs(x):
            if y > 0:
                self.wall.obj_bp.rotation_euler.z = math.radians(90)
            else:
                self.wall.obj_bp.rotation_euler.z = math.radians(-90)
            if self.typed_value == "":
                self.wall.obj_x.location.x = math.fabs(y)
            else:
                value = eval(self.typed_value)
                if bpy.context.scene.unit_settings.system == 'METRIC':
                    self.wall.obj_x.location.x = unit.millimeter(float(value))
                else:
                    self.wall.obj_x.location.x = unit.inch(float(value))
                
    def extend_wall(self):
        if self.previous_wall and not self.is_disconnected:
            prev_wall_rot = round(self.previous_wall.obj_bp.rotation_euler.z,2)
            wall_rot = round(self.wall.obj_bp.rotation_euler.z,2)
            
            extend_wall = False
            
            if prev_wall_rot == round(math.radians(0),2):
                if wall_rot == round(math.radians(-90),2):
                    extend_wall = True
            if prev_wall_rot == round(math.radians(-90),2):
                if wall_rot == round(math.radians(180),2):
                    extend_wall = True
            if prev_wall_rot == round(math.radians(180),2):
                if wall_rot == round(math.radians(90),2):
                    extend_wall = True
            if prev_wall_rot == round(math.radians(90),2):
                if wall_rot == round(math.radians(0),2):
                    extend_wall = True
            
            if extend_wall:
                obj = self.previous_wall.get_wall_mesh()
                bpy.ops.fd_object.apply_hook_modifiers(object_name=obj.name)
                
                mesh = obj.data
                
                bm = bmesh.new()
                
                size = (self.previous_wall.obj_x.location.x,self.previous_wall.obj_y.location.y,self.previous_wall.obj_z.location.z)
                
                verts = [(0.0, 0.0, 0.0),
                         (0.0, size[1], 0.0),
                         (size[0], size[1], 0.0),
                         (size[0], 0.0, 0.0),
                         (0.0, 0.0, size[2]),
                         (0.0, size[1], size[2]),
                         (size[0], size[1], size[2]),
                         (size[0], 0.0, size[2]),
                         (size[0]+bpy.context.scene.mv.default_wall_depth, size[1], 0.0),
                         (size[0]+bpy.context.scene.mv.default_wall_depth, 0.0, 0.0),
                         (size[0]+bpy.context.scene.mv.default_wall_depth, 0.0, size[2]),
                         (size[0]+bpy.context.scene.mv.default_wall_depth, size[1], size[2]),
                         ]
                
                faces = [(0, 1, 2, 3),   #bottom
                         (4, 7, 6, 5),   #top
                         (0, 4, 5, 1),   #left face
                         (1, 5, 6, 2),   #back face
                         (4, 0, 3, 7),   #wall face
                         (3, 9, 8, 2),   #2bottom
                         (7, 10, 11, 6), #2top
                         (2, 6, 11, 8),  #2backface
                         (7, 3, 9, 10),  #2wallface
                         (8, 11, 10, 9), #rightface
                        ]
                
                for v_co in verts:
                    bm.verts.new(v_co)
                
                for f_idx in faces:
                    bm.verts.ensure_lookup_table()
                    bm.faces.new([bm.verts[i] for i in f_idx])
                
                bm.to_mesh(mesh)
                
                mesh.update()
                
                vgroup = obj.vertex_groups.new(name="X Dimension")
                vgroup.add([2,3,6,7,8,9,10,11],1,'ADD')
                
                vgroup = obj.vertex_groups.new(name="Y Dimension")
                vgroup.add([1,2,8,11,6,5],1,'ADD')
                
                vgroup = obj.vertex_groups.new(name="Z Dimension")
                vgroup.add([4,5,6,7,10,11],1,'ADD')                                           
                
                handy_utils.hook_vertex_group_to_object(obj,'X Dimension',self.previous_wall.obj_x)
                handy_utils.hook_vertex_group_to_object(obj,'Y Dimension',self.previous_wall.obj_y)
                handy_utils.hook_vertex_group_to_object(obj,'Z Dimension',self.previous_wall.obj_z)
                
                self.previous_wall.obj_x.hide = True
                self.previous_wall.obj_y.hide = True
                self.previous_wall.obj_z.hide = True
                
                if len(obj.data.uv_textures) == 0:
                    bpy.ops.fd_object.unwrap_mesh(object_name=obj.name)                
                
    def set_type_value(self,event):
        if event.value == 'PRESS':
            if event.type == "ONE" or event.type == "NUMPAD_1":
                self.typed_value += "1"
            if event.type == "TWO" or event.type == "NUMPAD_2":
                self.typed_value += "2"
            if event.type == "THREE" or event.type == "NUMPAD_3":
                self.typed_value += "3"
            if event.type == "FOUR" or event.type == "NUMPAD_4":
                self.typed_value += "4"
            if event.type == "FIVE" or event.type == "NUMPAD_5":
                self.typed_value += "5"
            if event.type == "SIX" or event.type == "NUMPAD_6":
                self.typed_value += "6"
            if event.type == "SEVEN" or event.type == "NUMPAD_7":
                self.typed_value += "7"
            if event.type == "EIGHT" or event.type == "NUMPAD_8":
                self.typed_value += "8"
            if event.type == "NINE" or event.type == "NUMPAD_9":
                self.typed_value += "9"
            if event.type == "ZERO" or event.type == "NUMPAD_0":
                self.typed_value += "0"
            if event.type == "PERIOD" or event.type == "NUMPAD_PERIOD":
                last_value = self.typed_value[-1:]
                if last_value != ".":
                    self.typed_value += "."
            if event.type == 'BACK_SPACE':
                if self.typed_value != "":
                    self.typed_value = self.typed_value[:-1]
            
    def place_wall(self):
        self.wall.refresh_hook_modifiers()
        for child in self.wall.obj_bp.children:
            child.draw_type = 'TEXTURED'
        self.wall.obj_x.hide = True
        self.wall.obj_y.hide = True
        self.wall.obj_z.hide = True
        self.starting_point = (self.wall.obj_x.matrix_world[0][3], self.wall.obj_x.matrix_world[1][3], self.wall.obj_x.matrix_world[2][3])
        self.extend_wall()
        self.previous_wall = self.wall
        self.create_wall()
        self.typed_value = ""
        self.is_disconnected = False
        
    def event_is_place_wall(self,event):
        if not event.ctrl:
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                return True
            elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
                return True
            elif event.type == 'RET' and event.value == 'PRESS':
                return True
            else:
                return False
        else:
            return False
        
    def event_is_cancel(self,event):
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'ESC' and event.value == 'PRESS':
            return True
        else:
            return False
        
    def get_wall_count(self):
        wall_number = 0
        for obj in bpy.context.visible_objects:
            if obj.mv.type == "BPWALL":
                wall_number += 1
        return wall_number
            
    def modal(self, context, event):
        self.set_type_value(event)
        wall_length_text = str(unit.meter_to_active_unit(round(self.wall.obj_x.location.x,4)))
        wall_length_unit = '"' if context.scene.unit_settings.system == 'IMPERIAL' else 'mm'
        context.area.header_text_set(text=self.header_text + '   (Current Wall Length = ' + wall_length_text + wall_length_unit + ')')
        context.window.cursor_set('PAINT_BRUSH')
        context.area.tag_redraw()
        selected_point, selected_obj = handy_utils.get_selection_point(context,event,objects=[self.drawing_plane]) #Pass in Drawing Plane
        bpy.ops.object.select_all(action='DESELECT')
        self.wall.obj_y.location.y = bpy.context.scene.mv.default_wall_depth
        if selected_obj:
            if event.ctrl:
                self.is_disconnected = True
                self.wall.obj_bp.constraints.clear()
                self.wall.obj_bp.location.x = selected_point[0]
                self.wall.obj_bp.location.y = selected_point[1]
                self.wall.obj_bp.location.z = 0
                self.wall.obj_y.location.y = 0
                self.wall.obj_x.location.x = 0
                self.starting_point = (self.wall.obj_bp.location.x, self.wall.obj_bp.location.y, 0)
            else:
                selected_obj.select = True
                self.position_wall(selected_point)
            
        if self.event_is_place_wall(event):
            self.place_wall()

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
            
        if self.event_is_cancel(event):
            return self.cancel_drop(context,event)
            
        return {'RUNNING_MODAL'}
        
    def execute(self,context):
        wall_bp = handy_utils.get_wall_bp(context.active_object)
        if wall_bp:
            self.previous_wall = fd_types.Wall(wall_bp)
            self.starting_point = (self.previous_wall.obj_x.matrix_world[0][3], self.previous_wall.obj_x.matrix_world[1][3], self.previous_wall.obj_x.matrix_world[2][3])
            
        self.create_wall()
        
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0,0,0)
        self.drawing_plane = context.active_object
        self.drawing_plane.draw_type = 'WIRE'
        self.drawing_plane.dimensions = (100,100,1)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}