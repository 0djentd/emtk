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
from ..ui.emtk_ui import EMTKUi
from ..editors.adaptive import AdaptiveModalEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMTOOL_OT_emtkm(EMTKUi, ModalClustersOperator, Operator):
    """Tool for editing all modifiers of an object."""

    bl_idname = "object.emtkm"
    bl_label = "EMTKM"
    bl_description = "Edit modifiers on selected objects"

    def __init__(self):
        """Creates list of all editors."""

        # List of all editors
        self.__editors = []
        # List of possible editors for currently selected modifier
        self.__possible_editors = []
        # Active editor
        self.__active_editor = None

        self.__editors.append(AdaptiveModalEditor())

    # EMTKMod methods
    # TODO: rename this methods
    def emtk_modal_pre(self, context, event):
        """Modal method 1, before emtkmod"""
        editor = self.get_editor()
        if editor is not None:
            return editor.editor_modal_pre(
                context, event, self.m_list.get_cluster())
        else:
            raise TypeError

    def emtk_modal(self, context, event):
        """Modal method 2, after emtkmod"""

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

    def emtk_modifier_update(self, context):
        """
        This method is called by emtkmod every time active
        cluster or modifier is changed.
        """

        logger.debug('EMTKM modifier changed.')

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

    def emtk_operator_inv(self, context, event):
        """
        Method that is used by EMTKMod
        Additional invoke method
        """
        for editor in self.__editors:
            self.__initialize_emtkm_editor(editor)

    def emtk_operator_rm(self, context):
        """
        Method that is used by EMTKMod
        Additional remove method
        """
        del(self.__editors)
        del(self.__possible_editors)
        del(self.__active_editor)

    # UI

    def emtk_ui(self, context):
        """
        Method that is used by EMTKUI
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
        ui_t_2 = self.emtk_ui_list()
        for x in ui_t_2:
            ui_t.append(x)
        if self.__active_editor is not None:
            ui_t_3 = self.__active_editor.get_mappings_for_ui()
            for x in ui_t_3:
                ui_t.append([x, 20])
        else:
            ui_t.append(['No editor.', 20])
        return ui_t

    # Editor selection

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

    # Editors list

    def add_editor(self, editor):
        """Adds new editor type or replaces existing one."""
        self.remove_editor(editor)
        self.__initialize_emtkm_editor(editor)
        self.__editors.append(editor)

    def remove_editor(self, editor):
        """Removes editor from this operator."""
        remove = []
        for x in self.__editors:
            if editor.props['name'] == x.props['name']\
                    and editor.props['types']\
                    == x.props['types']:
                remove.append(x)
        for x in remove:
            if x is self.__active_editor:
                raise ValueError
            self.__editors.remove(x)

    def __get_editors(self, cluster):
        """Returns list of possible editors for cluster."""
        editors_list = []
        for editor in self.__editors:
            if cluster.type in editor.props['types']:
                editors_list.append(editor)
            elif 'ANY' in editor.props['types']:
                editors_list.append(editor)
        return editors_list

    def __initialize_emtkm_editor(self, editor):
        editor.first_x = self.first_x
        editor.first_y = self.first_y
