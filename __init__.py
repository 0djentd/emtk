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

import re
import logging

import bpy

# Modal operators
from . operators.bmtoolm import BMTOOL_OT_bmtoolm
from . operators.bmtoole2 import BMTOOL_OT_bmtoole2

# Operators
from . operators.dev.add_new_cluster import BMTOOL_OT_add_new_cluster

# Preferences
from . preferences.panel import BMToolPreferences
from . modal_input.operators import BMTOOLS_OT_start_editing_modal_shortcut
from . modal_input.operators import BMTOOLS_OT_add_or_update_modal_shortcut
from . modal_input.operators import\
        BMTOOL_OT_reparse_default_modifiers_props_kbs

# UI
from . ui.pie_menus import VIEW3D_MT_PIE_bmtools_pie_1
from . ui.bmtool_panel import VIEW3D_PT_bmtool_panel
from . ui.utils.operators import BMTOOLS_OT_bmtool_invoke_operator_func
from . ui.clusters_list_popup import BMTOOLS_OT_clusters_list_popup

# Class variables editor
from . ui.ui_class_variables_editor import UIClassVariablesEditorCache
from . ui.ui_class_variables_editor import UIClassVariablesEditor
from . ui.ui_class_variables_editor import get_prop_group_name

# Dev
from . operators.dev.add_all_modifiers import BMTOOL_OT_add_all_modifiers
from . operators.dev.add_all_modifiers import\
        BMTOOL_OT_add_all_modifiers_and_dump_props
from . operators.dev.add_cluster_type import BMTOOL_OT_add_cluster_type_object

bl_info = {
    "name": "BMTools",
    "author": "Sergey Shapochkin, also known as djentled",
    "version": (0, 4, 0),
    "blender": (3, 1, 0),
    "description": "Tools for editing modifiers and clusters.",
    "category": "Interface"
}

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

classes = [

    # modal operators
    BMTOOL_OT_bmtoolm,
    BMTOOL_OT_bmtoole2,

    # EMTK operators
    BMTOOL_OT_add_cluster_type_object,

    # prefs
    BMToolPreferences,
    BMTOOLS_OT_start_editing_modal_shortcut,
    BMTOOLS_OT_add_or_update_modal_shortcut,

    # popup operators
    BMTOOLS_OT_clusters_list_popup,

    # ui
    VIEW3D_MT_PIE_bmtools_pie_1,
    VIEW3D_PT_bmtool_panel,

    # dev
    BMTOOL_OT_add_all_modifiers,
    BMTOOL_OT_add_new_cluster,
    BMTOOL_OT_add_all_modifiers_and_dump_props,
    BMTOOL_OT_reparse_default_modifiers_props_kbs,

    # property groups
    UIClassVariablesEditorCache,

    # utils operators
    BMTOOLS_OT_bmtool_invoke_operator_func,
]

addon_keymaps = []


def register():
    logger.info('Registering BMTools and EMTK')

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Object Mode")

        kmi = km.keymap_items.new("wm.call_menu_pie", "V", "PRESS", alt=True)
        kmi.properties.name = "BMTOOLS_MT_PIE_bmtpie"
        addon_keymaps.append((km, kmi))

    for cls in classes:
        logger.debug(f'Register class {cls}')
        bpy.utils.register_class(cls)

    # Create scene property groups for all classes
    # that use class variables editor module.
    # Example:
    # bpy.context.scene.cls_var_editor_operator_clusters_list_popup
    for x in classes:
        line = get_prop_group_name(x)
        if line is not None and UIClassVariablesEditor in x.mro():
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(x)
                logger.debug(x.__name__)
                logger.debug(x.mro())
                logger.debug(line)

            logger.info(f'Adding property group {line} for {x}')
            prop = bpy.props.PointerProperty(type=UIClassVariablesEditorCache)
            setattr(bpy.types.Scene, line, prop)
    prefs = bpy.context.preferences.addons['bmtools'].preferences
    prefs.refresh_cache()
    logger.info('Finished registering BMTools and EMTK')


def unregister():
    logger.info('Unregistering BMTools and EMTK')

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    for x in dir(bpy.types.Scene):
        if re.match('cls_var_editor', x):
            logger.info(f'Removing property group {x}')
            prop_group = getattr(bpy.types.Scene, x)
            del(prop_group)

    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    for cls in reversed(classes):
        logger.debug(f'Unregister class {cls}')
        bpy.utils.unregister_class(cls)
    logger.info('Finished unregistering BMTools and EMTK')
