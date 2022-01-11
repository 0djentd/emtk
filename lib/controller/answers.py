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

import logging

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

from .actions import ClustersAction, ClusterRequest, ClustersCommand

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClusterActionAnswer():
    """
    This is base class for objects responsible for answering on
    actions from ClustersController and performing them.

    case_self methods are used when action subject is cluster itself.
    case_list methods are used when action subject is in this cluster's layer.
    case_all methods are used when action subject
    is anywhere in nested clusters.
    """
    def __init__(self, cluster, *args,
                 action_type, only_interpret=False,
                 **kwargs):

        self.cluster = cluster
        self.action_type = action_type
        self._only_interpret = only_interpret

    def ask(self, action):
        """
        Returns cluster response to action.
        """
        if self._only_interpret:
            actions = []
        elif action.subject is self.cluster:
            actions = self._answer_case_self(action)
        elif action.subject in self.cluster.get_list():
            actions = self._answer_case_list(action)
        elif action.subject in self.cluster.get_all_clusters_and_modifiers():
            actions = self._answer_case_all(action)
        else:
            raise ValueError('Action cant be interpreted')
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

    # This methods should only require commands on cluster or it's clusters.
    def _answer_case_self(self, action):
        return self._no_action_answer(action)

    def _answer_case_list(self, action):
        return self._no_action_answer(action)

    def _answer_case_all(self, action):
        return self._no_action_answer(action)

    # This methods should not require additional commands and only do something
    # with cluster itself or its list.
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

    def _answer_case_list(self, action):
        actions = []

        # Deconstruct cluster with components if not allowed to change it.
        if not self.cluster.parser_variables['dynamic']:
            actions.append(
                    ClustersCommand(
                        ClustersAction(
                            'DECONSTRUCT', self.cluster)))

        # If removing modifier and it is last modifier.
        elif len(self.cluster._modifiers_list) == 1:
            actions.append(ClustersAction('REMOVE', self.cluster))
            actions.append(
                    ClustersCommand(
                        ClustersAction(
                            'REMOVE', self.cluster)))
        return actions

    def _no_action_answer(self, action):
        return

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

        i = self.cluster._modifiers_list.index(action.subject)
        removing_active = False

        if self.cluster.active_modifier_get() == action.subject:
            removing_active = True

        if isinstance(action.subject, modifiers_type):
            if _WITH_BPY:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                new_context = bpy.context.copy()
                new_context['selected_objects'] = [self.cluster._object]
                new_context['active_object'] = self.cluster._object
                bpy.ops.object.modifier_remove(new_context, modifier=mod_name)
            else:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                self.cluster._object.modifier_remove(modifier=mod_name)
        else:
            action.subject._cluster_removed = True
            self.cluster._modifiers_list.remove(action.subject)

        if removing_active and len(self.cluster._modifiers_list) > (i + 1):
            self.cluster.active_modifier_set_by_index(i)
        elif removing_active and len(self.cluster._modifiers_list) == (i + 1):
            self.cluster.active_modifier_set_by_index(i - 1)


class ActionDefaultApply(ActionDefaultTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='APPLY', *args, **kwargs)

    def _interpret_case_list(self, action):
        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        i = self.cluster._modifiers_list.index(action.subject)
        removing_active = False

        if self.cluster.active_modifier_get() == action.subject:
            removing_active = True

        if isinstance(action.subject, modifiers_type):
            if _WITH_BPY:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                new_context = bpy.context.copy()
                new_context['selected_objects'] = [self.cluster._object]
                new_context['active_object'] = self.cluster._object
                bpy.ops.object.modifier_apply(new_context, modifier=mod_name)
            else:
                mod_name = action.subject.name
                self.cluster._modifiers_list.remove(action.subject)
                self.cluster._object.modifier_apply(modifier=mod_name)
        else:
            action.subject._cluster_removed = True
            self.cluster._modifiers_list.remove(action.subject)

        if removing_active and len(self.cluster._modifiers_list) > 0:
            self.cluster.active_modifier_set_by_index(i)


class ActionDefaultDeconstuct(ActionDefaultTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='DECONSTRUCT', *args, **kwargs)

    def _interpret_case_list(self, action):
        i = self.cluster._modifiers_list.index(action.subject)

        y = action.subject.get_list()

        removing_active = False

        if self.cluster.active_modifier_get() == action.subject:
            removing_active = True

        if action.subject.has_clusters():
            self.cluster._modifiers_list.remove(action.subject)
            action.subject._cluster_removed = True
            for x in reversed(y):
                self.cluster._modifiers_list.insert(i, x)
        else:
            parser = self.cluster._clusters_parser
            parse_result = parser._parse_modifiers_for_simple_clusters(y)
            self.cluster._modifiers_list.remove(action.subject)
            action.subject._cluster_removed = True
            for x in reversed(parse_result):
                self.cluster._modifiers_list.insert(i, x)

        if removing_active:
            self.cluster.active_modifier_set_by_index(i)


# Moving clusters invokes two commands, one has 'dry' clusters actions
# between moved cluster and actual modifiers and one has only 'dry'
# clusters actions. Second command is for cluster that initial
# moved cluster is moved 'through'

class ActionDefaultMove(ClusterActionAnswer):
    def __init__(self, *args, **kwargs):
        super().__init__(action_type='MOVE', *args, **kwargs)

    def _answer_case_list(self, action):
        actions = []
        i = self.cluster._modifiers_list.index(action.subject)
        if action.props['direction'] == 'UP':
            if i == 0:
                actions.append(ClustersCommand(
                    ClustersAction('DECONSTRUCT', self.cluster)))
        elif action.props['direction'] == 'DOWN':
            if i == len(self.cluster._modifiers_list) - 1:
                actions.append(ClustersCommand(
                    ClustersAction('DECONSTRUCT', self.cluster)))
        else:
            raise ValueError
        return actions

    def _interpret_case_list(self, action):
        if action.dry:
            return

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if isinstance(action.subject, modifiers_type):
            mod_name = action.subject.name
            if _WITH_BPY:
                new_context = bpy.context.copy()
                new_context['selected_objects'] = [self.cluster._object]
                new_context['active_object'] = self.cluster._object

            if action.props['direction'] == 'UP':
                for x in range(action.props['length']):
                    if _WITH_BPY:
                        bpy.ops.object.modifier_move_up(
                                new_context, modifier=mod_name)
                    else:
                        self.cluster._object.modifier_move_up(
                                modifier=mod_name)
                    # TODO: this is for moving modifiers in modifiers cluster.
                    # self.cluster._modifiers_list.insert(i+1, mod)
            elif action.props['direction'] == 'DOWN':
                for x in range(action.props['length']):
                    if _WITH_BPY:
                        bpy.ops.object.modifier_move_down(
                                new_context, modifier=mod_name)
                    else:
                        self.cluster._object.modifier_move_down(
                                modifier=mod_name)
                    # self.cluster._modifiers_list.insert(i-1, mod)
        else:
            i = self.cluster._modifiers_list.index(action.subject)
            mod = self.cluster._modifiers_list.pop(i)
            if action.props['direction'] == 'UP':
                self.cluster._modifiers_list.insert(i-1, mod)
            elif action.props['direction'] == 'DOWN':
                self.cluster._modifiers_list.insert(i+1, mod)

    def _no_action_answer(self, action):
        return
