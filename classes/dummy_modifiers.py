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


class DummyModifier():
    """
    Object that represents modifier.
    """

    def __init__(self, m_name, m_type):
        self.name = m_name
        self.m_type = m_type

    @property
    def type(self):
        return self.m_type

    @property
    def name(self):
        return self.m_name

    @name.setter
    def name(self, m_name):
        if isinstance(m_name, str):
            self.m_name = m_name
        else:
            raise TypeError


class DummyModifiers():
    """
    Object that can be used to replace modifiers stack in ModifiersList.
    """
    modifiers = []

    def __init__(self, modifiers):
        self.modifiers = modifiers

    def modifier_move_up(self, modifier=None):
        """
        Moves modifier up.
        Returns True or False.
        """
        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == modifier:
                mod = x

        if mod is None:
            return False

        i = self.modifiers.index(mod)
        if i < len(self.modifiers) - 1:
            x = self.modifiers.pop(mod)
            self.modifiers.insert(i+1, x)
        return True

    def modifier_move_down(self, modifier=None):
        """
        Moves modifier down.
        Returns True or False.
        """
        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == modifier:
                mod = x

        if mod is None:
            return False

        i = self.modifiers.index(mod)
        if i > 0:
            x = self.modifiers.pop(mod)
            self.modifiers.insert(i-1, x)
        return True
