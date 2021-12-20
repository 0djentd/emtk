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


class ClustersAction():
    """
    Simplest element used in clusters controller,
    represents action without any of its
    dependencies.
    """

    _verb = None
    _subject = None

    @property
    def verb(self):
        return self._verb

    @property
    def subject(self):
        return self._subject

    @property
    def layer(self):
        return self._layer

    def __init__(self, verb, subject, layer=None):
        if not isinstance(verb, str):
            raise TypeError(f'{type(verb)}')

        if len(verb) == 0:
            raise ValueError

        self._verb = verb
        self._subject = subject
        self._layer = layer

    def __str__(self):
        return f"[{self.verb} {self.subject}]"

    def __repr__(self):
        return f"[{self.verb} {self.subject}]"


class ClusterRequest():
    """
    Object that represents multiple actions or commands from one
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


class ClustersCommand():
    """
    This is an object that represents any number of actions.

    It should always have at least one action.
    """

    @property
    def initial_action(self):
        return self._initial_action

    @property
    def actions(self):
        if not self._initialized:
            raise ValueError
        return self._actions_to_do

    @property
    def status(self):
        if len(self.dependencies) != 0:
            return 'HAS_DEPENDENCIES'
        elif not self._initialized:
            return 'NOT_SOLVED'
        else:
            return 'ALLOWED'

    @actions.setter
    def actions(self, actions):
        if self._initialized:
            raise ValueError
        self._actions_to_do = actions
        self.check_this_command_sanity()
        self._initialized = True

    def __init__(self, initial_action):
        if not isinstance(initial_action, ClustersAction):
            raise TypeError

        self._initialized = False
        self._initial_action = initial_action
        self._actions_to_do = [initial_action]
        self.dependencies = []
        self.check_this_command_sanity()

    def __str__(self):
        result = 'ClustersCommand ['
        for x in self._actions_to_do:
            result = result + f'{x}'
        result = result + '] '
        return result

    def __repr__(self):
        result = 'ClustersCommand ['
        for x in self._actions_to_do:
            result = result + f'{x}'
        result = result + '] '
        return result

    def check_this_command_sanity(self):
        if not isinstance(self._actions_to_do, list):
            raise TypeError
        verbs = []
        for x in self._actions_to_do:
            if not isinstance(x, ClustersAction):
                raise TypeError
            if x.verb not in verbs:
                verbs.append(x.verb)
        if len(verbs) > 1:
            raise ValueError('Error in actions verbs.')
        if self._initial_action not in self._actions_to_do:
            raise ValueError


class ClustersBatchCommand():
    """
    This is an object that represents any number of commands.
    """

    @property
    def status(self):
        deps = []
        for x in self.commands:
            if x.status == 'NOT_SOLVED':
                return 'NOT_SOLVED'
            deps.extend(x.dependencies)
        for x in deps:
            if x not in self.commands:
                return 'NOT_SOLVED_DEPENDENCIES'
        return 'ALLOWED'

    def __init__(self, commands_to_do=None):
        if not isinstance(commands_to_do, list):
            commands_to_do = [commands_to_do]
        elif len(commands_to_do) == 0:
            raise ValueError
        self.commands = []
        for x in commands_to_do:
            if isinstance(x, ClustersCommand):
                self.commands.append(x)
            else:
                raise TypeError
        self.check_this_batch_command_sanity()

    def __str__(self):
        result = 'ClustersBatchCommand ['
        for x in self.commands:
            result = result + f'{x}'
        result = result + '] '
        return result

    def __repr__(self):
        result = 'ClustersBatchCommand ['
        for x in self.commands:
            result = result + f'{x}'
        result = result + '] '
        return result

    def check_this_batch_command_sanity(self):
        if len(self.commands) == 0:
            raise ValueError
        for x in self.commands:
            if not isinstance(x, ClustersCommand):
                raise TypeError
            else:
                x.check_this_command_sanity()
