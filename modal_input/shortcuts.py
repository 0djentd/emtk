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

import json
import string
import functools
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_LOG = logger.isEnabledFor(logging.DEBUG)

_MAPPING = ('letter', 'shift', 'ctrl', 'alt')


def refresh_cache(func):
    """Decorator for methods that require cache refresh."""
    def wrapper_refresh_cache(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if _LOG:
            logger.debug(f'Refreshing lru cache for {func}')
        self.cache_clear()
        return result
    return wrapper_refresh_cache


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
        self.cache_clear()

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, val):
        if type(val) is not bool:
            raise TypeError
        self._shift = val
        self.cache_clear()

    @property
    def ctrl(self):
        return self._ctrl

    @ctrl.setter
    def ctrl(self, val):
        if type(val) is not bool:
            raise TypeError
        self._ctrl = val
        self.cache_clear()

    @property
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, val):
        if type(val) is not bool:
            raise TypeError
        self._alt = val
        self.cache_clear()
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
        self.cache_clear()

    @property
    def description(self):
        """Shortcut description. Used in UI."""
        return self._description

    @description.setter
    def description(self, d):
        if d is None:
            self._description = 'No description'
        elif type(d) is str:
            self._description = d
        else:
            raise TypeError(f'Expected None or str, got {type(d)}')
    # }}}

    def compare(self, obj):
        """Compare with bpy.types.event or another ModalShortcut."""
        return self.compare_mappings(obj.letter,
                                     obj.shift,
                                     obj.ctrl,
                                     obj.alt)

    @functools.lru_cache
    def compare_mappings(self, letter, shift, ctrl, alt):
        if letter != self.letter:
            return
        if shift != self.shift:
            return
        if ctrl != self.ctrl:
            return
        if alt != self.alt:
            return
        return self

    def __str__(self):
        line = self.value + ': '
        line = line + self.letter
        for x in _MAPPING[1:]:
            if getattr(self, x):
                line = line + f' + {x}'
        return line

    def cache_clear(self):
        self.compare_mappings.cache_clear()

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
        self.cache_clear()

    @property
    def shortcuts(self):
        return self._shortcuts[:]

    @refresh_cache
    @shortcuts.setter
    def shortcuts(self, shortcuts):
        for x in shortcuts:
            if not isinstance(x, ModalShortcut):
                raise TypeError
        if len(find_duplicates(shortcuts)) != 0:
            raise ValueError
        self._shortcuts = shortcuts
    # }}}

    @refresh_cache
    def update_shortcut(self, shortcut):
        index = self.remove_shortcut(shortcut)
        if index is not None:
            self._shortcuts.insert(index, shortcut)
        self._shortcuts.append(shortcut)

    def remove_shortcut(self, shortcut):
        if not isinstance(shortcut, ModalShortcut):
            raise TypeError

        index = None

        remove = []
        for i, x in enumerate(self._shortcuts):
            if x == shortcut:
                index = i
                remove.append(x)

        for x in remove:
            self._shortcuts.remove(x)

        d = self.find_shortcut_by_mapping(
                                          shortcut.letter,
                                          shortcut.shift,
                                          shortcut.ctrl,
                                          shortcut.alt,
                                          )
        if d:
            index = self._shortcuts.index(d)
            self._shortcuts.remove(d)

        d = self.find_shortcut_by_value(
                                        shortcut.value,
                                        )
        if d:
            index = self._shortcuts.index(d)
            self._shortcuts.remove(d)

        if index is not None:
            self.cache_clear()
        return index

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
            y = x.compare_mappings(letter, shift, ctrl, alt)
            if y:
                return y

    def find_shortcut_by_event(self, event):
        return self.find_shortcut_by_mapping(event.type,
                                             event.shift,
                                             event.ctrl,
                                             event.alt)

    @functools.lru_cache
    def search_by_name(self, shortcut_name):
        result = []
        for x in self.shortcuts:
            if shortcut_name in x.value:
                result.append(x)
        return result

    def __str__(self):
        line = f'Group {self.name}, {len(self.shortcuts)} shortcuts.'
        return line

    def cache_clear(self):
        self.search_by_name.cache_clear()
        self.find_shortcut_by_mapping.cache_clear()
        self.find_shortcut_by_value.cache_clear()

    def serialize(self):
        serialized_shortcuts = []
        for x in self.shortcuts:
            serialized_shortcuts.append(x.serialize())
        result = {'name': self.name,
                  'shortcuts': serialized_shortcuts}
        return json.dumps(result)
