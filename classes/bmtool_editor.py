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
from ..lib.utils.modifier_prop_types import get_props_filtered_by_types
from ..lib.clusters.cluster_trait import ClusterTrait

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)


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
                      # Can be 'ANY' as well.
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
# class ModifierEditorTemplate(ModifierEditor):  # {{{
#     """Base class for editors that only use modifiers attributes."""
# 
#     # Variables {{{
#     # Modifiers mapping example:
#     # MODIFIER_MAPPING = {'cluster': BEVEL_CLUSTER,
#     #                     'modifiers': ['get_first()',
#     #                                   'get_first().get_last()']
#     #                     }
#     #
#     # List of modifiers mappings.
#     # _mappings = []
#     #
#     # List of available to editor modifiers attributes
#     # _attributes = [
#     #                {'attr': 'segments',
#     #                 'map': '1',
#     #                 'type': 'int',
#     #                 'min': 0,
#     #                 'kb': 'S',
#     #                 'sens': 0.00005},
#     #                {'attr': 'harden_normals',
#     #                 'map': '1',
#     #                 'type': 'int',
#     #                 'kb': 'S',
#     #                 'sens': 0.00005},
#     #                ]
#     #
#     # Currently active editor mode.
#     # (one of _attributes['attr'])
#     # self.mode
# 
#     __DEFAULT_MODE = 'SELECT_MODE'
# 
#     # }}}
# 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.mode = self.__DEFAULT_MODE
#         self._mappings = None
#         self._attributes = None
# 
#     # Editor methods {{{
#     def editor_switched_to(self, context, clusters):
#         """Called every time editor is switched to."""
#         self.mode = self.__DEFAULT_MODE
#         return self.switched_to(context, clusters)
# 
#     def editor_switched_from(self, context, clusters):
#         """Called every time editor is switched from."""
#         self.mode = self.__DEFAULT_MODE
#         return self.switched_from(context, clusters)
# 
#     def editor_modal_pre(self, context, event, clusters):
#         """Modal method 1."""
#         return self.modal_pre(context, event, clusters)
# 
#     def editor_modal(
#             self, context, event, clusters):
#         """Modal method 2"""
#         self.__modal_attrs(context, event, clusters)
#         return self.modal(context, event, clusters)
# 
#     def _no_editor_method(self):
#         return
#     # }}}
# 
#     def __modal_attrs(self, context, event, clusters):  # {{{
#         if not isinstance(clusters, list):
#             clusters = [clusters]
# 
#         if self.mode == self.__DEFAULT_MODE:
#             for x in self._attributes:
#                 if event.type == x['kb']\
#                         and event.value == 'PRESS':
# 
#                     # Toggle attrs
#                     if x['type'] == 'bool':
#                         for c in clusters:
#                             mods = self._get_mods_for_attr(x, c)
#                             for mod in mods:
#                                 setattr(mod, x['attr'], not getattr(
#                                     mod, x['attr']))
# 
#                     # Modes switcher
#                     else:
#                         self.mode = x
#             return
# 
#         # Get active _attributes element
#         x = self.mode
#         if x is None or x == self.__DEFAULT_MODE:
#             raise ValueError
# 
#         # Modal attr editing
#         for c in clusters:
#             mods = self._get_mods_for_attr(x, c)
#             val = self.delta_d(event) * x['sens']
#             if not isinstance(val, int):
#                 raise TypeError
# 
#             if x['min'] == 0 and val < 0:
#                 val = val * -1
# 
#             if x['type'] == 'int':
#                 val = int(val)
#                 for x in mods:
#                     setattr(x, x['attr'], val)
# 
#             if x['type'] == 'float':
#                 val = float(val)
#                 for x in mods:
#                     setattr(x, x['attr'], val)
#         return
#     # }}}
# 
#     # Utils {{{
#     def _get_mod_mapping(self, mapping_name):
#         """Returns modifiers mapping by its name."""
#         for x in self._mappings:
#             if x['name'] == mapping_name:
#                 return x
# 
#     def _get_mods_for_attr(self, x, cluster):
#         """Returns modifiers that can be edited at the same time."""
#         mapping = self._get_mod_mapping(x['map'])
#         mods = []
#         for m in mapping['mods']:
#             if m['attr'] == '':
#                 result = getattr(cluster, m['attr'])()
#             else:
#                 result = getattr(cluster, m['attr'])(*m['args'])
#             if not isinstance(result, list):
#                 result = [result]
#             for y in result:
#                 if not isinstance(y, bpy.types.Modifier):
#                     raise TypeError
#             mods.extend(result)
#         return mods
#     # }}}
# }}}


