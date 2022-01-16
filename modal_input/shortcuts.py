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

_MAPPING = ('letter', 'shift', 'ctrl', 'alt')

"""This module provides classes for modal operator shortcuts,
shortcuts groups, cache and some utility functions like serialization,
deserialization, converters for event type and search.

Some of methods are cached.
Cache is being cleared every time shortcuts are changed.
"""

# TODO: create base class for shortcuts cache and shortcuts group.
# TODO: check if cache actually working as expected.

# TODO:
# rename 'letter' to 'type'.
# rename 'value' to 'shortcut_id'.
# add 'value' as str in {'PRESS', 'RELEASE'}.
# add 'active' as bool.
# rename all props except 'shortcut_id' to 'event_{prop_name}'
# forbid assigning shortcuts props twice.


# Decorators {{{
def convert_mapping(func):
    """Converts object (expecting ModalShortcut
    or bpy.types.event) to mapping.
    """
    def wrapper_convert_mapping(self, obj, *args, **kwargs):
        if isinstance(obj, ModalShortcut):
            return func(self, obj.letter, obj.shift,
                        obj.ctrl, obj.alt, *args, **kwargs)
        else:
            return func(self, obj, *args, **kwargs)
    return wrapper_convert_mapping


def unwrap_str_to_obj(func):
    """Check if obj is str, find item with item.value == obj."""
    def wrapper_unwrap_str_to_obj(self, group, *args, **kwargs):
        if type(group) is str:
            group = self[group]
        return func(self, group, *args, **kwargs)
    return wrapper_unwrap_str_to_obj
# }}}


# Cache {{{
class CachedObject():
    def __init__(self, *args, **kwargs):
        self._cache_variables = set()

    def __cache_clear(self):
        for x in self._cache_variables:
            setattr(self, x, {})


def method_cache(func):
    """Creates cache for instance method. Instance should
    implement 'cache_clear' method and invoke it
    after attributes are changed.
    """
    def wrapper_method_cache(self, *args, **kwargs):
        if len(kwargs) != 0:
            raise TypeError
        cache_name = '_' + func.__name__ + '_cache'
        try:
            cache = getattr(self, cache_name)
        except AttributeError:
            cache = {}
            try:
                self._cache_variables.add(cache_name)
            except AttributeError:
                setattr(self, '_cache_variables', set(cache_name))
            setattr(self, cache_name, cache)

        try:
            result = cache[(args)]
        except KeyError:
            result = func(self, *args, **kwargs)
            cache.update({tuple(args): result})
        if len(cache) > 100:
            raise ValueError
        return result
    return wrapper_method_cache