# }}}


class ModalShortcutsCache():  # {{{
    """Object that represents modal shortcuts groups."""

    def __init__(self, shortcuts_groups=None):
        if type(shortcuts_groups) is str:
            self.shortcuts_groups = deserialize_shortcuts_cache(
                    shortcuts_groups)
        elif type(shortcuts_groups) is list:
            self.shortcuts_groups = shortcuts_groups
        elif shortcuts_groups is None:
            self.shortcuts_groups = []
        else:
            raise TypeError

    @property
    def shortcuts_groups(self):
        return self._shortcuts_groups

    @refresh_cache
    @shortcuts_groups.setter
    def shortcuts_groups(self, val):
        if type(val) is not list:
            raise TypeError
        for x in val:
            if not isinstance(x, ModalShortcutsGroup):
                raise TypeError
        self._shortcuts_groups = val

    @refresh_cache
    def update_shortcuts_group(self, group):
        if not isinstance(group, ModalShortcutsGroup):
            raise TypeError
        self.remove_shortcuts_group(group)
        self._shortcuts_groups.append(group)

    @refresh_cache
    def remove_shortcuts_group(self, group):
        if type(group) is int:
            self._shortcuts_groups.pop(group)
        elif type(group) is str:
            self._shortcuts_groups.remove(
                    self.find_shortcuts_group_by_name(group))
        elif isinstance(group, ModalShortcutsGroup)\
                and group in self._shortcuts_groups:
            self._shortcuts_groups.remove(group)
        else:
            raise TypeError

    @functools.lru_cache
    def find_shortcuts_group_by_name(self, name):
        for x in self.shortcuts_groups:
            if name == x.name:
                return x

    @functools.lru_cache
    def search_by_name(self, shortcuts_group_name, shortcut_name):
        result = []
        for x in self.shortcuts_groups:
            if shortcuts_group_name not in x.name:
                continue

            shortcuts = x.search_by_name(shortcut_name)
            if len(shortcuts) != 0:
                result.append(x)
        return result

    def serialize(self):
        serialized_shortcuts_groups = []
        for x in self.shortcuts_groups:
            serialized_shortcuts_groups.append(x.serialize())
        return json.dumps(serialized_shortcuts_groups)

    def cache_clear(self):
        self.search_by_name.cache_clear()
        self.find_shortcuts_group_by_name.cache_clear()
# }}}


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


# @functools.lru_cache
def find_duplicates(shortcuts):
    duplicates = []
    for x in shortcuts:
        for y in shortcuts:
            if x.compare(y) and y not in duplicates:
                duplicates.append(x)
    return duplicates


# @functools.lru_cache
def fix_duplicates(shortcuts):
    shortcuts = shortcuts[:]
    for x in find_duplicates(shortcuts):
        shortcuts.remove(x)
    return shortcuts


def _str_repr_event(event):
    line = event.type
    for x in _MAPPING[1:]:
        if getattr(event, x):
            line = line + f' + {x}'
    return line
# }}}


# Deserialization {{{
@functools.lru_cache
def deserialize_shortcuts_cache(serialized_shortcuts_groups):
    if type(serialized_shortcuts_groups) is not str:
        raise TypeError(type(serialized_shortcuts_groups))

    serialized_shortcuts_groups = json.loads(serialized_shortcuts_groups)
    if type(serialized_shortcuts_groups) is not list:
        raise TypeError

    shortcuts_groups = []
    for x in serialized_shortcuts_groups:
        shortcuts_groups.append(deserialize_shortcuts_group(x))
    return shortcuts_groups


@functools.lru_cache
def deserialize_shortcuts_group(serialized_shortcuts_group):
    if type(serialized_shortcuts_group) is not str:
        raise TypeError(type(serialized_shortcuts_group))

    serialized_shortcuts_group_2 = json.loads(serialized_shortcuts_group)
    if type(serialized_shortcuts_group_2) is not dict:
        raise TypeError
    for x in {'name', 'shortcuts'}:
        if x not in serialized_shortcuts_group_2:
            raise ValueError

    shortcuts = []
    for x in serialized_shortcuts_group_2['shortcuts']:
        shortcuts.append(deserialize_shortcut(x))
    return ModalShortcutsGroup(serialized_shortcuts_group_2['name'],
                               shortcuts)


