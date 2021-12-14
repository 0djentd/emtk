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

from ..clusters_layer import ClustersLayer


# TODO: this class should be removed
class BevelCluster(ClustersLayer):

    _MODCLUSTER_ID = 1300

    def __init__(self, priority=0):

        super().__init__()

        # Type that should be returned to ModifiersList
        self._MODCLUSTER_TYPE = 'BEVEL_CLUSTER'

        # Name that should be returned to ModifiersList
        self._MODCLUSTER_NAME = 'Double Bevel Cluster'

        self._MODCLUSTER_CREATEABLE = False

        self._MODCLUSTER_MODIFIERS_BY_TYPE = [
                ['TRIPLE_BEVEL'], ['TRIPLE_BEVEL']]

        self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES = [
                ['ANY'], ['ANY']]

        self._MODCLUSTER_PRIORITY = priority