def refresh_cache(func):
    """Decorator for methods that require cache refresh afterwards."""
    def wrapper_refresh_cache(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.cache_clear()
        return result
    return wrapper_refresh_cache


def check_refresh(func):
    """Refresh cache before using method if any of objects require it."""
    def wrapper_check_refresh(self, *args, **kwargs):
        refresh = False
        for x in self._data:
            if x.tag_refresh:
                refresh = True
                x.tag_refresh = False
        if refresh:
            self.cache_clear()
        return func(self, *args, **kwargs)
    return wrapper_check_refresh
# }}}


class HashedList():  # {{{
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if type(key) is str:
            result = self.find_by_value(key)
            if result:
                return result
            else:
                raise KeyError
        else:
            TypeError(f'Expected str, got {type(key)}')

    @unwrap_str_to_obj
    def __contains__(self, obj):
        return obj in self._data

    def __iter__(self):
        return iter(self._data)

    def __next__(self):
        return next(self._data)

    def __len__(self):
        return self._data.__len__()

    @refresh_cache
    @unwrap_str_to_obj
    def remove(self, obj):
        return self._data.remove(obj)

# }}}


class ModalShortcut(CachedObject):  # {{{
    """This object represents keyboard shortcut for modal operators."""

    def __init__(self, value, letter, shift, ctrl, alt, description=None):
        super().__init__()
        self._value = None
        self.tag_refresh = False
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
        """Letter to use in mapping."""
        return self._letter

    @letter.setter
    @refresh_cache
    def letter(self, val):
        c = _check_letter_type(val)
        if c:
            raise TypeError(c)
        self._letter = val
        self.cache_clear()

    @property
    def shift(self):
        """Shift value to use in mapping."""
        return self._shift

    @shift.setter
    @refresh_cache
    def shift(self, val):
        if type(val) is not bool:
            raise TypeError
        self._shift = val
        self.cache_clear()

    @property
    def ctrl(self):
        """Ctrl value to use in mapping."""
        return self._ctrl

    @ctrl.setter
    @refresh_cache
    def ctrl(self, val):
        if type(val) is not bool:
            raise TypeError
        self._ctrl = val
        self.cache_clear()

    @property
    def alt(self):
        """Alt value to use in mapping."""
        return self._alt

    @alt.setter
    @refresh_cache
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
    @refresh_cache
    def value(self, value):
        if type(value) is str:
            if len(value) == 0:
                raise ValueError
            if self._value is not None:
                raise ValueError
        else:
            raise TypeError
        self._value = value

    @property
    def description(self):
        """Shortcut description. Used in UI."""
        return self._description

    @description.setter
    @refresh_cache
    def description(self, d):
        if d is None:
            self._description = 'No shortcut description'
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

    @method_cache
    def compare_mappings(self, letter, shift, ctrl, alt):
        if letter != self.letter:
            return
        if shift is not self.shift:
            return
        if ctrl is not self.ctrl:
            return
        if alt is not self.alt:
            return
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        line = self.value + ': '
        line = line + self.letter
        for x in _MAPPING[1:]:
            if getattr(self, x):
                line = line + f' + {x}'
        return line

    def cache_clear(self):
        self._CachedObject__cache_clear()
        self.tag_refresh = True

    @method_cache
    def serialize(self):
        result = {'value': self.value,
                  'description': self.description}
        for x in _MAPPING:
            result.update({x: getattr(self, x)})
        return json.dumps(result)
# }}}


class ModalShortcutsGroup(CachedObject, HashedList):  # {{{
    """This object represents keyboard shortcut group for modal operators."""

    def __init__(self, value, shortcuts=None):
        super().__init__()
        if shortcuts is None:
            shortcuts = []
        self._value = None
        self.shortcuts = shortcuts
        self.value = value
        self.tag_refresh = False

    # Properties {{{
    @property
    def value(self):
        return self._value

    @value.setter
    @refresh_cache
    def value(self, val):
        if type(val) is str:
            if len(val) == 0:
                raise ValueError
            if self._value is not None:
                raise ValueError
        else:
            raise TypeError
        self._value = val

    @property
    def shortcuts(self):
        return self._data[:]

    @shortcuts.setter
    @refresh_cache
    def shortcuts(self, shortcuts):
        for x in shortcuts:
            if not isinstance(x, ModalShortcut):
                raise TypeError
        duplicates = find_duplicates(shortcuts)
        if len(duplicates) != 0:
            logger.error('Removing duplicates.')
            shortcuts = fix_duplicates(shortcuts)
        self._data = shortcuts
    # }}}

    # List methods {{{
    @refresh_cache
    def update(self, shortcut):
        e = self.find_by_value(shortcut.value)
        m = self.find_by_mapping(shortcut.letter,
                                 shortcut.shift,
                                 shortcut.ctrl,
                                 shortcut.alt)
        if m not in {None, e}:
            raise ValueError('Shortcut with this mapping already exists.')
        if e is not None:
            i = self._data.index(e)
            self._data.remove(e)
            self._data.insert(i, shortcut)
        else:
            self._data.append(shortcut)

    @refresh_cache
    def add(self, shortcut, index=None):
        if self.find_by_value(shortcut):
            raise ValueError('Shortcut already exists.')
        if self.find_by_mapping(shortcut):
            raise ValueError('Shortcut with this mapping already exists.')
        if index is None:
            self._data.append(shortcut)
        else:
            self._data.insert(index, shortcut)
    # }}}

    @check_refresh
    @method_cache
    def find_by_value(self, value):
        if type(value) is not str:
            raise TypeError(f'Expected str, got {type(value)}')
        for x in self:
            if x.value == value:
                return x

    @check_refresh
    @convert_mapping
    @method_cache
    def find_by_mapping(self, letter, shift, ctrl, alt):
        for x in self:
            if x.compare_mappings(letter, shift, ctrl, alt):
                return x

    def find_by_event(self, event):
        return self.find_by_mapping(event.type,
                                    event.shift,
                                    event.ctrl,
                                    event.alt)

    @check_refresh
    @method_cache
    def search_by_value(self, value):
        result = []
        for x in self:
            if value in x.value:
                result.append(x)
        return result

    @method_cache
    def __str__(self):
        line = f'Group {self.name}, {len(self.shortcuts)} shortcuts.'
        return line

    def cache_clear(self):
        self._CachedObject__cache_clear()
        self.tag_refresh = True

    @method_cache
    def serialize(self):
        serialized_shortcuts = []
        for x in self:
            serialized_shortcuts.append(x.serialize())
        result = {'name': self.value,
                  'shortcuts': serialized_shortcuts}
        return json.dumps(result)
# }}}


class ModalShortcutsCache(CachedObject, HashedList):  # {{{
    """Object that represents modal shortcuts groups."""

    def __init__(self, groups=None):
        super().__init__()
        self._data = None
        if type(groups) is str:
            self.shortcuts_groups = deserialize_shortcuts_cache(
                    groups)
        elif type(groups) is list:
            self.shortcuts_groups = groups
        elif groups is None:
            self.shortcuts_groups = []
        else:
            raise TypeError(
                    'Expected str, list of ModalShortcutsGroups or None.')

    # List methods {{{
    @refresh_cache
    def add(self, group):
        if not isinstance(group, ModalShortcutsGroup):
            raise TypeError
        if self.find_by_value(group.value):
            raise ValueError
        self._data.append(group)

    @refresh_cache
    def update(self, group):
        if not isinstance(group, ModalShortcutsGroup):
            raise TypeError
        e = self.find_by_value(group.value)
        if e:
            self._data.remove(e)
        self._data.append(group)
    # }}}

    @property
    def shortcuts_groups(self):
        return self._data

    @shortcuts_groups.setter
    @refresh_cache
    def shortcuts_groups(self, val):
        if type(val) is not list:
            raise TypeError
        for x in val:
            if not isinstance(x, ModalShortcutsGroup):
                raise TypeError
        self._data = val

    @method_cache
    def find_by_value(self, value):
        value = shortcuts_groups_name_format(value)
        for x in self.shortcuts_groups:
            if value == x.value:
                return x

    @check_refresh
    @method_cache
    def search_by_value(self, shortcuts_group_value, shortcut_value):
        shortcuts_group_value = shortcuts_groups_name_format(
                shortcuts_group_value)
        result = []
        for x in self.shortcuts_groups:
            if shortcuts_group_value not in x.value:
                continue
            shortcuts = x.search_by_value(shortcut_value)
            if len(shortcuts) != 0:
                result.append(x)
        return result

    @method_cache
    def serialize(self):
        obj = []
        for x in self.shortcuts_groups:
            obj.append(x.serialize())
        return json.dumps(obj)

    def cache_clear(self):
        self._CachedObject__cache_clear()
# }}}


# Utils {{{
@functools.lru_cache
def _check_letter_type(val):
    if type(val) is str:
        if len(val) == 1:
            if val not in string.ascii_uppercase:
                val = val.upper()
                if val not in string.ascii_lowercase:
                    return 'Expected letter in [A-Z], got {val}'
        else:
            return f'Expected str with length == 1, got {val}'
    else:
        return f'Expected str, got {type(val)}'


def find_duplicates(shortcuts):
    duplicates = []
    for x in shortcuts:
        if x in duplicates:
            continue
        for y in shortcuts:
            if y in duplicates or y is x:
                continue
            if x.compare(y):
                duplicates.append(x)
    return duplicates


def fix_duplicates(shortcuts):
    shortcuts = shortcuts[:]
    for x in find_duplicates(shortcuts):
        shortcuts.remove(x)
    return shortcuts


@functools.lru_cache
def shortcuts_groups_name_format(value):
    if type(value) is not str:
        value = str(value)
    value.strip()
    value.upper()
    value.replace(' ', '_')
    return value


def _str_repr_event(event):
    line = event.type
    for x in _MAPPING[1:]:
        if getattr(event, x):
            line = line + f' + {x}'
    return line
# }}}


# Deserialization {{{
@functools.lru_cache
def deserialize_shortcuts_cache(obj):
    if type(obj) is not str:
        raise TypeError(type(obj))

    obj = json.loads(obj)
    if type(obj) is not list:
        raise TypeError

    shortcuts_groups = []
    for x in obj:
        shortcuts_groups.append(deserialize_shortcuts_group(x))
    return shortcuts_groups


@functools.lru_cache
def deserialize_shortcuts_group(obj):
    if type(obj) is not str:
        raise TypeError(type(obj))

    obj_2 = json.loads(obj)
    if type(obj_2) is not dict:
        raise TypeError
    for x in {'name', 'shortcuts'}:
        if x not in obj_2:
            raise ValueError

    shortcuts = []
    for x in obj_2['shortcuts']:
        shortcuts.append(deserialize_shortcut(x))
    return ModalShortcutsGroup(obj_2['name'],
                               shortcuts)


@functools.lru_cache
def deserialize_shortcut(obj):
    if type(obj) is not str:
        raise TypeError(type(obj))

    s = json.loads(obj)
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
                             shortcut_elements['alt'])

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
