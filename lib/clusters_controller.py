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

    required_actions = []
    allowed_actions = []

    def __init__(self, extended_modifiers_list_obj, *args, **kwargs):
        self.e = extended_modifiers_list_obj

    def do(self, request):
        """
        Finds required actions and performs them.
        """
        actions = []
        for x in request['require']:
            actions.extend(self.get_required_actions(x))
        for x in reversed(actions):
            self.apply_action(x)

    def apply_action(self, action):
        """
        Performs ClustersAction on this ClustersList.
        """
        layer = self.e.get_cluster_cluster_belongs_to(action['subject'])
        layer.perform_action(action)

    # ============================
    # CLUSTERS ACTIONS SOLVER
    # ============================
    def get_required_actions(self, action):
        """
        Asks all clusters if action is allowed.

        Returns actions that are required to allow it by
        all clusters.
        """

        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')

        print(f'Trying to recursively get actions required for {action}')
        print(f'{action["subject"]}')

        self.required_actions.append(action)

        i = 0

        while len(self.required_actions) > 0:

            print(f'Recursive action solver iteration {i}')
            print(f'Already required actions is {self.required_actions}')
            print(f'Already allowed actions is {self.allowed_actions}')

            # Allowed action is an action that will be performed
            # to allow initial action. It is an allowed action too.
            # It requires no additional actions.

            # Required action is an action that will be performed,
            # but still not checked for being allowed
            # by all clusters.
            # Basically, this is an action that can potentially require
            # additional actions.

            # List of changes after iteration
            remove_req_actions = []
            add_req_actions = []

            # Get new list of required actions for
            # already existing required actions
            for x in self.required_actions:
                a = self._get_required_actions_recursive(x)

                # This action can be allowed.
                if len(a) == 0:
                    self.allowed_actions.append(x)
                    print(f'Allowed {x}')
                    remove_req_actions.append(x)

                # This action requires additional actions.
                else:
                    print(f'Not allowed {x}')
                    add_req_actions.extend(a)

            for x in remove_req_actions:
                self.required_actions.remove(x)

            for x in add_req_actions:

                # Dont add duplicates
                # TODO: should also check in allowed actions?
                already_there = False
                for y in self.required_actions:
                    if y['verb'] == x['verb']\
                            and y['subject'].name == x['subject'].name:
                        already_there = True
                if already_there is False:
                    self.required_actions.append(x)

            i += 1
            if i > 100:
                raise ValueError

        result = self.allowed_actions
        self.allowed_actions = []

        # Check result
        if len(self.required_actions) != 0:
            raise ValueError
        if len(result) == 0:
            raise ValueError
        print(f'Actions is {result}')

        # Remove duplicates
        remove = []
        for x in result:
            d = 0
            for y in result:
                if y['verb'] == x['verb']\
                        and y['subject'].name == x['subject'].name:
                    if d < 1:
                        d += 1
                    elif x not in remove:
                        remove.append(y)
        for x in remove:
            result.remove(x)

        print(f'Actions is {result}')
        return result

    def _get_required_actions_recursive(self, action):

        # Check arguments
        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')
        if action['subject'] is self.e:
            raise ValueError

        result = []

        # Get required actions.
        clusters = self.e.get_full_list()
        for x in clusters:
            print(f'Asking {x}')
            answer = x.ask(action)
            if isinstance(answer, ClusterRequest):
                print(f'Got answer {answer["require"]}')
                result.extend(answer['require'])

        if len(clusters) == 0:
            raise ValueError

        # Remove duplicates.
        remove = []
        for x in result:
            for y in self.required_actions:
                if x == y:
                    remove.append(x)

        for x in remove:
            print('Removing action from result')
            result.remove(x)
        return result

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
