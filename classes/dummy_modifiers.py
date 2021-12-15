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


class DummyBlenderModifier():
    """
    Object that represents modifier.
    """

    def __init__(self, m_name, m_type, *args, **kwargs):
        if not isinstance(m_name, str)\
                or not isinstance(m_type, str):
            raise TypeError

        super().__init__(*args, **kwargs)

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


class DummyBlenderObj():
    """
    Object that can be used to replace Blender obj in ModifiersList for
    unittests, debug, dry modifiers stack editing, storing changes to
    modifiers list and other purposes.
    """

    def __init__(self, modifiers=None, *args, **kwargs):

        if modifiers is None:
            modifiers = []

        if not isinstance(modifiers, list):
            raise TypeError

        for x in modifiers:
            if not isinstance(x, DummyBlenderModifier):
                raise TypeError

        super().__init__(*args, **kwargs)

        self.modifiers = modifiers

    def modifier_add(self, m_name, m_type):
        """
        Creates new modifier.
        """
        i = 0

        if not isinstance(m_name, str):
            raise TypeError

        if not isinstance(m_type, str):
            raise TypeError

        for x in self.modifiers:
            if m_name == x.name:
                i += 1
        m_name_2 = m_name + f'{i}'

        mod = DummyBlenderModifier(m_name_2, m_type)
        self.modifiers.append(mod)
        return mod

    def modifier_remove(self, m_name):
        """
        Removes modifier.
        """
        if not isinstance(m_name, str):
            raise TypeError

        mod_to_remove = None
        for x in self.modifiers:
            if x.name == m_name:
                mod_to_remove = x
        if mod_to_remove is not None:
            self.modifiers.remove(mod_to_remove)
            return True
        return False

    def modifier_move_up(self, m_name=None):
        """
        Moves modifier up.
        Returns True or False.
        """
        if not isinstance(m_name, str):
            raise TypeError

        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == m_name:
                mod = x

        if mod is None:
            return False

        i = self.modifiers.index(mod)
        if i < len(self.modifiers) - 1:
            x = self.modifiers.pop(mod)
            self.modifiers.insert(i+1, x)
        return True

    def modifier_move_down(self, m_name=None):
        """
        Moves modifier down.
        Returns True or False.
        """
        if not isinstance(m_name, str):
            raise TypeError

        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == m_name:
                mod = x

        if mod is None:
            return False

        i = self.modifiers.index(mod)
        if i > 0:
            x = self.modifiers.pop(mod)
            self.modifiers.insert(i-1, x)
        return True
