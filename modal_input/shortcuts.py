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

# import re
import json
import string
# import math
import functools

_MAPPING = ('letter', 'shift', 'ctrl', 'alt')


class ModalShortcut():  # {{{
    """This object represents keyboard shortcut for modal operators."""

    def __init__(self, value, letter, shift, ctrl, alt, description=None):
        self.value = value
        self.letter = letter
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt
        self.description = description

    # Properties {{{
    # Mapping {{{
    @property
    def letter(self):
        return self._letter

    @letter.setter
    def letter(self, val):
        c = _check_letter_type(val)
        if c:
            raise TypeError(c)
        self._letter = val
        self.clear_cache()

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, val):
        if type(val) is not bool:
            raise TypeError
        self._shift = val
        self.clear_cache()

    @property
    def ctrl(self):
        return self._ctrl

    @ctrl.setter
    def ctrl(self, val):
        if type(val) is not bool:
            raise TypeError
        self._ctrl = val
        self.clear_cache()

    @property
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, val):
        if type(val) is not bool:
            raise TypeError
        self._alt = val
        self.clear_cache()
    # }}}

    @property
    def value(self):
        """Shortcut value."""
        return self._value

    @value.setter
    def value(self, value):
        if type(value) is str:
            if len(value) == 0:
                raise ValueError
        else:
            raise TypeError
        self._value = value
        self.clear_cache()

    @property
    def description(self):
        """Shortcut description. Used in UI."""
        return self._description

    @description.setter
    def description(self, d):
        if type(d) is not str:
            raise TypeError
        self._description = d
    # }}}

    def compare(self, obj):
        """Compare with bpy.types.event or another ModalShortcut."""
        return self.__compare_mappings(obj.letter,
                                       obj.shift,
                                       obj.ctrl,
                                       obj.alt)

    def _compare_mappings(self, letter, shift, ctrl, alt):
        if letter != self.letter:
            return
        if shift != self.letter:
            return
        if ctrl != self.letter:
            return
        if alt != self.alt:
            return
        return self.value

    def __str__(self):
        line = self.letter
        for x in _MAPPING:
            if getattr(self, x):
                line = line + ' + {x}'
        line = line + ': ' + self.value
        return line

    def clear_cache(self):
        self._compare_mappings.clear_cache()

    def serialize(self):
        result = {'value': self.value,
                  'description': self.description}
        for x in _MAPPING:
            result.update({x: getattr(self, x)})
        return json.dumps(result)
# }}}


class ModalShortcutsGroup():  # {{{
    """This object represents keyboard shortcut group for modal operators."""

    def __init__(self, name, shortcuts=None):
        if shortcuts is None:
            shortcuts = []
        self.shortcuts = shortcuts
        self.name = name

    # Properties {{{
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if type(val) is str:
            if len(val) == 0:
                raise ValueError
        else:
            raise TypeError
        self._name = val
        self.clear_cache()

    @property
    def shortcuts(self):
        return self._shortcuts[:]

    @shortcuts.setter
    def shortcuts(self, shortcuts):
        for x in shortcuts:
            if not isinstance(x, ModalShortcut):
                raise TypeError
        if self.fix_duplicates(shortcuts):
            raise ValueError
        self._shortcuts = shortcuts
        self.clear_cache()
    # }}}

    def update_shortcut(self, shortcut):
        self.remove_shortcut(shortcut)
        self._shortcuts.add(shortcut)
        self.clear_cache()

    def remove_shortcut(self, shortcut):
        if not isinstance(shortcut, ModalShortcut):
            raise TypeError

        result = False

        remove = []
        for x in self._shortcuts:
            if x == shortcut:
                remove.append(x)
        for x in remove:
            self._shortcuts.remove(x)
            result = True

        d = self.find_shortcut_by_mapping(
                                          shortcut.letter,
                                          shortcut.shift,
                                          shortcut.ctrl,
                                          shortcut.alt,
                                          )
        if d:
            self._shortcuts.remove(d)
            result = True

        d = self.find_shortcut_by_value(
                                        shortcut.value,
                                        )
        if d:
            self._shortcuts.remove(d)
            result = True

        if result:
            self.clear_cache()
        return result

    @functools.lru_cache
    def find_shortcut_by_value(self, value):
        if type(value) is not str:
            raise TypeError
        for x in self.shortcuts:
            if x.value == value:
                return x

    @functools.lru_cache
    def find_shortcut_by_mapping(self, letter, shift, ctrl, alt):
        c = _check_letter_type(letter)
        if c:
            raise TypeError(c)

        m = [shift, ctrl, alt]
        for x in m:
            if type(x) is not bool:
                raise TypeError(f'Expected bool, got {type(x)}')

        for x in self.shortcuts:
            y = x.compare(letter, shift, ctrl, alt)
            if y:
                return y

    def __str__(self):
        line = f'Group {self.name}, {len(self.shortcuts)} shortcuts.'
        return line

    def clear_cache(self):
        fix_duplicates.clear_cache()
        find_duplicates.clear_cache()
        self.find_shortcut_by_mapping.clear_cache()
        self.find_shortcut_by_value.clear_cache()

    def serialize(self):
        serialized_shortcuts = []
        for x in self.shortcuts:
            serialized_shortcuts.append(x.serialize())
        result = {'name': self.name,
                  'shortcuts': serialized_shortcuts}
        return json.dumps(result)
