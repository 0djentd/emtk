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
        self.angle_limit = 0.123
        self.segments = 3

    def __str__(self):
        return f'{self.name}, {self.type}'

    def __repr__(self):
        return self.__str__()

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
    """Object that can be used to replace Blender obj in ModifiersList for
    unittests, debug, dry modifiers stack editing and other purposes.
    """

    def __init__(self, modifiers=None, *args,
                 saved_clusters_state=None, **kwargs):

        if modifiers is None:
            modifiers = []

        if not isinstance(modifiers, list):
            raise TypeError

        for x in modifiers:
            if not isinstance(x, DummyBlenderModifier):
                raise TypeError

        self.modifiers = modifiers
        self._check_modifiers_names()
        self.props = {}

        if saved_clusters_state is not None:
            if not isinstance(saved_clusters_state, dict):
                raise TypeError
            self.props.update(saved_clusters_state)

        super().__init__(*args, **kwargs)

    def modifier_add(self, m_name, m_type):
        """Creates new modifier."""
        if not isinstance(m_name, str):
            raise TypeError
        if not isinstance(m_type, str):
            raise TypeError

        i = 0
        for x in self.modifiers:
            if m_name in x.name:
                i += 1
        m_name_2 = m_name + f'{i}'
        mod = DummyBlenderModifier(m_name_2, m_type)
        self.modifiers.append(mod)
        self._check_modifiers_names()
        return mod

    def _check_modifiers_names(self):
        """Throws error if there is duplicate names in modifiers"""
        y = []
        for x in self.modifiers:
            for name in y:
                if x.name == name:
                    raise ValueError
            y.append(x.name)

    def modifier_remove(self, modifier=None):
        """Removes modifier."""

        if not isinstance(modifier, str):
            raise TypeError

        mod_to_remove = None
        for x in self.modifiers:
            if x.name == modifier:
                mod_to_remove = x
        if mod_to_remove is not None:
            self.modifiers.remove(mod_to_remove)
            return True
        self._check_modifiers_names()
        raise ValueError

    def modifier_apply(self, modifier=None):
        """Applies modifier."""
        return self.modifier_remove(modifier)

    def modifier_move_down(self, modifier=None):
        """Moves modifier up.

        Returns True or False.
        """
        if not isinstance(modifier, str):
            raise TypeError
        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == modifier:
                mod = x

        if mod is None:
            raise ValueError

        i = self.modifiers.index(mod)
        if i < len(self.modifiers) - 1:
            x = self.modifiers.pop(self.modifiers.index(mod))
            self.modifiers.insert(i+1, x)
        self._check_modifiers_names()
        return True

    def modifier_move_up(self, modifier=None):
        """Moves modifier down.

        Returns True or False.
        """
        if not isinstance(modifier, str):
            raise TypeError
        if len(self.modifiers) < 2:
            return False

        mod = None
        for x in self.modifiers:
            if x.name == modifier:
                mod = x

        if mod is None:
            raise ValueError

        i = self.modifiers.index(mod)
        if i > 0:
            x = self.modifiers.pop(self.modifiers.index(mod))
            self.modifiers.insert(i-1, x)
        self._check_modifiers_names()
        return True


# class DummyBlenderPrefsObj():
#     """Dummy blender addon prefs object."""
#     def __init__(self):
#         self.cluster_types = '[]'


# class DummyBlenderPrefs():
#     """Dummy blender prefs object."""
#     def __init__(self):
#         self.addons = {'emtk': {DummyBlenderPrefsObj()}}
