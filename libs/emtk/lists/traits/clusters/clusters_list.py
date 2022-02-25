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

import collections
import logging
import dataclasses
import json

from ....object_state import _get_object_state_subclass_by_name
from ....object_state import _remove_type_name_from_dict
from ....object_state import _add_type_name_to_dict

from ....controller.answers import ActionDefaultDeconstuct
from ....controller.actions import (
    ClustersAction,
    ClustersCommand,
)
from ...utils import check_if_removed

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


class ClustersListTrait():
    """
    Class that should be inherited by any ModifiersList subclass that uses
    clusters.
    """

    def find_cluster_by_name(self, name: str):
        for x in self.all_clusters():
            if x.name == name:
                return x

    def find_modifier_by_name(self, name: str):
        for x in self.all_modifiers():
            if x.name == name:
                return x

    def __init__(self, *args, no_default_actions=False, **kwargs):
        super().__init__(
            no_default_actions=no_default_actions,
            *args, **kwargs)
        if not no_default_actions:
            default_actions = [ActionDefaultDeconstuct]
            for x in default_actions:
                self.add_action_answer(x(self))

    def _check_if_cluster_removed(self):
        return

    def has_clusters(self):
        return True

    def _check_cluster_or_modifier(self, cluster):
        if type(cluster) is str:
            result = self.find_cluster_by_name(cluster)
            if result is None:
                result = self.find_modifier_by_name(cluster)
            if result is None:
                raise ValueError
            cluster = result
        elif cluster is None:
            return None
        else:
            # TODO: this probably doesnt work
            if cluster not in self.all_clusters()\
                    and cluster is not self:
                raise ValueError
        return cluster

    # Actions {{{
    @check_if_removed
    def deconstruct(self, clusters):
        """Deconstructs clusters on this layer."""
        if type(clusters) is not list:
            clusters = [clusters]
        result = []
        for x in clusters:
            result.append(self._check_cluster_or_modifier(x))
        clusters = result
        logger.info(f'Deconstructing {clusters} on layer {self}')

        for cluster in clusters:
            # TODO: use ClusterRequest instead.
            x = ClustersAction('DECONSTRUCT', cluster)
            x = ClustersCommand(x,
                                affect_clusters=False,
                                affect_modifiers=False,
                                dry_clusters=False,
                                dry_modifiers=False,
                                )

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'Created {x}')
            self._controller.do(x)

    @check_if_removed
    def create(self, cluster_type_instance):
        """Creates cluster or layer on this layer."""
        logger.info(f'Creating {cluster_type_instance} on layer {self}')
        raise ValueError
    

    def get_actual_modifier_by_index(self, i):
        """
        Returns modifier by index.
        Looks in nested clusters.
        Always return actual modifiers.
        """
        x = self.all_modifiers()
        return x[i]

    def get_actual_modifier_by_name(self, m_name):
        """
        Returns modifier by name.
        Looks in nested clusters.
        Returns None if not found.
        """
        for x in self.all_modifiers():
            if x.name == m_name:
                return x
        raise ValueError(f'No modifier with name "{m_name}"')

    # Iterators {{{
    def all_elements(self):
        """
        Returns list of all clusters and modifiers anywhere in this cluster.
        """
        result = self.all_modifiers()
        result.extend(self.all_clusters())
        return full_list(result)

    def all_clusters(self):
        """
        Returns full list of clusters, including nested ones.
        Also returns cluster that have other clusters in them.
        """
        result = []
        for x in self._data:
            result.append(x)
            if x.has_clusters():
                for y in x.all_clusters():
                    result.append(y)
        return full_list(result)

    def all_modifiers_clusters(self):
        """
        Returns list of this layer clusters including nested ones.
        Only return clusters that contain no other clusters.
        """
        result = []
        for x in self._data:
            if x.has_clusters():
                for y in x.all_modifiers_clusters():
                    result.append(y)
            else:
                result.append(x)
        return full_modifiers_clusters_list(result)

    def all_layers(self):
        """
        Returns list of all of this layer clusters that contain other
        clusters in it, including nested ones.
        Returns empty list if no such clusters found.
        """
        result = [x for x in self.all_clusters() if x.has_clusters()]
        return full_clusters_layers_list(result)

    def all_modifiers(self):
        """
        Returns full list of this layer actual modifiers,
        including nested ones.
        Returns empty list if no actual modifiers found.
        """
        result = []
        for x in self.all_modifiers_clusters():
            for y in x.all_modifiers():
                result.append(y)
        return full_modifiers_list(result)
    

    # @check_obj_ref
    @check_if_removed
    def get_cluster_or_layer(self, obj):
        """
        Returns cluster or layer that cluster or modifier belongs to.
        Also returns this ModifiersClustersList.
        Looks in all clusters.
        """
        if type(obj) is str:
            raise TypeError

        # if obj is self:
        #     raise TypeError(
        #             'First layer of ExtendedModifiersList is not a cluster.')

        if obj in self._data:
            return self

        g = self.all_clusters()
        for x in g:
            if obj in x:
                return x
        raise ValueError(f'Cluster {obj} is not in {self}.')

    @check_if_removed
    def get_trace_to(self, cluster):
        """Returns trace to cluster, starting from this layer."""
        result = []
        f = True
        c = cluster
        while f:
            layer = self.get_cluster_or_layer(c)
            result.append(layer)
            if layer is self:
                f = False
            c = layer
        result.reverse()
        return result

    # Used when moving clusters.
    @check_if_removed
    def recursive_get_first_actual_modifier(self, cluster):
        """Returns first actual modifier of a cluster."""
        x = self[0].has_clusters()
        if x.has_clusters():
            y = x[0]
            return x.recursive_get_first_actual_modifier(y)
        else:
            return x[0]

    @check_if_removed
    def recursive_get_last_actual_modifier(self, cluster):
        """Returns last actual modifier of a cluster."""
        x = self[-1].has_clusters()
        if x.has_clusters():
            y = x[-1]
            return x.recursive_get_last_actual_modifier(y)
        else:
            return x[-1]


