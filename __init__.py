# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
  "name" : "Tori 0.2.1",
  "author" : "Duane Dibbley",
  "version" : (0, 2, 1),
  "blender" : (2, 79, 0),
  "location" : "View3D > Add > Mesh",
  "description" : "Add-on for creating tori of varying configurations",
  "warning" : "This branch is deprecated. It was kept as a non-SciPy version, but the master branch now check for SciPy at run-time and gracefully disables any functionality depending on SciPy. Please consider upgrading, as this branch will receive no more updates and may be deleted at any time without prior notice."
  "category" : "Add Mesh"
}

import bpy
from bpy.types import Menu, INFO_MT_mesh_add
from . import EllipticTorus

class INFO_MT_mesh_elliptic_torus_add(Menu):
  bl_idname = "INFO_MT_mesh_elliptic_torus_add"
  bl_label = "Elliptic Torus"

  def draw(self, context):
    self.layout.operator("mesh.elliptic_torus_add")

  INFO_MT_mesh_add.append(draw)

def register():
  bpy.utils.register_module(__name__)

def unregister():
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()
