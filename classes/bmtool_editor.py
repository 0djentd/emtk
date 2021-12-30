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

                      # Cluster types that this editor
                      # can be used with.
                      # Example:
                      # ['BEVEL_CLUSTER', 'DOUBLE_BEVEL']
                      'cluster_types' = []
                      }
    # }}}

    # Editor methods {{{
    def editor_inv(self, context, clusters)
        """Called every time editor is switched to."""
        return self.inv(self, context, clusters)

    def editor_rm(self, context, event, cluster):
        """Called every time editor is switched from."""
        return self.rm(self, context, clusters)

    def editor_modal_pre(self, context, event, cluster):
        """Modal method 1."""
        return self.modal_pre(self, context, event, cluster)

    def editor_modal(self, context, event, cluster):
        """Modal method 2"""
        return self.modal(self, context, event, cluster)
    # }}}

    # Editor-specific method placeholders {{{
    def inv(self, context, clusters)
        """Called every time editor is switched to."""
        raise ValueError('No editor-specific method.')

    def rm(self, context, event, cluster):
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
    # example {{{
    """
    Modal mapping decides what modifiers to use when editing.
    TODO: this is kinda bad
    Examples:
    MODIFIER_MAPPING = {'cluster': BEVEL_CLUSTER,
                        'modifiers': ['get_first()', 'get_first().get_last()']
                        }

    MODIFIER_MAPPING = {'cluster': DOUBLE_BEVEL,
                        'modifiers': ['get_list()[1]']
                        }

    Attributes example:
    [
     {'attr': 'segments',  # Attribut name
      'mods': [<MODIFIER_MAPPING>, <MODIFIER_MAPPING>]  # Modal mappings
      'type': 'int',  # Attribute type
      'min': 0,  # Min value
      'kb': 'S',  # Shortcut
      'sens': 0.00005},  # Sens for modal editing

     {'attr': 'harden_normals',
      'mods': [<MODIFIER_MAPPING>, <MODIFIER_MAPPING>]
      'type': 'bool',
      'kb': 'H',
      'sens': 0.00005},

     {'attr': 'angle',
      'mods': [<MODIFIER_MAPPING>]
      'type': 'float',
      'min': 0,
      'kb': 'A',
      'sens': 0.0005}
      ]
    """  # }}}

    # Variables {{{
    _mappings = [
                 {'mapping_name': '1',
                  'cluster': 'BEVEL_CLUSTER',
                  'mods': [{'attr': 'get_first', 'args': ''}]}
                 ]

    _attributes = [
                   {'attr': 'segments',
                    'map': '1',
                    'type': 'int',
                    'min': 0,
                    'kb': 'S',
                    'sens': 0.00005},
                   {'attr': 'harden_normals',
                    'map': '1',
                    'type': 'int',
                    'kb': 'S',
                    'sens': 0.00005},
                   ]

    # Currently active editor mode.
    # self.mode

    _DEFAULT_MODE = 'SELECT_MODE'

    # }}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = self.__DEFAULT_MODE

    # Editor methods {{{
    def inv(self, context, clusters)
        """Called every time editor is switched to."""
        self.mode = self.__DEFAULT_MODE
        return self.inv(self, context, clusters)

    def rm(self, context, event, clusters):
        """Called every time editor is switched from."""
        # Resets editor's mode, kinda should be in every editor
        self.mode = self.__DEFAULT_MODE
        return self.rm(self, context, clusters)

    def modal_pre(self, context, event, clusters):
        """Modal method 1."""
        return self.modal_pre(self, context, event, clusters)

    def modal(
            self, context, event, clusters):
        """Modal method 2"""
        return self.modal(self, context, event, clusters)
    # }}}

    def modal_attrs(self, context, event, clusters):  # {{{

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
                        self.mode = x['attr']
            return

        # Get active attr by mode
        x = None
        for a in self._attributes:
            if a['attr'] == self.mode:
                x = a
        if x is None:
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
        return  # }}}

    # Utils {{{
    def _get_mod_mapping(self, mapping_name):
        for x in self._mappings:
            if x['name'] == mapping_name:
                return x

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
