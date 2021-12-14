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

from ..sorting_rule import SortingRule


class SortableClustersList():
    """
    Base class for ClusterLists that should be able to sort clusters.
    """

    def get_all_sorting_rules(self):
        """
        Returns all cluster names with all their sorting rules for this layer.

        Result looks like this:
        [['Bevel.123', sorting_rule],
         ['Bevel.124', sorting_rule]]
        """
        sorting_rules = []
        for x in self.get_list():
            for rule in x.get_sorting_rules():
                sorting_rules.append(x.name, rule)
        return sorting_rules

    def check_all_sorting_rules_sanity(self):
        """
        Checks all sorting rules sanity and returns list of rules
        that failed it.
        """

        result = []
        for x in self.get_all_sorting_rules():
            if not x[1].check_sorting_rule_sanity():
                result.append(x)
        return result

    def remove_sorting_rules_from_all_clusters(self, sorting_rules):
        """
        Removes sorting_rules from all clusters on this layer.
        Argument can be SortingRule or list of SortingRule.
        Returns number of rules removed.
        """
        if isinstance(sorting_rules, SortingRule):
            x = sorting_rules
            sorting_rules = [x]
        if isinstance(sorting_rules, list):
            for x in sorting_rules:
                if not isinstance(x, SortingRule):
                    raise TypeError
        i = 0
        for x in self.get_list():
            for y in sorting_rules:
                x.remove_sorting_rule(y)
                i += 1
        return i

    def apply_sorting_rules(self):
        """
        Apply sorting rules on this layer.
        Returns True or False, if cant sort properly.
        """

        sorting_rules = self.get_all_sorting_rules()
        if len(sorting_rules) == 0:
            return True

        # Cluster names that should be first or last
        # First collumn is rule priority, second is cluster name.
        # This lists looks like this:
        # [[5, 'Bevel.0124'],
        #  [4, 'Bevel.0123'],
        #  [3, 'Bevel.0125'],
        #  [1, 'Array'],
        #  [1, 'Bevel.0123']]
        clusters_that_should_be_first = []
        clusters_that_should_be_last = []

        # Get lists
        for x in sorting_rules:
            if x[1].last_cluster:
                if x[0] not in clusters_that_should_be_last:
                    clusters_that_should_be_last.append(
                            x[1].sorting_rule_priority, x[0])

            if x[1].first_cluster:
                if x[0] not in clusters_that_should_be_first:
                    clusters_that_should_be_first.append(
                            x[1].sorting_rule_priority, x[0])

        # Sort by priority
        clusters_that_should_be_first.sort()
        clusters_that_should_be_last.sort()

        # Lists without duplicates
        first_clusters_list = []
        last_clusters_list = []

        for x in clusters_that_should_be_first:
            if x[1] not in first_clusters_list:
                first_clusters_list.append(x[1])

        for x in clusters_that_should_be_last:
            if x[1] not in last_clusters_list:
                last_clusters_list.append(x[1])

        # Move clusters to first or last position in list.
        # Moves clusters with less priority first.
        for x in reversed(first_clusters_list):
            mod = self.get_cluster_by_name(x)
            self.move_to_index(-1, mod)

        for x in reversed(last_clusters_list):
            mod = self.get_cluster_by_name(x)
            self.move_to_index(0, mod)
