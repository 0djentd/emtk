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

import copy
import json

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

# from ..controller.actions import ClustersAction, ClusterRequest


class ClusterTrait():
    """
    This ModifiersList trait should be in every
    cluster used in ClustersList.
    """

    def __init__(self, *args,
                 cluster_name=None,
                 cluster_type=None,
                 modifiers_by_type=None,

                 # Arguments that can be skipped
                 modifiers_by_name=None,
                 cluster_tags=None,
                 cluster_priority=None,
                 cluster_is_sane=None,
                 cluster_createable=None,
                 cluster_initialized=None,
                 dont_define_cluster=None,
                 **kwargs
                 ):

        super().__init__(no_obj=True, *args, **kwargs)

        # ===============================================================
        # This is variables that should be defined in ModifiersCluster type.
        # ===============================================================

        if dont_define_cluster:
            x = {
                 # Name that should be returned by default to ModifiersList
                 'name': None,

                 # Type that should be returned to ModifiersList
                 'type': None,

                 # Priority interpreted by parser
                 'priority': None,

                 # ModifiersCluster tags
                 'default_tags': [],

                 # List of lists of possible modifier types that this
                 # ModifiersCluster should consists of
                 # Takes modifier order into consideration
                 # If not at index 0, can be 'ANY'
                 'by_type': [],

                 # List of lists of possible names for every modifier
                 # in _MODCLUSTER_MODIFIERS_BY_TYPE
                 # Takes modifier order into consideration
                 # Can be 'ANY'
                 'by_name': [],

                 # Can cluster's modifiers list be changed
                 # after initialization?
                 'dynamic': None,

                 # Can this cluster be created?
                 # In other words, can its _MODIFIERS_BY_TYPE be used
                 # to create new modifiers on object.
                 'createable': None,

                 # Force skip cluster sanity check.
                 # Should be False.
                 'sane': None,

                 # Dont throw an error when checking cluster sanity
                 # TODO: what is dat
                 'kinda_sane': None,
                 }

            self._cluster_definition = x

        elif not dont_define_cluster:
            self._cluster_definition = {}

            # Set cluster type name.
            if isinstance(cluster_name, str):
                if len(cluster_name) == 0:
                    raise ValueError
                self._cluster_definition['name'] = cluster_name
            else:
                raise TypeError

            # Set cluster type that will be returned to ClustersList.
            if isinstance(cluster_type, str):
                if len(cluster_type) == 0:
                    raise ValueError
                self._cluster_definition['type'] = cluster_type
            else:
                raise TypeError

            # Set cluster type default tags.
            if isinstance(cluster_tags, list):
                for x in cluster_tags:
                    if not isinstance(x, str):
                        raise TypeError
                self._cluster_definition['tags'] = cluster_tags
            elif cluster_tags is None:
                self._cluster_definition['tags'] = []
            else:
                raise TypeError

            # Set cluster type modifiers by type.
            if isinstance(modifiers_by_type, list):
                for x in modifiers_by_type:
                    if not isinstance(x, str):
                        if isinstance(x, list):
                            for y in x:
                                if not isinstance(y, str):
                                    raise TypeError
                        else:
                            raise TypeError
                self._cluster_definition['by_type'] = modifiers_by_type
            else:
                raise TypeError

            # Set cluster type modifiers by names.
            if isinstance(modifiers_by_name, list):
                for x in modifiers_by_name:
                    if not isinstance(x, str):
                        if isinstance(x, list):
                            for y in x:
                                if not isinstance(y, str):
                                    raise TypeError
                        else:
                            raise TypeError
                self._cluster_definition['by_name']\
                    = modifiers_by_name
            elif modifiers_by_name is None:
                self._cluster_definition['by_name'] = []
                for x in self._cluster_definition['by_type']:
                    self._cluster_definition['by_name'].append('ANY')
            else:
                raise TypeError

            # Set cluster priority for parser.
            if isinstance(cluster_priority, int):
                self._cluster_definition['priority'] = cluster_priority
            elif cluster_priority is None:
                self._cluster_definition['priority'] = 0
            else:
                raise TypeError

            # Allow cluster to skip sanity check.
            if cluster_is_sane is True:
                self._cluster_definition['sane'] = True
            else:
                self._cluster_definition['sane'] = False

            # Allow cluster to be changed.
            if cluster_is_sane is True:
                self._cluster_definition['dynamic'] = True
            else:
                self._cluster_definition['dynamic'] = False

            # Allow to create cluster with its modifers
            if cluster_createable is True:
                self._cluster_definition['createable'] = True
            else:
                self._cluster_definition['createable'] = False

            if cluster_initialized is True:
                self._cluster_definition['initialized'] = True
            else:
                self._cluster_definition['initialized'] = False

        self._cluster_props = {}

        # -------------------------------------------
        # Modifiers names that can be sometimes used
        # instead of default ones.
        self._cluster_props['by_name'] = []

        # Custom name that can be changed in runtime.
        self._cluster_props['name'] = None

        # Custom tags that can be changed in runtime.
        self._cluster_props['tags'] = []

        # Initialized.
        self._cluster_props['initialized'] = False

        # Modifiers list.
        self._modifiers_list = []

        # Sorting rules.
        self._sorting_rules = []

        # Cluster shouldnt be used, if it is already
        # removed from clusters list.
        self._cluster_removed = False

        # Should this cluster content be shown collapsed in ui?
        # Also stops recursive active_modifier_get_deep()
        self.modcluster_collapsed = True

        # Check cluster sanity.
        if not dont_define_cluster\
                and not self._cluster_definition['sane']\
                and not self.check_this_cluster_sanity():
            raise ValueError('This cluster cant be used.')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self._cluster_removed:
            name = self.get_this_cluster_name()
            result = f"Cluster {name}, {self.get_this_cluster_type()}"
        else:
            result = f"Already removed cluster {self._MODCLUSTER_NAME}"
        return result

    # Cluster name
    @property
    def name(self):
        return self.get_this_cluster_name()

    @name.setter
    def name(self, cluster_name):
        return self.set_this_cluster_custom_name(cluster_name)

    def get_this_cluster_name(self):
        """
        Returns this ModifiersCluster's custom name, or default name.
        """
        self._check_if_cluster_removed()
        if self._cluster_props['name'] is not None:
            return self._cluster_props['name']
        else:
            return self._cluster_definition['name']

    def get_this_cluster_custom_name(self):
        """
        Returns this ModifiersCluster's custom name.
        """
        self._check_if_cluster_removed()
        return self._cluster_props['name']

    def get_this_cluster_default_name(self):
        """
        Returns this ModifiersCluster's default name.
        """
        self._check_if_cluster_removed()
        return self._cluster_definition['name']

    def set_this_cluster_custom_name(self, cluster_name):
        """
        Sets cluster custom cluster name.
        Returns True or False, if cluster is not editable.
        """
        self._check_if_cluster_removed()
        if isinstance(cluster_name, str):
            self._cluster_props['name'] = cluster_name
        else:
            raise TypeError

    # Cluster type
    @property
    def type(self):
        return self.get_this_cluster_type()

    def get_this_cluster_type(self):
        """
        Returns this ModifiersCluster's type
        """
        self._check_if_cluster_removed()
        return self._cluster_definition['type']

    # Collapsed/expanded
    @property
    def collapsed(self):
        return self._cluster_props['collapsed']

    @collapsed.setter
    def collapsed(self, collapsed_val):
        if collapsed_val:
            self._cluster_props['collapsed'] = True
        elif not collapsed_val:
            self._cluster_props['collapsed'] = False

    """
    ===============================
    Methods reserved for subclasses
    ===============================
    """
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

    """
    =========================================
    Cluster subclass-specific additional actions.
    =========================================

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

    """
    ================================================
    Cluster subclass-specific additional interpretation.
    ================================================

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

    # ===========================
    # ModifiersCluster methods
    # ===========================
    def _check_if_cluster_removed(self):
        """
        This method throws an error when trying to access already
        removed cluster.
        """
        if self._cluster_removed:
            raise ValueError(f'Cluster {self} already removed.')

    def is_complex(self):
        """
        Checks if this cluster cant be considered as usual modifier.

        Returns True if modifier cluster consists of more than
        one blender modifier.
        Also returns True if has no modifiers at all.
        """

        if self.get_list_length() != 1:
            return True
        return False

    # TODO: remove
    def has_clusters(self):
        """
        Checks if this cluster have clusters in it.

        Returns False if this cluster consists of modifiers or something
        else.
        """
        return False

    """
    ===========================
    Cluster tags
    ===========================
    """
    def get_this_cluster_tags(self):
        """
        Returns this ModifiersCluster's custom tags, or default tags.
        """
        self._check_if_cluster_removed()
        return self._cluster_definition['tags'] + self._cluster_props['tags']

    def add_tag_to_this_cluster(self, custom_tag):
        """
        Set this ModifiersCluster's custom tags.
        Takes string as an argument.
        Returns True if successfully added tag.
        """
        self._check_if_cluster_removed()
        if isinstance(custom_tag, str):
            if custom_tag not in self._cluster_props['tags']:
                self._cluster_props['tags'].append(custom_tag)
                return True
            else:
                return False
        else:
            raise TypeError

    def remove_tag_from_this_cluster(self, custom_tag):
        """
        Remove this ModifiersCluster's custom tag.
        Takes string as an argument.
        Returns True if successfully removed tag.
        Returns False if no such tag or cant remove.
        """
        self._check_if_cluster_removed()
        y = []
        result = False
        for x in self._cluster_props['tags']:
            if x == custom_tag:
                y.append(x)
                result = True

        for x in y:
            self._cluster_props['tags'].remove(x)

        return result

    """
    ====================
    Initializing cluster
    ====================
    """
    def set_this_cluster_modifiers(self, modifiers):
        """
        Replaces list of modifiers with modifiers.
        Returns True or False, if cluster is not editable.
        """

        self._check_if_cluster_removed()

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
        if self._cluster_props['initialized'] is False:
            self._modifiers_list = modifiers
            self._cluster_props['initialized'] = True
            self._mod = self._modifiers_list[0]
            return True

        # Or allowed to reset modifiers
        elif self._MODCLUSTER_DYNAMIC:
            self._modifiers_list = modifiers
            self._mod = self._modifiers_list[0]
            return True

        else:
            return False

    """
    ================
    Clusters sorting
    ================
    """
    def add_sorting_rule(self, sorting_rule):
        """
        Add new sorting rule for this cluster or
        replace existing one.

        Returns True or False, if cluster not sortable.
        """

        self._check_if_cluster_removed()
        if 'NO_SORT' in self.get_this_cluster_tags():
            return False

        self.remove_sorting_rule(sorting_rule.name)

        self._sorting_rules.append(sorting_rule)
        return True

    def remove_sorting_rule(self, sorting_rule_name):
        """
        Removes sorting rule by name.

        Returns True or False, if no such sorting
        rule.
        """

        self._check_if_cluster_removed()
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

    def get_sorting_rules(self):
        """
        Returns sorting rules for this cluster.
        Returns empty list, if cluster disabled
        sorting.
        """
        self._check_if_cluster_removed()
        if 'NO_SORT' in self.get_this_cluster_tags():
            return []
        else:
            return self._sorting_rules

    # ==========
    # Parsing
    # ==========
    def get_this_cluster_possible_length(self):
        """
        Returns maximum possible modifiers sequence length for this cluster.
        """
        return len(self._cluster_definition['by_type'])

    def get_this_cluster_priority(self):
        """
        Returns priority for this cluster in parsing.
        """
        return self._cluster_definition['priority']

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

        # How many modifiers are correct?
        x = 0

        # How many modifiers should be correct?
        x2 = len(self._cluster_definition['by_type'])

        # Iteration number
        y = 0

        # Iterate over provided modifiers sequence
        for mod in modifiers:

            modifiers_by_type = self._cluster_definition['by_type']

            # Check modifiers by types
            if (modifiers_by_type[y] != ['ANY'])\
                    and (modifiers_by_type[y] != 'ANY'):

                # Check modifier type
                if isinstance(mod, ClusterTrait):
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG CLUSTER TYPE'
                else:
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG ACTUAL MODIFIER TYPE'

            # Use specific names list, if there is one
            if len(self._cluster_props['by_name']) != 0:
                modifiers_by_names\
                        = self._cluster_props['by_name']
            else:
                modifiers_by_names\
                        = self._cluster_definition['by_name']

            # Check name
            if (modifiers_by_names[y] != ['ANY'])\
                    and (modifiers_by_names[y] != 'ANY'):

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

            x += 1
            if x == x2:
                return 'FOUND'
            elif (x < x2) & (x == len(modifiers)):
                return 'CONTINUE'
            y += 1

        # Additional checks reserved for custom types
        additional_checks = self.modcluster_extra_availability_check(
                modifiers)

        if additional_checks is not None:
            return additional_checks

        return None

    # ===================
    # Cluster visibility
    # ===================
    def get_this_cluster_visibility(self):
        """
        Returns list with info about this cluster visability
        """
        self._check_if_cluster_removed()

        y1 = []
        y2 = []
        y3 = []
        y4 = []

        mods = self.get_full_actual_modifiers_list()
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
        self._check_if_cluster_removed()

        if vis_settings is None:
            vis_settings = [None, None, None, None]

        y1, y2, y3, y4 = vis_settings

        # y1 = vis_settings[0]
        # y2 = vis_settings[1]
        # y3 = vis_settings[2]
        # y4 = vis_settings[3]

        mods = self.get_full_actual_modifiers_list()

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
        self._check_if_cluster_removed()
        if vis_settings is None:
            vis_settings = [False, False, False, False]

        if True not in vis_settings:
            return

        old_cluster_vis = self.get_this_cluster_visibility()
        new_cluster_vis = []

        i = 0

        for x in old_cluster_vis:
            if vis_settings[i] is True:
                if x == 'HALF':
                    new_cluster_vis.append(False)
                elif x == 'ON':
                    new_cluster_vis.append(False)
                elif x == 'OFF':
                    new_cluster_vis.append(True)
            else:
                new_cluster_vis.append(None)

            i += 1

        self.set_this_cluster_visibility(new_cluster_vis)

    # =======================================
    # Utility
    # =======================================
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

        self._check_if_cluster_removed()

        # Additional checks
        if not self.check_this_cluster_sanity_custom():
            raise ValueError

        # If specified that cluster is sane
        if self._cluster_definition['sane']:
            return True

        l_1 = self._cluster_definition['by_type']
        len_1 = len(l_1)

        l_2 = self._cluster_definition['by_name']
        len_2 = len(l_2)

        if len(self._cluster_props['by_name']) > 0:
            if len_2 != len(self._cluster_props['by_name']):
                raise ValueError(
                        'Length of specified modifiers names is wrong.')
        if len_1 != len_2:
            raise ValueError(
                    f'Length of types ({l_1}) and names ({l_2}) is different.')
        if len_1 == 0:
            raise ValueError(
                    'Length of modifiers types cant be 0.')
        if self._cluster_definition['by_type'][0] == ['ANY']:
            raise ValueError(
                    'First modifier cant be any, specify modifier type.')
        for mod_types in self._cluster_definition['by_type']:
            if isinstance(mod_types, list):
                if len(mod_types) == 0:
                    raise ValueError('Modifier types length is 0.')
        for mod_names in self._cluster_definition['by_name']:
            if isinstance(mod_names, list):
                if len(mod_names) == 0:
                    raise ValueError('Modifier names length is 0.')
        return True

    def serialize_this_cluster_type(self):
        x = copy.copy(self._cluster_definition)

        if self.has_clusters():
            c = 'ClustersLayer'
        else:
            c = 'ModifiersCluster'

        x.update({'cluster_trait_subclass': f'{c}'})
        result = json.dumps(x)
        return result
