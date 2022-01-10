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

import math
# import string
import logging
# import copy
# import json
# import time
import re

import bpy

# from .bmtool_input import ModalInputOperator
from ..lib.utils.modifier_prop_types import get_props_filtered_by_types
from ..lib.clusters.cluster_trait import ClusterTrait
from ..classes.editor import ModalClustersEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AdaptiveModalEditor(ModalClustersEditor):
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
    __DELTA_INPUT_TYPES = {'INT', 'FLOAT'}

    # Can be edited using digits input.
    __DIGITS_INPUT_TYPES = {'INT', 'FLOAT'}

    # Can be edited using letters and digits input.
    __LETTERS_INPUT_TYPES = {'STRING'}

    # All types that use some type of modal editing.
    __MODAL_INPUT_PROP_TYPES\
        = __LETTERS_INPUT_TYPES.union(
                __DIGITS_INPUT_TYPES.union(
                    __DELTA_INPUT_TYPES))

    # All types that can be edited in default mode without switching.
    __NOT_MODAL_INPUT_PROP_TYPES = __TOGGLE_TYPES

    # Default editor mode.
    __DEFAULT_MODE = 'NO_MODE'
    # }}}

    # Variables {{{
    # Currently active mode.
    # self.mode

    # Currently active modal input mode.
    # This variable initialized in ModalInputOperator()
    # self.modal_input_mode

    # List of all modifiers
    # self.__mods

    # Property rna_type struct
    # self.__prop_def

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

    # Constructor {{{
    def __init__(self, *args, allow_cluster=True, **kwargs):
        t = self.__MODIFIER_TYPES

        # Allow using with '{mod_name}_CLUSTER' cluster types.
        if allow_cluster:
            new_types = []
            for x in self.__MODIFIER_TYPES:
                new_types.append(f'{x}_CLUSTER')
            t = t + new_types

        super().__init__(*args,
                         name='Adaptive_Editor',
                         cluster_types=t,
                         **kwargs)

        self.mode = self.__DEFAULT_MODE
        # Mappings
        self.__kbs_modal = {}
        self.__kbs_no_modal = {}
        self.__kbs_editing = {}

        # This variable is changed every time
        # modifiers type or editor is switched.
        self.__mods = []
        self.prop_def = None
    # }}}

    # ClustersEditor methods {{{
    def editor_switched_to(self, context, clusters):  # {{{
        """Called every time editor is switched to."""

        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        self.__switch_to_default()

        # Modal editing prop only.
        self.__kbs_modal = {}

        # Not modal prop editing.
        self.__kbs_no_modal = {}

        # Not a modifier prop.
        self.__kbs_editing = {}

        mods = self.__get_all_clusters_modifiers(clusters)
        mod = mods[0]
        self.__mods = mods
        prefs = bpy.context.preferences.addons['bmtools'].preferences
        kbs = prefs.get_modal_operators_shortcuts_group(mod.type)

        props = get_props_filtered_by_types(mods[0])
        for x in props:
            if x in self.__MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    try:
                        self.__kbs_modal.update({y: kbs[y]})
                    except KeyError:
                        s = prefs.generate_new_shortcut(x, y)
                        self.__kbs_modal.update(s)
            elif x in self.__NOT_MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    try:
                        self.__kbs_no_modal.update({y: kbs[y]})
                    except KeyError:
                        s = prefs.generate_new_shortcut(x, y)
                        self.__kbs_no_modal.update(s)
            else:
                raise TypeError

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

        self.__switch_to_default()

        self.__mods = []

        self.__kbs_modal = {}
        self.__kbs_no_modal = {}
        self.__kbs_editing = {}

        logger.debug('Editor switched from.')
    # }}}

    def editor_modal_pre(  # {{{
            self, context, event, *args, **kwargs):
        return
    # }}}

    def editor_modal(  # {{{
            self, context, event, *args, **kwargs):

        logger.debug(f'Event {event.type}, {event.value}')

        if self.mode == self.__DEFAULT_MODE:
            self.__default_mode(event)
        elif self.mode in self.__kbs_modal:
            self.__modal_mode(event)
        elif self.mode in self.__kbs_editing:
            raise ValueError
        elif self.mode in self.__kbs_no_modal:
            raise ValueError
    # }}}
    # }}}

    def __default_mode(self, event):  # {{{
        """
        No props besides bools and enums can be edited in default mode.
        No modal input mode can be used in default mode.
        Shortcuts form __kbs_editing and __kbs_no_modal can only be
        used in default mode.

        Returns True if event was interpreted.
        """
        logger.debug('Default')

        if self.modal_input_mode != 'NONE':
            raise ValueError
        if not self.__check_event_is_simple(event):
            return

        # Get prop name for this event.
        prop_name = self.__get_shortcut_name(event)

        if prop_name is not None:

            # Modifier prop def
            prop_def = self.__mods[0].rna_type.properties[prop_name]

            # Try to edit not modal props.
            if prop_name in self.__kbs_no_modal:
                if prop_def.type == 'BOOLEAN':
                    if self.__toggle_bool(prop_name):
                        return True
                elif prop_def.type == 'ENUM':
                    if self.__scroll_enum(prop_name):
                        return True
                else:
                    raise TypeError

            # Try to switch to modal prop mode.
            elif prop_name in self.__kbs_modal:
                logger.info(f'Switching to modal {prop_name}')
                self.__switch_to_mode(prop_name)

                # Switch to modal input mode
                t = prop_def.type
                if t in self.__DELTA_INPUT_TYPES:
                    self.modal_input_mode = 'DELTA'
                elif t in self.__DIGITS_INPUT_TYPES:
                    self.modal_input_mode = 'DIGITS'
                elif t in self.__LETTERS_INPUT_TYPES:
                    self.modal_input_mode = 'LETTERS'
                else:
                    raise TypeError
                return True

            # Other props
            elif prop_name in self.__kbs_editing:
                pass
        else:
            pass
    # }}}

    def __modal_mode(self, event):  # {{{
        """
        Mode used to edit properties within multiple iterations.

        When in modal mode, modal_input_mode shoul never be NONE.

        modal_input_mode always correct for active mode.
        This means there is no reason to check it twice.

        When in modal_input_mode, all complex events
        should go to ModalInput.

        Returns True if event was interpreted.
        """
        if self.modal_input_mode == 'NONE':
            raise TypeError

        if self.modal_input_mode == 'DELTA':
            logger.debug('Modal delta')

            if self.__check_event_is_simple(event):
                if self.__check_if_should_switch_mode(event):
                    return True
                elif self.__check_if_should_switch_input_mode(event):
                    return True
            else:
                if self.__check_if_delta_prop_changed(event):
                    return True

        elif self.modal_input_mode == 'DIGITS':
            logger.debug('Modal digits')

            if self.__check_event_is_simple(event):
                if self.__check_if_stop_modal_digits(event):
                    return True
                elif self.__check_if_modal_digits(event):
                    return True
            else:
                return

        elif self.modal_input_mode == 'LETTERS':
            logger.debug('Modal letters')

            if self.__check_event_is_simple(event):
                if self.__check_if_stop_modal_letters(event):
                    return True
                elif self.__check_if_modal_letters(event):
                    return True
            else:
                return
        else:
            raise TypeError
    # }}}

    # Simple events {{{
    def __check_if_should_switch_mode(self, event):

        prop_name = self.__get_shortcut_name(event)
        if prop_name == self.mode:
            logger.info('Switching back to default mode.')
            self.__switch_to_default()
            return True

    def __check_if_should_switch_input_mode(self, event):

        # TODO: move to attrs
        # Get prop name and def for mode
        prop_name = self.mode
        prop_def = self.__mods[0].rna_type.properties[self.mode]

        if event.type in self._ModalInputOperator__MODAL_DIGITS_LIST\
                and prop_def.type in self.__DIGITS_INPUT_TYPES:
            logger.info(f'Switching to modal digits {prop_name}')
            self.modal_input_mode = 'DIGITS'
            self.modal_digits(event, prop_def)
            return True

        elif event.type\
                in self._ModalInputOperatort__MODAL_LETTERS_LIST\
                and prop_def.type in self.__LETTERS_INPUT_TYPES:
            logger.info(f'Switching to modal letters {prop_name}')
            self.modal_input_mode = 'LETTERS'
            self.modal_letters(event, prop_def)
            return True

    # Digits and letters {{{
    def __check_if_modal_letters(self, event):
        # Get prop name and def for mode
        prop_name = self.mode
        prop_def = self.__mods[0].rna_type.properties[self.mode]

        logger.debug(f'Modal letters {prop_name}')
        if self.modal_letters(event, prop_def):
            return True

    def __check_if_stop_modal_letters(self, event):
        # Get prop name and def for mode
        prop_name = self.mode

        if event.type == 'RET':
            logger.info(f'Modal digits apply {prop_name}')
            val = self.modal_digits_pop()
            for mod in self.__mods:
                setattr(mod, self.mode, val)
            self.__switch_to_default()
            return True

    def __check_if_modal_digits(self, event):
        # Get prop name and def for mode
        prop_name = self.mode
        prop_def = self.__mods[0].rna_type.properties[self.mode]

        logger.debug(f'Modal digits {prop_name}')
        if self.modal_digits(event, prop_def):
            return True

    def __check_if_stop_modal_digits(self, event):
        # Get prop name and def for mode
        prop_name = self.mode

        if event.type == 'RET':
            logger.info(f'Modal letters apply {prop_name}')
            val = self.modal_letters_pop()
            for mod in self.__mods:
                setattr(mod, self.mode, val)
            self.__switch_to_default()
            return True
    # }}}
    # }}}

    # Complex events {{{
    def __check_if_delta_prop_changed(self, event):

        # Use active mode prop name.
        prop_name = self.mode
        prop_def = self.__mods[0].rna_type.properties[prop_name]

        logger.debug(f'Modal check if delta changed {prop_name}')

        if event.type not in {'MOUSEMOVE'}:
            return

        # Try to edit props.
        if prop_def.type == 'INT':
            self.__modal_int(event, prop_name)
        elif prop_def.type == 'FLOAT':
            self.__modal_float(event, prop_name)
        elif prop_def.type == 'STRING':
            self.__modal_str(event, prop_name)
        return
    # }}}

    # Properties editing {{{
    def __toggle_bool(self, prop_name):
        logger.info(f'Toggle {prop_name}')

        t = True
        for x in self.__mods:
            attr = getattr(x, prop_name)
            if attr is True:
                t = False
        for x in self.__mods:
            setattr(x, prop_name, t)

    def __scroll_enum(self, prop_name):
        logger.info(f'Scroll {prop_name}')

        prop_def = self.__mods[0].rna_type.properties[prop_name]
        for x in self.__mods:
            attr = getattr(x, prop_name)
            enum = prop_def.enum_items.keys()
            i = enum.index(attr)
            if i == len(enum) - 1:
                setattr(x, prop_name, enum[0])
            else:
                setattr(x, prop_name, enum[i + 1])

    def __modal_int(self, event, prop_name):
        logger.debug(f'Modal int {prop_name}')

        prop_def = self.__mods[0].rna_type.properties[prop_name]
        for x in self.__mods:
            attr_val = getattr(x, prop_name)
            new_val = self.modal_input_mouse(
                    attr_val, prop_def, event=event)
            setattr(x, prop_name, new_val)
        return

    def __modal_float(self, event, prop_name):
        logger.debug(f'Modal float {prop_name}')

        prop_def = self.__mods[0].rna_type.properties[prop_name]
        for x in self.__mods:
            attr_val = getattr(x, prop_name)
            new_val = self.modal_input_mouse(
                    attr_val, prop_def, event=event)
            setattr(x, prop_name, new_val)
        return

    def __modal_str(self, event, prop_name):
        logger.debug(f'Modal str {prop_name}')
        return
    # }}}

    # Props utils {{{
    def __get_shortcut_name(self, event) -> str:
        """Returns property name that were mapped to event type."""
        if len(event.type) > 1:
            return

        d = [self.__kbs_modal, self.__kbs_no_modal, self.__kbs_editing]
        for x in d:
            a = self.__get_shortcut_from_dict(event, x)
            if a is not None:
                return a

    def __get_shortcut_from_dict(self, event, kbs: dict) -> str:
        if not isinstance(kbs, dict):
            raise TypeError
        for x in kbs:
            if not isinstance(kbs[x], dict):
                raise TypeError

        logger.debug(f'Trying to get prop for {event.type} in {kbs}')
        for x in kbs:
            e = kbs[x]
            if event.type == e['letter']\
                    and event.shift == e['shift']\
                    and event.ctrl == e['ctrl']\
                    and event.alt == e['alt']:
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

    # Utils {{{
    def __check_event_is_simple(self, event):
        """Checks if event should not be passed to modal input base class."""
        if (event.type in self._ModalInputOperator__MODAL_LETTERS_LIST
                or event.type in {'PERIOD', 'BACK-SPACE', 'RET', 'SPACE'})\
                and event.value == 'PRESS':
            return True

    def __get_all_clusters_modifiers(self, clusters):
        """Returns list of modifiers to edit."""
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

    def __switch_to_mode(self, mode_name):
        if not isinstance(mode_name, str):
            raise TypeError
        if mode_name == self.__DEFAULT_MODE:
            return self.__switch_to_default()

        self.mode = mode_name
        self.__prop_def = self.__mods[0].rna_type.properties[mode_name]

    def __switch_to_default(self):
        self.mode = self.__DEFAULT_MODE
        self.modal_input_mode = self._ModalInputOperator__DEFAULT_MODE
        self.__prop_def = None
    # }}}

    # UI {{{
    def get_mappings_for_ui(self):
        """Returns list of strings with info about props.

        Example:
        ['Angle Limit: shift + A | 0.00123']
        """
        result = []
        d = [self.__kbs_modal, self.__kbs_no_modal, self.__kbs_editing]
        a = self.__get_props_names_format(d)
        b = self.__get_props_kbs_format(d)
        c = self.__get_props_val_format(d)

        result = []
        for x, y, z in zip(a, b, c):
            e = [x['name'],
                 y['shortcut'],
                 z['value']]

            line = ''
            for f in e:
                a = f
                length = len(a)
                if length < 20:
                    for h in range(20 - length):
                        a = a + " "
                if length > 20:
                    a = a[0:17] + '...'

                line = line + a

            result.append(line)

        for x in result:
            if not isinstance(x, str):
                raise TypeError
            if len(x) == 0:
                raise ValueError
        return result

    def __get_props_names_format(self, d):
        """
        [['angle_limit', 'Angle Limit']...]
        """

        result = []

        # All props mappings
        d = [self.__kbs_modal, self.__kbs_no_modal, self.__kbs_editing]
        for a in d:
            for x in a:
                name = re.sub('_', ' ', x).title()
                result.append({'name': name})
        return result

    def __get_props_kbs_format(self, d):
        """
        [['A + shift + ctrl']...]
        """

        result = []
        for a in d:
            for x in a:
                t = a[x]

                line = ''
                if t['shift']:
                    line = line + 'shift + '
                if t['ctrl']:
                    line = line + 'ctl + '
                if t['alt']:
                    line = line + 'alt + '
                line = line + f'{t["letter"]}'

                if len(line) == 0:
                    line = 'No kb shortcut.'
                result.append({'shortcut': line})
        return result

    def __get_props_val_format(self, d, round_val=2):
        """
        [['123.456']...]
        """

        result = []
        for a in d:
            for x in a:
                prop_def = self.__mods[0].rna_type.properties[x]
                val = getattr(self.__mods[0], x)
                if prop_def.type == 'FLOAT':
                    if prop_def.subtype in {'ANGLE', 'DEGREES'}:
                        val = val * math.degrees(1)
                    val = round(val, round_val)
                line = str(val)
                if len(line) == 0:
                    line = 'No kb shortcut.'
                result.append({'value': line})
        return result
    # }}}