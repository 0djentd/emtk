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


class ActiveModifierTrait():
    """
    Active modifier for ModifiersList.
    """

    # Active_modifier doesnt neccessary means that this is an actual modifier.
    # It mostly used for clusters, as every modifier is a cluster anyways.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Active modifier
        self._mod = None

    # ===============
    # Active modifier
    # ===============
    # TODO: this methods should be renamed
    @property
    def active_modifier(self):
        return self.active_modifiers_get()

    @active_modifier.setter
    def active_modifier(self, mod):
        return self.active_modifier_set(mod)

    def active_modifier_get(self):
        """Returns active modifier"""
        return self._mod

    def active_modifier_get_type(self):
        """Returns active modifier type"""
        return self.modifier_get_type(self._mod)

    def active_modifier_get_name(self):
        """Returns active modifier type"""
        return self.modifier_get_name(self._mod)

    def active_modifier_set_by_index(self, i):
        """Set active modifier by index"""
        self._mod = self._modifiers_list[i]

    def active_modifier_set(self, modifier):
        """
        Set active modifier by reference
        Returns True if successfully found modifier.
        Returns False if modifier is not in list.
        """
        if modifier in self.get_list():
            self._mod = modifier
            return True
        return False
