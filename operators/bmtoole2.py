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

from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator
from ..lib.utils.modifiers import get_modifier_state


class BMTOOL_OT_bmtoole2(ModifiersOperator, Operator):
    bl_idname = "object.bmtoole2"
    bl_label = "BMToolE2"
    bl_description = "Add modifiers on selected objects"

    # Display additional info
    _MODIFIERS_OPERATOR_V = True

    # Can be used with modifiers clusters
    _MODIFIERS_OPERATOR_MODIFIER_CLUSTERS = True

    # Dont use extended modifiers list, use object modifiers list
    _MODIFIERS_OPERATOR_DONT_USE_EXTENDED = False

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT' and self._BMTOOL_EDITMODE is False:
            return False
        elif len(context.selected_objects) > 1 and self._BMTOOL_SINGLE_OBJECT:
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):
        # self.clustermodlist_checks(context)
        # self.objmodlist_checks(context)
        # self.extmodlist_checks(context)
        # self.momodlist_checks(context)

        modifiers = []
        for x in context.object.modifiers:
            modifiers.append(x)

        mods = []
        if (len(modifiers)) == 0:
            for x in range(1):
                mod = context.object.modifiers.new('Bevel', 'BEVEL')
                mod.segments = 1
                mods.append(mod)

        self.create_objects_modifiers_lists(context)

        self.m_list._modifiers_list[0].set_this_cluster_visibility(
                (True, False, True, False))
        print(get_modifier_state(self.m_list._object.modifiers['Bevel']))
        del(self.selected_objects)
        del(self.m_list)
        return {'FINISHED'}
