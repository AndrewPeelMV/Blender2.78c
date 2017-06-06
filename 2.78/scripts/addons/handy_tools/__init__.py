bl_info = {
    "name": "hAndy Tools",
    "author": "Andrew Peel",
    "version": (1, 0, 0),
    "blender": (2, 7, 0),
    "location": "Tools Shelf",
    "description": "This add-on has a bunch of handy tools for blender",
    "warning": "",
    "wiki_url": "",
    "category": "Tools"
}

from . import library_panel
from . import handy_properties

def register():
    pass

def unregister():
    pass