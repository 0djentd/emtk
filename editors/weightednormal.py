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

from ..classes.bmtool_editor import ModalClustersEditor


# Example of custom editor using ModalClustersEditor base class.
class BMToolEditorWeightedNormal(ModalClustersEditor):
    _MODIFIER_EDITOR_NAME = 'Weighted Normal Editor'
    _DEFAULT_M_NAME = 'Weighted Normal'
    _DEFAULT_M_TYPE = 'WEIGHTED_NORMAL'
    _MODIFIER_CREATEABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(
                         *args,
                         name='Weighted Normal',
                         cluster_types=['WEIGHTED_NORMAL_CLUSTER',
                                        'WEIGHTED_NORMAL'],
                         **kwargs)

    def bmtool_editor_modal_2(
            self, context, event, m_list, selected_objects):
        """Editor-specific modal method"""

        mod = m_list.active_modifier_get()

        if event.type == 'MOUSEMOVE':

            # Modal
            if self.bmtool_mode == "weight":
                mod.weight = self.delta_d(context, event) * 0.00005
            elif self.bmtool_mode == "thresh":
                mod.thresh = self.delta_d(context, event) * 0.00005

        # Modal editing modes switcher
        elif (event.type == 'W') & (event.value == 'PRESS'):
            self.bmtool_mode = "weight"
        elif (event.type == 'T') & (event.value == 'PRESS'):
            self.bmtool_mode = "thresh"

        # Modifier actions
        elif (event.type == 'S') & (event.value == 'PRESS'):
            mod.keep_sharp = not mod.keep_sharp
        elif (event.type == 'F') & (event.value == 'PRESS'):
            mod.use_face_influence = not mod.use_face_influence

    def bmtool_editor_modifier_stats(
            self, context, m_list, selected_objects):
        """Editor info about current modifier"""
        mod = m_list.active_modifier_get()
        ui_t = []
        ui_t.append(f"---{self.bmtool_mode}---")
        ui_t.append(f"(T)hreshold {round(mod.thresh, 3)}")
        ui_t.append(f"(W)eight {round(mod.weight, 3)}")
        ui_t.append(f"Keep (s)harp {mod.keep_sharp}")
        ui_t.append(f"Use (f)ace influence {mod.use_face_influence}")
        return ui_t
