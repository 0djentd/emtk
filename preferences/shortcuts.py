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


# import re
import json
import string
# import math


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
                          max_iterations=500):

    shortcut = {}
    k = ['shift', 'ctrl', 'alt']
    for x in k:
        shortcut.update({x: False})
    letter_index = 0
    letter_index, shortcut['letter']\
        = _get_next_letter_in_shortcut_name(
                    shortcut_name, letter_index)

    checking = True
    iteration = 0
    while checking:
        if iteration > max_iterations:
            raise ValueError

        # If this loop breaks, iteration failed.
        for x, y in zip(already_existing_shortcuts.keys(),
                        already_existing_shortcuts.values()):

            # Check if shortcut already exists.
            if x == shortcut_name:
                raise ValueError

            # Props that are same.
            same = []
            for z, c in zip(shortcut.keys(),
                            shortcut.values()):
                if z in y.keys()\
                        and y[z] == shortcut[z]:
                    same.append(z)

            # If at least one element is different, return shortcut.
            if len(same) <= 4:
                return {shortcut_name: shortcut}

            # Filter elements
            e = []
            for x in same:
                if isinstance(shortcut[x], bool)\
                        and shortcut[x] is False:
                    e.append(x)

            # If all boolean elements already True, change letter.
            if len(e) == 0:
                letter_index, shortcut['letter']\
                        = _get_next_letter_in_shortcut_name(
                                shortcut['letter'], letter_index)
                for z in k:
                    shortcut.update({x: False})
                break

            # Change first changeable element
            shortcut[e[0]] = True

            # Start new iteratiion
            iteration += 1

    shortcut['sens'] = 0.005
    shortcut = {shortcut_name: shortcut}
    for x in shortcut:
        for y in shortcut[x]:
            if not isinstance(y, str):
                raise TypeError
            if not isinstance(shortcut[x][y], str)\
                    and not isinstance(shortcut[x][y], bool)\
                    and not isinstance(shortcut[x][y], int)\
                    and not isinstance(shortcut[x][y], float):
                raise TypeError
    return shortcut


def _get_next_letter_in_shortcut_name(shortcut_name, index):
    """
    Example:
    >>> get_next_letter_in_shortcut_name('angle_limit', 4)
    <<< L
    """
    if (index + 1) > len(shortcut_name):
        raise ValueError
    for i, x in enumerate(shortcut_name[index:-1]):
        if x in string.ascii_letters:
            new_index = i
            letter = x.upper()
            break
    new_index = index + new_index
    return new_index, letter
# }}}
