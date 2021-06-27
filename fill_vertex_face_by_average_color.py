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


import bpy


bl_info = {
    "name": "Fill Vertex Face by Average Color",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "[Vertex Paint Mode] 3D View > Side Bar > Tool > Fill Vertex Face",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/todashuta/blender-addon-fill-vertex-face-by-average-color/wiki",
    "tracker_url": "https://github.com/todashuta/blender-addon-fill-vertex-face-by-average-color/issues",
    "category": "Paint"
}


class FILL_VERTEX_FACE_BY_AVERAGE_COLOR_OT_main(bpy.types.Operator):
    bl_idname = "object.fill_vertex_face_by_average_color"
    bl_label = "Fill Vertex Face by Average Color"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob is not None
                and ob.type == "MESH"
                and ob.mode == "VERTEX_PAINT"
                and ob.data.vertex_colors.active is not None)

    def execute(self, context):
        from mathutils import Vector

        active_object = context.active_object
        mesh = active_object.data
        color_layer = mesh.vertex_colors.active

        average_colors = {}
        i = 0
        for poly in mesh.polygons:
            colors = []
            for _ in poly.loop_indices:
                colors.append(color_layer.data[i].color)
                i += 1
            # TODO: gamma-correction?
            average_colors[poly] = sum([Vector(c) for c in colors], Vector([0, 0, 0, 0])) / len(colors)

        i = 0
        if mesh.use_paint_mask:
            for poly in mesh.polygons:
                for _ in poly.loop_indices:
                    if poly.select:
                        color_layer.data[i].color = average_colors[poly]
                    i += 1
        else:
            for poly in mesh.polygons:
                for _ in poly.loop_indices:
                    color_layer.data[i].color = average_colors[poly]
                    i += 1

        return {"FINISHED"}


class FILL_VERTEX_FACE_BY_AVERAGE_COLOR_PT_panel(bpy.types.Panel):
    bl_label = "Fill Vertex Face"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "vertexpaint"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.operator(FILL_VERTEX_FACE_BY_AVERAGE_COLOR_OT_main.bl_idname)


classes = [
        FILL_VERTEX_FACE_BY_AVERAGE_COLOR_OT_main,
        FILL_VERTEX_FACE_BY_AVERAGE_COLOR_PT_panel,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
