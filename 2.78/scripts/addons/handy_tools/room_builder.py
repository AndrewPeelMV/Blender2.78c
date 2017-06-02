from . import assembly_group

def draw_wall():
    wall = assembly_group.Assembly()
    wall.create_assembly()
    wall.obj_x.location.x = 1
    wall.obj_y.location.y = 1
    wall.obj_z.location.z = 1
    wall.add_mesh("Wall", include_hooks = True)
    