# }}}


class ModalShortcutsCache():
    """Object that represents modal shortcuts groups."""

    def __init__(self, serialized_shortcuts_groups):
        if serialized_shortcuts_groups is '':
            serialized_shortcuts_groups = '[]'
        self.shortcuts_groups = deserialized_shortcuts_cache(
                serialized_shortcuts_groups)

    @property
    def shortcuts_groups(self):
        return self._shortcuts_groups

    @shortcuts_groups.setter
    def shortcuts_groups(self, val):
        if type(val) is not list:
            raise TypeError
        for x in val:
            if not isinstance(ModalShortcutsGroup):
                raise TypeError
        self._shortcuts_groups = val

    def serialize(self):
        serialized_shortcuts_groups = []
        for x in self.shortcuts_groups:
            serialized_shortcuts_groups.append(x.serialize())
        result = json.dumps(serialized_shortcuts_groups)
        return result

# Utils {{{
@functools.lru_cache
def _check_letter_type(val):
    if type(val) is str:
        if len(val) == 1:
            if val not in string.ascii_lowercase:
                val = val.upper()
        else:
            return f'Expected str with length == 1, got {val}'
    else:
        return f'Expected str, got {type(val)}'


@functools.lru_cache
def deserialize_shortcuts_cache(serialized_shortcuts_groups):
    if type(serialized_shortcuts_groups) is not str:
        raise TypeError
    deserialized_shortcuts_groups = json.loads(serialized_shortcuts_groups)

    if type(deserialized_shortcuts_groups) is list:
        for group in deserialized_shortcuts_groups:
            check_deserialized_shortcuts_group(group)
    else:
        raise TypeError

    groups = []
    for x in deserialized_shortcuts_cache:
        shortcuts = []
        for y in x['shortcuts']:
            elements = {}
            for k, v in y.items():
                elements.update({k: v})
            # probably dont work
            shortcuts.append(ModalShortcut(elements))
        name = x['name']
        groups.append(ModalShortcutsGroup(name, shortcuts))
    return groups

@functools.lru_cache
def check_deserialized_shortcuts_group(group: dict):
    if type(group) is dict:
        if type(group['name']) not str:
            raise TypeError
        if type(group['shortcuts']) is list:
            for shortcut in shortcuts:
                if type(shortcut) is dict:
                    if 'value' not in shortcut:
                        raise TypeError
                else:
                    raise TypeError
        else:
            raise TypeError
    else:
        raise TypeError


