'''
Created on Jun 5, 2017

@author: Andrew
'''
import bpy
from bpy_extras import view3d_utils

def get_selection_point(context, event, ray_max=10000.0,objects=None,floor=None):
    """Gets the point to place an object based on selection"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
    
    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_target = ray_origin + view_vector
    
    def visible_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""
 
        for obj in context.visible_objects:
             
            if objects:
                if obj in objects:
                    yield (obj, obj.matrix_world.copy())
             
            else:
                if floor is not None and obj == floor:
                    yield (obj, obj.matrix_world.copy())
                     
                if obj.draw_type != 'WIRE':
                    if obj.type == 'MESH':
                        if obj.mv.type not in {'BPASSEMBLY','BPWALL'}:
                            yield (obj, obj.matrix_world.copy())
         
                    if obj.dupli_type != 'NONE':
                        obj.dupli_list_create(scene)
                        for dob in obj.dupli_list:
                            obj_dupli = dob.object
                            if obj_dupli.type == 'MESH':
                                yield (obj_dupli, dob.matrix.copy())
 
            obj.dupli_list_clear()
 
    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""
        try:
            # get the ray relative to the object
            matrix_inv = matrix.inverted()
            ray_origin_obj = matrix_inv * ray_origin
            ray_target_obj = matrix_inv * ray_target
            ray_direction_obj = ray_target_obj - ray_origin_obj
     
            # cast the ray
            success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)
     
            if success:
                return location, normal, face_index
            else:
                return None, None, None
        except:
            print("ERROR IN obj_ray_cast",obj)
            return None, None, None
             
    best_length_squared = ray_max * ray_max
    best_obj = None
    best_hit = scene.cursor_location
    for obj, matrix in visible_objects_and_duplis():
        if obj.type == 'MESH':
            if obj.data:
                hit, normal, face_index = obj_ray_cast(obj, matrix)
                if hit is not None:
                    hit_world = matrix * hit
                    length_squared = (hit_world - ray_origin).length_squared
                    if length_squared < best_length_squared:
                        best_hit = hit_world
                        best_length_squared = length_squared
                        best_obj = obj
                        
    return best_hit, best_obj

def hook_vertex_group_to_object(obj_mesh,vertex_group,obj_hook):
    """ This function adds a hook modifier to the verties 
        in the vertex_group to the obj_hook
    """
    bpy.ops.object.select_all(action = 'DESELECT')
    obj_hook.hide = False
    obj_hook.hide_select = False
    obj_hook.select = True
    obj_mesh.hide = False
    obj_mesh.hide_select = False
    if vertex_group in obj_mesh.vertex_groups:
        vgroup = obj_mesh.vertex_groups[vertex_group]
        obj_mesh.vertex_groups.active_index = vgroup.index
        bpy.context.scene.objects.active = obj_mesh
        bpy.ops.fd_object.toggle_edit_mode(object_name=obj_mesh.name)
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.vertex_group_select()
        if obj_mesh.data.total_vert_sel > 0:
            bpy.ops.object.hook_add_selob()
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.fd_object.toggle_edit_mode(object_name=obj_mesh.name)
        
def get_wall_bp(obj):
    """ This will get the wall base point from the passed in object
    """
    if obj:
        if obj.mv.type == 'BPWALL':
            return obj
        else:
            if obj.parent:
                return get_wall_bp(obj.parent)        