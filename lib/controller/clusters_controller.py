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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

from .actions import (
                      ClusterRequest,
                      ClustersAction,
                      ClustersCommand,
                      ClustersBatchCommand
                      )


class ClustersController():
    """
    This is object responsible for clusters actions solver.
    """

    def __init__(self, extended_modifiers_list_obj, *args, **kwargs):
        self.e = extended_modifiers_list_obj

    def do(self, command):
        """
        Finds actions required for action, command or a batch, creates
        commands in a batch, solves and performs them.
        """
        if not isinstance(command, ClustersBatchCommand):
            if not isinstance(command, ClustersCommand):
                if not isinstance(command, ClustersAction):
                    raise TypeError
                else:
                    batch = ClustersBatchCommand(
                            ClustersCommand(command))
            else:
                batch = ClustersBatchCommand(command)
        else:
            batch = command

        self._solve_batch(batch)

        self._apply_batch(batch)

    # ==============
    # Solver
    # ==============
    def _solve_batch(self, batch):
        """
        Solves batch command.

        Returns None.
        """
        if not isinstance(batch, ClustersBatchCommand):
            raise TypeError

        s = True

        # Solve commands.
        while s:
            new_commands = []
            for x in batch.commands:

                # Solve command.
                if x.status == 'NOT_SOLVED':
                    self._solve_command(x)

                # Add its dependencies to batch, if any.
                if x.status == 'HAS_DEPENDENCIES':
                    for y in x.dependencies:
                        if y not in batch.commands:
                            new_commands.append(y)

            if len(new_commands) == 0:
                s = False
            else:
                batch.commands.extend(new_commands)

        # Sort commands
        batch.commands = self._sort_commands_by_layer_depth(
                batch.commands)

        # Check result.
        for x in batch.commands:
            if x.status != 'ALLOWED' and x.status != 'HAS_DEPENDENCIES':
                raise ValueError(f'This is not correct status {x.status}')
            for y in x.dependencies:
                if y not in batch.commands:
                    raise ValueError

    def _solve_command(self, command):
        """
        Solves all actions in command. Adds dependencies, if any.

        Returns None.
        """

        if not isinstance(command, ClustersCommand):
            raise TypeError

        self.e.check_obj_ref(command.initial_action.subject)

        # Allowed action is an action that will be performed
        # to allow initial action. It is an allowed action too.
        # It requires no additional actions.
        allowed_actions = []

        # Required action is an action that will be performed,
        # but still not checked for being allowed
        # by all clusters.
        # Basically, this is an action that can potentially require
        # additional actions.
        required_actions = [command.initial_action]

        # Any actions that is not of initial_action type
        # are considered dependency.

        i = 0

        f = False

        while not f:
            # List of changes to required actions list after iteration
            remove_req_actions = []
            add_req_actions = []

            # Get new list of required actions for
            # all already existing required actions
            for action in required_actions:
                answer = self._ask_clusters(action)

                # Remove duplicates.
                remove = []
                for x in answer:
                    for y in required_actions + allowed_actions:
                        if x.subject == y.subject\
                                and x.verb == y.verb:
                            if x not in remove:
                                remove.append(x)
                for x in remove:
                    answer.remove(x)

                # This action can be allowed, if every new
                # action is a duplicate.
                if len(answer) == 0:
                    allowed_actions.append(action)
                    remove_req_actions.append(action)

                # This action requires additional actions.
                else:
                    add_req_actions.extend(answer)

            # Change required actions list.
            for x in remove_req_actions:
                required_actions.remove(x)

            for x in add_req_actions:
                required_actions.append(x)

            if len(required_actions) == 0:
                f = True

            i += 1
            if i > 100:
                raise ValueError('Clusters actions solver depth limit')

        if len(required_actions) != 0:
            raise ValueError
        if len(allowed_actions) == 0:
            raise ValueError

        result = allowed_actions

        # Sort actions.
        result = self._sort_actions_by_layer_depth(
                result)

        # Filter dependencies.
        dependencies = []
        new_commands = []
        for x in result:
            if x.verb != command.initial_action.verb:
                dependencies.append(x)

        for x in dependencies:
            result.remove(x)
            new_commands.append(ClustersCommand(x))

        command.actions = result
        command.dependencies.extend(new_commands)

    def _ask_clusters(self, action):
        """
        Asks clusters about action.

        Returns list of additional actions and commands.
        """

        # Check arguments
        if not isinstance(action, ClustersAction):
            raise TypeError(f'Should be ClustersAction {type(action)}')
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
        return result

    # =========
    # Applying
    # =========
    def _apply_batch(self, batch):
        print(f'Applying {batch}')
        for x in batch.commands:
            self._apply_command(x)

    def _apply_command(self, command):
        print(f'Applying {command}')
        for x in command.actions:
            self._apply_action(x)

    def _apply_action(self, action):
        layer = self.e.get_cluster_cluster_belongs_to(action.subject)
        print(f'Applying {action} on layer {layer}')
        layer.do(action)

    # ==========
    # Utils
    # ==========
    def _sort_commands_by_layer_depth(self, commands):
        result = []
        d = []
        for x in commands:
            d.append([self.e.get_depth(x.initial_action.subject), x])
        d.sort(key=lambda z: z[0])
        for x in d:
            result.append(x[1])
        result.reverse()
        return result

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
