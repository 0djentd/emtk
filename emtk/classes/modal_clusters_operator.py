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

import logging

import bpy
from libemtk.modifiers_operator import ModifiersOperator
from modal_shortcuts.object import ModalInputOperator

from ..ui.emtk_ui import emtk_modifier_ui_draw

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

# TODO: use modal kbs for general editing too.
# TODO: actually working modal input str.


class ModalClustersOperator(ModalInputOperator, ModifiersOperator):
    """
    Base class for modal operators that use Blender modifier stack
    through ModififersOperator and ExtendedModifiersList.
    """

    # Var

    # Operator mode, can be 'ACTIONS' or 'EDITOR'.
    # self.mode

    # Clusters selection.
    # self.__selecting_clusters

    # Draw handler.
    # self.emtk_ui_draw_handler

    # Active object ModifiersList instance.
    # self.m_list()

    # Selected objects ModifiersList instances.
    # self.selected_objects[]

    # Mappings
    __emtk_kbs = {
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

    # Const
    # Default modal editing mode.
    __DEFAULT_MODE = 'ACTIONS'

    # Returned values that should trigger operator remove.
    __OPERATOR_REMOVE = [{'FINISHED'}, {'CANCELLED'}]

    # Create draw handler.
    __UI = True

    # Use statusbar to display modifier info.
    __UI_STATUSBAR = False

    # Use modifiers of any type.
    __EMTKM = True

    @classmethod
    def poll(self, context):
        """Check if operator can be used."""
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT' and context.mode != 'EDIT':
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def modal(self, context, event):
        """Method that is initiated every frame or whatever."""

        # Exit out of editor mode or finish operator.
        if (event.type == self.__emtk_kbs['exit']
                or event.type == 'LEFTMOUSE')\
                and event.value == 'PRESS':
            if self.mode != self.__DEFAULT_MODE:
                self.emtk_modifier_update(context)
                self.mode = self.__DEFAULT_MODE
            else:
                self.clear(context)
                return {'FINISHED'}

        # Cancell.
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.clear(context)
            return {'CANCELLED'}

        # Switch between editor and actions.
        elif event.type == 'SPACE' and event.value == 'PRESS':
            if self.mode == 'ACTIONS':
                self.mode = 'EDITOR'
                self.emtk_modifier_update(context)
            else:
                self.mode = 'ACTIONS'
                self.emtk_modifier_update(context)
            logger.info(f'Switched mode to {self.mode}')

        # Modal method.
        if self.mode == 'EDITOR':
            a = self.emtk_modal_pre(context, event)
            if a in self.__OPERATOR_REMOVE:
                self.clear(context)
                return a

        # Redraw UI
        if self.__UI:
            context.area.tag_redraw()
        if self.__UI_STATUSBAR:
            context.workspace.status_text_set()

        # Modal method.
        if self.mode == 'ACTIONS':
            a = self.__modal_actions(context, event)
            if a in self.__OPERATOR_REMOVE:
                self.clear(context)
                return a

        # Modal method.
        elif self.mode == 'EDITOR':
            a = self.emtk_modal(context, event)
            if a in self.__OPERATOR_REMOVE:
                self.clear(context)
                return a
        else:
            raise ValueError

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        """Method that is invoked once per operator usage."""

        self.mode = self.__DEFAULT_MODE
        self.__selecting_clusters = False
        self.first_x = event.mouse_x
        self.first_y = event.mouse_y

        # Operator-specific invoke
        self.emtk_operator_inv(context, event)

        # Add UI.
        if self.__UI:
            logger.info("EMTK UI is created")
            sv = bpy.types.SpaceView3D
            self.emtk_ui_draw_handler = sv.draw_handler_add(
                emtk_modifier_ui_draw, (self, context),
                'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()

        # TODO: this should be in lib
        # Create backup collection.
        addon_prefs = bpy.context.preferences.addons['emtk'].preferences
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

        # Create instances of ModifierList.
        result = self.create_objects_modifiers_lists(context)
        if result is False or result is None:
            self.report({'ERROR'}, "Error while parsing clusters")
            self.clear(context)
            return {'FINISHED'}

        # Trigger active modifier change
        self.emtk_modifier_update(context)

        logger.info("Finished initializing operator")

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    # Modal actions.

    def __modal_actions(self, context, event):
        """This method is used for general modifiers stack editing."""

        layer = self.m_list.get_layer()
        cluster = self.m_list.get_cluster()

        # Modifier visibility
        if (event.type == self.__emtk_kbs['visibility_1'])\
                & (event.value == 'PRESS'):
            if event.shift:
                if self.__selecting_clusters:
                    for x in layer.get_selection():
                        x.toggle_this_cluster_visibility(
                            [True, False, False, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                        [True, False, False, False])
            else:
                if self.__selecting_clusters:
                    for x in layer.get_selection():
                        x.toggle_this_cluster_visibility(
                            [False, True, False, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                        [False, True, False, False])

        # Modifier visibility 2
        elif (event.type == self.__emtk_kbs['visibility_2'])\
                & (event.value == 'PRESS'):
            if event.shift:
                if self.__selecting_clusters:
                    for x in layer.get_selection():
                        cluster.toggle_this_cluster_visibility(
                            [False, False, False, True])
                else:
                    cluster.toggle_this_cluster_visibility(
                        [False, False, False, True])
            else:
                if self.__selecting_clusters:
                    for x in layer.get_selection():
                        cluster.toggle_this_cluster_visibility(
                            [False, False, True, False])
                else:
                    cluster.toggle_this_cluster_visibility(
                        [False, False, False, True])

        # Sort modifiers
        elif (event.type == self.__emtk_kbs['sort'])\
                & (event.value == 'PRESS'):
            layer.apply_sorting_rules()

        # Duplicate cluster modifiers and parse
        elif (event.type == self.__emtk_kbs['add_new'])\
                & (event.value == 'PRESS'):

            if not self.__EMTKM:
                x = self.m_list.create_modifier(
                    self._DEFAULT_M_NAME, self._DEFAULT_M_TYPE)
                self.m_list.active = x
            else:
                self.m_list.duplicate(cluster)

            # Trigger active modifier change
            self.emtk_modifier_update(context)

        # Apply active cluster
        elif (event.type == self.__emtk_kbs['apply_remove'])\
                & event.shift & (event.value == 'PRESS'):

            # Remove cluster.
            if self.__selecting_clusters:
                layer.apply_clusters_selection()
            else:
                layer.apply(cluster)

            self.__stop_selecting_clusters()
            # Check if it was last actual modifier.
            # If so, finish operator.
            if len(self.m_list.all_modifiers()) == 0:
                self.clear(context)
                return {'FINISHED'}

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

        # Deconstruct cluster.
        elif (event.type == self.__emtk_kbs['construct_deconstruct'])\
                & event.shift & (event.value == 'PRESS'):

            for x in self.__get_clusters():
                if layer.deconstruct(x):
                    self.report({'INFO'}, "Deconstructed cluster")
                else:
                    self.report({'ERROR'}, "Cant deconstruct cluster")

        # Construct cluster from selection.
        elif (event.type == self.__emtk_kbs['construct_deconstruct'])\
                & (event.value == 'PRESS'):

            if self.__selecting_clusters:
                if layer.construct_cluster_from_selection():
                    self.report({'INFO'}, "Constructed cluster.")
                else:
                    self.report({'ERROR'}, "Cant create cluster.")
                self.__stop_selecting_clusters()
            else:
                self.report({'ERROR'}, "No clustes selected.")

        # Toggle selection.
        elif (event.type == self.__emtk_kbs['toogle_selection'])\
                & (event.value == 'PRESS'):

            # Toggle selecting clusters.
            if self.__selecting_clusters:
                self.__stop_selecting_clusters()
            else:
                self.__start_selecting_clusters()

        # Remove active cluster.
        elif (event.type == self.__emtk_kbs['apply_remove'])\
                & (event.value == 'PRESS'):
            logger.info('Removing cluster')

            # Remove cluster.
            if self.__selecting_clusters is True:
                layer.remove_clusters_selection()
            else:
                layer.remove(cluster)

            self.__stop_selecting_clusters()

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

        # Move modifier up.
        elif (event.type == self.__emtk_kbs['up'])\
                & event.shift & (event.value == 'PRESS'):
            logger.info('Moving cluster')

            # Move modifier.
            if self.__selecting_clusters:
                layer.move_up_selection()
            else:
                layer.move_up(cluster)

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

        # Move modifier down.
        elif (event.type == self.__emtk_kbs['down'])\
                & event.shift & (event.value == 'PRESS'):
            logger.info('Moving cluster')

            # Move modifier.
            if self.__selecting_clusters:
                layer.move_down_selection()
            else:
                layer.move_down(cluster)

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

        # Collapse cluster.
        elif (event.type == self.__emtk_kbs['collapse'])\
                & (event.value == 'PRESS'):
            logger.info('Collapse toggle cluster')
            self.__stop_selecting_clusters()

            # Collapse cluster.
            if event.shift:
                if (cluster.instance_data['collapsed'] is False)\
                        & (cluster.has_clusters() is False):
                    cluster.instance_data['collapsed'] = True
                elif (cluster.instance_data['collapsed'] is True)\
                        & (cluster.has_clusters() is False):
                    layer.instance_data['collapsed'] = True
                elif (cluster.instance_data['collapsed'] is True)\
                        & (cluster.has_clusters() is True):
                    layer.instance_data['collapsed'] = True

            # Uncollapse cluster.
            else:
                cluster.instance_data['collapsed'] = False

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

            self.__stop_selecting_clusters()

        # Scroll through modifiers up.
        elif (event.type == self.__emtk_kbs['up'])\
                & (event.value == 'PRESS'):

            # Only change modifier if there is more than one available.
            if len(layer) > 1:

                # First modifier.
                if event.ctrl:
                    if not self.__EMTKM:
                        x = []
                        for y in layer:
                            if y.type == self._DEFAULT_M_TYPE:
                                x.append(y)
                        layer.active = x[0]
                    else:
                        layer.active = layer[0]

                # Previous modifier.
                else:
                    if not self.__EMTKM:
                        layer.active = layer.iterate(
                            cluster, 'UP', self._DEFAULT_M_TYPE)
                    else:
                        layer.active = layer.iterate(cluster, 'UP', loop=True)

            # Trigger active modifier change.
            self.emtk_modifier_update(context)

        # Scroll through modifiers down.
        elif (event.type == self.__emtk_kbs['down'])\
                & (event.value == 'PRESS'):

            # Only change modifier if there is more than one available.
            if len(layer) > 1:
                # Last modifier.
                if event.ctrl:
                    if not self.__EMTKM:
                        x = []
                        for y in layer:
                            if y.type == self._DEFAULT_M_TYPE:
                                x.append(y)
                        layer.active = x[-1]
                    else:
                        layer.active = layer[-1]

                # Next modifier.
                else:
                    if not self.__EMTKM:
                        layer.active = layer.iterate(
                            cluster, 'DOWN', self._DEFAULT_M_TYPE)
                    else:
                        layer.active = layer.iterate(
                            cluster, 'DOWN', loop=True)

                # Trigger active modifier change.
                self.emtk_modifier_update(context)
        else:
            return False
        return True

    # TODO: rename this methods.
    # Methods reserved for operators.

    def emtk_modal_pre(self, context, event):
        """Operator-specific modal method 1

        Used before any other modal editing
        This method is called before ModalClustersOperator modal method.
        """
        return

    def emtk_modal(self, context, event):
        """Operator-specific modal method 2.

        All modal editing should be here.
        This method is called after ModalClustersOperator modal method.
        """
        return

    def emtk_modifier_update(self, context):
        """Operator-specific modifier update.

        This method is called every time active modifier changed
        in ModalClustersOperator.
        """
        return

    def emtk_operator_invoke(self, context, event):
        """Operator-specific invoke method.

        This method is called before ModalClustersOperator invoke.
        """
        return

    def emtk_operator_remove(self, context):
        """Operator-specific remove method

        This method is called when encountered FINISHED or CANCELLED in
        ModalClustersOperator modal methods.
        """
        return

    def clear(self, context):
        """Removes operator.

        Used when encountering FINISHED or CANCELLED in modal method
        to remove no longer needed properies, handlers or whatever.
        """

        # Remove ui
        context.workspace.status_text_set(None)
        if self.__UI:
            bpy.types.SpaceView3D.draw_handler_remove(
                self.emtk_ui_draw_handler, 'WINDOW')
            context.area.tag_redraw()
            logger.info("EMTK UI is removed")

        # Operator-specific remove
        self.emtk_operator_remove(context)

        already_removed = False

        # TODO: should not be here.
        if bpy.context.preferences.addons['emtk'].preferences.save_clusters:
            try:
                self.m_list.save_modifiers_state()
                self.m_list.save_clusters_state()
                logger.info("Saved modifiers and clusters.")
            except AttributeError:
                already_removed = True

        try:
            del(self.selected_objects)
        except AttributeError:
            already_removed = True

        try:
            del(self.m_list)
        except AttributeError:
            already_removed = True

        if already_removed:
            logger.info("Clusters were already removed.")

        logger.info("Modal operator finished.")

    # Clusters selection utils

    def __stop_selecting_clusters(self) -> None:
        self.__selecting_clusters = False
        layer = self.m_list.get_layer()
        layer.selection.clear()

    def __start_selecting_clusters(self) -> None:
        self.__selecting_clusters = True
        layer = self.m_list.get_layer()
        layer.selection.start(layer.active)

    # TODO: move this to lib
    def __get_clusters(self):
        """Returns selected clusters, or list with active cluster."""

        cluster = self.m_list.get_cluster()
        layer = self.m_list.get_layer()

        if self.__selecting_clusters:
            return layer.get_selection()
        else:
            return [cluster]
