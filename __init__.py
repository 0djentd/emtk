# Copyright 2022, Sergey Shapochkin

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

import logging

from . operators.bmtoolm import BMTOOL_OT_bmtoolm
from . operators.dev.add_all_modifiers import BMTOOL_OT_add_all_modifiers
from . operators.dev.add_all_modifiers import\
        BMTOOL_OT_add_all_modifiers_and_dump_props
from . operators.dev.add_cluster_type import BMTOOL_OT_add_cluster_type_object
from . operators.bmtoole2 import BMTOOL_OT_bmtoole2
from . operators.bmtoolm_lite import BMTOOL_OT_bmtoolm_2
from . utils.bmtool_preferences import BMToolPreferences
from . utils.bmtool_preferences import BMTOOLS_OT_start_editing_modal_shortcut
from . utils.bmtool_preferences import BMTOOLS_OT_add_or_update_modal_shortcut
from . ui.bmtools_pie import VIEW_3D_MT_PIE_bmtools_pie_1

bl_info = {
    "name": "BMTools",
    "author": "djentled, also known as Sergey Shapochkin",
    "version": (0, 4, 0),
    "blender": (3, 1, 0),
    "description": "Tools for adding, sorting and editing exsting modifiers.",
    "category": "Interface"
}

classes = [

    # modal operators
    BMTOOL_OT_bmtoolm,
    BMTOOL_OT_bmtoole2,
    BMTOOL_OT_bmtoolm_2,

    # lib ops
    BMTOOL_OT_add_cluster_type_object,

    # prefs
    BMToolPreferences,
    BMTOOLS_OT_start_editing_modal_shortcut,
    BMTOOLS_OT_add_or_update_modal_shortcut,

    # ui
    VIEW_3D_MT_PIE_bmtools_pie_1,

    # dev
    BMTOOL_OT_add_all_modifiers,
    BMTOOL_OT_add_all_modifiers_and_dump_props,
]

addon_keymaps = []


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    logging.info("BMTool v1.0")

    if kc:
        km = kc.keymaps.new(name="Object Mode")

        kmi = km.keymap_items.new("wm.call_menu_pie", "V", "PRESS", alt=True)
        kmi.properties.name = "BMTOOLS_MT_PIE_bmtpie"
        addon_keymaps.append((km, kmi))

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    logging.info("BMTool v1.0 removed.")

    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
