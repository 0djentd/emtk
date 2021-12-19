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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from .dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False


class ClustersController():
    """
    This is object responsible for clusters actions buffer.
    """

    def __init__(self, extended_modifiers_list_obj, *args, **kwargs):
        self.e = extended_modifiers_list_obj
        self.allowed_actions = []
        self.required_actions = []

    def do(self, request):
        """
        Finds actions required for request actions, solves and performs them.
        """

        for x in request.require:
            self.e.check_obj_ref(x.subject)

        actions = []
        for x in request.require:
            actions.extend(self.get_required_actions(x))

        actions = self._sort_actions_by_layer_depth(actions)

        for x in actions:
            self._apply_action(x)

    def check_action_solving(self, request, try_actions):
        """
        Checks if request will have try_actions in it after solving.

        Returns False, if it has try_actions.
        Returns True, if not.
        """
        for x in request.require:
            self.e.check_obj_ref(x.subject)

        actions = []
        for x in request.require:
            actions.extend(self.get_required_actions(x))
        for x in actions:
            for t in try_actions:
                if x == t:
                    return False
        return True

    def _sort_actions_by_layer_depth(self, actions):
        """
        Returns actions sorted by reversed layer depth.
        """
        result = []
        d = []
        for x in actions:
            d.append([self.e.get_depth(x.subject), x])
        d.sort(key=lambda z: z[0])
        for x in d:
            result.append(x[1])
        result.reverse()
        return result

    def _apply_action(self, action):
        """
        Performs ClustersAction on this ClustersList.
        """
        layer = self.e.get_cluster_cluster_belongs_to(action.subject)
        layer.do(action)

    # ============================
    # CLUSTERS ACTIONS SOLVER
    # ============================
    def get_required_actions(self, action):
        """
        Returns actions that are required to allow action by
        all clusters.
        """

        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')

        self.e.check_obj_ref(action.subject)

        self.required_actions.append(action)

        if len(self.allowed_actions) != 0 or len(self.required_actions) != 1:
            raise ValueError('One of actions lists is wrong len')

        self.e.check_obj_ref(self.required_actions[0].subject)

        i = 0

        while len(self.required_actions) > 0:

            # print('')
            # print(f'Recursive action solver iteration {i}')
            # print(f'Already required actions is {self.required_actions}')
            # print(f'Already allowed actions is {self.allowed_actions}')

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
                    remove_req_actions.append(x)

                # This action requires additional actions.
                else:
                    add_req_actions.extend(a)

            for x in remove_req_actions:
                self.required_actions.remove(x)

            for x in add_req_actions:
                self.required_actions.append(x)

            i += 1
            if i > 100:
                raise ValueError('Clusters actions solver depth limit')

        result = self.allowed_actions
        self.allowed_actions = []

        # Check result
        if len(self.required_actions) != 0:
            raise ValueError
        if len(self.allowed_actions) != 0:
            raise ValueError
        if len(result) == 0:
            raise ValueError
        return result

    def _get_required_actions_recursive(self, action):

        # Check arguments
        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')
        if action.subject is self.e:
            raise ValueError
        self.e.check_obj_ref(action.subject)

        result = []

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        # Get list of clusters to ask.
        if isinstance(action.subject, modifiers_type):
            clusters = []
            clusters.extend(self.e.get_trace_to(action.subject))
            clusters.append(self.e)
        else:
            clusters = []
            clusters.append(action.subject)
            clusters.extend(self.e.get_trace_to(action.subject))
            if action.subject.has_clusters():
                clusters.extend(action.subject.get_full_list())
            clusters.append(self.e)
        if len(clusters) == 0:
            raise ValueError

        # Ask clusters.
        for x in clusters:
            answer = x.ask(action)
            if isinstance(answer, ClusterRequest):
                result.extend(answer.require)

        # Remove duplicates.
        remove = []
        for x in result:
            for y in self.required_actions + self.allowed_actions:
                if x.subject == y.subject and x.verb == y.verb:
                    if x not in remove:
                        remove.append(x)
        for x in remove:
            result.remove(x)
        return result
