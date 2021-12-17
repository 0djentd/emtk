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

from .clusters_actions import ClusterRequest, ClustersAction


class ClustersController():
    """
    This is object responsible for clusters actions buffer.
    """

    def __init__(self, extended_modifiers_list_obj, *args, **kwargs):
        self.e = extended_modifiers_list_obj

    def get_required_actions(self, action, already_allowed_actions=None):
        """
        Asks all clusters if action is allowed.

        already_allowed_actions is a list of actions that
        should not be added to result.

        Returns actions that are required to allow it by
        all clusters.

        If action is allowed by all clusters, returns empty list.
        """

        # Check arguments
        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')
        if already_allowed_actions is None:
            already_allowed = []
        else:
            already_allowed = already_allowed_actions
        if not isinstance(already_allowed, list):
            raise TypeError(f'Should be list {type(already_allowed)}')
        for x in already_allowed:
            if not isinstance(x, ClustersAction):
                raise TypeError(f'Should be ClustersAction {type(x)}')
            if x['status'] != 'ALLOWED':
                raise ValueError

        result = []

        # Get required actions.
        for x in self.e.get_full_list():
            print(f'Asking {x}')
            answer = x.ask(action)
            if isinstance(answer, ClusterRequest):
                print(f'Got answer {answer["require"]}')
                for a in answer['require']:
                    add = True
                    for x in already_allowed:
                        if x['subject'] is a['subject']:
                            add = False
                    # Recursive search for required actions.
                    if add:
                        result.extend(
                                self.get_required_actions(a, already_allowed))

        # After loop, this action will be allowed, because there will be
        # required actions to allow it in result.
        action['status'] = 'ALLOWED'
        result.append(action)
        return result

    def do(self, request):
        """
        Finds required actions and performs them.
        """
        actions = []
        for x in request['require']:
            actions.extend(self.get_required_actions(x))

        for x in actions:
            self.apply_action(x)

    def apply_action(self, action):
        """
        Performs ClustersAction on this ClustersList.
        """
        layer = self.e.get_cluster_cluster_belongs_to(action['subject'])
        layer.perform_action(action)


# def remove(self, cluster):
#     """
#     Removes cluster from this list.
#     """
# 
#     y = ClustersAction('REMOVE', cluster)
# 
#     x = ClusterRequest(self, y)
# 
#     self.controller.do(x)

# def ask(self, question):
#     """
#     Returns actions required to allow action, if it is not
#     allowed.
#     Can return empty list.
#     """
#     if not isinstance(question, ClustersAction):
#         raise TypeError
# 
#     if not self.has(x['subject']):
#         return
# 
#     x = question
# 
#     q = x['verb']
# 
#     if self._MODCLUSTER_DYNAMIC is False:
#         x = [ClustersAction(self, 'REMOVE')]
#         return x
# 
#     # if q == 'REMOVE':
#     #     return self._dry_remove(x['subject'])
#     # elif q == 'ADD':
#     #     return self._dry_add(x['object_type'])
#     # elif q == 'MOVE':
#     #     return self._dry_move(x['subject'], x['direction'])
#     # elif q == 'CONSTRUCT':
#     #     return self._dry_construct(x['subject_list'])
#     # elif q == 'DECONSTRUCT':
#     #     return self._dry_deconstruct(x['subject'])

# def perform_action(self, action):
#     if action['subject'] not in self._modifiers_list:
#         raise ValueError
# 
#     x = action['verb']
# 
#     if x == 'REMOVE':
#         self._delete(action)
#     elif x == 'MOVE':
#         self._move(action)
#     elif x == 'DECONSTRUCT':
#         self._deconstruct(action)

# def get_trace_to(self, cluster):
#     """
#     Returns trace to cluster, starting from this layer.
#     Example:
#     [TripleBevel, DoubleBevel, DefaultBevel]
#     """
#
#     result = []
#     f = True
#     c = cluster
#     while f:
#         layer = self.get_cluster_cluster_belongs_to(c)
#         result.append(layer)
#         if layer is self:
#             f = False
#         c = layer
#     result.revert()
#     return result
