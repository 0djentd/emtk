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
import string
import logging
import copy
import json

import bpy

from .bmtool_input import BMToolModalInput
from ..lib.utils.modifier_types_utils import get_editable_modifier_props
from ..lib.utils.modifier_types_utils import filter_props_by_type


# TODO: rename to ClustersEditor
class ModifierEditor(BMToolModalInput):  # {{{
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
# }}}


# TODO: rename to ModalClustersEditor
class ModifierEditorTemplate(ModifierEditor):  # {{{
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
# }}}


class AdaptiveModifierEditor(ModifierEditor):  # {{{
    """
    Modifier editor that can be used with any Blender modifier.
    """

    # Variables {{{

    # All prop types.
    __ALL_TYPES = {'BOOLEAN', 'INT', 'FLOAT', 'STRING',
                   'ENUM', 'POINTER', 'COLLECTION'}

    # All editable in this editor prop types.
    __EDITABLE_TYPES = {'BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM'}

    __EDITABLE_SUBTYPES = {'NONE', 'PERCENTAGE',
                           'UNSIGNED', 'FACTOR',
                           'ANGLE', 'TIME', 'TIME_ABSOLUTE', 'DISTANCE',
                           'DISTANCE_CAMERA', 'POWER', 'TEMPERATURE',
                           'DIRECTION', 'VELOCITY', 'ACCELERATION',
                           'EULER', 'QUATERNION', 'AXISANGLE',
                           'XYZ', 'XYZ_LENGTH', 'COLOR_GAMMA',
                           'COORDS'}

    # Types of units
    __TYPES_UNITS = {'NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION',
                     'TIME', 'TIME_ABSOLUTE', 'VELOCITY', 'ACCELERATION',
                     'MASS', 'CAMERA', 'POWER', 'TEMPERATURE'}

    # Can be edited with single shortcut.
    __TOGGLE_TYPES = {'BOOLEAN'}

    # Can be edited using mouse input.
    __DELTA_D_TYPES = {'INT', 'FLOAT'}

    # Can be edited using digits input.
    __DIGIT_INPUT_TYPES = {'INT', 'FLOAT'}

    # Can be edited using letters and digits input.
    __STRING_INPUT_TYPES = {'ENUM', 'STRING'}

    # All types that use some type of modal editing.
    __MODAL_INPUT_TYPES\
        = __STRING_INPUT_TYPES\
        + __DIGIT_INPUT_TYPES\
        + __DELTA_D_TYPES

    # All types that can be edited in default mode without switching.
    __NOT_MODAL_INPUT_TYPES\
        = __EDITABLE_TYPES.difference(
                __MODAL_INPUT_TYPES)

    # List of modifier props with mapping.
    # Elements:
    # {'prop_name': ('event.type', 'event.shift', 'event.ctl', 'event.alt')}
    #
    # Example:
    # __modifier_props_mapping = {
    #                             'angle_limit': ('A', False, False, False),
    #                             'segments': ('S', False, False, False),
    #                             }

    # Default editor mode.
    __DEFAULT_MODE = 'NO_MODE'

    # }}}

    def editor_inv(self, context, event, clusters):
        mods = self.get_modifiers(clusters)
        self.mode = self.__DEFAULT_MODE
        self.__modifier_props = {}
        for x in get_editable_modifier_props(mods[0]):
            self.__modifier_props.update({x: self.get_kbs(x)})

    def editor_modal(self, context, event, clusters):
        # Get modifier
        mods = clusters[0].get_full_actual_modifiers_list()
        mod = mods[0]

        # TODO: doesnt work
        # Modifier prop name. Can be None.
        prop_name = self.__get_prop_name(event)

        # Modifier prop def
        if prop_name is not None:
            prop = mod.rna_type.properties[prop_name]

        # Filter only simple events.
        if event.type in list(string.ascii_uppercase)\
                and event.value == 'PRESS':

            if self.mode is self.__DEFAULT_MODE:

                # Try to switch to mode
                if prop_name is not None\
                        and prop_name\
                        not in self.__MODAL_INPUT_TYPES:
                    self.mode = prop_name
                    return

                # Try to toggle bool prop
                if prop.type == 'BOOL':
                    self.__toggle_bool(prop_name, prop, mods)
                elif prop.type == 'ENUM':
                    self.__scroll_enum(prop_name, prop, mods)
                return

        if prop.type in self.__MODAL_INPUT_TYPES:
            if prop.type == 'INT':
                self.__modal_int(event, prop_name, prop, mods)
            elif prop.type == 'FLOAT':
                self.__modal_float(event, prop_name, prop, mods)
            elif prop.type == 'STRING':
                self.__modal_str(event, prop_name, prop, mods)
            elif prop.type == 'ENUM':
                self.__modal_enum(event, prop_name, prop, mods)

    def __toggle_bool(self, prop_name, prop, mods):
        t = True
        for x in mods:
            attr = getattr(x, prop_name)
            if attr is True:
                t = False

        for x in mods:
            attr = getattr(x, prop_name)
            attr = t

    def __modal_int(self, event, prop_name, prop, mods):
        return

    def __modal_float(self, event, prop_name, prop, mods):
        return

    def __modal_str(self, event, prop_name, prop, mods):
        return

    def __modal_enum(self, event, prop_name, prop, mods):
        return

    def __get_prop_name(self, event):
        """
        Returns modifier property name that were
        mapped to this event type.

        Returns None, if not found any.
        """
        for x in self.__kbs:
            e = self.__kbs[x]
            if event.type == e[0]\
                    and event.shift is e[1]\
                    and event.ctrl is e[2]\
                    and event.alt is e[3]:
                return x

    def get_kbs(self, prop_name):
        if not isinstance(prop_name, str):
            raise TypeError
        result = prop_name[0]
        result.upper()
        return (result, False, False, False)

    def get_modifiers(self, clusters):
        if not isinstance(clusters, list):
            clusters = [clusters]
        mods = clusters[0].get_full_actual_modifiers_list()

        # Check that modifiers are of same type.
        t = None
        for x in mods:
            if not isinstance(x, bpy.types.Modifier):
                raise TypeError
            if t is None:
                t = x.type
            if x.type != t:
                raise TypeError
        return mods
    # }}}
