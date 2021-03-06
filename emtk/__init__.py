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
import logging
import re

import bpy
# Class variables editor
from class_variables_editor_ui.operators import \
    EMTK_OT_emtk_invoke_operator_func
from class_variables_editor_ui.panel import (UIClassVariablesEditor,
                                             UIClassVariablesEditorCache,
                                             get_prop_group_name)
# Modal input
from modal_shortcuts.operators import (
    EMTK_OT_add_or_update_modal_shortcut,
    EMTK_OT_reparse_default_modifiers_props_kbs,
    EMTK_OT_start_editing_modal_shortcut)

# Dev
from .operators.dev.add_all_modifiers import (
    EMTK_OT_add_all_modifiers, EMTK_OT_add_all_modifiers_and_dump_props)
from .operators.dev.add_cluster_type import EMTK_OT_add_cluster_type_object
from .operators.dev.add_modifiers import EMTK_OT_add_modifiers
# Operators
from .operators.dev.add_new_cluster import EMTK_OT_add_new_cluster
# Modal operators
from .operators.emtkm import EMTK_OT_emtkm
# Preferences
from .preferences import EMTKPreferences
from .ui.clusters_list_popup import EMTK_OT_clusters_list_popup
from .ui.emtk_panel import VIEW3D_PT_emtk_panel
# UI
from .ui.pie_menus import VIEW3D_MT_PIE_emtk_pie_1

bl_info = {
    "name": "EMTK",
    "author": "Sergey Shapochkin, also known as djentled, also known as djentd",
    "version": (0, 5, 0),
    "blender": (3, 1, 0),
    "description": "Tools for editing modifiers and clusters.",
    "category": "Interface"
}

logger = logging.getLogger(__package__)
# logger.setLevel(logging.ERROR)
# logging.basicConfig(level=logging.ERROR)

logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

classes = [

    # modal operators
    EMTK_OT_emtkm,
    EMTK_OT_add_modifiers,

    # libemtk operators
    EMTK_OT_add_cluster_type_object,

    # prefs
    EMTKPreferences,
    EMTK_OT_start_editing_modal_shortcut,
    EMTK_OT_add_or_update_modal_shortcut,

    # popup operators
    EMTK_OT_clusters_list_popup,

    # ui
    VIEW3D_MT_PIE_emtk_pie_1,
    VIEW3D_PT_emtk_panel,

    # dev
    EMTK_OT_add_all_modifiers,
    EMTK_OT_add_new_cluster,
    EMTK_OT_add_all_modifiers_and_dump_props,
    EMTK_OT_reparse_default_modifiers_props_kbs,

    # property groups
    UIClassVariablesEditorCache,

    # utils operators
    EMTK_OT_emtk_invoke_operator_func,
]

addon_keymaps = []


def register():
    logger.info('Registering EMTK and libemtk')

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Object Mode")

        kmi = km.keymap_items.new("wm.call_menu_pie", "V", "PRESS", alt=True)
        kmi.properties.name = "EMTK_MT_PIE_emtk_pie"
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
    try:
        prefs = bpy.context.preferences.addons['emtk'].preferences
        prefs.refresh_cache()
        # FIXME: auto generate shortcuts on addon first launch
        # or blender update.
        # This throws json error.
    except KeyError:
        logger.info('Skipped cache refresh.')
    logger.info('Finished registering EMTK and libemtk.')


def unregister():
    logger.info('Unregistering EMTK and libemtk')

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    for x in dir(bpy.types.Scene):
        if re.match('cls_var_editor', x):
            logger.info(f'Removing property group {x}')
            prop_group = getattr(bpy.types.Scene, x)
            del prop_group

    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    for cls in reversed(classes):
        logger.debug(f'Unregister class {cls}')
        bpy.utils.unregister_class(cls)
    logger.info('Finished unregistering EMTK and libemtk')
