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

import logging
# import functools

# from .utils import check_if_removed, check_obj_ref

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Decorators {{{
def _check_obj_type(self, obj, allow_no_value):
    if obj in self._modifiers_list:
        return obj
    if isinstance(obj, int):
        return self._modifiers_list[obj]
    if isinstance(obj, str):
        for x in self._modifiers_list:
            if x.name == obj:
                return x
        raise ValueError(
                f'No object with name "{obj}" in {self._modifiers_list}')
    if obj is None and allow_no_value:
        return None
    raise TypeError(
            f'Expected cluster, modifier, int or str, got {type(obj)}.')


def _check_if_obj_is_list(self, obj, allow_no_value):
    if type(obj) is not list:
        return _check_obj_type(self, obj, allow_no_value)
    obj_2 = []
    for x in obj:
        obj_2.append(_check_obj_type(self, x, allow_no_value))
    return obj_2


def unwrap_obj_ref_seq(func, allow_no_value=False):
    """Unwrapper for ModifiersList methods parameters.

    Supported obj types: ClusterTrait, int, str.
    Also works with lists of variables of this types.

    Creates [obj], if type(obj) is not list.

    For each element in obj:
        Check if it is in the modifiers list;
        If it is index of modifiers list element;
        If it is 'name' attribute of modifiers list element;

    Provides new list with modifiers list elements references.
    """
    def wrapper_unwrap_obj_ref_seq(self, obj, *args, **kwargs):
        obj = _check_if_obj_is_list(self, obj, allow_no_value)
        return func(self, obj, *args, **kwargs)
    return wrapper_unwrap_obj_ref_seq


def unwrap_obj_ref_seq_allow_no_value(func):
    """Same as unwrap_obj_ref_seq, but allows obj to be None."""
    return unwrap_obj_ref_seq(func, allow_no_value=True)


def unwrap_obj_ref(func, allow_no_value=False):
    """Unwrapper for ModifiersList methods parameters.

    Supported obj types: ClusterTrait, int, str.
    Check if obj is in the modifiers list;
    If obj is index of modifiers list element;
    If obj is 'name' attribute of modifiers list element;

    Provides modifiers list element to function.
    """

    def wrapper_unwrap_obj_ref(self, obj, *args, **kwargs):
        obj = _check_obj_type(self, obj, allow_no_value)
        return func(self, obj, *args, **kwargs)
    return wrapper_unwrap_obj_ref


def unwrap_obj_ref_allow_no_value(func):
    """Same as unwrap_obj_ref, but allows obj to be None."""
    return unwrap_obj_ref(func, allow_no_value=True)
# }}}


class Selection():
    """
    Selection is sum of two lists:
    clusters between 'cluster_to_select_from' and active cluster
    (methods that operate on it is 'start' and 'stop'), and
    'additional selection', that is not being affected
    by active cluster ('add', 'remove')
    """
    def __init__(self, modifiers_list):
        # ModifiersList subclass object.
        self._modifiers_list = modifiers_list
        # Selection
        self._additional_selection = []
        # Cluster or modifier that selection started from
        self._cluster_to_select_from = None

    @property
    def main_selection(self):
        return self.get()

    @property
    def additional_selection(self):
        return self._additional_selection[:]

    @additional_selection.setter
    def additional_selection(self, val):
        self._additional_selection = []
        self.add(val)

    @unwrap_obj_ref_allow_no_value
    def start(self, obj):
        if obj is None:
            obj = self._modifiers_list.active
        self._cluster_to_select_from = obj

    def stop(self):
        """Stop selecting clusters using active cluster
        and add clusters to 'additional selection' list."""
        self.add(self.get(add_additional_selection=False))
        self._cluster_to_select_from = None

    def get(self, *, add_main_selection=True,
            add_additional_selection=True, add_active=False):
        """Get list of all selected clusters."""
        result = []
        m = self._modifiers_list
        if add_main_selection:
            if self._cluster_to_select_from is not None:
                start_index = m.index(self._cluster_to_select_from)
                end_index = m.index(m.active)
                if start_index < end_index:
                    result.extend(m[start_index:end_index+1])
                else:
                    result.extend(m[end_index:start_index+1])
        if add_additional_selection:
            result.extend(self._additional_selection)
        if add_active:
            if m.active not in result:
                result.append(m.active)
        return result

    @unwrap_obj_ref_seq
    def add(self, val):
        """Add cluster/clusters to additional selection."""
        for x in val:
            selection = self._additional_selection
            if x in selection:
                continue
            selection.append(x)

    @unwrap_obj_ref_seq_allow_no_value
    def remove(self, obj):
        """Remove cluster from additional selection."""
        if obj is None:
            self._additional_selection.pop(-1)
        for x in obj:
            self._additional_selection.remove(x)

    def clear(self):
        """Stop selecting and clear 'additional selection' list."""
        self.stop()
        self._selected_clusters = []
