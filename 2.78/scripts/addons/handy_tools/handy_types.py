'''
Created on Jun 1, 2017

@author: Andrew
'''
import bpy
import bmesh
from . import handy_utils

class Assembly:
    
    obj_bp = None
    
    obj_x = None
    obj_y = None
    obj_z = None
    
    def __init__(self,obj_bp=None):
        """ 
        Assembly Constructor. If you want to create an instance of
        an existing Assembly then pass in the base point of the assembly 
        in the obj_bp parameter
        
        **Parameters:**
        
        * **obj_bp** (bpy.types.object, (optional))
        
        **Returns:** None
        """
        if obj_bp:
            self.obj_bp = obj_bp
            for child in obj_bp.children:
                if child.mv.type == 'XDIM':
                    self.obj_x = child
                if child.mv.type == 'YDIM':
                    self.obj_y = child
                if child.mv.type == 'ZDIM':
                    self.obj_z = child
                if self.obj_bp and self.obj_x and self.obj_y and self.obj_z:
                    break    
    
    def create_assembly(self):
        """ 
        This creates the basic structure for an assembly.
        This must be called first when creating an assembly from a script.
        """
        
        self.obj_bp = bpy.data.objects.new("ASSEMBLY.Base_Point",None)
        bpy.context.scene.objects.link(self.obj_bp)
        
        self.obj_x = bpy.data.objects.new("ASSEMBLY.X_DIM",None)
        bpy.context.scene.objects.link(self.obj_x)
        self.obj_x .parent = self.obj_bp
        
        self.obj_y = bpy.data.objects.new("ASSEMBLY.Y_DIM",None)
        bpy.context.scene.objects.link(self.obj_y)
        self.obj_y.parent = self.obj_bp 
        
        self.obj_z = bpy.data.objects.new("ASSEMBLY.Z_DIM",None)
        bpy.context.scene.objects.link(self.obj_z)
        self.obj_z.parent = self.obj_bp
        
    def add_mesh(self,name,include_hooks = True):
        width = self.obj_x.location.x
        height = self.obj_z.location.z
        depth = self.obj_y.location.y
        
        verts = [(0.0, 0.0, 0.0),
                 (0.0, depth, 0.0),
                 (width, depth, 0.0),
                 (width, 0.0, 0.0),
                 (0.0, 0.0, height),
                 (0.0, depth, height),
                 (width, depth, height),
                 (width, 0.0, height),
                 ]
    
        faces = [(0, 1, 2, 3),
                 (4, 7, 6, 5),
                 (0, 4, 5, 1),
                 (1, 5, 6, 2),
                 (2, 6, 7, 3),
                 (4, 0, 3, 7),
                ]
        
        mesh = bpy.data.meshes.new(name)
        
        bm = bmesh.new()
    
        for v_co in verts:
            bm.verts.new(v_co)
        
        for f_idx in faces:
            bm.verts.ensure_lookup_table()
            bm.faces.new([bm.verts[i] for i in f_idx])
        
        bm.to_mesh(mesh)
        
        mesh.update()
        
        obj_mesh = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.scene.objects.link(obj_mesh)
        obj_mesh.parent = self.obj_bp
        
        if include_hooks:
            vg_x_dim = obj_mesh.vertex_groups.new(name="X Dimension")
            vg_x_dim.add([2,3,6,7],1,'ADD')
            
            vg_y_dim = obj_mesh.vertex_groups.new(name="Y Dimension")
            vg_y_dim.add([1,2,5,6],1,'ADD')
            
            vg_z_dim = obj_mesh.vertex_groups.new(name="Z Dimension")
            vg_z_dim.add([4,5,6,7],1,'ADD')
            
            handy_utils.hook_vertex_group_to_object(obj_mesh,"X Dimension",self.obj_x)
            handy_utils.hook_vertex_group_to_object(obj_mesh,"Y Dimension",self.obj_y)
            handy_utils.hook_vertex_group_to_object(obj_mesh,"Z Dimension",self.obj_z)
            
class Wall(Assembly):
    
    def __init__(self,obj_bp=None):
        pass