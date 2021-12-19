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
    from .dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False


class ClustersAction():
    """
    Simplest element used in clusters controller,
    represents action without any of its
    dependencies.
    """

    verb = None
    subject = None

    def __init__(self, verb, subject, layer=None):
        if not isinstance(verb, str):
            raise TypeError(f'{type(verb)}')

        if len(verb) == 0:
            raise ValueError

        self.verb = verb
        self.subject = subject
        self.layer = layer

    def __str__(self):
        return f"Cluster action {self.verb} {self.subject}"

    def __repr__(self):
        return f"ClusterAction [{self.verb} {self.subject}]"


class ClustersCommand():
    """
    This is an object that represents any number of actions.
    """

    def __init__(self, initial_action, actions_to_do, command_status):
        if isinstance(actions_to_do, list):
            for x in actions_to_do:
                if not isinstance(x, ClustersAction):
                    raise TypeError
            actions = actions_to_do
        elif isinstance(actions_to_do, ClustersAction):
            actions = [actions_to_do]
        else:
            raise TypeError

        self.initial_action = initial_action
        self.actions = actions
        self.command_status = command_status


class ClustersBatchCommand():
    """
    This is an object that represents any number of commands.
    """

    def __init__(self, initial_command, commands_to_do, command_status):
        if isinstance(commands_to_do, list):
            for x in commands_to_do:
                if not isinstance(x, ClustersCommand):
                    raise TypeError
            commands = commands_to_do
        elif isinstance(commands_to_do, ClustersCommand):
            commands = [commands_to_do]
        else:
            raise TypeError

        self.initial_command = initial_command
        self.command_status = command_status
        self.commands = commands


class ClusterRequest():
    """
    Object that represents multiple actions from one
    cluster, controller, or list.
    Doesnt have any initial action, like command.
    """
    o = None
    require = None

    def __init__(self, obj, require):
        if isinstance(require, list):
            for x in require:
                if not isinstance(x, ClustersAction):
                    raise TypeError
            actions = require
        elif isinstance(require, ClustersAction):
            actions = [require]
        else:
            raise TypeError

        self.o = obj
        self.require = actions

    def __str__(self):
        return f"Cluster request from {self.o} {self.require}"

    def __repr__(self):
        return f"ClusterRequest from {self.o} {self.require}"
