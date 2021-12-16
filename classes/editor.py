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

import math


class ModifierEditor():
    """
    Modifier editor base class
    Designed to be used with BMToolM
    """

    # Editor name for UI
    _MODIFIER_EDITOR_NAME = "No editor-specific name"

    # Default modifier name for this editor
    _DEFAULT_M_NAME = None

    # Type of modifiers that this editor should be associated with
    _DEFAULT_M_TYPE = None

    # TODO: remove this
    # Can modifier be created from within editor using _DEFAULT_M_TYPE?
    _MODIFIER_CREATEABLE = False

    # Can be used with modifier clusters
    _MODIFIERS_CLUSTER_EDITOR = False

    # TODO: Allow using editor with any modifier
    _MODIFIER_ANY = False

    # Default mode
    _DEFAULT_EDITOR_MODE = "Select mode"

    # Try to use bmtool operator as editor
    _BMTOOL_EDITOR_OPERATOR = True

    bmtool_mode = _DEFAULT_EDITOR_MODE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================
    # Editor method placeholders
    # ==========================================
    def bmtool_editor_inv(
            self, context, m_list, selected_objects):
        """
        Editor invoke method, called every time editor is switched to
        """
        # Resets editor's mode, kinda should be in every editor
        self.bmtool_mode = self._DEFAULT_EDITOR_MODE
        return

    def bmtool_editor_remove(
            self, context, m_list, selected_objects):
        """
        Editor remove method, called every time editor is switched from
        """
        # Resets editor's mode, kinda should be in every editor
        self.bmtool_mode = self._DEFAULT_EDITOR_MODE
        return

    def bmtool_editor_modal_1(
            self, context, event, m_list, selected_objects, delta_d):
        """
        Modal method 1
        """
        return

    def bmtool_editor_modal_2(
            self, context, event, m_list, selected_objects, delta_d):
        """
        Modal method 2
        """
        if self._BMTOOL_EDITOR_OPERATOR:
            self.delta_d = delta_d
            self.m_list = m_list
            self.bmtool_modal_2(context, event)
        return

    def bmtool_editor_modifier_defaults(
            self, context, m_list, selected_objects):
        """
        Modifier defaults
        """
        if self._BMTOOL_EDITOR_OPERATOR:
            return self.bmtool_modifier_defaults(context)
        return

    def bmtool_editor_modifier_stats(
            self, context, m_list, selected_objects):
        """
        UI info about modifier
        """
        ui_t = []
        ui_t.append("No editor-specific modifier stats")
        if self._BMTOOL_EDITOR_OPERATOR:
            self.m_list = m_list
            return self.bmtool_modifier_stats(context)
        return ui_t

    # TODO: should be in utils
    # Returns VL
    # VL = vector length
    # VL from object center (currently from initialisation)
    # TODO: should take into consideration distance to object center.
    # TODO: should use object center as center.
    # TODO: should not change settings when changing mode
    def delta_d(self, context, event):
        x = self.vec_len(self.first_x, event.mouse_x,
                         self.first_y, event.mouse_y
                         )
        y = pow(x, 2)
        return y

    # Vector length
    def vec_len(self, x1, x2, y1, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    # ==========================================
    # Compat. method placeholders for bmtool operators
    # ==========================================
    def bmtool_modal_2(self, context, event):
        self.report({'INFO'}, "No editor-specific operator modal 2 method")
        return

    def bmtool_modifier_defaults(self, context):
        self.report({'INFO'}, "No editor-specific operator mod defaults")
        return

    def bmtool_modifier_stats(self, context):
        ui_t = []
        ui_t.append(
                "No editor-specific modifier stats. No operator-editor stats.")
        return ui_t
