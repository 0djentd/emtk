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

# import math
# import string
import logging
# import copy
# import json
# import time
# import re

# import bpy

# from .bmtool_input import BMToolModalInput
from ..lib.utils.modifier_prop_types import get_props_filtered_by_types
from ..lib.clusters.cluster_trait import ClusterTrait
from .bmtool_editor import ModalClustersEditor

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)


class AdaptiveModalModifiersEditor(ModalClustersEditor):
    """
    Editor that can be used with any Blender object
    implementing rna_type attribute, including modifier.
    """

    # Constants {{{

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

    # Default editor mode.
    __DEFAULT_MODE = 'NO_MODE'
    # }}}

    # Variables {{{
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
    # }}}

    def __init__(self, *args, **kwargs):
        # Allow using with '{mod_name}_CLUSTER' cluster types.
        new_types = []
        for x in self.__MODIFIER_TYPES:
            new_types.append(f'{x}_CLUSTER')
        t = self.__MODIFIER_TYPES + new_types

        super().__init__(*args,
                         name='Adaptive_Editor',
                         cluster_types=t,
                         **kwargs)

        self.mode = self.__DEFAULT_MODE
        self.__additional_info_counter = 0
        self.__toggle_skip_frames_counter = 0
        self.__kbs_modal = {}
        self.__kbs_no_modal = {}
        self.__kbs_editing = {}
        self.__mods = []

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

        self.__mods = mods

        for x in props:
            if x in self.__MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    names = [self.__kbs_modal,
                             self.__kbs_no_modal,
                             self.__kbs_editing]
                    self.__kbs_modal.update(
                            {y: self.__get_kbs(y, names)})

            elif x in self.__NOT_MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    names = [self.__kbs_modal,
                             self.__kbs_no_modal,
                             self.__kbs_editing]
                    self.__kbs_no_modal.update(
                            {y: self.__get_kbs(y, names)})

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

        self.__additional_info_counter = 0
        self.__toggle_skip_frames_counter = 0

        self.__mods = []

        self.__kbs_modal = {}
        self.__kbs_no_modal = {}
        self.__kbs_editing = {}

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

        logger.debug(f'Event {event.type}, {event.value}')

        # Simple events (event type is in digits and letters).
        if ((self.mode == self.__DEFAULT_MODE)
                or (event.type in self._BMToolModalInput__MODAL_LETTERS_LIST)
                or (event.type == 'PERIOD')
                or (event.type == 'BACK-SPACE')
                or (event.type == 'RET')
                or (event.type == 'SPACE'))\
                and event.value == 'PRESS':
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

        if self.mode is self.__DEFAULT_MODE:  # {{{

            # Get prop name and prop def for event.
            # Most of iterations this will be None,
            # including modal prop editing.
            prop_name = self.__get_prop_name(event)
            if prop_name is not None:

                # Get modifier
                mods = clusters[0].get_full_actual_modifiers_list()
                mod = mods[0]

                # Modifier prop def
                prop_def = mod.rna_type.properties[prop_name]
            else:
                prop_def = None

            logger.debug(f'Prop name is {prop_name}')
            logger.debug(f'Prop def is {prop_def}')

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
                logger.info(f'Switching to modal {prop_name}')
                self.mode = prop_name

            # Other props
            elif prop_name in self.__kbs_editing:
                pass
        # }}}

        elif self.mode in self.__kbs_modal:  # {{{

            # Get modifier
            mod = self.__mods[0]

            # Switch from mode with same kbs.
            # Get prop name for event.
            prop_name = self.__get_prop_name(event)
            if prop_name == self.mode\
                    and self.modal_input_mode in {'NONE', 'DELTA_D'}:
                logger.info('Switching back to default mode.')
                self.mode = self.__DEFAULT_MODE
                return

            # Try to switch to different input mode.
            # TODO: exit out of digits and str modes
            elif self.modal_input_mode in {'NONE', 'DELTA_D'}:

                # Get prop name and def for mode
                prop_name = self.mode
                prop_def = mod.rna_type.properties[self.mode]
                if event.type in self._BMToolModalInput__MODAL_DIGITS_LIST\
                        and prop_def.type in self.__DIGITS_INPUT_TYPES:
                    logger.info(f'Switching to modal digits {prop_name}')
                    self.modal_input_mode = 'DIGITS'
                    self.modal_digits(event)
                    return

                elif event.type\
                        in self._BMToolModalInput__MODAL_LETTERS_LIST\
                        and prop_def.type in self.__LETTERS_INPUT_TYPES:
                    logger.info(f'Switching to modal letters {prop_name}')
                    self.modal_input_mode = 'LETTERS'
                    self.modal_letters(event)
                    return

            # Letters or digits input mode.
            elif self.modal_input_mode in {'LETTERS', 'DIGITS'}:

                # Get prop name and def for mode
                prop_name = self.mode
                prop_def = mod.rna_type.properties[self.mode]

                if self.modal_input_mode == 'DIGITS':
                    if event.type == 'RET':
                        logger.info(f'Modal digits apply {prop_name}')
                        val = self.modal_digits_pop()
                        for mod in self.__mods:
                            setattr(mod, self.mode, val)
                        self.mode = self.__DEFAULT_MODE
                        return

                    logger.debug(f'Modal digits {prop_name}')
                    self.modal_digits(event)
                    return

                elif self.modal_input_mode == 'LETTERS':
                    if event.type == 'RET':
                        logger.info(f'Modal letters apply {prop_name}')
                        val = self.modal_letters_pop()
                        for mod in self.__mods:
                            setattr(mod, self.mode, val)
                        self.mode = self.__DEFAULT_MODE
                        return
                    logger.debug(f'Modal letters {prop_name}')
                    self.modal_letters(event)
                    return
        # }}}

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
        logger.info(f'Toggle {prop_name}')
        t = True
        for x in mods:
            attr = getattr(x, prop_name)
            if attr is True:
                t = False
        for x in mods:
            setattr(x, prop_name, t)

    def __scroll_enum(self, prop_name, prop, mods):
        logger.info(f'Scroll {prop_name}')
        for x in mods:
            attr = getattr(x, prop_name)
            enum = prop.enum_items.keys()
            i = enum.index(attr)
            if i == len(enum) - 1:
                setattr(x, prop_name, enum[0])
            else:
                setattr(x, prop_name, enum[i + 1])

    def __modal_int(self, event, prop_name, prop, mods):
        logger.debug(f'Modal int {prop_name}')
        for x in mods:
            attr_val = getattr(x, prop_name)
            new_val = self.modal_input_mouse(
                    attr_val, prop, event=event)
            setattr(x, prop_name, new_val)
        return

    def __modal_float(self, event, prop_name, prop, mods):
        logger.debug(f'Modal float {prop_name}')
        for x in mods:
            attr_val = getattr(x, prop_name)

            new_val = self.modal_input_mouse(
                    attr_val, prop, event=event)
            setattr(x, prop_name, new_val)
        return

    # TODO: what is that
    def __modal_str(self, event, prop_name, prop, mods):
        logger.debug(f'Modal str {prop_name}')
        return

    # Props {{{
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

    def __get_kbs(self, prop_name, props_dicts):
        if not isinstance(prop_name, str):
            raise TypeError
        result = prop_name[0].upper()
        result = [result, False, False, False]
        for z in range(4):
            if z == 0:
                continue
            for props in props_dicts:
                for x in props:
                    if props[x][0] == result[0]\
                            and props[x][1] == result[1]\
                            and props[x][2] == result[2]\
                            and props[x][3] == result[3]:
                        result[z] = True
        if len(result) > 4:
            raise TypeError
        return result
    # }}}

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

    def get_mappings_for_ui(self):
        """Returns list of strings with info about props.

        Example:
        ['Angle Limit: shift + A | 0.00123']
        """
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
                if len(self.__mods) != 0:
                    val = getattr(self.__mods[0], x)
                    line = line + f'{val}'
                result.append(line)

        for x in result:
            if not isinstance(x, str):
                raise TypeError
            if len(x) == 0:
                raise ValueError
        return result