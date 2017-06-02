'''
Created on Jun 1, 2017

@author: Andrew
'''
import bpy
import bmesh

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
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.vertex_group_select()
        if obj_mesh.data.total_vert_sel > 0:
            bpy.ops.object.hook_add_selob()
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()

class Assembly:
    
    obj_bp = None
    
    obj_x = None
    obj_y = None
    obj_z = None
    
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
            
            hook_vertex_group_to_object(obj_mesh,"X Dimension",self.obj_x)
            hook_vertex_group_to_object(obj_mesh,"Y Dimension",self.obj_y)
            hook_vertex_group_to_object(obj_mesh,"Z Dimension",self.obj_z)
            
            
            
            