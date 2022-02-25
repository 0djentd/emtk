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

from ....sorting_rule import SortingRule


class SortableClustersListTrait():
    """
    Base class for ClusterLists that should be able to sort clusters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_sorting_rules(self):
        """
        Returns all cluster names with all their sorting rules for this layer.

        Result looks like this:
        [['Bevel.123', sorting_rule],
         ['Bevel.124', sorting_rule]]
        """

        sorting_rules = []
        for x in self._data:
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
        Argument can be SortingRule or list of SortingRules.

        Returns number of rules removed.
        """
        if isinstance(sorting_rules, SortingRule):
            x = sorting_rules
            sorting_rules = [x]
        elif isinstance(sorting_rules, list):
            for x in sorting_rules:
                if not isinstance(x, SortingRule):
                    raise TypeError(f'{x} should be a SortingRule.')
        else:
            raise TypeError(f'{sorting_rules} should be a SortingRules list.')

        i = 0
        for x in self._data:
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

        # First element is priority
        # Second is cluster name that should be before third
        # This lists looks like this:
        # [[4, 'Bevel.123', 'Bevel.124'],
        #  [4, 'Bevel.123', 'Boolean.123'],
        #  [3, 'Bevel.129', 'Bevel.126']]
        clusters_order = []

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

            for y in x[1].after_clusters:
                e = x[1].sorting_rule_priority + y + x[0]
                if e not in clusters_order:
                    clusters_order.append(e)

            for y in x[1].before_clusters:
                e = x[1].sorting_rule_priority + x[0] + y
                if e not in clusters_order:
                    clusters_order.append(e)

        # Sort by priority
        clusters_that_should_be_first.sort()
        clusters_that_should_be_last.sort()
        clusters_order.sort()

        # Lists without duplicates sorted by priority
        first_clusters_list = []
        last_clusters_list = []
        clusters_order_list = []

        # Remove duplicates with lower priority
        for x in clusters_that_should_be_first:
            if x[1] not in first_clusters_list:
                first_clusters_list.append(x[1])

        for x in clusters_that_should_be_last:
            if x[1] not in last_clusters_list:
                last_clusters_list.append(x[1])

        for x in clusters_order:
            z = False
            for y in clusters_order_list:
                if (y[1] == x[1]) & (y[2] == x[2]):
                    z = True
            if not z:
                clusters_order_list.append(x)

        # Move clusters to first or last position in list.
        # Moves clusters with less priority first.
        for x in reversed(first_clusters_list):
            mod = self.get_cluster_by_name(x)
            self.move_to_index(-1, mod)

        for x in reversed(last_clusters_list):
            mod = self.get_cluster_by_name(x)
            self.move_to_index(0, mod)

    # TODO: does it works?
    def move_cluster_before_cluster(
            self, cluster_1, cluster_2, direction='UP'):
        """
        If direcion is 'UP' moves cluster_1 before cluster_2.
        If direcion is 'UP' moves cluster_2 after cluster_1.
        """
        if not isinstance(cluster_1, str):
            raise TypeError

        if not isinstance(cluster_2, str):
            raise TypeError

        f_1 = False
        f_2 = False
        i = 0

        for x in self._data:
            if x.name == cluster_1:
                f_1 = True
                mod1 = x
            if x.name == cluster_2:
                f_2 = True
                mod2 = x

            # If found cluster_1 first, it is already before cluster_2.
            if f_1 and not f_2:
                return True

            # If found cluster_2, count how many iterations it takes
            # to find cluster_1.
            elif f_2 and not f_1:
                i += 1

            elif f_1 and f_2:
                break

        # Probably no such cluster found.
        if not f_1 or not f_2:
            raise ValueError

        for x in range(i):
            if direction == 'UP':
                self.move_up(mod2)
            elif direction == 'DOWN':
                self.move_down(mod1)
        return True
