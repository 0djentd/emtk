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

from .modifiers_cluster import ModifiersCluster


# This class should inherit exactly one of following classes:
# ModifiersCluster, ClustersLayer, ClustersGroup
class SampleCluster(ModifiersCluster):
    """
    This is example of custom cluster type.
    """
    def __init__(self, bevel_name='Big Bevel', *args, **kwargs):
        # Most essential cluster variables can be created using
        # ModififersCluster constructor.
        # It has some type and sanity checks to
        # simplify creating new cluster types.
        super().__init__(cluster_name='Triple Bevel',
                         cluster_type='TRIPLE_BEVEL',
                         modifiers_by_type=[
                             ['BEVEL'], ['BEVEL'], ['BEVEL']],
                         modifiers_by_name=[
                             [bevel_name], ['ANY'], ['ANY']],
                         cluster_priority=50,
                         cluster_createable=True,
                         **kwargs
                         )

        # If for some reason you cant use ModifiersCluster constructor
        # method, you need to define this variables manually.
        # For list of them, look at ModifiersCluster's
        # constructor.
        # super().__init__(*args, **kwargs)

    # ============================
    # ModifiersClustersList actions.
    # TODO: create some examples of this methods usecases.
    # ============================
    def cluster_being_moved(self, modifiers_clusters_list, direction):
        """
        Method reserved for object-specific actions on cluster move in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to and direction
        as one of UP or DOWN.

        Returns True if cluster can be successfully moved.
        Returns False if cluster shouldnt be moved.
        """
        # Increase this cluster's first modifier segments
        # count every time cluster moved up in list.
        if direction == 'UP':
            self.get_first().segments += 1
        elif direction == 'DOWN':
            self.get_first().segments -= 1
        return True

    def cluster_being_deconstructed(self, clusters_list):
        """
        Method reserved for object-specific actions on cluster
        deconstruction in ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully moved.
        Returns False if cluster shouldnt be moved.
        """
        return False

    def cluster_being_removed(self, modifiers_clusters_list):
        """
        Method reserved for object-specific actions on cluster remove in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully removed.
        Returns False if cluster shouldnt be removed.
        """
        # This will not allow to remove this cluster, if
        # total amount of segments is more than 40.
        segments = 0
        for x in self.get_list():
            segments += x.segments
        if segments > 40:
            return False
        return True

    def cluster_being_applied(self, modifiers_clusters_list):
        """
        Method reserved for object-specific actions on cluster apply in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully applied.
        Returns False if cluster shouldnt be applied.
        """
        # Set bevel segments count to 30 before applying cluster.
        for x in self.get_list():
            x.segments = 30
        return True

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
        # This will only allow to use bevels with more than 3 segments
        # in this cluster.
        for mod in modifiers:
            if not mod.segments > 3:
                return False
        return

    def check_this_cluster_sanity_custom(self):
        """
        Method reserved for clustertype-specific sanity checks.

        Should return True or False.
        """
        return True
