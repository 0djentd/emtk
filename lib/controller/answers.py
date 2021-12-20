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

from .actions import ClustersAction, ClusterRequest


class ClusterActionAnswer():
    """
    This is base class for objects responsible for answering on
    actions from ClustersController and performing them.

    case_self methods are used when action subject is cluster itself.
    case_list methods are used when action subject is in this cluster's layer.
    case_all methods are used when action subject
    is anywhere in nested clusters.
    """
    def __init__(self, cluster, *args, action_type, **kwargs):
        self.cluster = cluster
        self.action_type = action_type

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

    # This methods should only require actions on cluster or it's clusters.
    def _answer_case_self(self, action):
        return self._no_action_answer(action)

    def _answer_case_list(self, action):
        return self._no_action_answer(action)

    def _answer_case_all(self, action):
        return self._no_action_answer(action)

    def _interpret_case_self(self, action):
        return self._no_action_answer(action)

    def _interpret_case_list(self, action):
        return self._no_action_answer(action)

    def _interpret_case_all(self, action):
        return self._no_action_answer(action)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _answer_case_self(self, action):

        # If removing cluster, remove all its components.
        actions = []
        for y in self.cluster._modifiers_list:
            actions.append(ClustersAction(self.action_type, y))
        return actions

    def _answer_case_list(self, action):
        actions = []

        # Deconstruct cluster with components if not allowed to change it.
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction('DECONSTRUCT', self.cluster))

        # If removing modifier and it is last modifier.
        elif len(self.cluster._modifiers_list) == 1:
            actions.append(ClustersAction('REMOVE', self.cluster))

        return actions

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


class ActionDefaultDeconstuct(ClusterActionAnswer):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='DECONSTRUCT', *args, **kwargs)

    def _answer_case_list(self, action):
        actions = []
        if not self.cluster._MODCLUSTER_DYNAMIC:
            actions.append(ClustersAction('DECONSTRUCT', self.cluster))
        return actions

    def _interpret_case_list(self, action):
        clusters_index = self.cluster._modifiers_list.index(action.subject)

        y = action.subject.get_list()

        removing_active = False

        if self.cluster.active_modifier_get() == action.subject:
            removing_active = True

        if action.subject.has_clusters():
            self.cluster._modifiers_list.remove(action.subject)
            for x in reversed(y):
                self.cluster._modifiers_list.insert(clusters_index, x)
        else:
            parser = self.cluster._clusters_parser
            parse_result = parser._parse_modifiers_for_simple_clusters(y)
            self.cluster._modifiers_list.remove(action.subject)
            for x in reversed(parse_result):
                self.cluster._modifiers_list.insert(clusters_index, x)
            if removing_active:
                self.cluster.active_modifier_set_by_index(clusters_index)

    def _no_action_answer(self, action):
        return []

# Moving modifiers is more complex, because if it will be the same action
# for cluster that is being moved and all modifiers and clusters in it, it
# will have no way to know when to actually move it in list, and when
# to just move actual modifiers.

# Action that should be only used in cluster that is
# requested to be moved is 'MOVE'.
# Action that should be in all its clusters and modifiers is 'MOVED'.


class ActionDefaultMove(ClusterActionAnswer):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='MOVE', *args, **kwargs)


class ActionDefaultMoved(ClusterActionAnswer):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='MOVED', *args, **kwargs)
