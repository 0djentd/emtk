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
import functools

from .utils import check_if_removed, check_obj_ref

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _check_obj_type(self, obj):
    if obj in self._ModifiersList_obj:
        return obj
    if isinstance(obj, int):
        return self._ModifiersList_obj[obj]
    if isinstance(obj, str):
        for x in self._ModifiersList_obj:
            if x.name == obj:
                return x
        raise ValueError(
                f'No object with name "{obj}" in {self._ModifiersList_obj}')
    raise TypeError(
            f'Expected cluster, modifier, int or str, got {type(obj)}.')


def _check_if_obj_is_list(self, obj):
    if type(obj) is not list:
        return _check_obj_type(self, obj)
    obj_2 = []
    for x in obj:
        obj_2.append(_check_obj_type(self, x))
    return obj_2


def unwrap_obj_ref_seq(func):
    """
    Unwrapper for ModifiersList methods parameters.
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
        obj = _check_if_obj_is_list(self, obj)
        return func(self, obj, *args, **kwargs)
    return wrapper_unwrap_obj_ref


def unwrap_obj_ref(func):
    """
    Unwrapper for ModifiersList methods parameters.
    Supported obj types: ClusterTrait, int, str.

    Check if obj is in the modifiers list;
    If obj is index of modifiers list element;
    If obj is 'name' attribute of modifiers list element;

    Provides modifiers list element to function.
    """

    def wrapper_unwrap_obj_ref(self, obj, *args, **kwargs):
        obj = _check_obj_type(self, obj)
        return func(self, obj, *args, **kwargs)
    return wrapper_unwrap_obj_ref


class Selection():
    def __init__(self, modifiers_list):
        # ModifiersList subclass object.
        self._ModifiersList_obj = modifiers_list

        # Active modifier
        self._mod = None
        # Selection
        self._additional_selection = []
        # Cluster or modifier that selection started from
        self._cluster_to_select_from = None

    @property
    def active(self):
        if self._mod is None:
            if len(self._ModifiersList_obj) != 0:
                return self._ModifiersList_obj[0]
        return self._mod

    @active.setter
    @unwrap_obj_ref
    def active(self, mod):
        if isinstance(mod, int):
            self._mod = self._ModifiersList_obj[mod]
        else:
            if mod not in self._ModifiersList_obj:
                raise ValueError
            self._mod = mod

    @property
    def _selection(self):
        return self.get_selection()

    @_selection.setter
    def _selection(self, val):
        self.clear()
        self.add(val)

    @unwrap_obj_ref_seq
    def add(self, val):
        self._additional_selection.extend(val)

    @unwrap_obj_ref
    def start(self, obj):
        self._cluster_to_select_from = self._ModifiersList_obj.index(obj)

    def stop(self):
        """Stop selecting selecting clusters."""
        self.add(self._ModifiersList_obj[
            self._cluster_to_select_from:self.active]
        self._cluster_to_select_from = None

    def get(self):
        if self._cluster_to_select_from is not None:
        
        return []

    def clear(self):
        self._selected_clusters = None

    def pop(self):
        selection = self.get()
        self.clear()
        return selection

    def __getitem__(self, index):
        return self._selection.__getitem__(index)

    # TODO: modify decorator for this?
    def __setitem__(self, index, val):
        return self._selection.__setitem__(index, val)

    def __delitem__(self, index):
        return self._selection.__delitem__(index)

    @unwrap_obj_ref
    def __contains__(self, obj):
        return obj in self._selection

    def __iter__(self):
        return iter(self._selection)

    def __next__(self):
        return next(self._selection)

    def __len__(self):
        return self._selection.__len__()
