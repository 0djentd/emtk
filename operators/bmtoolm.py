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

from ..lib.bmtool_operator import BMToolMod
from ..ui.bmtool_ui import BMToolUi

from ..editors.weightednormal import BMToolEditorWeightedNormal
from ..editors.bevel import BMToolEditorBevel


# Tool for editing all modifiers of an object
class BMTOOL_OT_bmtoolm(BMToolUi, BMToolMod, Operator):
    bl_idname = "object.bmtoolm"
    bl_label = "BMToolM"
    bl_description = "Edit modifiers on selected objects"

    _BMTOOLM = True

    # List of all editors
    # _editors[]

    # List of possible editors for currently selected modifier
    # _possible_editors[]

    # Active editor
    # _active_editor

    def __init__(self):
        """
        Creates list of all editors
        """

        self._editors = []
        self._possible_editors = []
        self._active_editor = None

        editor = BMToolEditorWeightedNormal()
        self._editors.append(editor)

        editor = BMToolEditorBevel()
        self._editors.append(editor)

    def sel_editor(self):
        """
        Returns currently active editor
        """

        # Probably not needed
        if self._active_editor in self._possible_editors:
            return self._active_editor

    def get_editors(self):
        """
        Returns list of editors for self.m_list.active_modifier_get_type
        of modifiers.
        """

        editors_list = []
        for editor in self._editors:
            if self.m_list.active_modifier_get_type(
                    ) == editor._DEFAULT_M_TYPE:
                editors_list.append(editor)
        return editors_list

    def bmtool_modifier_update(self, context):
        """
        This method is called every time active modifier changed
        in BMToolMod
        """

        # Call remove method of editor
        if self._active_editor is not None:
            self._active_editor.bmtool_editor_remove(
                    context, self.m_list, self.selected_objects)

        # Get list of possible ediors
        self._possible_editors = self.get_editors()

        # Set first editor, if any
        if len(self._possible_editors) > 0:
            self._active_editor = self._possible_editors[0]
        else:
            self._active_editor = None

        # Call invoke method of editor
        if self._active_editor is not None:
            self._active_editor.bmtool_editor_inv(
                    context, self.m_list, self.selected_objects)

    def bmtool_modal_1(self, context, event):
        """
        Modal method 1
        Method is used by BMToolMod
        """

        editor = self.sel_editor()
        if editor is not None:
            return editor.bmtool_editor_modal_1(context, event,
                                                self.m_list,
                                                self.selected_objects)

    def bmtool_modal_2(self, context, event):
        """
        Modal method 2
        Method is used by BMToolMod
        """

        # Scroll through possible editors
        if (event == 'T') & (event.value == 'PRESSED'):
            active_editor_i = self._possible_editor.index(self._active_editor)
            if active_editor_i < len(self._possible_editors) - 1:
                self._active_editor = self._possible_editors[active_editor_i+1]
            else:
                self._active_editor = self._possible_editors[0]

        editor = self.sel_editor()
        if editor is not None:
            return editor.bmtool_editor_modal_2(context, event,
                                                self.m_list,
                                                self.selected_objects)

    def bmtool_modifier_add(self, context):
        """
        Adds modifier
        Method is used by BMToolMod
        """

        editor = self.sel_editor()
        if editor is not None and editor._MODIFIER_CREATEABLE:
            return self.m_list.create_modifier(editor._DEFAULT_M_NAME,
                                               editor._DEFAULT_M_TYPE)

    def bmtool_modifier_defaults(self, context):
        """
        Set modifier defaults from editor
        Method is used by BMToolMod
        """

        editor = self.sel_editor()
        if editor is not None:
            return editor.bmtool_editor_modifier_defaults(
                    context, self.m_list, self.selected_objects)

    def bmtool_ui(self, context):
        """
        Method that is used by BMToolUI
        Returns list of strings
        """

        ui_t = []
        ui_t.append("BMToolM 2")
        ui_t.append(" ")
        if self._active_editor is not None:
            ui_t.append(
                    f"Editor - {self._active_editor._MODIFIER_EDITOR_NAME}")
            ui_t.append("Possible editors:")
            for x in self._possible_editors:
                ui_t.append(x._MODIFIER_EDITOR_NAME)
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

        editor = self.sel_editor()
        if editor is not None:
            return editor.bmtool_editor_modifier_stats(
                    context, self.m_list, self.selected_objects)
        else:
            ui_t = []
            modifier_type = self.m_list.active_modifier_get_type()
            ui_t.append(f"No editor for {modifier_type} modifier")
            return ui_t

    def bmtool_modifier_inv(self, context, event):
        """
        Method that is used by BMToolMod
        Additional invoke method
        """
        for editor in self._editors:
            editor.first_x = event.mouse_x
            editor.first_y = event.mouse_y
