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

import math
import logging
import copy
import json

import bpy

from .bmtool_input import BMToolModalInput


# TODO: rename to ClustersEditor
class ModifierEditor(BMToolModalInput):
    """Editor base class"""

    # Constructor {{{
    def __init__(self, *args, name, cluster_types, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(name, str):
            raise TypeError
        if not isinstance(cluster_types, list):
            cluster_types = [cluster_types]
        for x in cluster_types:
            if not isinstance(x, str):
                raise TypeError

        self.props = {
                      # Editor name to be shown in ui
                      'name': name,

                      # List of cluster types that this editor
                      # can be used with.
                      # Example:
                      # ['BEVEL_CLUSTER', 'BEVEL']
                      'cluster_types': cluster_types
                      }
    # }}}

    # Editor methods {{{
    def editor_switched_to(self, context, clusters):
        """Called every time editor is switched to."""
        return self.switched_to(context, clusters)

    def editor_switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        return self.switched_from(context, clusters)

    def editor_modal_pre(self, context, event, clusters):
        """Modal method 1."""
        return self.modal_pre(context, event, clusters)

    def editor_modal(self, context, event, clusters):
        """Modal method 2"""
        return self.modal(context, event, clusters)
    # }}}

    # Editor-specific method placeholders {{{
    def switched_to(self, context, clusters):
        """Called every time editor is switched to."""
        self._no_editor_method()

    def switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        self._no_editor_method()

    def modal_pre(self, context, event, clusters):
        """Modal method 1."""
        self._no_editor_method()

    def modal(self, context, event, clusters):
        """Modal method 2"""
        self._no_editor_method()

    def _no_editor_method(self):
        raise ValueError('No editor-specific method.')
    # }}}


# TODO: rename to ModalClustersEditor
class ModifierEditorTemplate(ModifierEditor):
    """Base class for editors that only use modifiers attributes."""

    # Variables {{{
    # Modifiers mapping example:
    # MODIFIER_MAPPING = {'cluster': BEVEL_CLUSTER,
    #                     'modifiers': ['get_first()',
    #                                   'get_first().get_last()']
    #                     }
    #
    # List of modifiers mappings.
    # _mappings = []
    #
    # List of available to editor modifiers attributes
    # _attributes = [
    #                {'attr': 'segments',
    #                 'map': '1',
    #                 'type': 'int',
    #                 'min': 0,
    #                 'kb': 'S',
    #                 'sens': 0.00005},
    #                {'attr': 'harden_normals',
    #                 'map': '1',
    #                 'type': 'int',
    #                 'kb': 'S',
    #                 'sens': 0.00005},
    #                ]
    #
    # Currently active editor mode.
    # (one of _attributes['attr'])
    # self.mode

    __DEFAULT_MODE = 'SELECT_MODE'

    # }}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = self.__DEFAULT_MODE
        self._mappings = None
        self._attributes = None

    # Editor methods {{{
    def editor_switched_to(self, context, clusters):
        """Called every time editor is switched to."""
        self.mode = self.__DEFAULT_MODE
        return self.switched_to(context, clusters)

    def editor_switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        self.mode = self.__DEFAULT_MODE
        return self.switched_from(context, clusters)

    def editor_modal_pre(self, context, event, clusters):
        """Modal method 1."""
        return self.modal_pre(context, event, clusters)

    def editor_modal(
            self, context, event, clusters):
        """Modal method 2"""
        self.__modal_attrs(context, event, clusters)
        return self.modal(context, event, clusters)

    def _no_editor_method(self):
        return
    # }}}

    def __modal_attrs(self, context, event, clusters):  # {{{
        if not isinstance(clusters, list):
            clusters = [clusters]

        if self.mode == self.__DEFAULT_MODE:
            for x in self._attributes:
                if event.type == x['kb']\
                        and event.value == 'PRESS':

                    # Toggle attrs
                    if x['type'] == 'bool':
                        for c in clusters:
                            mods = self._get_mods_for_attr(x, c)
                            for mod in mods:
                                setattr(mod, x['attr'], not getattr(
                                    mod, x['attr']))

                    # Modes switcher
                    else:
                        self.mode = x
            return

        # Get active _attributes element
        x = self.mode
        if x is None or x == self.__DEFAULT_MODE:
            raise ValueError

        # Modal attr editing
        for c in clusters:
            mods = self._get_mods_for_attr(x, c)
            val = self.delta_d(event) * x['sens']
            if not isinstance(val, int):
                raise TypeError

            if x['min'] == 0 and val < 0:
                val = val * -1

            if x['type'] == 'int':
                val = int(val)
                for x in mods:
                    setattr(x, x['attr'], val)

            if x['type'] == 'float':
                val = float(val)
                for x in mods:
                    setattr(x, x['attr'], val)
        return
    # }}}

    # Utils {{{
    def _get_mod_mapping(self, mapping_name):
        """Returns modifiers mapping by its name."""
        for x in self._mappings:
            if x['name'] == mapping_name:
                return x

    def _get_mods_for_attr(self, x, cluster):
        """Returns modifiers that can be edited at the same time."""
        mapping = self._get_mod_mapping(x['map'])
        mods = []
        for m in mapping['mods']:
            if m['attr'] == '':
                result = getattr(cluster, m['attr'])()
            else:
                result = getattr(cluster, m['attr'])(*m['args'])
            if not isinstance(result, list):
                result = [result]
            for y in result:
                if not isinstance(y, bpy.types.Modifier):
                    raise TypeError
            mods.extend(result)
        return mods
    # }}}
