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

from ..controller.actions import (
                                  ClustersAction,
                                  ClustersCommand,
                                  ClustersBatchCommand,
                                  )

from ..controller.answers import (
                                  ClusterActionAnswer,
                                  ActionDefaultRemove,
                                  ActionDefaultApply,
                                  ActionDefaultMove,
                                  ActionDefaultDeconstuct
                                  )

from .utils import check_if_removed, check_obj_ref
from .selection import Selection, unwrap_obj_ref

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_NO_EMPTY_LISTS = False

"""
=============================
MODIFIERS LIST METHODS NAMING
=============================

ModifiersCluster is a Cluster without clusters in it.

ClustersLayer, or Layer, is a Cluster too, but without modifiers.

All methods that have 'actual_modifier' in their name
return actual Blender modifiers references, and assume that arguments
use Blender modifiers instead of clusters.

All methods that have 'cluster' in their name return Clusters or Layers.

All methods that have 'recursive' in their name recursively calls cluster
methods of same functional as called method.

All methods that have 'loop' in their name iterate 'around' list, used
for creating tools that have some kind of UI. They work on single
layer, unless specified.

Almost all methods that dont have anything of above in their name
doesnt have anything to do with modifiers and operate on list in general.
"""


class ModifiersList():
    """Base class for cluster_trait and first_layer_clusters_list."""

    def __init__(self, obj=None, *args, no_obj=None,  # {{{
                 no_default_actions=False,
                 **kwargs):
        super().__init__()

        if not no_obj:
            if obj is None:
                raise ValueError

        self._object = obj
        self._data = []
        self._actions = {}
        self._mod = None
        self._selection = Selection(self)
        if not no_default_actions:
            default_actions = [ActionDefaultRemove, ActionDefaultApply,
                               ActionDefaultMove, ActionDefaultDeconstuct]
            for x in default_actions:
                self.add_action_answer(x(self))
    # }}}

    # Selection {{{
    @property
    @check_if_removed
    def active(self):
        return self._mod

    @active.setter
    @check_if_removed
    @unwrap_obj_ref
    def active(self, mod):
        self._mod = mod

    @property
    @check_if_removed
    def selection(self):
        return self._selection

    @check_if_removed
    def get_selection(self):
        return self.selection.get()
    # }}}

    # List methods {{{
    @check_if_removed
    def __getitem__(self, index):
        return self._data.__getitem__(index)

    @check_if_removed
    def __setitem__(self, index, val):
        return self._data.__setitem__(index, val)

    @check_if_removed
    def __delitem__(self, index):
        return self._data.__delitem__(index)

    @check_if_removed
    def __contains__(self, obj):
        return obj in self._data

    @check_if_removed
    def __iter__(self):
        return iter(self._data)

    @check_if_removed
    def __next__(self):
        return next(self._data)

    @check_if_removed
    def __len__(self):
        return self._data.__len__()

    @check_if_removed
    def index(self, obj):
        return self._data.index(obj)

    def items(self):
        return self._data

    def names(self):
        result = []
        for x in self._data:
            result.append(x.name)
        return result

    def types(self):
        result = []
        for x in self._data:
            result.append(x.type)
        return result

    # remove(obj) is defined in 'Clusters actions' section.

    # TODO:
    # add(obj) is defined in 'Clusters actions' section.

    # }}}

    # This method is different in clusters.
    def _check_if_cluster_removed(self):
        if len(self) == 0 and _NO_EMPTY_LISTS:
            raise ValueError

    # This method is different in clusters list.
    def has_clusters(self):
        return False

    def serialize(obj):
        raise NotImplementedError

    # Clusters actions {{{
    """
    This methods create a new command and pass it to
    interpreter. This will automatically add
    necessary commands to it, creating a ClustersBatchCommand,
    solve it and send to interpreters.

    Use ClustersCommand and controller.solve(command)
    instead if you want to check if
    there is anything wrong with solved command.
    """
    @check_if_removed
    @check_obj_ref
    def remove(self, obj=None):
        """
        Removes cluster or modifier from this list.
        If cluster is None, removes cluster itself.
        """
        logger.info(f'Removing {obj} on layer {self}')

        if obj is None:
            obj = self
        x = ClustersAction('REMOVE', obj)
        x = ClustersCommand(x,
                            affect_clusters=True,
                            affect_modifiers=True,
                            dry_clusters=False,
                            dry_modifiers=False,
                            )
        self._controller.do(x)

    @check_if_removed
    @check_obj_ref
    def apply(self, obj=None):
        """
        Removes cluster or modifier from this list.
        If cluster is None, applies cluster itself.
        """
        logger.info(f'Applying {obj} on layer {self}')

        if obj is None:
            obj = self
        x = ClustersAction('APPLY', obj)
        x = ClustersCommand(x,
                            affect_clusters=True,
                            affect_modifiers=True,
                            dry_clusters=False,
                            dry_modifiers=False,
                            )
        self._controller.do(x)

    def move_up(self, obj):
        """Moves cluster or modifier in this list.
        Returns True, if successfully moved cluster or modifier.
        """
        return self._move(obj, direction='UP')

    def move_down(self, obj):
        """Moves cluster or modifier in this list.
        Returns True, if successfully moved cluster or modifier.
        """
        return self._move(obj, direction='DOWN')

    @check_if_removed
    @check_obj_ref
    def _move(self, obj, direction, allow_deconstruct=False):
        """Moves cluster or modifier in this list.
        If allow_deconstruct is true, skips check
        for position in list.

        Returns None or False.
        """
        logger.info(f'Moving {obj} on layer {self}')
        logger.debug(f'Direction is {direction} allow_deconstruct={self}')
        if len(self._data) < 2:
            logger.info('Not enough modifiers.')
            return False

        i = self._data.index(obj)

        if direction == 'UP':
            if i == 0 and not allow_deconstruct:
                logger.info('Already first in the list.')
                return False
            cluster_to_move_through = self._data[i-1]
            direction_2 = 'DOWN'
        elif direction == 'DOWN':
            if i == len(self._data) - 1\
                    and not allow_deconstruct:
                logger.info('Already last in the list.')
                return False
            cluster_to_move_through = self._data[i+1]
            direction_2 = 'UP'
        else:
            raise ValueError(
                    "Direction should be either 'UP' or 'DOWN'")

        # This only used when moving actual modifiers with dry=true.
        length = len(
                cluster_to_move_through.get_full_actual_modifiers_list())

        x = ClustersAction('MOVE', obj)
        x_2 = ClustersAction('MOVE', cluster_to_move_through)
        x_2.dry = True

        x.props['direction'] = direction
        x_2.props['direction'] = direction_2

        x.props['length'] = length
        x_2.props['length'] = length

        x = ClustersCommand(x,
                            affect_clusters=True,
                            affect_modifiers=True,
                            dry_clusters=True,
                            dry_modifiers=False,
                            )

        x_2 = ClustersCommand(x_2,
                              affect_clusters=True,
                              affect_modifiers=True,
                              dry_clusters=True,
                              dry_modifiers=True,
                              )

        if direction == 'UP':
            x.reverse_by_layer = False
            x_2.reverse_by_layer = True
        else:
            x.reverse_by_layer = True
            x_2.reverse_by_layer = False

        self._controller.do([x, x_2])
        return True

    @check_if_removed
    @check_obj_ref
    def move_to_index(self, obj, i):
        """Moves cluster to index. Returns True if moved modifier."""
        # TODO: not tested
        if i < len(self._data):
            m_i = self.index(obj)
            d_i = i - m_i
            x = 0
            if d_i > 0:
                while x <= d_i:
                    self.move_up(obj)
                    x += 1
                return True
            elif d_i < 0:
                while x >= d_i:
                    self.move_up(obj)
                    x -= 1
                return True

    @check_if_removed
    def ask(self, action):
        self._actions[action.verb].ask(action)

    # TODO: remove this
    @check_if_removed
    def do(self, action):
        """
        Do batch command, simple command or action on this
        modifiers list elements.
        """
        if not isinstance(action, list):
            action = [action]

        # Check all elements first
        for x in action:
            self._check_controller_action(x)

        for x in action:
            if isinstance(x, ClustersBatchCommand):
                raise TypeError
                self.do_batch(x)
            elif isinstance(x, ClustersCommand):
                raise TypeError
                self.do_command(x)
            elif isinstance(x, ClustersAction):
                self.do_action(x)

    @check_if_removed
    def do_batch(self, batch):
        for x in batch.commands:
            self.do_command(x)

    @check_if_removed
    def do_command(self, command):
        for x in command.actions:
            self.do_action(x)

    @check_if_removed
    def do_action(self, action):
        logger.debug(f'Cluster {self}, action is {action}')
        if action.subject not in self._data:
            layer = self.get_cluster_or_layer(action.subject)
            layer.do_action(action)
        else:
            self._actions[action.verb].do(action)

    def _check_controller_action(self, x):
        """
        This methods checks if all action.subjects can be
        found in this list or its clusters.
        """
        if isinstance(x, ClustersBatchCommand):
            self._check_batch(x)
        elif isinstance(x, ClustersCommand):
            self._check_command(x)
        elif isinstance(x, ClustersAction):
            self._check_action(x)
        else:
            raise TypeError

    @check_if_removed
    def _check_batch(self, batch):
        if not isinstance(batch, ClustersBatchCommand):
            raise TypeError
        for x in batch.commands:
            self._check_command(x)

    @check_if_removed
    def _check_command(self, command):
        if not isinstance(command, ClustersCommand):
            raise TypeError
        for x in command.actions:
            self._check_action(x)

    @check_if_removed
    def _check_action(self, action):
        if not isinstance(action, ClustersAction):
            raise TypeError
        for x in self.get_all_clusters_and_modifiers():
            if x is action.subject:
                return
        raise ValueError

    @check_if_removed
    def add_action_answer(self, action_answer):
        """
        Adds new ClusterActionAnswer to this cluster.
        Replaces existing one with same action_answer.action_type.
        """
        if not isinstance(action_answer, ClusterActionAnswer):
            raise TypeError
        self._actions.update({action_answer.action_type: action_answer})
    # }}}

    # Modifiers list utils. {{{
    # ==============================================
    # This methods work on _modifiers_list
    # This means that they dont differ simple or nested clusters and modifiers
    # ==============================================

    # This methods are different in clusters list.
    def get_full_actual_modifiers_list(self):
        return self._data

    def get_actual_full_actual_modifiers_list(self):
        return self._data

    def get_full_list(self):
        return self._data

    def get_all_clusters_and_modifiers(self):
        return self._data

    @check_if_removed
    def get_list_in_range_not_inclusive(self, mod1, mod2):
        """Returns list of objects between two objects. Not inclusive."""

        if (mod1 is None) or (mod2 is None):
            raise TypeError

        e = []
        x = self.index(mod1)
        y = self.index(mod2)

        if x > y:
            if (x-y) < 2:
                return e
            y += 1
            x -= 1
        elif x < y:
            if (y-x) < 2:
                return e
            y -= 1
            x += 1

        return self._data[x:y+1]

    @check_if_removed
    def get_list_in_range_inclusive(self, mod1, mod2):
        """
        Returns list of objects between two objects. Inclusive.
        If two references of same object, returns list
        with one object.
        """
        mod1 = self._check_cluster_or_modifier(mod1)
        mod2 = self._check_cluster_or_modifier(mod2)

        if (mod1 is None) or (mod2 is None):
            raise TypeError

        x = self.index(mod1)
        y = self.index(mod2)

        if x > y:
            return self._data[y:x+1]
        elif x < y:
            return self._data[x:y+1]
        elif x == y:
            e = []
            e.append(self._data[x])
            return e
    # }}}

    # Iterating over list {{{
    def previous(self, mod, m_type=None, loop=True):
        return self.find_next_or_previous(mod, m_type, 'UP', loop)

    def next(self, mod, m_type=None, loop=True):
        return self.find_next_or_previous(mod, m_type, 'DOWN', loop)

    # @check_obj_ref
    @check_if_removed
    def iterate(self, mod, direction, m_type=None, loop=True):
        """Iterate over clusters or modifiers starting from mod.

        Direction should be a str in {'UP', 'DOWN'}
        If m_type is specified, only use objects with obj.m_type.
        If loop is False, will stop at the end or beginning of the list.

        Returns object from this list.
        Can return None, if m_type is not None.
        Can return None, if loop is False.
        """
        if type(mod) is int:
            i = mod
        else:
            mod = self._check_cluster_or_modifier(mod)
            i = self._data.index(mod)

        # Any type.
        if m_type is None:
            if direction == 'UP':
                if not loop and i == 0:
                    return self._data[0]
                return self._data[i - 1]
            elif direction == 'DOWN':
                if not loop and i == len(self._data) - 1:
                    return self._data[-1]
                if i + 1 > len(self._data) - 1:
                    return self._data[i + 1 - len(
                        self._data)]
                return self._data[i + 1]
            else:
                raise ValueError

        # Specified type.
        # This will return None if there is no modifier or cluster
        # with specified type.
        else:
            result = None
            for x in range(len(self._data) + 1):
                if x == 0:
                    continue
                # TODO: does it works tho
                if not loop:
                    if i + x == len(self._data) + 1:
                        return result
                if direction == 'UP':
                    e = self._data[i - x]
                elif direction == 'DOWN':
                    if i + x > len(self._data) - 1:
                        e = self._data[i + x - len(
                            self._data)]
                    else:
                        e = self._data[i + x]
                if e.type == m_type:
                    if loop:
                        return e
                    result = e
    # }}}
