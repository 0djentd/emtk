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

import json
import logging

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False

from .actions import (
    ClusterRequest,
    ClustersAction,
    ClustersCommand,
    ClustersBatchCommand
)

from ..lists.traits.clusters.clusters_list import ClustersListTrait

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ClustersController():
    """This is object responsible for clusters actions solver."""

    def __init__(self, extended_modifiers_list_obj, *args, **kwargs):
        self.e = extended_modifiers_list_obj

    # TODO: not add additional command to batch if its initial action anywhere
    # in batch already.
    def do(self, command):
        """
        Finds actions required for action, command or a batch, creates
        commands in a batch, solves and performs them.
        """
        if not isinstance(command, list):
            commands = [command]
        else:
            commands = command

        for command in commands:
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

    # Solver
    def _solve_batch(self, batch):
        """
        Solves batch command.

        Returns None.
        """
        if not isinstance(batch, ClustersBatchCommand):
            raise TypeError
        logger.debug(f'Solving {batch}')

        s = True

        # Solve commands.
        while s:
            # This is commands that should be added after command.
            new_commands = []
            # This is commands that should be added before command.
            new_dependencies = []
            for x in batch.commands:

                # Solve command.
                if x.status == 'NOT_SOLVED':
                    self._populate_command_actions(x)
                    new_dependencies.extend(self._get_command_deps(x))
                    new_commands.extend(self._solve_dependencies(x))

            # TODO: wrong index?
            for x in reversed(new_dependencies):
                i = batch.commands.index(x[0])
                batch.commands.insert(i, x[1])
            for x in new_commands:
                i = batch.commands.index(x[0])
                batch.commands.insert(i+1, x[1])

            if len(new_commands) == 0 and len(new_dependencies) == 0:
                s = False

        # Check result.
        for x in batch.commands:
            if x.status != 'ALLOWED':
                raise ValueError(f'This is not correct status {x.status}')

    def _populate_command_actions(self, command, *args, **kwargs):
        """
        Adds actions for command's initial action subject's
        clusters and modifiers to command.
        """

        logger.debug(f'Populating {command}')

        if isinstance(command.initial_action.subject, Modifier):
            command.actions = [command.initial_action]
            return command

        actions = []
        if command.affect_clusters:
            if isinstance(command.initial_action.subject, ClustersListTrait):

                # Reverse actions sorting on layer, looks like this:
                # layer 0: doublebevel --> doublebevel
                # layer 1: bevel1 bevel2 --> bevel2 bevel1
                # Used when moving modifiers.
                # Later in _sort_actions actions list are being reversed again.
                if not command.reverse_by_layer:
                    clusters = command.initial_action.subject.all_clusters()
                    clusters = reversed(clusters)
                else:
                    clusters = command.initial_action.subject.all_clusters()
                logger.debug(f'Adding clusters actions for {clusters}')
                for x in clusters:
                    a = ClustersAction(command.initial_action.verb, x)
                    a.props = command.initial_action.props
                    a.dry = command.dry_clusters
                    logger.debug(f'adding {a}')
                    actions.append(a)
            else:
                o = command.initial_action.subject
                logger.debug(
                    f'Not adding clusters actions, {o} has no clusters.')

        if command.affect_modifiers:
            if not command.reverse_by_layer:
                modifiers = command.initial_action.\
                    subject.all_modifiers()
                modifiers = reversed(modifiers)
            else:
                modifiers = command.initial_action.\
                    subject.all_modifiers()

            logger.debug(f'Adding modifiers actions for {modifiers}')
            for x in modifiers:
                a = ClustersAction(command.initial_action.verb, x)
                a.props = command.initial_action.props
                a.dry = command.dry_modifiers
                logger.debug(f'adding {a}')
                actions.append(a)

        actions = self._sort_actions_by_layer_depth(
            actions)
        logger.debug(f'{actions}')
        command.actions = actions
        logger.debug(f'Populated {command}')
        return command

    def _get_command_deps(self, command):
        """
        Returns commands that should be performed before command.

        Example:
        [[initial_command, commands_to_add]
         [initial_command, commands_to_add_2]]
        """

        deps = []

        for x in command.actions:
            if not isinstance(x.subject, Modifier):
                answer = x.subject.ask(x)
                if answer is not None:
                    for y in answer.require:
                        if not isinstance(y, ClustersCommand):
                            raise TypeError
                    deps.extend(answer.require)
        result = []
        for y in deps:
            result.append([command, y])
        return result

    def _solve_dependencies(self, command):
        """
        Returns commands that should be performed after command.

        Example:
        [[initial_command, commands_to_add]
         [initial_command, commands_to_add_2]]
        """
        for x in reversed(self.e.get_trace_to(command.initial_action.subject)):
            answer = x.ask(command.initial_action)
            if isinstance(answer, ClusterRequest):
                if len(answer.require) != 0:
                    for y in answer.requiere:
                        if not isinstance(y, ClustersCommand):
                            raise TypeError
                    result = []
                    for y in answer.require:
                        result.append([command, y])
                    return result
        return []

    # Applying
    # TODO: to be removed

    def _apply_batch(self, batch):
        logger.debug(f'Applying {batch}')
        for x in batch.commands:
            self._apply_command(x)

    def _apply_command(self, command):
        logger.debug(f'Applying {command}')
        for x in command.actions:
            self._apply_action(x)

    def _apply_action(self, action):
        # TODO: this is for dependency commands, that can potentially
        # remove action subject.
        if action.subject not in self.e.all_elements():
            return

        layer = self.e.get_cluster_or_layer(action.subject)
        logger.debug(f'Applying {action} on layer {layer}')
        layer.do(action)

    # Utils

    def _sort_commands_by_layer_depth(self, commands):
        result = []
        d = []
        for x in commands:
            d.append([len(self.e.get_trace_to(x.initial_action.subject)), x])
        d.sort(key=lambda z: z[0])
        for x in d:
            result.append(x[1])
        result.reverse()
        return result

    def _sort_actions_by_layer_depth(self, actions):
        """
        Returns actions sorted by reversed layer depth
        (modifiers clusters first, then layers).
        """
        result = []
        d = []
        for x in actions:
            d.append([len(self.e.get_trace_to(x.subject)), x])
        d.sort(key=lambda z: z[0])

        for x in d:
            result.append(x[1])
        result.reverse()
        return result

    # Serialize

    def _serialize_batch_command(self, batch):
        result = []
        for x in batch.commands:
            result.append(self._serialize_command(x))
        result = json.dumps(result)
        return result

    def _serialize_command(self, command):
        result = []
        for x in command.actions:
            result.append(self._serialize_action(x))
        return result

    def _serialize_action(self, action):
        result = [action.verb, action.subject.name, action.subject.type]
        if isinstance(action.subject, Modifier):
            result.append('MODIFIER')
        else:
            result.append('CLUSTER')
        return result

    # Deserialize

    def deserialize_batch_command(self, batch):
        result = []
        for x in batch.commands:
            action = self._deserialize_command(x)
            result.append(action)
        return result

    def _deserialize_command(self, command):
        result = []
        for x in command.actions:
            action = self._deserialize_action(x)
            result.append(action)
        return result

    def _deserialize_action(self, action):
        subject = self._find_obj(action[1], action[2], action[2])
        return ClustersAction(action[0], subject)

    def _find_obj(self, obj_name, obj_type, obj_class):
        if not isinstance(obj_name, str):
            raise TypeError
        if not isinstance(obj_type, str):
            raise TypeError
        if not isinstance(obj_class, str):
            raise TypeError

        if obj_class == 'MODIFIER':
            obj_list = self.e.all_modifiers()
        elif obj_class == 'CLUSTER':
            obj_list = self.e.all_clusters()
        else:
            raise TypeError

        for x in obj_list:
            if x.type == obj_type:
                if x.name == obj_name:
                    return x
