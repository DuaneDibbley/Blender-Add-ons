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

from math import cos, sin, atan2, pi, sqrt

def getParamAndNormal(major, minor, input_param, steps, spacing_type):
  if input_param == 0:
    return 0.0, 0.0

  if major == minor:
    spacing_type = "spacing.area"

  if spacing_type == "spacing.normal":
    normal_angle = 2*pi*input_param/steps
    output_param = atan2(minor*sin(2*pi*input_param/steps), major*cos(2*pi*input_param/steps))

  elif spacing_type == "spacing.radius":
    output_param = atan2(major*sin(2*pi*input_param/steps), minor*cos(2*pi*input_param/steps))
    normal_angle = atan2(major*sin(output_param), minor*cos(output_param))

  else:
    output_param = 2*pi*input_param/steps
    normal_angle = atan2(major*sin(2*pi*input_param/steps), minor*cos(2*pi*input_param/steps))

  return output_param, normal_angle