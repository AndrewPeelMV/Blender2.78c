'''
Created on Jun 5, 2017

@author: Andrew
'''
import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

ENUM_OBJECT_TYPES = [('NONE',"None","None"),
                     ('CAGE',"CAGE","Cage used to represent the bounding area of an assembly"),
                     ('XDIM',"Visible Prompt X Dimension","Visible prompt control in the 3D viewport"),
                     ('YDIM',"Visible Prompt Y Dimension","Visible prompt control in the 3D viewport"),
                     ('ZDIM',"Visible Prompt Z Dimension","Visible prompt control in the 3D viewport"),
                     ('BP',"Base Point","Parent object of an assembly"),
                     ('BPWALL',"Wall Base Point","Parent object of a wall"),
                     ('BPDIM', "Visual Dimension A", "Base Point for OpenGL Dimension")]

class handy_object(bpy.types.PropertyGroup):

    type = EnumProperty(name="type",
                        items=ENUM_OBJECT_TYPES,
                        description="Handy Object Type",
                        default='NONE')

bpy.utils.register_class(handy_object)
bpy.types.Object.handy = PointerProperty(type = handy_object)    