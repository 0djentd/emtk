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

# This is not correct.
from .lists.modifiers_list import ModifiersList


class ClustersAction():
    """
    This thing looks like this:
    x = {
         'verb': 'REMOVE',
         'subject': <obj BevelCluster>
         'status': = 'STILL_NOT_ALLOWED'
         }
    """

    def __init__(self, verb, subject):
        if not isinstance(verb, str):
            raise TypeError(f'{type(verb)}')

        if len(verb) == 0:
            raise ValueError

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if not isinstance(subject, modifiers_type)\
                and not isinstance(subject, ModifiersList):
            raise TypeError(f'{type(subject)}')

        self.verb = verb
        self.subject = subject
        self.status = 'STILL_NOT_ALLOWED'

    def __str__(self):
        return f"Cluster action {self.verb} {self.subject}"

    def __repr__(self):
        return f"ClusterAction [{self.verb} {self.subject}]"


class ClusterRequest():
    """
    This thing looks like this:
    x = {
         'from': <obj BevelCluster>,
         'require': [<action>, <action>]
         }
    """

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


class ClusterActionAnswer():
    """
    This is object responsible for answering on actions from ClustersController
    and performing them.

    case_self methods are used when action subject is cluster itself.
    case_list methods are used when action subject is in this cluster's layer.
    case_all methods are used when action subject is anywhere in nested clusters.
    """
    def __init__(self, cluster, *args, **kwargs):
        self.cluster = cluster

    def ask(self, action):
        """
        Returns cluster response to action.
        """
        if action.subject is self.cluster:
            self._answer_case_self(action)
        elif action.subject in self.cluster.get_list():
            self._answer_case_list(action)
        elif action.subject in self.cluster.get_all_clusters_and_modifiers():
            self._answer_case_all(action)
        raise ValueError('Action cant be interpreted')

    def do(self, action):
        """
        Interprets action.
        """
        if action.subject is self.cluster:
            self._interpret_case_self(action)
        elif action.subject in self.cluster.get_list():
            self._interpret_case_list(action)
        elif action.subject in self.cluster.get_all_clusters_and_modifiers():
            self._interpret_case_all(action)
        raise ValueError('Action cant be interpreted')

    def _answer_case_self(self, action):
        return self._no_action_answer(self, action)

    def _answer_case_list(self, action):
        return self._no_action_answer(self, action)

    def _answer_case_all(self, action):
        return self._no_action_answer(self, action)

    def _interpret_case_self(self, action):
        return self._no_action_answer(self, action)

    def _interpret_case_list(self, action):
        return self._no_action_answer(self, action)

    def _interpret_case_all(self, action):
        return self._no_action_answer(self, action)

    def _no_action_answer(self, action):
        raise ValueError('No class-specific method.')

    def _check_action(self, action):
        if not isinstance(action, ClustersAction):
            raise TypeError
        if action.subject is None:
            raise TypeError


class DefaultRemove(ClusterActionAnswer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_type = 'REMOVE'

    def _answer_case_self(self, action):

        # If removing cluster, remove it.
        actions = []
        for y in self.cluster._modifiers_list:
            actions.append(ClustersAction('REMOVE', y))
        return actions

    def _answer_case_list(self, action):
        actions = []

        # Remove cluster with components if not allowed to change it.
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction('REMOVE', cluster))

        # If removing modifier and it is last modifier.
        if len(self.cluster._modifiers_list) == 1:
            actions.append(ClustersAction('REMOVE', cluster))
        return actions

    def _answer_case_all(self, action):
        actions = []

        # Remove cluster with components if not allowed to change it.
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction('REMOVE', cluster))
        return actions

    def _interpret_case_self(self, action):
        if not self.cluster.cluster_being_removed():
            raise ValueError('Not allowed to remove cluster')

    def _interpret_case_list(self, action):
        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if isinstance(action.subject, modifiers_type):
            if _WITH_BPY:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                bpy.ops.object.modifier_remove(modifier=mod_name)
            else:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                self.cluster._object.modifier_remove(modifier=mod_name)
        else:
            self.cluster._modifiers_list.remove(action.subject)
