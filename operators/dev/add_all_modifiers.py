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

import json

import bpy

from ...lib.utils.modifier_prop_types import get_all_editable_props
from ...lib.utils.modifier_prop_types import get_props_filtered_by_types


class BMTOOL_OT_add_all_modifiers(bpy.types.Operator):
    bl_idname = "object.add_all_modifiers"
    bl_label = "BMTool add all modifiers"
    bl_description = "Add all modifiers on selected objects"

    # All supported modifier types. {{{
    __MODIFIER_TYPES = [
                        "DATA_TRANSFER",
                        "MESH_CACHE",
                        "MESH_SEQUENCE_CACHE",
                        "NORMAL_EDIT",
                        "WEIGHTED_NORMAL",
                        "UV_PROJECT",
                        "UV_WARP",
                        "VERTEX_WEIGHT_EDIT",
                        "VERTEX_WEIGHT_MIX",
                        "VERTEX_WEIGHT_PROXIMITY",
                        "ARRAY",
                        "BEVEL",
                        "BOOLEAN",
                        "BUILD",
                        "DECIMATE",
                        "EDGE_SPLIT",
                        "NODES",
                        "MASK",
                        "MIRROR",
                        # "MESH_TO_VOLUME",
                        "MULTIRES",
                        "REMESH",
                        "SCREW",
                        "SKIN",
                        "SOLIDIFY",
                        "SUBSURF",
                        "TRIANGULATE",
                        "VOLUME_TO_MESH",
                        "WELD",
                        "WIREFRAME",
                        "ARMATURE",
                        "CAST",
                        "CURVE",
                        "DISPLACE",
                        "HOOK",
                        "LAPLACIANDEFORM",
                        "LATTICE",
                        "MESH_DEFORM",
                        "SHRINKWRAP",
                        "SIMPLE_DEFORM",
                        "SMOOTH",
                        "CORRECTIVE_SMOOTH",
                        "LAPLACIANSMOOTH",
                        "SURFACE_DEFORM",
                        "WARP",
                        "WAVE",
                        # "VOLUME_DISPLACE",
                        "CLOTH",
                        "COLLISION",
                        "DYNAMIC_PAINT",
                        "EXPLODE",
                        "FLUID",
                        "OCEAN",
                        "PARTICLE_INSTANCE",
                        "PARTICLE_SYSTEM",
                        "SOFT_BODY",
                        "SURFACE"
                        ]
    # }}}

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):

        modifiers = []
        for x in self.__MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)
            else:
                self.report({'INFO'}, f'Cant create modifier {x}')
        for x in modifiers:
            self.report({'INFO'}, f'{x}')
        return {'FINISHED'}


class BMTOOL_OT_add_default_modifiers_props_to_kbs(bpy.types.Operator):
    bl_idname = "object.add_default_modifiers_props_to_kbs"
    bl_label = "BMTool add all modifiers props to kbs"

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) != 1:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):

        modifiers = []
        for x in self.__MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append([mod.type, mod])
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)
            prefs = bpy.context.preferences.addons['bmtools'].preferences
            already_created = prefs.get_modal_operators_shortcuts_group(x[0]).values():
            for y in props:
                shortcut = get_kbs(y, already_created)
                bpy.ops.bmtools.add_or_update_modal_shortcut(
                        bmtool_operator_shortcut_name=name,
                        bmtool_operator_shortcut_group=x[0]
                        bmtool_operator_shortcut_letter=letter,
                        bmtool_operator_shortcut_shift=shift,
                        bmtool_operator_shortcut_ctrl=ctrl,
                        bmtool_operator_shortcut_alt=alt
                        bmtool_operator_shortcut_sens=0.005,
                        )

        return {'FINISHED'}


class BMTOOL_OT_add_all_modifiers_and_dump_props(bpy.types.Operator):
    bl_idname = "object.add_all_modifiers_and_dump_props"
    bl_label = "BMTool add all modifiers and dump props"
    bl_description = "Add all modifiers on selected objects and dump props"

    # All supported modifier types. {{{
    __MODIFIER_TYPES = [
                        "DATA_TRANSFER",
                        "MESH_CACHE",
                        "MESH_SEQUENCE_CACHE",
                        "NORMAL_EDIT",
                        "WEIGHTED_NORMAL",
                        "UV_PROJECT",
                        "UV_WARP",
                        "VERTEX_WEIGHT_EDIT",
                        "VERTEX_WEIGHT_MIX",
                        "VERTEX_WEIGHT_PROXIMITY",
                        "ARRAY",
                        "BEVEL",
                        "BOOLEAN",
                        "BUILD",
                        "DECIMATE",
                        "EDGE_SPLIT",
                        "NODES",
                        "MASK",
                        "MIRROR",
                        # "MESH_TO_VOLUME",
                        "MULTIRES",
                        "REMESH",
                        "SCREW",
                        "SKIN",
                        "SOLIDIFY",
                        "SUBSURF",
                        "TRIANGULATE",
                        "VOLUME_TO_MESH",
                        "WELD",
                        "WIREFRAME",
                        "ARMATURE",
                        "CAST",
                        "CURVE",
                        "DISPLACE",
                        "HOOK",
                        "LAPLACIANDEFORM",
                        "LATTICE",
                        "MESH_DEFORM",
                        "SHRINKWRAP",
                        "SIMPLE_DEFORM",
                        "SMOOTH",
                        "CORRECTIVE_SMOOTH",
                        "LAPLACIANSMOOTH",
                        "SURFACE_DEFORM",
                        "WARP",
                        "WAVE",
                        # "VOLUME_DISPLACE",
                        "CLOTH",
                        "COLLISION",
                        "DYNAMIC_PAINT",
                        "EXPLODE",
                        "FLUID",
                        "OCEAN",
                        "PARTICLE_INSTANCE",
                        "PARTICLE_SYSTEM",
                        "SOFT_BODY",
                        "SURFACE"
                        ]
    # }}}

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):

        modifiers = []
        for x in self.__MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)

        h = '/home/djentled/Documents/Projects/bmtools_utils/props_dump'

        # Get all editable prop names filtered by types and modifiers.
        all_props = {}
        for x in modifiers:
            props = get_props_filtered_by_types(x)
            for p in props:
                props[p] = list(props[p])
            all_props.update({x.type: props})

        result = all_props

        f = h + '_p'
        with open(f, 'w') as f:
            json.dump(result, f, indent=4)

        # # Get prop names filtered by types.
        # # get all types
        all_types = {}
        for x in all_props:
            for y in all_props[x]:
                props_names = all_props[x][y]
                if y not in all_types:
                    all_types.update({y: props_names})
                else:
                    for z in props_names:
                        if z not in all_types[y]:
                            all_types[y].append(z)
        result = all_types

        f = h + '_t'
        with open(f, 'w') as f:
            json.dump(result, f, indent=4)

        result = {}
        for x in modifiers:
            props = get_all_editable_props(x)
            result.update({str(x.type): list(props)})

        f = h + '_e'
        with open(f, 'w') as f:
            json.dump(result, f, indent=4)

        result = {}
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)
            result.update({str(x.type): list(props)})

        f = h + '_a'
        with open(f, 'w') as f_2:
            json.dump(result, f_2, indent=4)
        print(f.closed)

        return {'FINISHED'}
