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
  "name" : "Elliptic Torus",
  "author" : "Duane Dibbley",
  "version" : (0, 3, 0),
  "blender" : (2, 79, 0),
  "location" : "View3D > Add > Mesh",
  "description" : "Add an elliptic torus with the cross-section correctly following the ellipse",
  "category" : "Add Mesh"
}

import bpy
from bpy.types import Panel, Menu, Operator
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty, EnumProperty
from math import cos, sin, pi
from mathutils import Vector, Matrix, Euler
from . import HelperFunctions

class MESH_OT_elliptic_torus_add(Operator):
  bl_idname = "mesh.elliptic_torus_add"
  bl_label = "Elliptic Torus"
  bl_options = {"REGISTER", "UNDO", "PRESET"}
  major_major = FloatProperty(name="Ring's Major Semi-Axis", description="Half the major axis of the ring", default=2.3, min=0.0, max=100.0, step=1, precision=3)
  major_minor = FloatProperty(name="Ring's Minor Semi-Axis", description="Half the major axis of the ring", default=1.05, min=0.0, max=100.0, step=1, precision=3)
  vstep = IntProperty(name="Ring Segments", description="Number of segments for the ellipse", default=48, min=4, max=1024)
  ring_spacing_type = EnumProperty(items=[("spacing.area", "Equal Area", "Equally increment the parameter phi equally for each point on the ring (standard ellipse equations)"),
                                          ("spacing.normal", "Equiangular Normal", "Space between points on the ring equiangularly by the direction of the normals"),
                                          ("spacing.radius", "Equiangular Radius", "Space between points on the ring equiangularly by the direction of the radii"),
                                          ("spacing.arc", "Equal Arc Length", "Place points on the ring at equal distance")],
                                   name="Ring Spacing", description="Define how to calculate the space between the points on the ring", default="spacing.area")
  minor_major = FloatProperty(name="Cross-Section's Major Semi-Axis", description="Half the major of the cross-section", default=0.2, min=0.0, max=100.0, step=1, precision=3)
  minor_minor = FloatProperty(name="Cross-Section's Minor Semi-Axis", description="Half the minor of the cross-section", default=0.1, min=0.0, max=100.0, step=1, precision=3)
  ustep = IntProperty(name="Cross-Section Segments", description="Number of segments for the cross-section", default=12, min=4, max=1024)
  cross_twist = IntProperty(name="Cross-Section Twists", description="Number of twists of the cross-section; 1 twist equals 180 degrees", default=0, min=0, max=256)
  cross_rotation = FloatProperty(name="Cross-Section Initial Rotation", description="Initial rotation of the cross-section", default=0.0, min=-pi/2.0, max=pi/2.0, step=10, precision=3, subtype="ANGLE")
  cross_spacing_type = EnumProperty(items=[("spacing.area", "Equal Area", "Equally increment the parameter phi equally for each point on the cross-section (standard ellipse equations)"),
                                           ("spacing.normal", "Equiangular Normal", "Space between points on the cross-section equiangularly by the direction of the normals"),
                                           ("spacing.radius", "Equiangular Radius", "Space between points on the cross-section equiangularly by the direction of the radii"),
                                           ("spacing.arc", "Equal Arc Length", "Place points on the cross-section at equal distance")],
                                    name="Cross-Section Spacing", description="Define how to calculate the space between the points on the cross-section", default="spacing.area")
  tube_thickness_method = EnumProperty(items=[("thickness.cross", "Equal Cross-Sections", "Keep the cross-sections equally sized"),
                                               ("thickness.tube", "Constant Tube Thickness", "Scale cross-sections to keep constant tube thickness")],
                                        name="Tube Thickness Method", description="How to calculate the tube thickness", default="thickness.cross")
  ring_location = FloatVectorProperty(name="Location", description="Location", default=(0.0, 0.0, 0.0), step=1, precision=3, subtype="XYZ", unit="LENGTH", size=3)
  ring_rotation = FloatVectorProperty(name="Rotation", description="Rotation", default=(0.0, 0.0, 0.0), step=10, precision=3, subtype="XYZ", unit="ROTATION", size=3)

  def execute(self, context):
    #Create the base shape of the cross-section
    cross = []
    for u in range(self.ustep):
      theta, cross_normal_angle = HelperFunctions.getParamAndNormal(self.minor_major, self.minor_minor, u, self.ustep, self.cross_spacing_type)
      x = self.minor_major*cos(theta)
      y = 0.0
      z = self.minor_minor*sin(theta)
      cross.append(Vector((x, y, z)))

    #Create the base shape of the ring, and combine it with information on how to rotate and align the cross-section
    ring_vert = []
    ring_norm = []
    for v in range(self.vstep):
      phi, ring_normal_angle = HelperFunctions.getParamAndNormal(self.major_major, self.major_minor, v, self.vstep, self.ring_spacing_type)
      x = self.major_major*cos(phi)
      y = self.major_minor*sin(phi)
      z = 0.0
      ring_vert.append(Vector((x, y, z)))
      ring_norm.append(ring_normal_angle)

    #Calculate cross-section transformation matrix for each of the vertices of the ring
    cross_trans = []
    for v in range(self.vstep):
      prev_vert = ring_vert[(self.vstep+v-1)%self.vstep]
      this_vert = ring_vert[v]
      next_vert = ring_vert[(v+1)%self.vstep]
      angle = (this_vert-prev_vert).angle(this_vert-next_vert)/2.0
      cross_trans_mat = Matrix().Rotation(self.cross_rotation+self.cross_twist*v*pi/self.vstep, 4, Vector((0.0, 1.0, 0.0)))
      if self.tube_thickness_method == "thickness.tube":
        cross_trans_mat = Matrix().Scale(1.0/sin(angle), 4, Vector((1.0, 0.0, 0.0)))*cross_trans_mat
      cross_trans_mat = Matrix().Rotation(ring_norm[v], 4, Vector((0.0, 0.0, 1.0)))*cross_trans_mat
      cross_trans.append(cross_trans_mat)

    vertices = []
    faces = []
    for v in range(self.vstep):
      for u in range(self.ustep):
        cross_vert = (cross_trans[v]*cross[u].to_4d()).to_3d()+ring_vert[v]

        #Append the vertex coordinates to the list of vertices, and append a face to the list of faces.
        #The list of faces uses vertices that have not yet been created when appending intermediate faces,
        #however this is remedied at the end, as then it bridges with the vertices created at the beginning.
        #It uses modulo to make sure it doesn't overflow.
        vertices.append(cross_vert)
        if v == self.vstep-1:
          u_bridge_pos = (u+self.cross_twist%2*self.ustep//2)%self.ustep
        else:
          u_bridge_pos = u
        faces.append([v*self.ustep+u, ((v+1)%self.vstep)*self.ustep+u_bridge_pos, ((v+1)%self.vstep)*self.ustep+((u_bridge_pos+1)%self.ustep), v*self.ustep+((u+1)%self.ustep)])

    #Deselect everything
    bpy.ops.object.select_all(action="DESELECT")

    #Create the mesh and the object, select it and make it active.
    elliptic_torus_mesh = bpy.data.meshes.new("Elliptic Torus")
    elliptic_torus_mesh.from_pydata(vertices, [], faces)
    elliptic_torus_mesh.update()
    elliptic_torus_object = bpy.data.objects.new("Elliptic Torus", elliptic_torus_mesh)
    elliptic_torus_object.location = self.ring_location
    elliptic_torus_object.rotation_euler = Euler(self.ring_rotation, "XYZ")
    context.scene.objects.link(elliptic_torus_object)
    elliptic_torus_object.select = True
    bpy.context.scene.objects.active = elliptic_torus_object
    return {"FINISHED"}
