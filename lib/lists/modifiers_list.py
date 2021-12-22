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

from .traits.utils.modifiers_list_utils import ModifiersListUtilsTrait
from ..controller.actions import (
                                  ClusterRequest,
                                  ClustersAction,
                                  ClustersCommand,
                                  ClustersBatchCommand,
                                  )

from ..controller.answers import (
                                  ActionDefaultRemove,
                                  ActionDefaultApply,
                                  ActionDefaultMove,
                                  ActionDefaultDeconstuct
                                  )


class ModifiersList(ModifiersListUtilsTrait):
    """
    Simple list of Blender modifiers without Modifiers Clusters.

    Doesnt require modifiers to be on same object or even exist on
    any object.

    All methods assuming that passed modifiers, their names, types
    and such are actual Blender modifiers. Same goes for returned values.

    Has different methods for finding specific modifiers, such as
    finding next modifier of specific type starting from specific
    modifier, returning list of modifiers of specific type etc.

    Doesnt require modifiers to be on same object or even exist on
    any object.
    """

    # TODO: rework name and docstring
    # TODO: Add checks for passed function arguments
    # TODO: copying modifier settings
    # TODO: proper log

    # ============================================================
    #
    #               MODIFIERS LIST METHODS NAMING
    #
    # ============================================================
    # All methods that have 'actual_modifier' in their name
    # return actual Blender modifiers references, and assume that arguments
    # use Blender modifiers.
    #
    # All methods that have 'modifier' in their name return Cluster modifiers
    # unless used within SimpleModifiersList, which uses ActualModifiers.
    # ModifiersCluster is a SimpleModifiersList.
    #
    # All methods that have 'cluster' in their name return Clusters, or even
    # nested clusters.
    #
    # All methods that have 'recursive' in their name recursively calls cluster
    # methods of same functional as called method. This also means that nested
    # clusters are supported.
    # NestedModifiersCluster use ModifiersClustersList.
    #
    # All methods that have 'loop' in their name iterate 'around' list, used
    # for creating tools that have some kind of UI. They work on single
    # layer, unless specified.
    #
    # All methods that dont have anything of above in their name doesnt have
    # anything to do with modifiers and operate on list in general.
    # ============================================================

    # Additional info
    _MODIFIERS_LIST_V = True

    def __init__(self, obj=None, *args, no_obj=None,
                 actions=None, no_default_actions=False,
                 **kwargs):
        super().__init__(*args, **kwargs)

        if not no_obj:
            if obj is None:
                raise ValueError

        self._object = obj

        self.__DUMMY_MODIFIERS = False
        self._modifiers_list = []
        self._additional_info_log = []
        self._actions = []
        if not no_default_actions:
            default_actions = []
            default_actions.append(ActionDefaultRemove(self))
            default_actions.append(ActionDefaultApply(self))
            default_actions.append(ActionDefaultDeconstuct(self))
            default_actions.append(ActionDefaultMove(self))
            self._actions.extend(default_actions)
        if actions is not None and isinstance(actions, list):
            self._actions.extend(actions)

    def __len__(self):
        return len(self._modifiers_list)

    def _check_if_cluster_removed(self):
        pass

    def remove(self, cluster=None):
        """
        Removes cluster or modifier from this list.
        If cluster is None, removes cluster itself.
        """
        if cluster is None:
            cluster = self
        x = ClustersAction('REMOVE', cluster)
        x = ClustersCommand(x,
                            affect_clusters=True,
                            affect_modifiers=True,
                            dry_clusters=False,
                            dry_modifiers=False,
                            )
        self._controller.do(x)

    def apply(self, cluster=None):
        """
        Removes cluster or modifier from this list.
        If cluster is None, applies cluster itself.
        """
        if cluster is None:
            cluster = self
        x = ClustersAction('APPLY', cluster)
        x = ClustersCommand(x,
                            affect_clusters=True,
                            affect_modifiers=True,
                            dry_clusters=False,
                            dry_modifiers=False,
                            )
        self._controller.do(x)

    def move_up(self, cluster):
        """
        Removes cluster from this list.
        Returns None or False, if cluster already first in this list.
        """
        return self._move(cluster, direction='UP')

    def move_down(self, cluster):
        """
        Removes cluster from this list.
        Returns None or False, if cluster already last in this list.
        """
        return self._move(cluster, direction='DOWN')

    def _move(self, cluster, direction):
        """
        Moves cluster or modifier in this list.
        Returns None or False.
        """
        if len(self._modifiers_list) < 2:
            return False

        i = self._modifiers_list.index(cluster)

        if direction == 'UP':
            if i == 0:
                return False
            cluster_to_move_through = self._modifiers_list[i-1]
            direction_2 = 'DOWN'
        elif direction == 'DOWN':
            if i == len(self._modifiers_list) - 1:
                return False
            cluster_to_move_through = self._modifiers_list[i+1]
            direction_2 = 'UP'
        else:
            raise ValueError

        length = len(
                cluster_to_move_through.get_full_actual_modifiers_list())

        x = ClustersAction('MOVE', cluster)
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

    def deconstruct(self, cluster):
        x = ClustersAction('DECONSTRUCT', cluster)
        x = ClustersCommand(x,
                            affect_clusters=False,
                            affect_modifiers=False,
                            dry_clusters=False,
                            dry_modifiers=False,
                            )

        self._controller.do(x)

    def ask(self, action):
        for x in self._actions:
            if x.action_type == action.verb:
                return x.ask(action)
        raise ValueError(f'No implementation for action type {action.verb}')

    def do(self, action):
        """
        Do batch command, simple command or action of this
        modifiers list elements.
        """
        if not isinstance(action, list):
            action = [action]

        # Check all elements first
        # TODO: function for this
        for x in action:
            if not isinstance(x, ClustersBatchCommand)\
                    and not isinstance(x, ClustersCommand)\
                    and not isinstance(x, ClustersAction):
                raise TypeError(f'Expected ClustersAction, got {type(x)}')

        for x in action:
            if isinstance(x, ClustersBatchCommand):
                self.do_batch(x)
            elif isinstance(x, ClustersCommand):
                self.do_command(x)
            elif isinstance(x, ClustersAction):
                self.do_action(x)

    def do_batch(self, batch):
        for x in batch.commands:
            self.do_command(x)

    def do_command(self, command):
        for x in command.actions:
            self.do_action(x)

    def do_action(self, action):
        print(f'Cluster {self}, action is {action}')
        for x in self._actions:
            if x.action_type == action.verb:
                return x.do(action)
        raise ValueError(f'No implementation for action type {action.verb}')

    def move_to_index(self, mod, i):
        """
        Moves cluster to index.

        Returns True if moved modifier.
        Returns False if any errors.
        """
        # TODO: not tested
        if i < self.get_list_length():
            m_i = self.get_index(mod)
            d_i = i - m_i
            x = 0
            if d_i > 0:
                while x <= d_i:
                    self.move_up(mod)
                    x += 1
                return True
            elif d_i < 0:
                while x >= d_i:
                    self.move_up(mod)
                    x -= 1
                return True

    # ==============================================
    # This methods work on _modifiers_list's level.
    # This means that they dont differ simple or nested clusters and modifiers
    # ==============================================
    def get_full_actual_modifiers_list(self):
        self._check_if_cluster_removed()
        return self.get_list()

    def get_actual_full_actual_modifiers_list(self):
        self._check_if_cluster_removed()
        return self.get_actual_list()

    def get_list(self):
        """
        Returns shallow copy of this layer's list.
        Should be used instead of get_actual_list
        when possible.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list

    def get_full_list(self):
        return self.get_list()

    def get_all_clusters_and_modifiers(self):
        return self.get_list()

    def get_actual_list(self):
        """
        Returns reference to this layer's list.
        Its better idea to usual get_list when possible instead
        of this method.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list

    def get_list_in_range_not_inclusive(self, mod1, mod2):
        """
        Returns list of objects between two objects.
        Not inclusive.
        """
        self._check_if_cluster_removed()

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

    def get_list_in_range_inclusive(self, mod1, mod2):
        """
        Returns list of objects between two objects.
        Inclusive.
        If two references of same object, returns list
        with one object.
        """
        self._check_if_cluster_removed()

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

    def get_list_length(self):
        """
        Returns length of list of objects.
        """
        self._check_if_cluster_removed()
        return len(self._modifiers_list)

    def get_list_by_type(self, m_type):
        """
        Returns list of m_type objects.
        """
        self._check_if_cluster_removed()
        y = []
        for x in self._modifiers_list:
            if x.type == m_type:
                y.append(x)
        return y

    def get_by_index(self, i):
        """
        Returns object by index.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list[i]

    def get_index(self, mod):
        """
        Returns index of object.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list.index(mod)

    def get_first(self):
        """
        Returns first object.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list[0]

    def get_last(self):
        """
        Returns last object.
        """
        self._check_if_cluster_removed()
        return self._modifiers_list[-1]

    # ===============
    # INFO ABOUT LIST
    # ===============
    def has_modifier(self, mod):
        """
        Returns True, if found object in list.
        Can return False.
        """
        if mod in self.get_list():
            return True
        return False

    def has_modifier_by_type(self, m_type):
        """
        Returns True if found any mod of m_type.
        Can return False.
        """

        for mod in self._modifiers_list:
            if mod.type == m_type:
                return True
        return False

    def has_modifier_by_name(self, m_name):
        """
        Returns True if found any objects with m_name.
        Can return False.
        """

        for mod in self._modifiers_list:
            if mod.name == m_name:
                return True
        return False

    # =================
    # Finding modifiers
    # =================
    # ------------------------------------
    # 'find' methods that looking for modifiers relatively
    # to modifiers.
    # ------------------------------------
    def find_previous(self, mod, m_type):
        self._check_if_cluster_removed()
        return self.find_previous_modifier(mod, m_type)

    def find_previous_modifier(self, mod, m_type):
        """
        Returns index of previous
        modifier of m_type type wrt mod
        Returns None if not found any
        """
        self._check_if_cluster_removed()

        # Offset for iterating over list
        x = 1
        m_list_len = self.get_list_length()
        while x < m_list_len + 1:
            # y = index of modifier that should be returned
            # created on every iteration
            y = self.get_index(mod) - x
            if y < 0:
                return None
            elif self.get_by_index(y).type == m_type:
                return self.get_by_index(y)
            x += 1

    def find_next(self, mod, m_type):
        self._check_if_cluster_removed()
        return self.find_next_modifier(mod, m_type)

    def find_next_modifier(self, mod, m_type):
        """
        Returns index of next modifier of m_type type wrt mod.
        Returns None if not found any.
        """
        self._check_if_cluster_removed()

        # Offset for iterating over list
        x = 1
        m_list_len = self.get_list_length()
        while x < m_list_len + 1:
            y = self.get_index(mod) + x
            if y >= m_list_len:
                return None
            elif self._modifiers_list[y].type == m_type:
                return self.get_by_index(y)
            x += 1

    def find_previous_any(self, mod):
        self._check_if_cluster_removed()
        return self.find_previous_modifier_any(mod)

    def find_previous_modifier_any(self, mod):
        """
        Returns any previous modifier wrt mod
        """
        self._check_if_cluster_removed()

        x = self.get_index(mod)
        y = self.get_list_length()

        if y > 0:
            if x > 0:
                return self.get_by_index(x - 1)
            else:
                return self.get_by_index(0)

    def find_next_any(self, mod):
        self._check_if_cluster_removed()
        return self.find_next_modifier_any(mod)

    def find_next_modifier_any(self, mod):
        """
        Returns any next modifier
        wrt mod
        """
        self._check_if_cluster_removed()

        x = self.get_index(mod)
        y = self.get_list_length()

        if x < (y - 1):
            return self.get_by_index(x+1)
        else:
            return self.get_by_index(y-1)

    # ------------------------------------
    # Methods that are looping around list
    # ------------------------------------
    def find_previous_loop(self, mod, m_type):
        self._check_if_cluster_removed()
        return self.find_previous_modifier_loop(mod, m_type)

    def find_previous_modifier_loop(self, mod, m_type):
        """
        Returns previous
        modifier of m_type type
        wrt mod
        Loops around m_list
        Returns None if not found any
        """
        self._check_if_cluster_removed()

        # Offset for iterating over list
        x = 1
        m_list_len = self.get_list_length()
        while x < m_list_len + 1:
            y = self.get_index(mod) - x
            if y < 0:
                y = y + m_list_len
            if self._modifiers_list[y].type == m_type:
                return self.get_by_index(y)
            x += 1

    def find_next_loop(self, mod, m_type):
        self._check_if_cluster_removed()
        return self.find_next_modifier_loop(mod, m_type)

    def find_next_modifier_loop(self, mod, m_type):
        """
        Returns next
        modifier of m_type type
        wrt mod
        Loops around m_list
        Returns None if not found any
        """
        self._check_if_cluster_removed()

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

    def find_previous_any_loop(self, mod):
        self._check_if_cluster_removed()
        return self.find_previous_modifier_any_loop(mod)

    def find_previous_modifier_any_loop(self, mod):
        """
        Returns any previous modifier
        wrt mod
        Loops around m_list
        """
        self._check_if_cluster_removed()

        # TODO: changed index_get to get_index
        x = self.get_index(mod)
        y = self.get_list_length()
        if x > 0:
            return self._modifiers_list[x-1]
        else:
            return self._modifiers_list[y-1]

    def find_next_any_loop(self, mod):
        self._check_if_cluster_removed()
        return self.find_next_modifier_any_loop(mod)

    def find_next_modifier_any_loop(self, mod):
        """
        Returns any next modifier
        wrt mod
        Loops around m_list
        """
        self._check_if_cluster_removed()

        x = self.get_index(mod)
        y = self.get_list_length()
        if x < (y - 1):
            return self._modifiers_list[x + 1]
        else:
            return self._modifiers_list[0]
