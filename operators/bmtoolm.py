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

from ..classes.bmtool_operator import BMToolMod
from ..ui.bmtool_ui import BMToolUi

from ..editors.weightednormal import BMToolEditorWeightedNormal
from ..editors.bevel import BMToolEditorBevel


class BMTOOL_OT_bmtoolm(BMToolUi, BMToolMod, Operator):
    """Tool for editing all modifiers of an object."""

    bl_idname = "object.bmtoolm"
    bl_label = "BMToolM"
    bl_description = "Edit modifiers on selected objects"

    # List of all editors
    # _editors[]

    # List of possible editors for currently selected modifier
    # _possible_editors[]

    # Active editor
    # _active_editor

    def __init__(self):
        """Creates list of all editors."""

        self._editors = []
        self._possible_editors = []
        self._active_editor = None

        editor = BMToolEditorWeightedNormal()
        self._editors.append(editor)

        editor = BMToolEditorBevel()
        self._editors.append(editor)

    def add_editor(self, editor):
        """Adds new editor type or replaces existing one."""
        self.remove_editor(editor)
        self._initialize_bmtoolm_editor(editor)
        self._editors.append(editor)

    def remove_editor(self, editor):
        """Removes editor from this operator."""
        remove = []
        for x in self._editors:
            if editor.props['name'] == x.props['name']\
                    and editor.props['cluster_types']\
                    == x.props['cluster_types']:
                remove.append(x)
        for x in remove:
            if x is self._active_editor:
                raise ValueError
            self._editors.remove(x)

    def get_editor(self):
        """Returns currently active editor."""
        if self._active_editor in self._possible_editors:
            return self._active_editor
        elif self._active_editor is None:
            return
        else:
            raise TypeError

    def _get_editors(self, cluster):
        """Returns list of possible editors for cluster."""
        editors_list = []
        for editor in self._editors:
            if cluster.type in editor.props['cluster_types']:
                editors_list.append(editor)
        return editors_list

    def sel_previous_editor(self):
        """Selects previous possible editor."""
        i = self._possible_editors.index(self._active_editor)
        if i == 0:
            self._active_editor = self._possible_editors[-1]
        else:
            self._active_editor = self._possible_editors[i - 1]

    def sel_next_editor(self):
        """Selects next possible editor."""
        i = self._possible_editors.index(self._active_editor)
        if i < len(self._possible_editors) - 1:
            self._active_editor = self._possible_editors[i + 1]
        else:
            self._active_editor = self._possible_editors[0]

    def bmtool_modifier_update(self, context):
        """
        This method is called by bmtoolmod every time active
        cluster or modifier is changed.
        """

        # Call remove method of editor
        if self._active_editor is not None:
            self._active_editor.bmtool_editor_remove(
                    context, self.get_cluster())

        # Get list of possible ediors
        self._possible_editors = self._get_editors(self.m_list.get_cluster())

        # Set first editor, if any
        if len(self._possible_editors) > 0:
            self._active_editor = self._possible_editors[0]
        else:
            self._active_editor = None

        # Call invoke method of editor
        if self._active_editor is not None:
            self._active_editor.bmtool_editor_inv(
                    context, self.get_cluster())

    def bmtool_modal_1(self, context, event):
        """Modal method 1, before bmtoolmod"""
        editor = self.get_editor()
        if editor is not None:
            return editor.bmtool_editor_modal_1(
                context, event, self.m_list.get_clust())

    def bmtool_modal_2(self, context, event):
        """Modal method 2, after bmtoolmod"""

        # Scroll through possible editors
        if (event == 'T') & (event.value == 'PRESSED'):
            self.sel_next_editor()

        editor = self.get_editor()
        if editor is not None:
            return editor.bmtool_editor_modal_2(
                    context, event, self.m_list.get_clust())

    def bmtool_ui(self, context):
        """
        Method that is used by BMToolUI
        Returns list of strings
        """

        ui_t = []
        if self._active_editor is not None:
            ui_t.append(
                    f"Editor - {self._active_editor.props['name']}")
            ui_t.append("Possible editors:")
            for x in self._possible_editors:
                ui_t.append(x.props['name'])
        else:
            ui_t.append("No active editor")

        ui_t.append(" ")
        ui_t_2 = self.bmtool_ui_list(context)
        for x in ui_t_2:
            ui_t.append(x)
        return ui_t

    def bmtool_ui_modifier_stats(self, context):
        """
        Method that is used by BMToolUI
        Returns modifier-specific ui text with
        info about its settings in a list of strings
        """

        editor = self.get_editor()

        if editor is not None:
            return editor.bmtool_editor_modifier_stats(
                    context, self.get_cluster())
        else:
            ui_t = []
            ui_t.append("No editors for selected cluster.")
            return ui_t

    def bmtool_operator_inv(self, context, event):
        """
        Method that is used by BMToolMod
        Additional invoke method
        """
        for editor in self._editors:
            self._initialize_bmtoolm_editor(editor)

    def _initialize_bmtoolm_editor(self, editor):
        editor.first_x = self.first_x
        editor.first_y = self.first_y
