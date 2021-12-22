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

from ...modifiers_list import ModifiersList

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ....dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False

from ....controller.actions import (
                                    ClusterRequest,
                                    ClustersAction
                                    )


class ObjectClustersListTrait():
    """
    This is class that can be used to add methods
    for editing object's modifiers to ClustersList.
    """

    def __init__(self, obj=None, *args, no_obj=None, **kwargs):
        super().__init__(*args, **kwargs)

        # if not no_obj:
        #     if obj is None:
        #         raise ValueError

        # self._object = obj

    # ===================================
    # Changing modifiers_list of an object
    # ===================================

    # def move_clusters(self, clusters, direction):
    #     """
    #     Moves list of clusters.

    #     Returns True or False.
    #     """
    #     if not isinstance(clusters, list):
    #         raise TypeError

    #     # Dont move, if modifier is last or first.
    #     if direction == 'UP':
    #         x = self.get_index(clusters[0])
    #         if x == 0:
    #             return False
    #     elif direction == 'DOWN':
    #         x = self.get_index(clusters[-1])
    #         if x == self.get_list_length() - 1:
    #             return False
    #     else:
    #         raise ValueError

    #     clusters_to_move = clusters

    #     if direction == 'DOWN':
    #         clusters_to_move = clusters_to_move.reverse()

    #     for cluster in clusters_to_move:
    #         if direction == 'UP':
    #             if not self.move_up(cluster):
    #                 return False
    #         elif direction == 'DOWN':
    #             if not self.move_down(cluster):
    #                 return False
    #     return True

    # def move_to_index(self, mod, i):
    #     """
    #     Moves cluster to index.

    #     Returns True if moved modifier.
    #     Returns False if any errors.
    #     """
    #     # TODO: not tested
    #     if i < self.get_list_length():
    #         m_i = self.get_index(mod)
    #         d_i = i - m_i
    #         x = 0
    #         if d_i > 0:
    #             while x <= d_i:
    #                 self.move_up(mod)
    #                 x += 1
    #             return True
    #         elif d_i < 0:
    #             while x >= d_i:
    #                 self.move_up(mod)
    #                 x -= 1
    #             return True
