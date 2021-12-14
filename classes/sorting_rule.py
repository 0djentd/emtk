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

import random


class SortingRule():
    """
    Base class for cluster sorting rules.
    """

    def __init__(self,
                 s_name=None, *,
                 sorting_rule_priority=None,
                 after_clusters=None,
                 before_clusters=None,
                 last_cluster=None,
                 first_cluster=None,
                 sorting_rule_is_sane=None,
                 *args, **kwargs
                 ):

        # Sorting rule name. Should be unique.
        if s_name is None:
            r = random.randint(0, 99999999)
            self.name = f'DefaultSortingRuleName{r}'
        else:
            self.name = s_name

        # Skip sanity checks for this rule
        if sorting_rule_is_sane:
            self.__SORTING_RULE_IS_SANE = True
        else:
            self.__SORTING_RULE_IS_SANE = False

        # Sorting priority, used when some of the rules conflict
        # with each other.
        if sorting_rule_priority is None:
            self.sorting_rule_priority = 0
        elif isinstance(sorting_rule_priority, int):
            self.sorting_rule_priority = sorting_rule_priority
        else:
            raise TypeError

        # Names of cluster types this cluster should be placed after.
        # THIS SHOULD BE _MODCLUSTER_TYPE, NOT _MODCLUSTER_NAME
        if after_clusters is None:
            self.after_clusters = []
        elif isinstance(after_clusters, list):
            for x in after_clusters:
                if not isinstance(x, str):
                    raise TypeError
            self.after_clusters = after_clusters
        else:
            raise TypeError

        # Names of cluster types this cluster should be placed before.
        if before_clusters is None:
            self.before_clusters = []
        elif isinstance(before_clusters, list):
            for x in before_clusters:
                if not isinstance(x, str):
                    raise TypeError
            self.before_clusters = before_clusters
        else:
            raise TypeError

        # Should this cluster be placed first in the list?
        if first_cluster:
            self.first_cluster = True
        else:
            self.first_cluster = False

        # Should this cluster be placed last in the list?
        if last_cluster:
            self.last_cluster = True
        else:
            self.last_cluster = False

    @property
    def name(self):
        return self._sorting_rule_name

    @name.setter
    def name(self, s_name):
        if isinstance(s_name, str):
            self._sorting_rule_name = s_name
        else:
            raise TypeError

    def check_sorting_rule_sanity(self):
        """
        Checks sorting rule for usual errors.
        Return True or False.
        """

        if self._SortingRule__SORTING_RULE_IS_SANE:
            return True

        for x in self.after_clusters:
            if not isinstance(x, str):
                return False

        for x in self.before_clusters:
            if not isinstance(x, str):
                return False

        if not isinstance(self.sorting_rule_priority, int):
            return False

        if self.last_cluster and self.first_cluster:
            return False

        for x in self.after_clusters:
            if x in self.before_clusters:
                return False
        return True