# Iterators {{{
class clusters_list_generated_list(collections.UserList):

    def __init__(self, obj, *args, **kwargs):
        self.data = list(obj)

    def items(self):
        return self.data

    def names(self, use_dict=False):
        if use_dict:
            result = {}
            for x in self.data:
                result.update({x.name: x})
        else:
            result = [x.name for x in self.data]
        return result

    def types(self, use_dict=False):
        if use_dict:
            result = {}
            for x in self.data:
                result.update({x.type: x})
        else:
            result = [x.type for x in self.data]
        return result


class clusters_list_generated_clusters_list(clusters_list_generated_list):

    def tags(self):
        return [x.get_this_cluster_tags() for x in self.data]


class full_modifiers_list(clusters_list_generated_list):
    """List of all modifiers."""
    pass


class full_modifiers_clusters_list(clusters_list_generated_clusters_list):
    """List of all modifiers clusters."""
    pass


class full_clusters_layers_list(clusters_list_generated_clusters_list):
    """List of all clusters layers."""
    pass


class full_clusters_list(clusters_list_generated_clusters_list):
    """List of all clusters."""
    pass


class full_list(clusters_list_generated_list):
    """List of all modifiers and clusters."""
    pass



@dataclasses.dataclass
class ClustersListState():  
    def serialize(self):
        logger.debug(f'Serializing {self}')
        self._check_type(self)
        state = {}
        for x, y in self.__dataclass_fields__.items():
            if x == 'items_data':
                items_data = []
                for z in getattr(self, x):
                    element = _add_type_name_to_dict(z)
                    element['data'] = element['data'].serialize()
                    items_data.append(element)
                state.update({x: items_data})
            elif x == 'data':
                state.update({x: _add_type_name_to_dict(self.data)})
            else:
                state.update({x: getattr(self, x)})
        return json.dumps(state)

    @classmethod
    def deserialize(cls, obj):
        state = json.loads(obj)
        data = {}
        for x in cls.__dataclass_fields__:
            if x == 'items_data':
                items_data = []
                for y in state[x].items():
                    items_data.append(
                        _get_object_state_subclass_by_name(
                            y['type']).deserialize(y))
                data.update({x: items_data})
            elif x == 'data':
                data.update({x: _remove_type_name_from_dict(state[x])})
            else:
                data.update({x: state[x]})
        return cls(**data)

    @classmethod
    def get_data_from_obj(cls, obj):
        names = []
        for x in type(obj).mro():
            names.append(x.__name__)
        if 'ModifiersList' not in names:
            raise TypeError(f'Expected cluster, got {type(obj)}')

        data = {}
        data.update({'name': ''})
        data.update({'tags': []})
        data.update({'data': cls._get_data(obj)})
        data.update({'items_data': cls._get_items_data(obj)})
        return cls(**data)

    @staticmethod
    def _get_items_data(obj):
        result = []
        for x in obj:
            result.append(get_object_data(x))
        return result

    @staticmethod
    def _get_data(obj):
        try:
            return obj.instance_data
        except AttributeError:
            return {}
    
