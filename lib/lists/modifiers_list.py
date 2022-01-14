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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

    def __init__(self, obj=None, *args, no_obj=None,
                 no_default_actions=False,
                 **kwargs):
        super().__init__()

        if not no_obj:
            if obj is None:
                raise ValueError

        self._object = obj
        self.__DUMMY_MODIFIERS = False
        self._modifiers_list = []
        self._actions = {}
        if not no_default_actions:
            default_actions = [ActionDefaultRemove, ActionDefaultApply,
                               ActionDefaultMove, ActionDefaultDeconstuct]
            for x in default_actions:
                self.add_action_answer(x(self))

    def __len__(self):
        return len(self._modifiers_list)

    # This method is different in clusters.
    def _check_if_cluster_removed(self):
        pass

    # This method is different in clusters.
    def has_clusters(self):
        return False

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
        if len(self._modifiers_list) < 2:
            logger.info('Not enough modifiers.')
            return False

        i = self._modifiers_list.index(obj)

        if direction == 'UP':
            if i == 0 and not allow_deconstruct:
                logger.info('Already first in the list.')
                return False
            cluster_to_move_through = self._modifiers_list[i-1]
            direction_2 = 'DOWN'
        elif direction == 'DOWN':
            if i == len(self._modifiers_list) - 1\
                    and not allow_deconstruct:
                logger.info('Already last in the list.')
                return False
            cluster_to_move_through = self._modifiers_list[i+1]
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
        if i < len(self._modifiers_list):
            m_i = self.get_index(obj)
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
        if action.subject not in self._modifiers_list:
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

    @check_if_removed
    def get_list(self):
        """Returns list of objects"""
        return self._modifiers_list

    # This methods are different in clusters list.
    def get_full_actual_modifiers_list(self):
        return self.get_list()

    def get_actual_full_actual_modifiers_list(self):
        return self.get_list()

    def get_full_list(self):
        return self.get_list()

    def get_all_clusters_and_modifiers(self):
        return self.get_list()

    @check_if_removed
    def get_list_in_range_not_inclusive(self, mod1, mod2):
        """Returns list of objects between two objects. Not inclusive."""

        if (mod1 is None) or (mod2 is None):
            raise TypeError

        e = []
        x = self.get_index(mod1)
        y = self.get_index(mod2)

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

        return self._modifiers_list[x:y+1]

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

        x = self.get_index(mod1)
        y = self.get_index(mod2)

        if x > y:
            return self._modifiers_list[y:x+1]
        elif x < y:
            return self._modifiers_list[x:y+1]
        elif x == y:
            e = []
            e.append(self._modifiers_list[x])
            return e

    @check_if_removed
    def get_list_length(self):
        """Returns length of list of objects."""
        return len(self._modifiers_list)

    @check_if_removed
    def get_list_by_type(self, m_type):
        """Returns list of m_type objects."""
        y = []
        for x in self._modifiers_list:
            if x.type == m_type:
                y.append(x)
        return y

    @check_if_removed
    def get_by_index(self, i):
        """Returns object by index."""
        return self._modifiers_list[i]

    @check_if_removed
    def get_index(self, mod):
        """Returns index of object."""
        return self._modifiers_list.index(mod)

    @check_if_removed
    def get_first(self):
        """Returns first object."""
        return self._modifiers_list[0]

    @check_if_removed
    def get_last(self):
        """Returns last object."""
        return self._modifiers_list[-1]

    # ===============
    # INFO ABOUT LIST
    # ===============
    @check_if_removed
    def has_modifier(self, mod):
        """Returns True, if found object in list."""
        if mod in self.get_list():
            return True
        return False

    # TODO: replace this with 'has obj with attr'
    @check_if_removed
    def has_modifier_by_type(self, m_type):
        """Returns True if found any mod of m_type."""
        for mod in self._modifiers_list:
            if mod.type == m_type:
                return True
        return False

    @check_if_removed
    def has_modifier_by_name(self, m_name):
        """Returns True if found any objects with m_name."""
        for mod in self._modifiers_list:
            if mod.name == m_name:
                return True
        return False
    # }}}

    # Finding modifiers {{{
    # ------------------------------------
    # 'find' methods that looking for modifiers relatively
    # to modifiers.
    # ------------------------------------

    @check_if_removed
    def find_previous(self, mod, m_type):
        return self.find_previous_modifier(mod, m_type)

    @check_if_removed
    def find_previous_modifier(self, mod, m_type):
        """
        Returns index of previous
        modifier of m_type type wrt mod
        Returns None if not found any
        """

        # Offset for iterating over list
        x = 1
        m_list_len = len(self._modifiers_list) 
        while x < m_list_len + 1:

            # y = index of modifier that should be returned
            # created on every iteration
            y = self.get_index(mod) - x
            if y < 0:
                return None
            elif self.get_by_index(y).type == m_type:
                return self.get_by_index(y)
            x += 1

    @check_if_removed
    def find_next(self, mod, m_type):
        return self.find_next_modifier(mod, m_type)

    @check_if_removed
    def find_next_modifier(self, mod, m_type):
        """
        Returns index of next modifier of m_type type wrt mod.
        Returns None if not found any.
        """

        # Offset for iterating over list
        x = 1
        m_list_len = len(self._modifiers_list)
        while x < m_list_len + 1:
            y = self.get_index(mod) + x
            if y >= m_list_len:
                return None
            elif self._modifiers_list[y].type == m_type:
                return self.get_by_index(y)
            x += 1

    @check_if_removed
    def find_previous_any(self, mod):
        return self.find_previous_modifier_any(mod)

    @check_if_removed
    def find_previous_modifier_any(self, mod):
        """
        Returns any previous modifier wrt mod
        """

        x = self.get_index(mod)
        y = len(self._modifiers_list)

        if y > 0:
            if x > 0:
                return self.get_by_index(x - 1)
            else:
                return self.get_by_index(0)

    @check_if_removed
    def find_next_any(self, mod):
        return self.find_next_modifier_any(mod)

    @check_if_removed
    def find_next_modifier_any(self, mod):
        """
        Returns any next modifier
        wrt mod
        """

        x = self.get_index(mod)
        y = len(self._modifiers_list)

        if x < (y - 1):
            return self.get_by_index(x+1)
        else:
            return self.get_by_index(y-1)
    # }}}

    # Methods that are looping around list {{{
    @check_if_removed
    def find_previous_loop(self, mod, m_type):
        return self.find_previous_modifier_loop(mod, m_type)

    @check_if_removed
    def find_previous_modifier_loop(self, mod, m_type):
        """
        Returns previous
        modifier of m_type type
        wrt mod
        Loops around m_list
        Returns None if not found any
        """

        # Offset for iterating over list
        x = 1
        m_list_len = len(self._modifiers_list)
        while x < m_list_len + 1:
            y = self.get_index(mod) - x
            if y < 0:
                y = y + m_list_len
            if self._modifiers_list[y].type == m_type:
                return self.get_by_index(y)
            x += 1

    @check_if_removed
    def find_next_loop(self, mod, m_type):
        return self.find_next_modifier_loop(mod, m_type)

    @check_if_removed
    def find_next_modifier_loop(self, mod, m_type):
        """
        Returns next
        modifier of m_type type
        wrt mod
        Loops around m_list
        Returns None if not found any
        """

        # Offset for iterating over list
        x = 1
        m_list_len = len(self._modifiers_list)
        while x < m_list_len + 1:
            # y = index of modifier that should be returned
            # created on every iteration
            # TODO: changed index_get to get_index
            y = self.get_index(mod) + x
            if y >= m_list_len:
                y = y - m_list_len
            if self._modifiers_list[y].type == m_type:
                return self._modifiers_list[y]
            x += 1

    @check_if_removed
    def find_previous_any_loop(self, mod):
        return self.find_previous_modifier_any_loop(mod)

    @check_if_removed
    def find_previous_modifier_any_loop(self, mod):
        """
        Returns any previous modifier
        wrt mod
        Loops around m_list
        """

        x = self._modifiers_list.index(mod)
        y = len(self._modifiers_list)
        if x > 0:
            return self._modifiers_list[x-1]
        else:
            return self._modifiers_list[y-1]

    @check_if_removed
    def find_next_any_loop(self, mod):
        return self.find_next_modifier_any_loop(mod)

    @check_if_removed
    def find_next_modifier_any_loop(self, mod):
        """
        Returns any next modifier
        wrt mod
        Loops around m_list
        """

        x = self._modifiers_list.index(mod)
        y = len(self._modifiers_list)
        if x < (y - 1):
            return self._modifiers_list[x + 1]
        else:
            return self._modifiers_list[0]
    # }}}
