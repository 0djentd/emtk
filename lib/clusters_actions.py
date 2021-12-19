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
    Simples element used in clusters controller,
    represents action without any of its
    dependencies.
    """

    verb = None
    subject = None
    status = None

    def __init__(self, verb, subject):
        if not isinstance(verb, str):
            raise TypeError(f'{type(verb)}')

        if len(verb) == 0:
            raise ValueError

        self.verb = verb
        self.subject = subject
        self.status = 'STILL_NOT_ALLOWED'

    def __str__(self):
        return f"Cluster action {self.verb} {self.subject}"

    def __repr__(self):
        return f"ClusterAction [{self.verb} {self.subject}]"


class ClusterRequest():
    """
    Object that represents multiple actions from one
    cluster, controller, or list.
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
    case_all methods are used when action subject
    is anywhere in nested clusters.
    """
    def __init__(self, cluster, *args, **kwargs):
        self.cluster = cluster

    def ask(self, action):
        """
        Returns cluster response to action.
        """
        if action.subject is self.cluster:
            actions = self._answer_case_self(action)
        elif action.subject in self.cluster.get_list():
            actions = self._answer_case_list(action)
        elif action.subject in self.cluster.get_all_clusters_and_modifiers():
            actions = self._answer_case_all(action)
        else:
            return []
        return ClusterRequest(self.cluster, actions)

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
        else:
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
        if action.verb is None:
            raise TypeError


class ActionDefaultTemplate(ClusterActionAnswer):
    """
    This is a template for cluster actions that should not
    be possible, if layer doesnt allows it.
    """

    def __init__(self, *args, action_type, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_type = action_type

    def _answer_case_self(self, action):

        # If removing cluster, remove it.
        actions = []
        for y in self.cluster._modifiers_list:
            actions.append(ClustersAction(self.action_type, y))
        return actions

    def _answer_case_list(self, action):
        actions = []

        # Remove cluster with components if not allowed to change it.
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction(self.action_type, self.cluster))

        # If removing modifier and it is last modifier.
        if len(self.cluster._modifiers_list) == 1:
            actions.append(ClustersAction(self.action_type, self.cluster))
        return actions

    def _answer_case_all(self, action):
        actions = []

        # Remove cluster with components if not allowed to change it.
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction(self.action_type, self.cluster))
        return actions

    def _interpret_case_self(self, action):
        return

    def _interpret_case_list(self, action):
        raise ValueError('No action-specific method')

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


# Remove and apply are practically the same action, as modifier being removed
# from modifiers list when its applied in blender.

# TODO: dont remove cluster on apply, create a duplicate blender
# object and allow copying modifier with its cluster from it.

class ActionDefaultRemove(ActionDefaultTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='REMOVE', *args, **kwargs)

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


class ActionDefaultApply(ActionDefaultTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='APPLY', *args, **kwargs)

    def _interpret_case_list(self, action):
        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if isinstance(action.subject, modifiers_type):
            if _WITH_BPY:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                bpy.ops.object.modifier_apply(modifier=mod_name)
            else:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                self.cluster._object.modifier_apply(modifier=mod_name)
        else:
            self.cluster._modifiers_list.remove(action.subject)

# Moving modifiers is more complex, because if it will be the same action
# for cluster that is being moved and all modifiers and clusters in it, it
# will have no way to know when to actually move it in list, and when
# to just move actual modifiers.

# Action that should be only used in cluster that is
# requested to be moved is 'MOVE'.
# Action that should be in all its clusters and modifiers is 'MOVED'.


# TODO: this method doent checks clusters in layers above it.
class ActionDefaultMove():
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='MOVE', *args, **kwargs)

    def _answer_case_self(self, action):
        actions = []
        for i, x in enumerate(self.cluster.get_list()):
            actions.append(ClustersAction('MOVED', x))
            actions[i].direction = action.direction
        return self._no_action_answer(self, action)

    def _answer_case_list(self, action):
        i = self._modifiers_list.index(action.subject)
        if action.direction == 'UP':
            if i == 0:
                raise ValueError
            else:
                actions = [ClustersAction('MOVE', action.subject)]
        elif action.direction == 'DOWN':
            if i == self.cluster.get_list_length() - 1:
                raise ValueError
            else:
                actions = [ClustersAction('MOVE', action.subject)]

        actions[0].direction = action.direction
        return actions

    def _answer_case_all(self, action):
        return []

    def _interpret_case_self(self, action):
        return self.cluster.cluster_being_moved(
                direction=action.direction)

    def _interpret_case_list(self, action):
        i = self._modifiers_list.index(action.subject)
        mod = action.subject.name

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if action.direction == 'UP':
            if i == 0:
                raise ValueError
            else:
                if isinstance(modifiers_type):
                    if _WITH_BPY:
                        bpy.ops.object.modifier_move_up(modifier=mod)
                    else:
                        self.cluster._object.move_up(modifier=mod)
                else:
                    c = self.cluster._modifiers_list.pop(i)
                    self.cluster._modifiers.list.insert(i-1, c)

        elif action.direction == 'DOWN':
            if i == self.cluster.get_list_length() - 1:
                raise ValueError
            else:
                if isinstance(modifiers_type):
                    if _WITH_BPY:
                        bpy.ops.object.modifier_move_down(modifier=mod)
                    else:
                        self.cluster._object.move_down(modifier=mod)
                else:
                    c = self.cluster._modifiers_list.pop(i)
                    self.cluster._modifiers.list.insert(i+1, c)
        else:
            raise ValueError

    def _interpret_case_all(self, action):
        return []


class ActionDefaultMoved():
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='MOVED', *args, **kwargs)

    def _answer_case_self(self, action):
        actions = []
        # TODO: should it actually require that?
        for i, x in enumerate(
                self.cluster.get_all_clusters_and_modifiers()):
            actions.append(ClustersAction('MOVED', x))
            actions[i].direction = action.direction
        # TODO: should it actually require that?
        actions.append(ClustersAction('MOVED', self.cluster))
        return actions

    def _answer_case_list(self, action):
        actions = []

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if isinstance(action.subject, modifiers_type):
            actions.append(ClustersAction('MOVED', action.subject))
            actions[0].direction = action.direction
        # TODO: should it actually require that?
        else:
            for i, x in enumerate(
                    action.subject.get_all_clusters_and_modifiers()):
                actions.append(ClustersAction('MOVED', x))
                actions[i].direction = action.direction
        return actions

    def _answer_case_all(self, action):
        return []

    def _interpret_case_self(self, action):
        return

    def _interpret_case_list(self, action):
        i = self._modifiers_list.index(action.subject)
        mod = action.subject.name

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if action.direction == 'UP':
            if isinstance(modifiers_type):
                if i == 0:
                    raise ValueError
                if _WITH_BPY:
                    bpy.ops.object.modifier_move_up(modifier=mod)
                else:
                    self.cluster._object.move_up(modifier=mod)

        elif action.direction == 'DOWN':
            if isinstance(modifiers_type):
                if i == self.cluster.get_list_length() - 1:
                    raise ValueError
                if _WITH_BPY:
                    bpy.ops.object.modifier_move_down(modifier=mod)
                else:
                    self.cluster._object.move_down(modifier=mod)
        else:
            raise ValueError

    def _interpret_case_all(self, action):
        return


default_clusters_actions = [ActionDefaultMoved,
                            ActionDefaultMove,
                            ActionDefaultApply,
                            ActionDefaultRemove]