@functools.lru_cache
def deserialize_shortcut(serialized_shortcut):
    if type(serialized_shortcut) is not str:
        raise TypeError(type(serialized_shortcut))

    s = json.loads(serialized_shortcut)
    return ModalShortcut(s['value'],
                         s['letter'],
                         s['shift'],
                         s['ctrl'],
                         s['alt'])
# }}}


def generate_new_shortcut(shortcut_value: str,  # {{{
                          already_existing_shortcuts: list = [],
                          max_iterations: int = 512,
                          ignore_duplicates=False) -> dict:
    """Generates new unique modal operator shortcut object."""

    if type(shortcut_value) is str:
        if len(shortcut_value) == 0:
            raise TypeError
    else:
        raise TypeError
    if isinstance(already_existing_shortcuts, list):
        for x in already_existing_shortcuts:
            if not isinstance(x, ModalShortcut):
                raise TypeError
    else:
        raise TypeError
    if type(max_iterations) is not int:
        raise TypeError
    if type(ignore_duplicates) is not bool:
        raise TypeError

    shortcut_elements = {'value': shortcut_value}
    k = ['shift', 'ctrl', 'alt']
    for x in k:
        shortcut_elements.update({x: False})
    letter_index = None
    letter_index, shortcut_elements['letter']\
        = _get_next_letter_in_shortcut_name(
                    shortcut_elements['value'], letter_index)

    if len(already_existing_shortcuts) == 0:
        return ModalShortcut(shortcut_elements['value'],
                             shortcut_elements['letter'],
                             shortcut_elements['shift'],
                             shortcut_elements['ctrl'],
                             shortcut_elements['alt'],
                             )

    iteration = 0
    checking = True
    while checking:
        if iteration > max_iterations:
            raise ValueError

        reparse = False

        # If this loop breaks, parse iteration failed.
        for x in already_existing_shortcuts:

            # Check if shortcut already exists.
            if x.value == shortcut_elements['value']:
                if not ignore_duplicates:
                    raise ValueError(
                            f'{shortcut_elements["value"]} already exists.')
                else:
                    continue

            # Props that are same.
            same = []
            for z in _MAPPING:
                if getattr(x, z) == shortcut_elements[z]:
                    same.append(z)

            # If at least one element is different, check next.
            if len(same) < 4:
                continue

            # Filter elements.
            e = []
            for z in same:
                if isinstance(shortcut_elements[z], bool)\
                        and shortcut_elements[z] is False:
                    e.append(z)

            # If all boolean elements already True, change letter.
            if len(e) == 0:
                letter_index, shortcut_elements['letter']\
                        = _get_next_letter_in_shortcut_name(
                                shortcut_elements['value'], letter_index)
                for z in k:
                    shortcut_elements.update({z: False})
                reparse = True
                break
            else:
                # Change first changeable element
                shortcut_elements[e[0]] = True
                reparse = True
                break

        # Start new iteratiion
        if reparse:
            iteration += 1
        else:
            checking = False

    return ModalShortcut(shortcut_elements['value'],
                         shortcut_elements['letter'],
                         shortcut_elements['shift'],
                         shortcut_elements['ctrl'],
                         shortcut_elements['alt'])


@functools.lru_cache
def _get_next_letter_in_shortcut_name(shortcut_value, index):
    """
    Example 1:
    >>> get_next_letter_in_shortcut_name('angle_limit', 4)
    <<< 6, L

    Example 2:
    >>> get_next_letter_in_shortcut_name('angle_limit', None)
    <<< 0, A
    """
    if not isinstance(shortcut_value, str):
        raise TypeError

    if index is None:
        for i, x in enumerate(shortcut_value):
            if x in string.ascii_letters:
                new_index = i
                letter = x.upper()
                break

    elif type(index) is int:
        if index + 1 >= len(shortcut_value):
            raise ValueError
        for i, x in enumerate(shortcut_value[index:-1]):
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
