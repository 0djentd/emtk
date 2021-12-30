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
                      'name' = name,

                      # List of cluster types that this editor
                      # can be used with.
                      # Example:
                      # ['BEVEL_CLUSTER', 'BEVEL']
                      'cluster_types' = []
                      }
    # }}}

    # Editor methods {{{
    def editor_switched_to(self, context, clusters)
        """Called every time editor is switched to."""
        return self.switched_to(self, context, clusters)

    def editor_switched_from(self, context, event, cluster):
        """Called every time editor is switched from."""
        return self.switched_from(self, context, clusters)

    def editor_modal_pre(self, context, event, cluster):
        """Modal method 1."""
        return self.modal_pre(self, context, event, cluster)

    def editor_modal(self, context, event, cluster):
        """Modal method 2"""
        return self.modal(self, context, event, cluster)
    # }}}

    # Editor-specific method placeholders {{{
    def switched_to(self, context, clusters)
        """Called every time editor is switched to."""
        raise ValueError('No editor-specific method.')

    def switched_from(self, context, cluster):
        """Called every time editor is switched from."""
        raise ValueError('No editor-specific method.')

    def modal_pre(self, context, event, cluster):
        """Modal method 1."""
        raise ValueError('No editor-specific method.')

    def modal(self, context, event, cluster):
        """Modal method 2"""
        raise ValueError('No editor-specific method.')
    # }}}


class ModifierEditorTemplate(ModifierEditor):
    """Base class for editors that only use modifiers attributes."""

    # Variables {{{
    # Modifiers mapping example:
    # MODIFIER_MAPPING = {'cluster': BEVEL_CLUSTER,
    #                     'modifiers': ['get_first()', 'get_first().get_last()']
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

    _DEFAULT_MODE = 'SELECT_MODE'

    # }}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = self.__DEFAULT_MODE
        self._mappings = None
        self._attributes = None

    # Editor methods {{{
    def editor_switched_to(self, context, clusters)
        """Called every time editor is switched to."""
        self.mode = self.__DEFAULT_MODE
        return self.switched_to(self, context, clusters)

    def editor_switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        self.mode = self.__DEFAULT_MODE
        return self.switched_from(self, context, clusters)

    def editor_modal_pre(self, context, event, clusters):
        """Modal method 1."""
        return self.modal_pre(self, context, event, clusters)

    def editor_modal(
            self, context, event, clusters):
        """Modal method 2"""
        self.__modal_attrs(context, event, clusters)
        return self.modal(self, context, event, clusters)
    # }}}

    def __modal_attrs(self, context, event, clusters):  # {{{
        if self.mode == self._DEFAULT_MODE:
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
        for x in self._mappings:
            if x['name'] == mapping_name:
                return x

    # TODO: what is dat
    def _get_mods_for_attr(self, x, cluster):
        mapping = self._get_mod_mapping(x['map'])
        mods = []
        for m in mapping['mods']:
            result = getattr(cluster, m['attr'])(m['args'])
            if not isinstance(result, list):
                result = [result]
            for y in result:
                if not isinstance(y, bpy.types.Modifier):
                    raise TypeError
            mods.extend(result)
        return mods
    # }}}
