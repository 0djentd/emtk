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
    It should always have at least one action.
    """

    @property
    def initial_action(self):
        return self._initial_action

    @property
    def actions(self):
        return self._actions_to_do

    @actions.setter
    def actions(self, actions):
        self._actions_to_do = actions
        self.check_this_command_sanity()

    @property
    def status(self):
        if len(self._actions_to_do) > 0:
            return 'STILL_NOT_ALLOWED'
        elif self.required_command is not None:
            return 'DEPENDENCY'
        else:
            return 'ALLOWED'

    def __init__(self,
                 initial_action=None, *args,
                 actions_to_do=None,
                 command_status='STILL_NOT_ALLOWED'):

        if not isinstance(initial_action, ClustersAction):
            raise TypeError

        if actions_to_do is not None:
            if isinstance(actions_to_do, list):
                a = actions_to_do
            else:
                raise TypeError
        else:
            a = []

        self._initial_action = initial_action
        self._actions_to_do = [initial_action]
        self._actions_to_do.extend(a)
        self._command_status = command_status
        self.required_command = None
        self.check_this_command_sanity()

    def check_this_command_sanity(self):
        verbs = []
        if not isinstance(self.actions_to_do, list):
            raise TypeError
        for x in self.actions_to_do:
            if not isinstance(x, ClustersAction):
                raise TypeError
            verbs.append(x.verb)
        if len(verbs) > 1:
            raise ValueError('Error in actions verbs.')
        if self.initial_action not in self.actions_to_do:
            raise ValueError
        if not isinstance(self._command_status, str):
            raise TypeError
        if len(self._command_status) == 0:
            raise ValueError


class ClustersBatchCommand():
    """
    This is an object that represents any number of commands.
    """

    @property
    def commands_to_do(self):
        return self._commands_to_do

    @commands_to_do.setter
    def commands_to_do(self, commands):
        self._commands_to_do = commands
        self.check_this_batch_command_sanity()

    def __init__(self,
                 commands_to_do=None,
                 *args,
                 batch_status='STILL_NOT_ALLOWED',
                 **kwargs):

        if isinstance(commands_to_do, list):
            for x in commands_to_do:
                if isinstance(x, ClustersCommand):
                    self._commands_to_do = commands_to_do
                else:
                    raise TypeError
        else:
            raise TypeError

        self.batch_status = batch_status

    def check_this_batch_command_sanity(self):
        for x in self._commands_to_do:
            x.check_this_command_sanity()


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