class AdaptiveModifierEditor(ModifierEditor):  # {{{
    """Modifier editor that can be used with any Blender modifier."""

    # Const {{{

    # All supported modifier types. {{{
    __MODIFIER_TYPES = [
                        "DATA_TRANSFER",
                        "MESH_CACHE",
                        "MESH_SEQUENCE_CACHE",
                        "NORMAL_EDIT",
                        "WEIGHTED_NORMAL",
                        "UV_PROJECT",
                        "UV_WARP",
                        "VERTEX_WEIGHT_EDIT",
                        "VERTEX_WEIGHT_MIX",
                        "VERTEX_WEIGHT_PROXIMITY",
                        "ARRAY",
                        "BEVEL",
                        "BOOLEAN",
                        "BUILD",
                        "DECIMATE",
                        "EDGE_SPLIT",
                        "NODES",
                        "MASK",
                        "MIRROR",
                        "MESH_TO_VOLUME",
                        "MULTIRES",
                        "REMESH",
                        "SCREW",
                        "SKIN",
                        "SOLIDIFY",
                        "SUBSURF",
                        "TRIANGULATE",
                        "VOLUME_TO_MESH",
                        "WELD",
                        "WIREFRAME",
                        "ARMATURE",
                        "CAST",
                        "CURVE",
                        "DISPLACE",
                        "HOOK",
                        "LAPLACIANDEFORM",
                        "LATTICE",
                        "MESH_DEFORM",
                        "SHRINKWRAP",
                        "SIMPLE_DEFORM",
                        "SMOOTH",
                        "CORRECTIVE_SMOOTH",
                        "LAPLACIANSMOOTH",
                        "SURFACE_DEFORM",
                        "WARP",
                        "WAVE",
                        "VOLUME_DISPLACE",
                        "CLOTH",
                        "COLLISION",
                        "DYNAMIC_PAINT",
                        "EXPLODE",
                        "FLUID",
                        "OCEAN",
                        "PARTICLE_INSTANCE",
                        "PARTICLE_SYSTEM",
                        "SOFT_BODY",
                        "SURFACE"
                        ]
    # }}}

    # All prop types.
    __ALL_TYPES = {'BOOLEAN', 'INT', 'FLOAT', 'STRING',
                   'ENUM', 'POINTER', 'COLLECTION'}

    # All editable prop types for this editor
    __EDITABLE_TYPES = {'BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM'}
    __EDITABLE_SUBTYPES = {'NONE', 'PERCENTAGE',
                           'UNSIGNED', 'FACTOR',
                           'ANGLE', 'TIME', 'TIME_ABSOLUTE', 'DISTANCE',
                           'DISTANCE_CAMERA', 'POWER', 'TEMPERATURE',
                           'DIRECTION', 'VELOCITY', 'ACCELERATION',
                           'EULER', 'QUATERNION', 'AXISANGLE',
                           'XYZ', 'XYZ_LENGTH', 'COLOR_GAMMA',
                           'COORDS'}

    # Types of units.
    __TYPES_UNITS = {'NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION',
                     'TIME', 'TIME_ABSOLUTE', 'VELOCITY', 'ACCELERATION',
                     'MASS', 'CAMERA', 'POWER', 'TEMPERATURE'}

    # Can be edited with single shortcut.
    # TODO: enum should not be in this set.
    __TOGGLE_TYPES = {'BOOLEAN', 'ENUM'}

    # Can be edited using mouse input.
    __DELTA_D_TYPES = {'INT', 'FLOAT'}

    # Can be edited using digits input.
    __DIGITS_INPUT_TYPES = {'INT', 'FLOAT'}

    # Can be edited using letters and digits input.
    __LETTERS_INPUT_TYPES = {'STRING'}

    # All types that use some type of modal editing.
    __MODAL_INPUT_PROP_TYPES\
        = __LETTERS_INPUT_TYPES.union(
                __DIGITS_INPUT_TYPES.union(
                    __DELTA_D_TYPES))

    # All types that can be edited in default mode without switching.
    __NOT_MODAL_INPUT_PROP_TYPES = __TOGGLE_TYPES
    # __NOT_MODAL_INPUT_PROP_TYPES\
    #     = __EDITABLE_TYPES.difference(
    #             __MODAL_INPUT_PROP_TYPES)

    # Default editor mode.
    __DEFAULT_MODE = 'NO_MODE'
    # }}}

    # Var {{{
    # Currently active mode.
    # self.mode

    # Currently active modal input mode.
    # This variable initialized in BMToolModalInput()
    # self.modal_input_mode

    # Mappings.
    # Lists of modifier props names with mapping.
    # Elements:
    # {'prop_name': ('event.type', 'event.shift', 'event.ctl', 'event.alt')}
    # Example:
    # __kbs_modal = {
    #                'angle_limit': ('A', False, False, False),
    #                'segments': ('S', False, False, False),
    #                }

    # Modal editing prop only.
    # __kbs_modal = {}
    # Not modal prop editing.
    # __kbs_no_modal = {}
    # Not a modifier prop.
    # __kbs_editing = {}

    # Number of iterations to skip on simple events.
    __TOGGLE_SKIP_FRAMES = 30
    # }}}

    def __init__(self, *args, **kwargs):
        # Allow using with '{mod_name}_CLUSTER' cluster types.
        new_types = []
        for x in self.__MODIFIER_TYPES:
            new_types.append(f'{x}_CLUSTER')
        t = self.__MODIFIER_TYPES + new_types

        self.__previous_event_type = None

        super().__init__(*args,
                         name='Adaptive_Editor',
                         cluster_types=t,
                         **kwargs)

    # ClustersEditor methods {{{
    def editor_switched_to(self, context, clusters):  # {{{
        """Called every time editor is switched to."""
        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        self.mode = self.__DEFAULT_MODE
        self.__additional_info_counter = 0
        self.__toggle_skip_frames_counter = 0

        # Modal editing prop only.
        self.__kbs_modal = {}
        # Not modal prop editing.
        self.__kbs_no_modal = {}
        # Not a modifier prop.
        self.__kbs_editing = {}

        mods = self.__get_all_cluster_modifiers(clusters)
        props = get_props_filtered_by_types(mods[0])

        for x in props:
            if x in self.__MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    self.__kbs_modal.update({y: self.__get_kbs(y)})
            elif x in self.__NOT_MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    self.__kbs_no_modal.update({y: self.__get_kbs(y)})

        logger.debug('Editor switched to.')
        logger.debug('Modal props mappings')
        logger.debug(self.__kbs_modal)
        logger.debug('Not modal props mappings')
        logger.debug(self.__kbs_no_modal)
        logger.debug('Editing mappings')
        logger.debug(self.__kbs_editing)
    # }}}

    def editor_switched_from(self, context, clusters):  # {{{
        """Called every time editor is switched from."""
        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        self.mode = self.__DEFAULT_MODE
        self.modal_input_mode = self._BMToolModalInput__DEFAULT_MODE
        logger.debug('Editor switched from.')
    # }}}

    def editor_modal_pre(self, context, event, clusters):  # {{{
        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError
        return
    # }}}

    def editor_modal(self, context, event, clusters):  # {{{
        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        # Info
        if self.__additional_info_counter < 30:
            self.__additional_info_counter += 1
        else:
            self.__additional_info_counter = 0
            logger.debug('Adaptive modifiers editor modal.')
            logger.debug(f'Mode {self.mode}')
            logger.debug(f'Mode_2 {self.modal_input_mode}')

        # Simple events (event type is in digits and letters).
        if self.mode == self.__DEFAULT_MODE\
                or event.type\
                in self._BMToolModalInput__MODAL_LETTERS_AND_DIGITS_LIST:

            self.__modal_simple_events(context, event, clusters)

        # Complex events (anything else).
        elif self.mode in self.__kbs_modal:
            self.__modal_complex_events(context, event, clusters)
        else:
            pass
        return
    # }}}

    def __modal_simple_events(self, context, event, clusters):  # {{{
        logger.debug('Checking simple events')

        # Skip frames.
        # if event.type == self.__previous_event_type:
        #     logger.debug('Skipped frame')
        #     return
        # else:
        #     self.__previous_event_type = event.type

        # DEFAULT MODE
        if self.mode is self.__DEFAULT_MODE:
            # Get prop name and prop def for event.
            # Most of iterations this will be None,
            # including modal prop editing.
            prop_name = self.__get_prop_name(event)
            if prop_name is not None:
                logger.debug(f'Prop name is {prop_name}')

                # Get modifier
                mods = clusters[0].get_full_actual_modifiers_list()
                mod = mods[0]

                # Modifier prop def
                prop_def = mod.rna_type.properties[prop_name]
            else:
                prop_def = None

            # Try to edit not modal props.
            if prop_name in self.__kbs_no_modal:
                if prop_def.type == 'BOOLEAN':
                    self.__toggle_bool(prop_name, prop_def, mods)
                elif prop_def.type == 'ENUM':
                    self.__scroll_enum(prop_name, prop_def, mods)
                else:
                    raise ValueError

            # Try to switch to modal prop mode.
            elif prop_name in self.__kbs_modal:
                self.mode = prop_name

            # Other props
            elif prop_name in self.__kbs_editing:
                pass

        # MODAL
        elif self.mode in self.__kbs_modal:

            # Switch from mode with same kbs.
            # Get prop name for event.
            prop_name = self.__get_prop_name(event)
            if prop_name == self.mode:
                logger.debug('Switching bask to default mode.')
                self.mode = self.__DEFAULT_MODE

            # Try to switch to different input mode.
            # TODO: exit out of digits and str modes
            elif self.modal_input_mode in {'NONE', 'DELTA_D'}:

                # Get prop def for mode
                prop_def = mod.rna_type.properties[self.mode]
                if event.type in list(string.digits)\
                        and prop_def.type in self.__DIGITS_INPUT_TYPES:
                    self.modal_input_mode = 'DIGITS'
                elif event.type in list(string.ascii_uppercase)\
                        and prop_def.type in self.__LETTERS_INPUT_TYPES:
                    self.modal_input_mode = 'LETTERS'
            else:
                if self.modal_input_mode == 'LETTERS':
                    if event.type == 'RETURN':
                        for mod in mods:
                            setattr(mod, self.mode, self.modal_letters_pop())
                    self.modal_letters(event)
                elif self.modal_input_mode == 'DIGITS':
                    if event.type == 'RETURN':
                        for mod in mods:
                            setattr(mod, self.mode, self.modal_digits_pop())
                    self.modal_digits(event)

        # Check that there are no unexpected for simple events modes.
        else:
            raise ValueError
    # }}}

    def __modal_complex_events(self, context, event, clusters):  # {{{
        logger.debug('Checking modal events')

        # Get modifier
        mods = clusters[0].get_full_actual_modifiers_list()
        mod = mods[0]

        # Use active mode prop name.
        prop_name = self.mode
        prop_def = mod.rna_type.properties[prop_name]

        # Try to edit props.
        if prop_def.type == 'INT':
            self.__modal_int(event, prop_name, prop_def, mods)
        elif prop_def.type == 'FLOAT':
            self.__modal_float(event, prop_name, prop_def, mods)
        elif prop_def.type == 'STRING':
            self.__modal_str(event, prop_name, prop_def, mods)
        return
    # }}}
    # }}}

    def __toggle_bool(self, prop_name, prop, mods):
        t = True
        for x in mods:
            attr = getattr(x, prop_name)
            if attr is True:
                t = False
        for x in mods:
            attr = getattr(x, prop_name)
            attr = t

    def __scroll_enum(self, prop_name, prop, mods):
        for x in mods:
            attr = getattr(x, prop_name)
            enum = prop.enum_items.keys()
            i = enum.index(attr)
            if i == len(enum) - 1:
                attr = enum[0]
            else:
                attr = enum[i + 1]

    def __modal_int(self, event, prop_name, prop, mods):
        return

    def __modal_float(self, event, prop_name, prop, mods):
        return

    def __modal_str(self, event, prop_name, prop, mods):
        return

    def __modal_enum(self, event, prop_name, prop, mods):
        return

    def __get_prop_name(self, event) -> str:
        """Returns property name that were mapped to event type."""
        if len(event.type) > 1:
            return

        d = [self.__kbs_modal, self.__kbs_no_modal, self.__kbs_editing]
        for x in d:
            a = self.__get_prop_from_dict(event, x)
            if a is not None:
                return a

    def __get_prop_from_dict(self, event, kbs: dict) -> str:
        if not isinstance(kbs, dict):
            raise TypeError
        logger.debug(f'Trying to get prop for {event.type} in {kbs}')
        for x in kbs:
            e = kbs[x]
            if event.type == e[0]\
                    and event.shift == e[1]\
                    and event.ctrl == e[2]\
                    and event.alt == e[3]:
                logger.debug(f'found {x} in {kbs}')
                return x

    def __get_kbs(self, prop_name):
        if not isinstance(prop_name, str):
            raise TypeError
        result = prop_name[0].upper()
        return (result, False, False, False)

    def __get_all_cluster_modifiers(self, clusters):
        if not isinstance(clusters, list):
            clusters = [clusters]
        mods = []
        for x in clusters:
            mods.extend(x.get_full_actual_modifiers_list())

        # Check that modifiers are of same type.
        t = None
        for x in mods:
            if t is None:
                t = x.type
            elif x.type != t:
                raise TypeError
        return mods

    # TODO: buffer modifiers
    def get_mappings_for_ui(self):
        result = []
        b = 30
        d = [self.__kbs_modal, self.__kbs_no_modal, self.__kbs_editing]
        for a in d:
            for x in a:
                if not isinstance(x, str):
                    raise TypeError
                t = a[x]
                line = ''
                line = line + f'{x}: '
                if t[1]:
                    line = line + 'shift + '
                if t[2]:
                    line = line + 'ctl + '
                if t[3]:
                    line = line + 'alt + '
                line = line + f'{t[0]} '
                m = b - len(line)
                for y in range(m):
                    line = line + '  '
                line = line + '| '
                result.append(line)

        for x in result:
            if not isinstance(x, str):
                raise TypeError
            if len(x) == 0:
                raise ValueError
        return result
# }}}
