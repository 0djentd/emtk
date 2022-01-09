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

from bpy.types import Operator

from ..classes.modal_clusters_operator import ModalClustersOperator
from ..ui.bmtool_ui import BMToolUi

from ..editors.adaptive import\
        AdaptiveModalEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMTOOL_OT_bmtoolm(BMToolUi, ModalClustersOperator, Operator):
    """Tool for editing all modifiers of an object."""

    bl_idname = "object.bmtoolm"
    bl_label = "BMToolM"
    bl_description = "Edit modifiers on selected objects"
    bl_options = {'GRAB_CURSOR'}

    # List of all editors
    # _BMTOOL_OT_bmtoolm_editors[]

    # List of possible editors for currently selected modifier
    # _BMTOOL_OT_bmtoolm_possible_editors[]

    # Active editor
    # _BMTOOL_OT_bmtoolm_active_editor

    def __init__(self):
        """Creates list of all editors."""

        self.__editors = []
        self.__possible_editors = []
        self.__active_editor = None

        editor = AdaptiveModalEditor()
        self.__editors.append(editor)

        # editor = BMToolEditorWeightedNormal()
        # self.__editors.append(editor)

        # editor = BMToolEditorBevel()
        # self.__editors.append(editor)

    # BMToolMod methods {{{
    def bmtool_modal_pre(self, context, event):
        """Modal method 1, before bmtoolmod"""
        editor = self.get_editor()
        if editor is not None:
            return editor.editor_modal_pre(
                context, event, self.m_list.get_cluster())
        else:
            raise TypeError

    def bmtool_modal(self, context, event):
        """Modal method 2, after bmtoolmod"""

        # Scroll through possible editors.
        if (event == 'T') & (event.value == 'PRESSED'):
            if event.shift:
                self.sel_previous_editor()
            else:
                self.sel_next_editor()

        # Editor modal.
        editor = self.get_editor()
        if editor is not None:
            return editor.editor_modal(
                    context, event, self.m_list.get_cluster())
        else:
            raise TypeError

    def bmtool_modifier_update(self, context):
        """
        This method is called by bmtoolmod every time active
        cluster or modifier is changed.
        """

        logger.debug('BMToolM modifier changed.')

        # Call remove method of editor
        if self.__active_editor is not None:
            self.__active_editor.editor_switched_from(
                    context, self.m_list.get_cluster())

        # Get list of possible ediors
        self.__possible_editors = self.__get_editors(self.m_list.get_cluster())

        # Set first editor, if any
        if len(self.__possible_editors) > 0:
            self.__active_editor = self.__possible_editors[0]
        else:
            self.__active_editor = None

        # Call invoke method of editor
        if self.__active_editor is not None:
            self.__active_editor.editor_switched_to(
                    context, self.m_list.get_cluster())

    def bmtool_operator_inv(self, context, event):
        """
        Method that is used by BMToolMod
        Additional invoke method
        """
        for editor in self.__editors:
            self.__initialize_bmtoolm_editor(editor)

    def bmtool_operator_rm(self, context):
        """
        Method that is used by BMToolMod
        Additional remove method
        """
        del(self.__editors)
        del(self.__possible_editors)
        del(self.__active_editor)
    # }}}

    # UI {{{
    def bmtool_ui(self, context):
        """
        Method that is used by BMToolUI
        Returns list of strings
        """

        ui_t = []
        if self.__active_editor is not None:
            if self.mode == 'EDITOR':
                e = self.__active_editor
                ui_t.append(f"Selected editor: {e.props['name']}")
                ui_t.append(f"Editor mode: {e.mode}")
                ui_t.append(f"Editor input mode: {e.modal_input_mode}")
                ui_t.append(f"Digits: {e.modal_digits_get()}")
                ui_t.append(f"Letters: {e.modal_letters_get()}")

            ui_t.append("Possible editors:")
            for x in self.__possible_editors:
                ui_t.append(x.props['name'])
        else:
            ui_t.append("No active editor")

        ui_t.append(" ")
        ui_t_2 = self.bmtool_ui_list()
        for x in ui_t_2:
            ui_t.append(x)
        ui_t_3 = self.__active_editor.get_mappings_for_ui()
        for x in ui_t_3:
            ui_t.append([x, 20])
        return ui_t
    # }}}

    # Editor selection {{{
    def get_editor(self):
        """Returns currently active editor."""
        if self.__active_editor in self.__possible_editors:
            return self.__active_editor
        else:
            raise TypeError

    def sel_previous_editor(self):
        """Selects previous possible editor."""
        i = self.__possible_editors.index(self._active_editor)
        if i == 0:
            self.__active_editor = self.__possible_editors[-1]
        else:
            self.__active_editor = self.__possible_editors[i - 1]

    def sel_next_editor(self):
        """Selects next possible editor."""
        i = self._possible_editors.index(self._active_editor)
        if i < len(self._possible_editors) - 1:
            self._active_editor = self._possible_editors[i + 1]
        else:
            self._active_editor = self._possible_editors[0]
    # }}}

    # Editors list {{{
    def add_editor(self, editor):
        """Adds new editor type or replaces existing one."""
        self.remove_editor(editor)
        self.__initialize_bmtoolm_editor(editor)
        self.__editors.append(editor)

    def remove_editor(self, editor):
        """Removes editor from this operator."""
        remove = []
        for x in self.__editors:
            if editor.props['name'] == x.props['name']\
                    and editor.props['cluster_types']\
                    == x.props['cluster_types']:
                remove.append(x)
        for x in remove:
            if x is self.__active_editor:
                raise ValueError
            self.__editors.remove(x)

    def __get_editors(self, cluster):
        """Returns list of possible editors for cluster."""
        editors_list = []
        for editor in self.__editors:
            if cluster.type in editor.props['cluster_types']:
                editors_list.append(editor)
        return editors_list

    def __initialize_bmtoolm_editor(self, editor):
        editor.first_x = self.first_x
        editor.first_y = self.first_y
    # }}}