@functools.lru_cache
def find_duplicates(shortcuts):
    duplicates = []
    for x in shortcuts:
        for y in shortcuts:
            if x.compare(y) and y not in duplicates:
                duplicates.append(x)
    return duplicates


@functools.lru_cache
def fix_duplicates(shortcuts):
    shortcuts = shortcuts[:]
    for x in find_duplicates(shortcuts):
        shortcuts.remove(x)
    return shortcuts
# }}}


# Serialization {{{
def serialize_kbs(shortcuts: dict) -> str:
    """Serialize json dict with shortcuts."""
    check_shortcuts_formatting(shortcuts)

    kbs = json.dumps(shortcuts)

    if not isinstance(kbs, str):
        raise TypeError
    if deserialize_kbs(kbs) != shortcuts:
        raise ValueError
    return kbs


def deserialize_kbs(kbs: str) -> dict:
    """Deserialize json string with shortcuts."""
    if not isinstance(kbs, str):
        raise TypeError
    shortcuts = json.loads(kbs)
    check_shortcuts_formatting(shortcuts)
    return shortcuts
# }}}


# Checks {{{
def check_shortcuts_formatting(shortcuts: dict) -> bool:
    if not isinstance(shortcuts, dict):
        raise TypeError(f'Expected dict, got {type(shortcuts)}')
    for x in shortcuts:
        check_shortcuts_group_formatting(shortcuts[x])


def check_shortcuts_group_formatting(shortcuts_group: dict) -> bool:
    if not isinstance(shortcuts_group, dict):
        raise TypeError(f'Expected dict, got {type(shortcuts_group)}')
    for y in shortcuts_group.values():
        check_shortcut_formatting(y)


def check_shortcut_formatting(shortcut):
    if not isinstance(shortcut, dict):
        raise TypeError(f'Expected dict, got {type(shortcut)}')
    e = False
    for x in shortcut:
        if isinstance(shortcut[x], dict):
            e = x
    if e is not False:
        shortcut = shortcut[e]
    if len(shortcut) < 4:
        raise ValueError
    g = {'letter', 'shift', 'ctrl', 'alt'}
    for x in g:
        if x not in shortcut:
            raise ValueError(f'Expected {x}, got {shortcut}')
    for x, y in zip(shortcut.keys(), shortcut.values()):
        check_shortcut_element_formatting(x, y)
    return True


def check_shortcut_element_formatting(element_name, element):
    if element_name == 'letter':
        if not isinstance(element, str):
            raise TypeError
        if len(element) != 1:
            raise ValueError
        if element not in string.ascii_uppercase:
            if element in string.ascii_lowercase:
                element = element.upper()
            else:
                raise ValueError
    elif element_name in {'shift', 'alt', 'ctrl'}:
        if not isinstance(element, bool):
            raise TypeError
    elif element_name == 'sens':
        if not isinstance(element, float):
            raise TypeError

    if not isinstance(element, str)\
            and not isinstance(element, bool)\
            and not isinstance(element, int)\
            and not isinstance(element, float):
        raise TypeError(f'Expected str, bool, int or float, got {element}')
# }}}


# Filtering {{{
def filter_shortcuts_group_by_str(
        shortcuts: dict, s: str) -> dict:
    """Filters shortcuts in a shortcuts group by name.

    Returns new shortcuts group.
    """
    result = {}
    for x, z in zip(
            shortcuts.keys(),
            shortcuts.values()):
        if s in x:
            result.update({x: z})
    return result


def search_modal_operators_shortcuts(
        shortcuts: dict, shortcut_name: str) -> dict:
    """Filters shortcuts groups dict by shortcut name.

    Returns new shortcuts groups dict.
    """
    if not isinstance(shortcut_name, str):
        raise TypeError

    result = {}
    for x, y in zip(shortcuts.keys(), shortcuts.values()):
        f = filter_shortcuts_group_by_str(y, shortcut_name)
        if len(f) > 0:
            result.update({x: f})
    check_shortcuts_formatting(result)
    return result
# }}}


