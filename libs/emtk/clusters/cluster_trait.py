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

import copy
import json

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

# from ..object_state import ListObjectState
from ..lists.utils import check_if_removed


class ClusterTrait():
    """This ModifiersList trait should be in every
    cluster used in ClustersList.
    """

    """
    data: list[modifier]    ->  ClusterState 2
    default_data: dict      ->  ClusterState 1
    instance_data: dict     ->  ClusterState 2

    # List of clusters or modifiers. This list is used for __getitem__.
    data

    # Variables that can be changed in cluster instance.
    # They can be stored in ClusterState and serialized/deserialized.
    instance_data = {}

    # Variables (constants) that are defined in constructor and
    # should not be changed.
    # They stored in ClusterDefinition.
    # If you need to somehow change this.instance_data (for example, change type
    # of modifier),
    # its better to create new cluster, reparse modifiers,
    # and copy other.instance_data.
    default_data: dict
    """

    def __init__(self,
                 *args,
                 cluster_name=None,
                 cluster_type=None,
                 modifiers_by_type=None,
                 modifiers_by_name=None,
                 cluster_tags=None,
                 cluster_priority=None,
                 cluster_is_sane=None,
                 cluster_is_kinda_sane=None,
                 cluster_dynamic=None,
                 cluster_createable=None,
                 dont_define_cluster=None,
                 **kwargs
                 ):

        # Cluster shouldnt be used, if it is already
        # removed from clusters list.
        self._cluster_removed = False

        super().__init__(no_obj=True, *args, **kwargs)

        d = {
            'name': cluster_name,
            'type': cluster_type,
            'by_type': modifiers_by_type,
            'by_name': modifiers_by_name,
            'tags': cluster_tags,
            'priority': cluster_priority,
            'sane': cluster_is_sane,
            'kinda_sane': cluster_is_kinda_sane,
            'dynamic': cluster_dynamic,
            'createable': cluster_createable,
        }

        # Check dict.
        self.default_data\
            = self._check_cluster_definition(d)

        self.instance_data = {}

        # Modifiers names that can be sometimes used
        # instead of default ones.
        self.instance_data['by_name'] = []

        # Custom name that can be changed in runtime.
        self.instance_data['name'] = None

        # Custom tags that can be changed in runtime.
        self.instance_data['tags'] = []

        # Initialized.
        # TODO: remove this
        self.instance_data['initialized'] = False

        # Collapsed.
        self.instance_data['collapsed'] = True

        # Show expanded
        self.instance_data['show_expanded'] = False
        self.instance_data['show_definition_expanded'] = False
        self.instance_data['show_props_expanded'] = False

        # Modifiers list.
        self._data = []

        # Sorting rules.
        self._sorting_rules = []

        # Check cluster sanity.
        if not dont_define_cluster\
                and not self.default_data['sane']\
                and not self.check_this_cluster_sanity():
            raise ValueError('This cluster cant be used.')

        # TODO: dont need this

    def _check_cluster_definition(self, cluster_definition):
        """
        Checks types in cluster definition and add default
        values.

        Returns cluster definition.
        """
        x = cluster_definition

        # Check if essential values specified.
        if x['name'] is None\
                or x['type'] is None\
                or x['by_type'] is None:
            raise TypeError

        # Replace None with default values where
        # it is possible.
        if x['tags'] is None:
            x['tags'] = []
        if x['by_name'] is None:
            x['by_name'] = []
        if x['priority'] is None:
            x['priority'] = 0
        if x['createable'] is None:
            x['createable'] = True
        if x['dynamic'] is None:
            x['dynamic'] = False
        if x['sane'] is None:
            x['sane'] = False
        if x['kinda_sane'] is None:
            x['kinda_sane'] = False

        # Check types.
        if not isinstance(x, dict)\
                or not isinstance(x['name'], str)\
                or not isinstance(x['type'], str)\
                or not isinstance(x['tags'], list)\
                or not isinstance(x['by_type'], list)\
                or not isinstance(x['by_name'], list)\
                or not isinstance(x['priority'], int)\
                or not isinstance(x['createable'], bool)\
                or not isinstance(x['dynamic'], bool)\
                or not isinstance(x['sane'], bool)\
                or not isinstance(x['kinda_sane'], bool):
            raise TypeError

        # Check length.
        if len(x['name']) == 0\
                or len(x['type']) == 0\
                or len(x['by_type']) == 0:
            raise ValueError

        # Check types in lists.
        for y in x['by_name']:
            if isinstance(y, list):
                if len(y) == 0:
                    raise ValueError
                for z in y:
                    if not isinstance(z, str):
                        raise TypeError
            elif not isinstance(y, str):
                raise TypeError
        for y in x['by_type']:
            if isinstance(y, list):
                if len(y) == 0:
                    raise ValueError
                for z in y:
                    if not isinstance(z, str):
                        raise TypeError
            elif not isinstance(y, str):
                raise TypeError
        for y in x['tags']:
            if not isinstance(y, str):
                raise TypeError
        return x

    # Props

    @property
    def name(self):
        return self.get_this_cluster_name()

    @name.setter
    def name(self, cluster_name):
        return self.set_this_cluster_custom_name(cluster_name)

    @check_if_removed
    def get_this_cluster_name(self):
        """
        Returns this ModifiersCluster's custom name, or default name.
        """
        if self.instance_data['name'] is not None:
            return self.instance_data['name']
        else:
            return self.default_data['name']

    @check_if_removed
    def get_this_cluster_custom_name(self):
        """
        Returns this ModifiersCluster's custom name.
        """
        return self.instance_data['name']

    @check_if_removed
    def get_this_cluster_default_name(self):
        """
        Returns this ModifiersCluster's default name.
        """
        return self.default_data['name']

    @check_if_removed
    def set_this_cluster_custom_name(self, cluster_name):
        """
        Sets cluster custom cluster name.
        Returns True or False, if cluster is not editable.
        """
        if isinstance(cluster_name, str):
            self.instance_data['name'] = cluster_name
        else:
            raise TypeError

    @property
    def type(self):
        return self.get_this_cluster_type()

    @check_if_removed
    def get_this_cluster_type(self):
        """
        Returns this ModifiersCluster's type
        """
        return self.default_data['type']

    # Methods reserved for subclasses
    # TODO: remove this

    def modcluster_extra_availability_check(self, modifiers):
        """
        Additional method reserved for custom types.
        Checks if modifiers can be considered as
        ModifiersCluster of this type.

        Returns CONTINUE if can potentially be available,
        but missing some modifiers that can be found later.
        Returns FOUND if modifiers can be considered
        ModifiersCluster of this type.
        Returns False, if not usable.
        Returns None, if no decision.
        """
        return

    def check_this_cluster_sanity_custom(self):
        """
        Method reserved for object-specific sanity checks.

        Should return True or False.
        """
        return True

    # Cluster subclass-specific additional actions.

    """
    This three methods should return None, ClustersCommand or
    list of ClustersCommands (not ClustersBatchCommand).
    Command will be put before recived command in ClustersBatchCommand.

    Make sure not to change clusters state in this methods, because
    sometimes this methods will be called without actually performing
    action after.

    Intended usecase:
    Additional ClustersCommands that are required for action to be
    allowed by this cluster.
    """

    def cluster_answer_case_self(self, action):
        """
        This method is called when action.subject is cluster itself.
        """
        return

    def cluster_answer_case_list(self, action):
        """
        This method is called when action.subject is in cluster's list.
        """
        return

    def cluster_answer_case_all(self, action):
        """
        This method is called when action.subject is somewhere in this
        cluster's layers and modifiers clusters.
        """
        return

    # Cluster subclass-specific additional interpretation.

    """
    This three methods called just before applying action and
    should return None.

    Intended usecase:
    Additional actions on cluster itself, without changing other
    clusters in any way.
    """

    def cluster_do_case_self(self, action):
        """
        This method is called when action.subject is cluster itself.
        """
        return

    def cluster_do_case_list(self, action):
        """
        This method is called when action.subject is in cluster's list.
        """
        return

    def cluster_do_case_all(self, action):
        """
        This method is called when action.subject is somewhere in this
        cluster's layers and modifiers clusters.
        """
        return

    # Cluster tags

    @check_if_removed
    def get_this_cluster_tags(self):
        """
        Returns this ModifiersCluster's custom tags, or default tags.
        """
        return self.default_data['tags'] + self.instance_data['tags']

    @check_if_removed
    def add_tag_to_this_cluster(self, custom_tag):
        """
        Set this ModifiersCluster's custom tags.
        Takes string as an argument.
        Returns True if successfully added tag.
        """
        if isinstance(custom_tag, str):
            if custom_tag not in self.instance_data['tags']:
                self.instance_data['tags'].append(custom_tag)
                return True
            else:
                return False
        else:
            raise TypeError

    @check_if_removed
    def remove_tag_from_this_cluster(self, custom_tag):
        """
        Remove this ModifiersCluster's custom tag.
        Takes string as an argument.
        Returns True if successfully removed tag.
        Returns False if no such tag or cant remove.
        """
        y = []
        result = False
        for x in self.instance_data['tags']:
            if x == custom_tag:
                y.append(x)
                result = True
        for x in y:
            self.instance_data['tags'].remove(x)
        return result

    # Initializing cluster

    @check_if_removed
    def set_this_cluster_modifiers(self, modifiers):
        """
        Replaces list of modifiers with modifiers.
        Returns True or False, if cluster is not editable.
        """
        if not isinstance(modifiers, list):
            raise TypeError
        if len(modifiers) == 0:
            raise ValueError

        for x in modifiers:
            if _WITH_BPY:
                if not isinstance(x, bpy.types.Modifier)\
                        and not isinstance(x, ClusterTrait):
                    raise TypeError

            elif not _WITH_BPY:
                if not isinstance(x, DummyBlenderModifier)\
                        and not isinstance(x, ClusterTrait):
                    raise TypeError

        # If havent set modifiers already
        if self.instance_data['initialized'] is False:
            self._data = modifiers
            self.instance_data['initialized'] = True
            self._mod = self._data[0]
            return True

        # Or allowed to reset modifiers
        elif self.default_data['dynamic']:
            self._data = modifiers
            self._mod = self._data[0]
            return True

        else:
            return False

    # Clusters sorting

    @check_if_removed
    def add_sorting_rule(self, sorting_rule):
        """
        Add new sorting rule for this cluster or
        replace existing one.

        Returns True or False, if cluster not sortable.
        """
        if 'NO_SORT' in self.get_this_cluster_tags():
            return False

        self.remove_sorting_rule(sorting_rule.name)

        self._sorting_rules.append(sorting_rule)
        return True

    @check_if_removed
    def remove_sorting_rule(self, sorting_rule_name):
        """
        Removes sorting rule by name.

        Returns True or False, if no such sorting
        rule.
        """
        removed_sorting_rule = False
        r = []
        for x in self._sorting_rules:
            if x.name == sorting_rule_name:
                r += x
        for x in r:
            self._sorting_rules.remove(x)
            removed_sorting_rule = True
        if removed_sorting_rule is False:
            raise ValueError
        return removed_sorting_rule

    @check_if_removed
    def get_sorting_rules(self):
        """
        Returns sorting rules for this cluster.
        Returns empty list, if cluster disabled
        sorting.
        """
        if 'NO_SORT' in self.get_this_cluster_tags():
            return []
        else:
            return self._sorting_rules

    # Parsing

    def get_this_cluster_possible_length(self):
        """Returns maximum possible modifiers sequence length."""
        return len(self.default_data['by_type'])

    def get_this_cluster_priority(self):
        """Returns priority for this cluster in parsing."""
        return self.default_data['priority']

    def check_availability(self, modifiers):
        """
        Checks if sequence of modifiers or clusters can be
        considered ModifiersCluster of this type.

        Returns CONTINUE if can potentially be available,
        but missing some modifiers that can be found later.
        Returns FOUND if modifiers or clusters can be considered
        ModifiersCluster of this type.
        Returns False, if not usable.
        """
        for mod in modifiers:
            if _WITH_BPY:
                if isinstance(mod, bpy.types.Modifier):
                    pass
            elif not _WITH_BPY:
                if isinstance(mod, DummyBlenderModifier):
                    pass
            elif isinstance(mod, ClusterTrait):
                pass
            else:
                raise TypeError(f'{mod} is not a modifier or cluster.')

        # How many modifiers should be correct?
        x2 = len(self.default_data['by_type'])

        # Iterate over provided modifiers sequence
        for y, mod in enumerate(modifiers):

            modifiers_by_type = self.default_data['by_type']

            # Check modifiers by types
            if modifiers_by_type[y] != ['ANY']\
                    and modifiers_by_type[y] != 'ANY':

                # Check modifier type
                if isinstance(mod, ClusterTrait):
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG CLUSTER TYPE'
                else:
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG ACTUAL MODIFIER TYPE'

            # Use specific names list, if there is one
            if len(self.instance_data['by_name']) != 0:
                modifiers_by_names\
                    = self.instance_data['by_name']
            else:
                modifiers_by_names\
                    = self.default_data['by_name']

            # Check name
            if modifiers_by_names[y] != ['ANY']\
                    and modifiers_by_names[y] != 'ANY':

                # Check modifiers names
                if isinstance(mod, ClusterTrait):
                    if isinstance(modifiers_by_names[y], list):
                        if mod.name\
                                not in modifiers_by_names[y]:
                            return 'WRONG CLUSTER NAME'
                    else:
                        if mod.name\
                                != modifiers_by_names[y]:
                            return 'WRONG CLUSTER NAME'
                else:
                    if isinstance(modifiers_by_names[y], list):
                        if mod.name not in modifiers_by_names[y]:
                            return 'WRONG ACTUAL MODIFIER NAME'
                    else:
                        if mod.name != modifiers_by_names[y]:
                            return 'WRONG ACTUAL MODIFIER NAME'

            if y + 1 == x2:
                return 'FOUND'
            elif y + 1 < x2 and y + 1 == len(modifiers):
                return 'CONTINUE'

        # Additional checks reserved for custom types
        additional_checks = self.modcluster_extra_availability_check(
            modifiers)

        if additional_checks is not None:
            return additional_checks

        return None

    # Cluster visibility

    def get_this_cluster_visibility(self):
        """
        Returns list with info about this cluster visability
        """
        y1 = []
        y2 = []
        y3 = []
        y4 = []

        mods = self.all_modifiers()
        for mod in mods:
            y1.append(mod.show_render)
            y2.append(mod.show_viewport)
            y3.append(mod.show_in_editmode)
            y4.append(mod.show_on_cage)

        y = [y1, y2, y3, y4]

        result = []

        for x in y:
            if True in x:
                if False in x:
                    result.append('HALF')
                else:
                    result.append('ON')
            else:
                result.append('OFF')
        return result

    def set_this_cluster_visibility(self,
                                    vis_settings=None
                                    ):
        """
        Sets this cluster visibility.
        Takes list as an argument.
        """
        if vis_settings is None:
            vis_settings = [None, None, None, None]

        y1, y2, y3, y4 = vis_settings

        mods = self.all_modifiers()

        if y1 is not None:
            for mod in mods:
                mod.show_render = y1

        if y2 is not None:
            for mod in mods:
                mod.show_viewport = y2

        if y3 is not None:
            for mod in mods:
                mod.show_in_editmode = y3

        if y4 is not None:
            for mod in mods:
                mod.show_on_cage = y4

    def toggle_this_cluster_visibility(self, vis_settings=None):
        """
        Toggles this cluster visibility.
        If not all actual modifiers have some kind
        of visibility, turns it off completely.

        Takes list as an argument.
        """
        result = []
        for x in vis_settings:
            result.append(bool(x))
        vis_settings = result

        old_cluster_vis = self.get_this_cluster_visibility()
        new_cluster_vis = []

        for i, x in enumerate(old_cluster_vis):
            if vis_settings[i] is True:
                if x == 'HALF':
                    new_cluster_vis.append(False)
                elif x == 'ON':
                    new_cluster_vis.append(False)
                elif x == 'OFF':
                    new_cluster_vis.append(True)
            else:
                new_cluster_vis.append(None)
        self.set_this_cluster_visibility(new_cluster_vis)

    # Utility
    # TODO: allow checking without throwing error

    @check_if_removed
    def check_this_cluster_sanity(self):
        """
        Checks if this cluster type would work properly.

        Reccomended to check every time enabling new
        cluster type or changing existing one.

        Basically should always return False, because
        modifiers clusters are kinda unusable and
        overengeneered.

        Returns True if not found any errors.
        """

        # Additional checks
        if not self.check_this_cluster_sanity_custom():
            raise ValueError

        if self.default_data['sane']:
            return True

        l_1 = self.default_data['by_type']
        len_1 = len(l_1)

        l_2 = self.default_data['by_name']
        len_2 = len(l_2)

        if len(self.instance_data['by_name']) > 0:
            if len_2 != len(self.instance_data['by_name']):
                raise ValueError(
                    'Length of specified modifiers names is wrong.')
        if len_1 != len_2:
            raise ValueError(
                f'Length of types ({l_1}) and names ({l_2}) is different.')
        if len_1 == 0:
            raise ValueError(
                'Length of modifiers types cant be 0.')
        if self.default_data['by_type'][0] == ['ANY']:
            raise ValueError(
                'First modifier cant be any, specify modifier type.')
        for mod_types in self.default_data['by_type']:
            if isinstance(mod_types, list):
                if len(mod_types) == 0:
                    raise ValueError('Modifier types length is 0.')
        for mod_names in self.default_data['by_name']:
            if isinstance(mod_names, list):
                if len(mod_names) == 0:
                    raise ValueError('Modifier names length is 0.')
        return True

    def serialize_this_cluster_type(self):
        result = json.dumps(self.get_this_cluster_parser_variables())
        return result

    # TODO: what is that
    def get_this_cluster_parser_variables(self):
        x = copy.copy(self.default_data)

        # TODO: use some attribute instead
        if self.has_clusters():
            c = 'ClustersLayer'
        else:
            c = 'ModifiersCluster'
        x.update({'cluster_trait_subclass': f'{c}'})
        return x

    def _check_if_cluster_removed(self):
        """
        This method throws an error when trying to access already
        removed cluster.
        """
        if self._cluster_removed:
            name = self.default_data["name"]
            raise ValueError(f'Cluster {name} at {id(self)} already removed.')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self._cluster_removed and self.instance_data['initialized']:
            name = self.get_this_cluster_name()
            result = f"Cluster {name}, {self.get_this_cluster_type()}"
        else:
            result\
                = f"Already removed cluster {self.default_data['name']}"
        return result
