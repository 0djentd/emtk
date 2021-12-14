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

# import bpy
from bpy.types import Operator

# from ..classes.modifiers_operator import ModifiersOperator
# from ..classes.lists.modifiers_list import ModifiersList
from ..classes.lists.object_modifiers_list import ObjectModifiersList
from ..classes.lists.object_modifiers_clusters_list import ObjectModifiersClustersList
from ..classes.lists.extended_modifiers_list import ExtendedModifiersList
from ..classes.lists.clusters_list import ClustersList
from ..classes.modifiers_operator import ModifiersOperator


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

        x = self.m_list._modifiers_list[0].get_this_cluster_visibility()

        self.report({'INFO'}, f"{x}")

        x2 = len(self.m_list.get_first())

        self.report({'INFO'}, f"{x2}")

        self.report({'INFO'}, f"{self.m_list.get_first()}")

        for line in self.m_list.modifiers_list_info_get():
            self.report({'INFO'}, line)

        for line in self.m_list._clusters_parser._additional_info_log:
            self.report({'INFO'}, line)

        for x in self.m_list.get_list():
            self.report({'INFO'}, f"{x}")
            for y in x.get_list():
                self.report({'INFO'}, f"{y}")

        return {'FINISHED'}

    def objmodlist_checks(self, context):
        m_list = ObjectModifiersList()
        m_list.create_modifiers_list(context.object)

        for line in m_list.modifiers_list_info_get():
            self.report({'INFO'}, line)

        for x in m_list.get_list():
            self.report({'INFO'}, f"{x}")
            for y in x.get_list():
                self.report({'INFO'}, f"{y}")
        return

    def extmodlist_checks(self, context):
        m_list = ExtendedModifiersList()

        m_list.create_modifiers_list(context.object)

        for line in m_list.modifiers_list_info_get():
            self.report({'INFO'}, line)

        for x in m_list.get_list():
            self.report({'INFO'}, f"{x}")
            for y in x.get_list():
                self.report({'INFO'}, f"{y}")
        self.report({'INFO'}, f"{m_list._mod}")
        return

    # def momodlist_checks(self, context):
    #     self.create_objects_modifiers_lists(context)

    #     for line in self.m_list.modifiers_list_info_get():
    #         self.report({'INFO'}, line)

    #     for x in self.m_list.get_list():
    #         self.report({'INFO'}, f"{x}")
    #         for y in x.get_list():
    #             self.report({'INFO'}, f"{y}")
    #     self.report({'INFO'}, f"{self.m_list._mod}")
    #     return

    def clustermodlist_checks(self, context):

        mods = []
        for x in range(3):
            mod = context.object.modifiers.new('BEVEL', 'BEVEL')
            mods.append(mod)

        self.report({'INFO'}, "Trying to create modifiers list with clusters")
        m_list = ClustersList()
        x = m_list._parse_modifiers(mods)
        m_list._modifiers_list = x

        for x in m_list.get_list():
            self.report({'INFO'}, f"{x}")
            for y in x.get_list():
                self.report({'INFO'}, f"{y}")

        modlist = []
        modlist.append(m_list.get_list())
        modlist.append(m_list.get_list_length())
        modlist.append(m_list.get_last())
        modlist.append(m_list.get_first())
        modlist.append(m_list.get_by_index(0))
        modlist.append(m_list.get_index(m_list.get_by_index(0)))
        modlist.append(m_list.get_last()._modifiers_list)
        for line in modlist:
            self.report({'INFO'}, f"{line}")
        for line in m_list.modifiers_list_info_get():
            self.report({'INFO'}, line)