# Utils {{{
def generate_new_shortcut(
                          shortcut_name: str,
                          already_existing_shortcuts: dict,
                          max_iterations=512) -> dict:
    """Generates new unique modal operator shortcut dict.

    Example:
    >>> d = {'array': {'letter': 'a', 'shift': True,\
    ...                'ctrl': False, 'alt': False}}
    >>> generate_new_shortcut('angle', d, max_iterations=10)
    <<< {'angle': {'letter': 'a', 'shift': True, 'ctrl': True, 'alt': False}}
    """

    if not isinstance(shortcut_name, str):
        raise TypeError
    if not isinstance(already_existing_shortcuts, dict):
        raise TypeError
    for x, y in zip(already_existing_shortcuts.keys(),
                    already_existing_shortcuts.values()):
        if not isinstance(x, str):
            raise TypeError
        if not isinstance(y, dict):
            raise TypeError
        k = ['letter', 'shift', 'ctrl', 'alt']
        for z in k:
            if z not in y:
                raise ValueError
            if type(y[z]) is not str\
                    and type(y[z]) is not bool\
                    and type(y[z]) is not float:
                raise TypeError
    shortcut = {}
    k = ['shift', 'ctrl', 'alt']
    for x in k:
        shortcut.update({x: False})
    letter_index = None
    letter_index, shortcut['letter']\
        = _get_next_letter_in_shortcut_name(
                    shortcut_name, letter_index)

    if len(already_existing_shortcuts) == 0:
        return {shortcut_name: shortcut}

    iteration = 0
    checking = True
    while checking:
        if iteration > max_iterations:
            raise ValueError

        # If this loop breaks, loop iteration failed.
        reparse = False

        for x, y in zip(already_existing_shortcuts.keys(),
                        already_existing_shortcuts.values()):

            # Check if shortcut already exists.
            if x == shortcut_name:
                raise ValueError(f'{shortcut_name} already exists.')

            # Props that are same.
            same = []
            for z in shortcut:
                if z in y.keys()\
                        and y[z] == shortcut[z]:
                    same.append(z)

            # If at least one element is different, check next.
            if len(same) < 4:
                continue

            # Filter elements.
            e = []
            for z in same:
                if isinstance(shortcut[z], bool)\
                        and shortcut[z] is False:
                    e.append(z)

            # If all boolean elements already True, change letter.
            if len(e) == 0:
                letter_index, shortcut['letter']\
                        = _get_next_letter_in_shortcut_name(
                                shortcut_name, letter_index)
                for z in k:
                    shortcut.update({z: False})
                reparse = True
                break
            else:
                # Change first changeable element
                shortcut[e[0]] = True
                reparse = True
                break

        if reparse:
            # Start new iteratiion
            iteration += 1
        else:
            checking = False

    shortcut = {shortcut_name: shortcut}
    check_shortcut_formatting(shortcut)
    for x, y in zip(already_existing_shortcuts.keys(),
                    already_existing_shortcuts.values()):
        if shortcut_name == x:
            if shortcut[shortcut_name] == y:
                raise ValueError(shortcut, x, y)
    return shortcut


def _get_next_letter_in_shortcut_name(shortcut_name, index):
    """
    Example 1:
    >>> get_next_letter_in_shortcut_name('angle_limit', 4)
    <<< 6, L

    Example 2:
    >>> get_next_letter_in_shortcut_name('angle_limit', None)
    <<< 0, A
    """
    if not isinstance(shortcut_name, str):
        raise TypeError

    if index is None:
        for i, x in enumerate(shortcut_name):
            if x in string.ascii_letters:
                new_index = i
                letter = x.upper()
                break
    elif isinstance(index, int):
        if (index + 1) >= len(shortcut_name):
            raise ValueError
        for i, x in enumerate(shortcut_name[index:-1]):
            if i == 0:
                continue
            if x in string.ascii_letters:
                new_index = i
                letter = x.upper()
                break
        new_index = index + new_index
    else:
        raise TypeError
    return new_index, letter
# }}}
