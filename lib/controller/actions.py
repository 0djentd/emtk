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
        """Returns actions's verb."""
        return self._verb

    @property
    def subject(self):
        """Returns actions's subject."""
        return self._subject

    def __init__(self, verb, subject, layer=None):
        if not isinstance(verb, str):
            raise TypeError

        if len(verb) == 0:
            raise ValueError

        self._verb = verb
        self._subject = subject
        self.dry = False
        self.props = {}

    def __str__(self):
        return f"[{self.verb} {self.subject.name} d:{self.dry} p:{self.props}]"

    def __repr__(self):
        return self.__str__()


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
                if not isinstance(x, ClustersAction)\
                        and not isinstance(x, ClustersCommand):
                    raise TypeError
            actions = require
        elif isinstance(require, ClustersAction)\
                or isinstance(require, ClustersCommand):
            actions = [require]
        elif require is None:
            actions = []
        else:
            raise TypeError

        self.o = obj
        self.require = actions

    def __str__(self):
        return f"ClusterRequest from {self.o.name} {self.require}"

    def __repr__(self):
        return self.__str__()


class ClustersCommand():
    """This is an object that represents any number of actions.
    It should always have at least one action.
    """

    _initial_action = 'NO_INITIAL_ACTION'
    _actions_to_do = 'NO_ACTIONS'
    affect_clusters = None
    affect_modifiers = None
    dry_clusters = None
    dry_modifiers = None

    @property
    def initial_action(self):
        return self._initial_action

    @property
    def actions(self):
        if not self._initialized:
            raise ValueError
        return self._actions_to_do + [self._initial_action]

    @property
    def status(self):
        if not self._initialized:
            return 'NOT_SOLVED'
        else:
            return 'ALLOWED'

    @actions.setter
    def actions(self, actions):
        if self._initialized:
            raise ValueError
        self._actions_to_do = actions
        self._initialized = True
        self.check_this_command_sanity()

    def __init__(self, initial_action, *args,
                 actions=None,
                 affect_clusters=False,
                 affect_modifiers=False,
                 dry_clusters=False,
                 dry_modifiers=False,
                 **kwargs
                 ):

        if not isinstance(initial_action, ClustersAction):
            raise TypeError(
                    f'Expected ClustersAction, got {type(initial_action)}')
        if actions is not None:
            if isinstance(actions, list):
                for x in actions:
                    if not isinstance(x, ClustersAction):
                        raise TypeError(
                                f'Expected ClustersAction, got {type(x)}')
                actions_to_do = actions
            else:
                raise TypeError
        else:
            actions_to_do = []

        self.affect_clusters = affect_clusters
        self.affect_modifiers = affect_modifiers
        self.dry_clusters = dry_clusters
        self.dry_modifiers = dry_modifiers

        self.reverse_by_layer = False

        self._initialized = False
        self._initial_action = initial_action
        self._actions_to_do = actions_to_do

        self.check_this_command_sanity()

    def __str__(self):
        result = f'ClustersCommand {self._initial_action} ['
        y = 0
        for x in self._actions_to_do:
            if y < 4:
                y += 1
                result = result + f'{x}'
        result = result + '] '
        a = ''
        d = ''
        if self.affect_clusters:
            a += 'c'
        if self.affect_modifiers:
            a += 'm'
        if self.dry_clusters:
            d += 'c'
        if self.dry_modifiers:
            d += 'm'

        result = result + f' a: {a}, d: {d}'
        return result

    def __repr__(self):
        return self.__str__()

    def check_this_command_sanity(self):
        if not isinstance(self._initial_action, ClustersAction):
            raise TypeError
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


class ClustersBatchCommand():
    """
    This is an object that represents any number of commands.
    """

    @property
    def status(self):
        for x in self.commands:
            if x.status == 'NOT_SOLVED':
                return 'NOT_SOLVED'
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
        return self.__str__()

    def check_this_batch_command_sanity(self):
        if len(self.commands) == 0:
            raise ValueError
        for x in self.commands:
            if not isinstance(x, ClustersCommand):
                raise TypeError
            else:
                x.check_this_command_sanity()
