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


class ModifiersListUtils():
    """
    Some utility functional for ModifiersList.
    Can be used with any ModifiersClustersList as well.
    """

    _MODIFIER_CLUSTERS = False

    # TODO: this can be removed
    _MODCLUSTER_DEFAULT_MODIFIER = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __init_subclass__(cls):
        cls._additional_info_log = []

    def _modifier_info(self, mod):
        """
        Returns list of strings with info about modifier or cluster.
        """

        mod_name = self.modifier_get_name(mod)
        mod_type = self.modifier_get_type(mod)
        mod_index = self.get_index(mod)
        ui_t = []
        ui_t.append(f"{mod_name} {mod_type} {mod_index}")
        return ui_t

    # ========================
    # Utility
    # ========================
    def modifiers_list_info_get(self):
        """
        Returns list of strings with info about modifier list.
        Used from operator.
        """
        x = copy.deepcopy(self._additional_info_log)
        self._additional_info_log.clear()
        x = x + self._modifiers_list_info()
        return x

    def _modifiers_list_info(self, cluster=False):
        """
        Returns list of strings with
        info about this modifiers list
        """

        ui_t = []
        if cluster is False:
            ui_t.append("----------------------------------")
            ui_t.append("    Info about modifiers list    ")

        # Check if modifiers_list at least kinda working
        if not isinstance(self._modifiers_list, list):
            ui_t.append("Modifiers list is not working correctly")
            return ui_t

        # Info about cluster types
        if self.has_clusters():
            ui_t.append(f"ModifierCluster count is {self.get_list_length()}")

            # Info about all clusters.
            for mod in self.get_full_list():
                ui_t.append(" ")
                if isinstance(mod, ModifiersListUtils):
                    ui_t.append(f"Cluster {mod}")
                    ui_t += mod._modifiers_list_info(True)

        # Info about actual modifiers
        else:
            if len(self._modifiers_list) > 0:
                for mod in self.get_list():
                    ui_t.append(f"{mod}")
            else:
                ui_t.append("This list is 0 modifiers long")
        ui_t.append("----------------------------------")
        ui_t.append(" ")
        return ui_t
