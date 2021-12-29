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

import copy
import logging
import string

import bpy

from ..lib.modifiers_operator import ModifiersOperator
from ..ui.bmtool_ui import bmtool_modifier_ui_draw

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Modal modifier operator base class
class BMToolMod(ModifiersOperator):
    """
    Base class for modal operators that use Blender modifier stack
    through ModififersOperator and ExtendedModifiersList.
    """

    # Default bmtool modal editing mode.
    _BMTOOL_DEFAULT_MODE = "Please select BMTool mode"

    # Allows operator to be used in edit mode.
    _BMTOOL_EDITMODE = False

    # Dont let to use operator if more than one object is selected.
    _BMTOOL_SINGLE_OBJECT = False

    # Create draw handler.
    _BMTOOL_UI = False

    # Use statusbar to display modifier info.
    _BMTOOL_UI_STATUSBAR = False

    # Keymap for bmtoolm.
    bmtool_kbs = {
                  'visibility_1': 'V',
                  'visibility_2': 'B',
                  'sort': 'T',
                  'add_new': 'N',
                  'apply_remove': 'X',
                  'construct_deconstruct': 'C',
                  'toogle_selection': 'G',
                  'up': 'E',
                  'down': 'F',
                  'collapse': 'R',
                  'exit': 'Q'
                  }

    _MODAL_LETTERS = string.ascii_uppercase

    _MODAL_DIGITS = {
                     'ZERO': '0',
                     'ONE': '1',
                     'TWO': '2',
                     'THREE': '3',
                     'FOUR': '4',
                     'FIVE': '5',
                     'SIX': '6',
                     'SEVEN': '7',
                     'EIGHT': '8',
                     'NINE': '9',
                     }

    _MODAL_DIGITS_NUMPAD = {
                            'NUMPAD_0': '0',
                            'NUMPAD_1': '1',
                            'NUMPAD_2': '2',
                            'NUMPAD_3': '3',
                            'NUMPAD_4': '4',
                            'NUMPAD_5': '5',
                            'NUMPAD_6': '6',
                            'NUMPAD_7': '7',
                            'NUMPAD_8': '8',
                            'NUMPAD_9': '9',
                            }

    # ------------------------------------------------------------
    # Some variables that are created when operator is initialized
    # by modifiers_operator
    # ------------------------------------------------------------
    # GUI draw handler
    # bmtool_ui_draw_handler

    # Active object ModifiersList instance
    # m_list()

    # Selected objects ModifiersList instances
    # selected_objects[]

    # TODO: rename Modifier-specific to modifier-specific operator, as
    # it better represents functionality

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Check if modifier can be used
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

    def modal(self, context, event):
        """
        Method that is initiated every frame or whatever.
        """
        # Redraw UI
        if self._BMTOOL_UI:
            context.area.tag_redraw()
        if self._BMTOOL_UI_STATUSBAR:
            context.workspace.status_text_set()

        # Active cluster reference
        cluster = self.m_list.get_cluster()

        # Active cluster layer
        layer = self.m_list.get_layer()

        """
        This is different modes of this operator.

        'ACTIONS' is modal loop for general actions on clusters list,
        for example applying, moving and switching visibility of modifiers.

        'EDITOR' is bmtool_editor modal loop.
        It is used for modal editing of modifiers and clusters properties
        within editor.

        This two methods always switch back to previous mode:
        'DIGITS' is digits input mode.
        'STR' is string input mode.
        """
        if self._mode = 'ACTIONS':
            a = self._modal_actions(context, event)
        elif self._mode = 'EDITOR':
            a = self._modal_editor(context, event)
        elif self._mode = 'INT':
            a = self._modal_numbers_set(context, event)
        elif self._mode = 'STR':
            a = self._modal_str_set(context, event)
        if a is not True and a is not False:
            return a
        return {'RUNNING_MODAL'}

        # Exit out of modifier editing mode or finish operator.
        elif (event.type == self.bmtool_kbs['exit'])\
                & (event.value == 'PRESS'):
            if self.bmtool_mode != self._BMTOOL_DEFAULT_MODE:
                self.bmtool_mode = self._BMTOOL_DEFAULT_MODE
            else:
                self.clear(context)
                return {'FINISHED'}

        # Finish.
        elif event.type == 'LEFTMOUSE':
            if self.bmtool_mode != self._BMTOOL_DEFAULT_MODE:
                self.bmtool_mode = self._BMTOOL_DEFAULT_MODE
            else:
                self.clear(context)
                return {'FINISHED'}

        # Cancell.
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.clear(context)
            return {'CANCELLED'}

        # ------------------------------
        # Operator-specific modal
        # ------------------------------
        else:
            result = self.bmtool_modal_2(context, event)
            if result == {'FINISHED'}:
                self.clear(context)
                return {'FINISHED'}
            elif result == {'CANCELLED'}:
                self.clear(context)
                return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def _modal_actions(self, context, event):
        # Modifier visibility
        if (event.type == self.bmtool_kbs['visibility_1'])\
                & (event.value == 'PRESS'):
            if event.shift:
                if self._selecting_clusters:
                    for x in layer.get_cluster_selection():
                        x.toggle_this_cluster_visibility(
                                [True, False, False, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                            [True, False, False, False])
            else:
                if self._selecting_clusters:
                    for x in layer.get_cluster_selection():
                        x.toggle_this_cluster_visibility(
                                [False, True, False, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                            [False, True, False, False])

            # Clear selection
            self._selecting_clusters = False
            layer.clear_cluster_selection()

        # Modifier visibility 2
        elif (event.type == self.bmtool_kbs['visibility_2'])\
                & (event.value == 'PRESS'):
            if event.shift:
                if self._selecting_clusters:
                    for x in layer.get_cluster_selection():
                        cluster.toggle_this_cluster_visibility(
                                [False, False, False, True])
                else:
                    cluster.toggle_this_cluster_visibility(
                            [False, False, False, True])
            else:
                if self._selecting_clusters:
                    for x in layer.get_cluster_selection():
                        cluster.toggle_this_cluster_visibility(
                                [False, False, True, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                            [False, False, False, True])

            # Clear selection
            self._selecting_clusters = False
            layer.clear_cluster_selection()

        # Sort modifiers
        elif (event.type == self.bmtool_kbs['sort'])\
                & (event.value == 'PRESS'):
            layer.apply_sorting_rules()

        # Add new modifier of the same type and switch to it
        elif (event.type == self.bmtool_kbs['add_new'])\
                & (event.value == 'PRESS'):

            if self._BMTOOLM is False:
                x = self.m_list.create_modifier(
                        self._DEFAULT_M_NAME, self._DEFAULT_M_TYPE)
                self.m_list.active_modifier_set(x)

                # TODO: why bmtool_modifier_defaults doesnt need modifier?
                self.bmtool_modifier_defaults(context)

            elif self._BMTOOLM is True:
                self.bmtool_modifier_add(context)
                self.bmtool_modifier_defaults(context)

            # Reset mode
            self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

            # Trigger active modifier change
            self.bmtool_modifier_update(context)

        # Apply active cluster
        elif (event.type == self.bmtool_kbs['apply_remove'])\
                & event.shift & (event.value == 'PRESS'):

            # Remove cluster.
            if self._selecting_clusters:
                layer.apply_clusters_selection()
            else:
                layer.apply(cluster)

            # Clear selection
            self._selecting_clusters = False
            layer.clear_cluster_selection()

            # Check if it was last actual modifier.
            # If so, finish operator.
            if len(self.m_list.get_full_actual_modifiers_list()) == 0:
                self.clear(context)
                return {'FINISHED'}

            # Reset mode.
            self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

        # Deconstruct active cluster.
        elif (event.type == self.bmtool_kbs['construct_deconstruct'])\
                & event.shift & (event.value == 'PRESS'):

            if layer.deconstruct(cluster):
                self.report({'INFO'}, "Deconstructed cluster")
            else:
                self.report({'ERROR'}, "Cant deconstruct cluster")

        # Construct cluster from selection
        elif (event.type == self.bmtool_kbs['construct_deconstruct'])\
                & (event.value == 'PRESS'):

            if self._selecting_clusters:
                if layer.construct_cluster_from_selection():
                    self.report({'INFO'}, "Constructed cluster")
                else:
                    self.report({'ERROR'}, "Cant create cluster")
                layer.clear_cluster_selection()
                self._selecting_clusters = False
            else:
                # TODO: what is dat
                layer.clear_cluster_selection()
                layer.add_cluster_to_selection(cluster)
                if layer.construct_cluster_from_selection():
                    self.report({'INFO'}, "Constructed cluster")
                else:
                    self.report({'ERROR'}, "Cant create cluster")
                layer.clear_cluster_selection()

            # Select currently active cluster.
            cluster = self.m_list.get_cluster()
            layer = self.m_list.get_active_cluster_layer()

        # Toggle selection.
        elif (event.type == self.bmtool_kbs['toogle_selection'])\
                & (event.value == 'PRESS'):

            # Toggle selecting clusters.
            if self._selecting_clusters:
                self._selecting_clusters = False
                layer.clear_cluster_selection()
            else:
                layer.start_selecting_clusters()
                self._selecting_clusters = True

        # Remove active cluster.
        elif (event.type == self.bmtool_kbs['apply_remove'])\
                & (event.value == 'PRESS'):

            # TODO: this only moves object to new collection, should create
            # a backup instead.
            # if self.backup_mesh_on_modifier_apply_remove:
            #     objCollections = self.m_list._object.users_collection

            #     if self.backup_collection not in objCollections:
            #         self.backup_collection.objects.link(self.m_list._object)
            #         for x in objCollections:
            #             x.object.unlink(self.m_list._object)

            # Remove cluster.
            if self._selecting_clusters is True:
                layer.remove_clusters_selection()
            else:
                layer.remove(cluster)

            # Clear selection
            self._selecting_clusters = False
            layer.clear_cluster_selection()

            # Reset mode.
            self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

        # Move modifier up.
        elif (event.type == self.bmtool_kbs['up'])\
                & event.shift & (event.value == 'PRESS'):

            # Move modifier.
            if self._selecting_clusters:
                layer.move_up_selection()
            else:
                layer.move_up(cluster)

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

            if self._BMTOOL_V:
                self.report({'INFO'}, "Moved modifier up.")

        # Move modifier down.
        elif (event.type == self.bmtool_kbs['down'])\
                & event.shift & (event.value == 'PRESS'):

            # Move modifier.
            if self._selecting_clusters:
                layer.move_down_selection()
            else:
                layer.move_down(cluster)

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

            if self._BMTOOL_V:
                self.report({'INFO'}, "Moved modifier down.")

        # Collapse cluster.
        elif (event.type == self.bmtool_kbs['collapse'])\
                & (event.value == 'PRESS'):
            self._selecting_clusters = False
            layer.clear_cluster_selection()

            # Collapse cluster.
            if event.shift:
                if (cluster.collapsed is False)\
                        & (cluster.has_clusters() is False):
                    cluster.collapsed = True
                elif (cluster.collapsed is True)\
                        & (cluster.has_clusters() is False):
                    layer.collapsed = True
                elif (cluster.collapsed is True)\
                        & (cluster.has_clusters() is True):
                    layer.collapsed = True

            # Uncollapse cluster.
            else:
                cluster.collapsed = False

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

            # Clear selection
            self._selecting_clusters = False
            layer.clear_cluster_selection()

        # Scroll through modifiers up.
        elif (event.type == self.bmtool_kbs['up'])\
                & (event.value == 'PRESS'):

            # Only change modifier if there is more than one available.
            if layer.get_list_length() > 1:

                # First modifier.
                if event.ctrl:
                    if not self._BMTOOLM:
                        x = layer.get_list_by_type(self._DEFAULT_M_TYPE)
                        layer.active_modifier_set(x[0])
                    else:
                        x = layer.get_list()
                        layer.active_modifier_set(x[0])

                # Previous modifier.
                else:
                    if not self._BMTOOLM:
                        layer.active_modifier_set(
                            layer.find_previous_loop(
                                cluster, self._DEFAULT_M_TYPE))
                    else:
                        layer.active_modifier_set(
                            layer.find_previous_any_loop(cluster))

            # Reset mode.
            self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

            # Trigger active modifier change.
            self.bmtool_modifier_update(context)

        # Scroll through modifiers down.
        elif (event.type == self.bmtool_kbs['down'])\
                & (event.value == 'PRESS'):

            # Only change modifier if there is more than one available.
            if layer.get_list_length() > 1:
                # Last modifier.
                if event.ctrl:
                    if not self._BMTOOLM:
                        x = layer.get_list_by_type(self._DEFAULT_M_TYPE)
                        layer.active_modifier_set(x[-1])
                    else:
                        x = layer.get_list()
                        layer.active_modifier_set(x[-1])

                # Next modifier.
                else:
                    if not self._BMTOOLM:
                        layer.active_modifier_set(
                            layer.find_next_loop(
                                cluster, self._DEFAULT_M_TYPE))
                    else:
                        layer.active_modifier_set(
                            layer.find_next_any_loop(cluster))

                # Reset mode.
                self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

                # Trigger active modifier change.
                self.bmtool_modifier_update(context)
        else:
            return False
        return True

    def _modal_editor(self, context, event):
        return self.bmtool_modal_2(context, event)

    # INT, STR, FLOAT
    def _modal_digits_set(self, event):
        """This thing writes a string that can be used in modal operator
        to get integer, float, or string.
        Returns True, if event type was in digits list.
        """
        for x in self._MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.bmtool_modal_numbers_str\
                    = self.bmtool_modal_numbers_str + self._MODAL_DIGITS[x]
                return True
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str + '.'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str[0:-1]
        elif event.type == 'RETURN' and event.value == 'PRESS':
            self._mode = self._previous_mode
        else:
            return False
        return True

    def _modal_numbers_get_val(self, t='ANY'):
        """
        Returns numbers that were typed with _modal_numbers_set.
        """
        if len(self.bmtool_modal_numbers_str) == 0:
            return None

        if t == 'ANY':
            if '.' in self.bmtool_modal_numbers_str:
                return float(self.bmtool_modal_numbers_str)
            else:
                return int(self.bmtool_modal_numbers_str)
        elif t == 'INT':
            i = None
            for z, x in enumerate(self.bmtool_modal_numbers_str):
                if x == '.':
                    i = z
            return int(self.bmtool_modal_numbers_str[0:i])
        elif t == 'FLOAT':
            result = copy.copy(self.bmtool_modal_numbers_str)
            f = False
            for x in self.bmtool_modal_numbers_str:
                if x == '.':
                    f = True
            if f is False:
                result = result + '.0'
            return float(result)

    def _modal_numbers_clear(self):
        self.bmtool_modal_numbers_str = ''

    # STR
    def _modal_str_set(self, event):
        """This thing writes a string that can be used in modal operator.
        Returns True, if event type was in letters and digits list.
        """
        for x in self._MODAL_LETTERS:
            if event.type == x and event.value == 'PRESS':
                if event.shift:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x
                else:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x.lower()
                return True
        for x in self._MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.bmtool_modal_str = self.bmtool_modal_str + x
                return True
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str + '.'
        elif event.type == 'MINUS' and event.value == 'PRESS':
            if event.shift:
                self.bmtool_modal_numbers_str\
                        = self.bmtool_modal_numbers_str + '_'
            else:
                self.bmtool_modal_numbers_str\
                        = self.bmtool_modal_numbers_str + '-'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str[0:-1]
        elif event.type == 'RETURN' and event.value == 'PRESS':
            self._mode = self._previous_mode
        else:
            return False
        return True

    def _modal_str_get(self):
        return self.bmtool_modal_str

    def _modal_str_clear(self):
        self.bmtool_modal_str = ''

    def clear(self, context):
        """
        Removes operator.

        Used when encountering FINISHED or CANCELLED in modal method
        to remove no longer needed properies, handlers or whatever.
        """

        context.workspace.status_text_set(None)
        if self._BMTOOL_UI:
            bpy.types.SpaceView3D.draw_handler_remove(
                    self.bmtool_ui_draw_handler, 'WINDOW')
            context.area.tag_redraw()
            logger.info("BMTool UI is removed")
        self.bmtool_modifier_remove(context)
        if bpy.context.preferences.addons['bmtools'].preferences.save_clusters:
            self.m_list.save_modifiers_state()
            self.m_list.save_clusters_state()
            logger.info("Saved modifiers and clusters.")
        del(self.selected_objects)
        del(self.m_list)
        logger.info("Modal operator finished")

    def invoke(self, context, event):
        """
        Method that is invoked once per operator usage.
        """

        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "Not inside View3D")
            return {'CANCELLED'}
        elif context.mode != 'OBJECT' and self._BMTOOL_EDITMODE is False:
            self.report({'WARNING'}, "Should be in object mode")
            return {'CANCELLED'}
        elif len(context.selected_objects) > 1 and self._BMTOOL_SINGLE_OBJECT:
            self.report({'WARNING'}, "More than one object selected")
            return {'CANCELLED'}
        elif len(context.selected_objects) == 0:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}
        elif context.object.type != 'MESH':
            self.report({'WARNING'}, "Selected object cant be edited")
            return {'CANCELLED'}

        # Displays info about operator variables on invoke
        if self._BMTOOL_V:
            self.display_additional_info_about_bmtool(context)

        # ------------------------------
        # Operator-specific
        # ------------------------------
        self.bmtool_modifier_inv(context, event)

        # Add UI
        if self._BMTOOL_UI:
            logger.info("BMTool UI is created")
            sv = bpy.types.SpaceView3D
            self.bmtool_ui_draw_handler = sv.draw_handler_add(
                    bmtool_modifier_ui_draw, (self, context),
                    'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()
            self.bmtool_modal_numbers_str = ''

        # Default modal editing mode
        # TODO: implement through enum or whatever
        # TODO: does this thing actually used?
        # Can it be replaced by editor mode?
        self.bmtool_mode = self._BMTOOL_DEFAULT_MODE

        # Backup collection.
        addon_prefs = bpy.context.preferences.addons['bmtools'].preferences
        b = addon_prefs.backup_mesh_on_modifier_apply_remove
        self.backup_mesh_on_modifier_apply_remove = b
        if b:
            c = addon_prefs.backup_collection_name
            self.backup_collection_name = c
            # TODO: different collections for different objects in
            # that backup collection.
            if c not in bpy.data.collections:
                backups = bpy.data.collections.new(name=c)
                bpy.context.scene.collection.children.link(backups)
            else:
                backups = bpy.data.collections[c]
            self.backup_collection = backups

        # ================================
        # Create instances of ModifierList
        # ================================
        # creates self.selected_objects[]
        # and self.m_list, as a reference to active object
        # in it
        result = self.create_objects_modifiers_lists(context)
        if result is False or result is None:
            self.report({'ERROR'}, "Error while parsing clusters")
            self.clear(context)
            return {'FINISHED'}

        if self._BMTOOL_V:
            self.report(
                    {'INFO'},
                    f"Created {len(self.selected_objects)} modifiers lists")

        # ==========================================
        # Create or select modifier on active object
        # ==========================================
        # If custom operator specified that it needs to create new modifier
        if self._BMTOOL_MODIFIER_CREATE:
            mod_new = self.m_list.create_modifier(
                    self._DEFAULT_M_NAME, self._DEFAULT_M_TYPE)
            self.m_list.active_modifier_set(mod_new)

        # if operator specified _DEFAULT_M_NAME
        # and _DEFAULT_M_TYPE on initialisation
        # and is not _BMTOOLM
        elif not self._BMTOOLM:

            # select existing
            if self.m_list.has_modifier_by_type(
                    self._DEFAULT_M_TYPE) and self.m_list.get_list_length(
                            ) > 0:

                # select mod of _DEFAULT_M_TYPE
                list_by_type\
                        = self.m_list.get_list_by_type(self._DEFAULT_M_TYPE)
                self.m_list.active_modifier_set(list_by_type[-1])

            # create new
            else:
                mod_new = self.m_list.create_modifier(
                        self._DEFAULT_M_NAME, self._DEFAULT_M_TYPE)
                self.m_list.active_modifier_set(mod_new)
                self.bmtool_modifier_defaults(context)

                if self._BMTOOL_V:
                    self.report({'INFO'}, "Created new modifier")

        # if not specified, and there is modifiers already
        # select first
        elif self.m_list.get_list_length() > 0:
            self.m_list.active_modifier_set(self.m_list.get_first())

        # If not usual modifier operator and no modifiers
        else:
            self.report({'ERROR'}, "Cant create modifier or select one.")
            self.clear(context)
            return {'CANCELLED'}

        # For cluster selection
        self._selecting_clusters = False

        # Trigger active modifier change
        self.bmtool_modifier_update(context)

        logger.info("Finished initializing operator")

        self.first_x = event.mouse_x
        self.first_y = event.mouse_y

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def display_additional_info_about_bmtool(self, context):
        logger.debug("BMTool is created")
        logger.debug(f"_BMTOOLM {self._BMTOOLM}")
        logger.debug(f"_DEFAULT_M_NAME {self._DEFAULT_M_NAME}")
        logger.debug(f"_DEFAULT_M_TYPE {self._DEFAULT_M_TYPE}")
        logger.debug(f"_BMTOOL_DEFAULT_MODE {self._BMTOOL_DEFAULT_MODE}")
        logger.debug(f"_BMTOOL_EDITMODE {self._BMTOOL_EDITMODE}")
        logger.debug(f"_BMTOOL_MODIFIER_CREATE {self._BMTOOL_MODIFIER_CREATE}")
        logger.debug(f"_BMTOOL_SINGLE_OBJECT {self._BMTOOL_SINGLE_OBJECT}")
        logger.debug(f"_BMTOOL_UI {self._BMTOOL_UI}")
        logger.debug(f"_BMTOOL_UI_STATUSBAR {self._BMTOOL_UI_STATUSBAR}")
        logger.debug(f"_BMTOOL_V {self._BMTOOL_V}")

    # --------------------------------
    # Operator-specific modal method 1
    # --------------------------------
    # Used before any other modal editing
    def bmtool_modal_1(self, context, event):
        """
        This method is called before BMToolMod modal method.
        """
        return

    # --------------------------------
    # Operator-specific modal method 2.
    # --------------------------------
    # All modal editing should be here.
    def bmtool_modal_2(self, context, event):
        """
        This method is called after BMToolMod modal method.
        """
        return

    # -------------------------------
    # Operator-specific modifier add method.
    # -------------------------------
    def bmtool_modifier_add(self, context):
        """
        This method is called when BMToolMod trying to create
        modifier and _BMTOOLM is true.
        """
        return

    # ------------------------------
    # Default operator modifier-specific settings.
    # TODO: what even is this?
    # TODO: should require modifier.
    # ------------------------------
    def bmtool_modifier_defaults(self, context):
        """
        This method is called when BMToolMod trying to set modifier defaults
        and _BMTOOLM is true.
        """
        return

    # ------------------------------
    # Operator-specific modifier update.
    # ------------------------------
    def bmtool_modifier_update(self, context):
        """
        This method is called every time active modifier changed
        in BMToolMod.
        """
        return

    # ------------------------------
    # Operator-specific inv. method.
    # ------------------------------
    # TODO: this method should be renamed.
    def bmtool_modifier_inv(self, context, event):
        """
        This method is called before BMToolMod invoke.
        """
        return

    # -------------------------------
    # Operator-specific remove method
    # -------------------------------
    # TODO: this method should be renamed.
    def bmtool_modifier_remove(self, context):
        """
        This method is called when encountered FINISHED or CANCELLED in
        BMToolMod modal methods.
        """
        return
