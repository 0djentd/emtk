# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright 2022, Sergey Shapochkin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import json

import bpy

from ...libs.libemtk.utils.modifier_prop_types import get_all_editable_props
from ...libs.libemtk.utils.modifier_prop_types import MODIFIER_TYPES


class EMTK_OT_add_all_modifiers(bpy.types.Operator):
    bl_idname = "object.add_all_modifiers"
    bl_label = "EMTK add all modifiers"
    bl_description = "Add all modifiers on selected objects"

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
        for x in MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)
            else:
                self.report({'INFO'}, f'Cant create modifier {x}')
        for x in modifiers:
            self.report({'INFO'}, f'{x}')
        return {'FINISHED'}


class EMTK_OT_add_all_modifiers_and_dump_props(bpy.types.Operator):
    bl_idname = "object.add_all_modifiers_and_dump_props"
    bl_label = "EMTK add all modifiers and dump props"
    bl_description = "Add all modifiers on selected objects and dump props"

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
        for x in MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)

        h = '/home/djentled/Documents/Projects/emtk_utils/props_dump'

        # # Get all editable prop names filtered by types and modifiers.
        # all_props = {}
        # for x in modifiers:
        #     props = get_props_filtered_by_types(x)
        #     for p in props:
        #         props[p] = list(props[p])
        #     all_props.update({x.type: props})

        # result = all_props

        # f = h + '_p'
        # with open(f, 'w') as f:
        #     json.dump(result, f, indent=4)

        # # # Get prop names filtered by types.
        # # # get all types
        # all_types = {}
        # for x in all_props:
        #     for y in all_props[x]:
        #         props_names = all_props[x][y]
        #         if y not in all_types:
        #             all_types.update({y: props_names})
        #         else:
        #             for z in props_names:
        #                 if z not in all_types[y]:
        #                     all_types[y].append(z)
        # result = all_types

        # f = h + '_t'
        # with open(f, 'w') as f:
        #     json.dump(result, f, indent=4)

        # result = {}
        # for x in modifiers:
        #     props = get_all_editable_props(x)
        #     result.update({str(x.type): list(props)})

        # f = h + '_e'
        # with open(f, 'w') as f:
        #     json.dump(result, f, indent=4)

        # result = {}
        # for x in modifiers:
        #     props = get_all_editable_props(x, no_ignore=True)
        #     result.update({str(x.type): list(props)})

        # f = h + '_a'
        # with open(f, 'w') as f_2:
        #     json.dump(result, f_2, indent=4)

        result = {}
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)
            result_element = {}
            for y in list(props):
                rna = x.rna_type.properties[y]
                props_elements = {}
                prop_props = ['type',
                              'subtype',
                              'unit',
                              'step',
                              'min',
                              'max',
                              'soft_min',
                              'soft_max']

                for z in prop_props:
                    try:
                        a = getattr(rna, z)
                    except AttributeError:
                        a = 'no_attr'
                    props_elements.update({z: a})

                result_element.update({y: str(props_elements)})
            result.update({str(x.type): result_element})

        f = h + '_a_a'
        with open(f, 'w') as f_2:
            json.dump(result, f_2, indent=4)

        print(f_2.closed)

        return {'FINISHED'}
