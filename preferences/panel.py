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

from bpy.types import AddonPreferences

from bpy.props import (
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )

from ..modal_input.preferences import ModalShortcutsPreferences


class BMToolPreferences(ModalShortcutsPreferences, AddonPreferences):
    bl_idname = "bmtools"

    needs_restart = False

    # Properties {{{
    settings_category: EnumProperty(
            name="Settings category",
            items=[('GENERAL', 'General settings', 'CUBE', 0),
                   ('SHORTCUTS', 'Shortcuts settings', 'CUBE', 1),
                   ('ADDITIONAL', 'Additional settings', 'CUBE', 2),
                   ],
            default='GENERAL'
            )

    save_clusters: BoolProperty(
            name="Save clusters on operator finish",
            default=True
            )

    save_clusters_backup: BoolProperty(
            name="Save clusters backup on operator finish",
            default=True
            )

    backup_mesh_on_modifier_apply_remove: BoolProperty(
            name="Backup mesh on modifier apply or remove.",
            default=True
            )

    backup_collection_name: StringProperty(
            name="Name of collection that will be used for mesh backup.",
            default='BMToolM mesh backup'
            )

    custom_cluster_types: BoolProperty(
            name="Use custom cluster types.",
            default=True
            )

    always_add_custom_cluster_types: BoolProperty(
            name="Always add custom cluster types.",
            default=True
            )

    cluster_types: StringProperty(
            name="ClusterTypes",
            default="[]"
            )
    # }}}

    def draw(self, context):
        layout = self.layout
        if self.needs_restart:
            layout.label(text='Please restart Blender.')
        layout.prop(self, "settings_category", expand=True)
        if self.settings_category == 'GENERAL':
            self.__draw_general_settings(context)
        elif self.settings_category == 'SHORTCUTS':
            self.__draw_shortcuts_search(context)
        elif self.settings_category == 'ADDITIONAL':
            self.__draw_additional_settings(context)
        else:
            raise ValueError

    def __draw_general_settings(self, context):
        layout = self.layout
        layout.label(text="General settings")
        layout.prop(self, "save_clusters")
        if self.save_clusters_backup:
            layout.prop(self, "save_clusters_backup")
        layout.prop(self, "backup_mesh_on_modifier_apply_remove")
        if self.backup_mesh_on_modifier_apply_remove:
            layout.prop(self, "backup_collection_name")
        layout.prop(self, "custom_cluster_types")
        if self.custom_cluster_types:
            layout.prop(self, "always_add_custom_cluster_types")
            layout.prop(self, "cluster_types")
        layout.prop(self, "bmtool_modal_operators_serialized_shortcuts")

    def __draw_shortcuts_search(self, context):
        return type(self)._ModalShortcutsPreferences__draw_shorcuts_search(context)

    def __draw_additional_settings(self, context):
        layout = self.layout
        layout.label(text="Additional settings")
