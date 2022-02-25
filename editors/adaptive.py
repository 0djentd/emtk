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
import logging
import typing
import string

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..libs.emtk.dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False

from ..libs.emtk.utils.modifier_prop_types import get_props_filtered_by_types
from ..libs.emtk.clusters.cluster_trait import ClusterTrait
from ..classes.editor import ModalClustersEditor
from ..libs.modal_input.shortcuts import generate_new_shortcut

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

# TODO: add modifiers types switcher.
# TODO: remove some constants from AdaptiveModalEditor class.


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
    

    # Constructor {{{
    # Currently active mode.
    # self.mode

    # Currently active modal input mode.
    # This variable initialized in ModalInputOperator()
    # self.modal_input_mode

    # List of all modifiers
    # self.__mods

    # Property rna_type struct
    # self.__prop_def

    # Sets of modifier props names.
    # Modal editing prop only.
    # __kbs_modal = set()
    # Not modal prop editing.
    # __kbs_no_modal = set()
    # Not a modifier prop.
    # __kbs_editing = set()

    def __init__(self, *args, allow_cluster=True, **kwargs):
        super().__init__(*args,
                         name='Adaptive_Editor',
                         obj_types=['ANY'],
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
    

    # ClustersEditor methods {{{
    def editor_switched_to(self, context, clusters):  
        """Called every time editor is switched to."""

        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        self.__switch_to_default()

        self.__kbs_modal = set()
        self.__kbs_no_modal = set()
        self.__kbs_editing = set()

        mods = self.__get_all_clusters_modifiers(clusters)
        mod = mods[0]
        self.__mods = mods

        # Get existing shortcuts
        prefs = bpy.context.preferences.addons['bmtools'].preferences
        s = prefs.modal_shortcuts.find_by_value(mod.type)
        self.modal_shortcuts = s

        # Filter properties.
        props = get_props_filtered_by_types(mods[0])
        for x in props:
            if x in self.__MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    self.__kbs_modal.add(y)
            elif x in self.__NOT_MODAL_INPUT_PROP_TYPES:
                for y in props[x]:
                    self.__kbs_no_modal.add(y)
            else:
                raise TypeError

        # Generate missing shortcuts.
        new_props = []
        for x in props:
            for y in props[x]:
                if not s.find_by_shortcut_id(y):
                    new_props.append(x)
        for x in new_props:
            s.add(generate_new_shortcut(x, s.shortcuts))

        logger.debug('Editor switched to.')
        logger.debug('Modal props mappings')
        logger.debug(self.__kbs_modal)
        logger.debug('Not modal props mappings')
        logger.debug(self.__kbs_no_modal)
        logger.debug('Editing mappings')
        logger.debug(self.__kbs_editing)
    

    def editor_switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        if not isinstance(clusters, list):
            clusters = [clusters]
        for x in clusters:
            if not isinstance(x, ClusterTrait):
                raise TypeError

        self.__switch_to_default()
        self.__mods = []
        self.__kbs_modal = set()
        self.__kbs_no_modal = set()
        self.__kbs_editing = set()
        logger.debug('Editor switched from.')

    def editor_modal_pre(
            self, context, event, *args, **kwargs):
        return

    def editor_modal(
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
    

    def __default_mode(self, event):  
        """
        No props besides bools and enums can be edited in default mode.
        No modal input mode can be used in default mode.
        Shortcuts form __kbs_editing and __kbs_no_modal can only be
        used in default mode.

        Returns True if event was interpreted.
        """
        logger.debug('Default mode')

        if self.modal_input_mode != 'NONE':
            raise ValueError
        if not self.__check_event_is_simple(event):
            return

        # Get prop name for this event.
        prop_name = self.__get_shortcut_value(event)

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
    

    def __modal_mode(self, event):  
        """
        Mode used to edit properties within multiple iterations.

        When in modal mode, modal_input_mode shoul never be NONE.

        modal_input_mode always correct for active mode.
        This means there is no reason to check it twice.

        When in modal_input_mode, all complex events
        should go to ModalInput.

        Returns True if event was interpreted.
        """
        logger.debug(f'Modal {self.modal_input_mode}')

        if self.modal_input_mode == 'DELTA':
            if self.__check_event_is_simple(event):
                if self.__check_if_should_switch_mode(event):
                    return True
                elif self.__check_if_should_switch_input_mode(event):
                    return True
            else:
                if self.__check_if_delta_prop_changed(event):
                    return True

        elif self.modal_input_mode == 'DIGITS':
            if self.__check_event_is_simple(event):
                if self.__check_if_stop_modal_digits(event):
                    return True
                elif self.__check_if_modal_digits(event):
                    return True
            else:
                return

        elif self.modal_input_mode == 'LETTERS':
            if self.__check_event_is_simple(event):
                if self.__check_if_stop_modal_letters(event):
                    return True
                elif self.__check_if_modal_letters(event):
                    return True
            else:
                return
        else:
            raise TypeError
    

    # Simple events {{{
    def __check_if_should_switch_mode(self, event):
        prop_name = self.__get_shortcut_value(event)
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
                in string.ascii_uppercase\
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
    
    

    # Complex events {{{
    def __check_if_delta_prop_changed(self, event) -> None:

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
        for x in self.__mods:
            new_val = self.modal_input_mouse_rna_type(
                x, prop_name, event)
            setattr(x, prop_name, new_val)
        return

    def __modal_float(self, event, prop_name):
        logger.debug(f'Modal float {prop_name}')
        for x in self.__mods:
            new_val = self.modal_input_mouse_rna_type(
                x, prop_name, event)
            setattr(x, prop_name, new_val)
        return

    def __modal_str(self, event, prop_name):
        logger.debug(f'Modal str {prop_name}')
        return
    

    # Utils {{{
    def __get_shortcut_value(
            self, event: bpy.types.Event) -> typing.Union[str, None]:
        logger.debug(f'Look up kbs for {event.type}')
        if len(event.type) != 1:
            return None
        s = self.modal_shortcuts.find_by_event(event)
        if s:
            return s.shortcut_id
        return None

    def __check_event_is_simple(self, event: bpy.types.Event) -> bool:
        """Checks if event should not be passed to modal input base class."""
        if (event.type in string.ascii_uppercase
                or event.type in {'PERIOD', 'BACK-SPACE', 'RET', 'SPACE'})\
                and event.value == 'PRESS':
            return True
        return False

    def __get_all_clusters_modifiers(self, clusters):
        """Returns list of modifiers to edit."""
        if not isinstance(clusters, list):
            clusters = [clusters]
        mods = []
        for x in clusters:
            mods.extend(x.all_modifiers())

        # Check that modifiers are of same type.
        t = None
        for x in mods:
            if t is None:
                t = x.type
            elif x.type != t:
                raise TypeError
        return mods

    def __switch_to_mode(self, mode_name: str) -> None:
        if mode_name == self.__DEFAULT_MODE:
            return self.__switch_to_default()
        self.mode = mode_name
        self.__prop_def = self.__mods[0].rna_type.properties[mode_name]

    def __switch_to_default(self) -> None:
        self.mode = self.__DEFAULT_MODE
        self.modal_input_mode = self._ModalInputOperator__DEFAULT_MODE
        self.__prop_def = None
    

    # UI {{{
    def get_mappings_for_ui(self):
        """Returns list of strings with info about props.

        Example:
        ['Angle Limit: shift + A | 0.00123']
        """

        result = []
        for x in self.modal_shortcuts.shortcuts:
            result.append(str(x) + ' ' + self.__get_props_val_format(
                getattr(self.__mods[0], x.shortcut_id), x.shortcut_id))
        return result

    def __get_props_val_format(self,
                               value,
                               attr_name: str,
                               round_val: int = 2):
        """
        [['123.456']...]
        """
        prop_def = self.__mods[0].rna_type.properties[attr_name]
        if prop_def.type == 'FLOAT':
            if prop_def.subtype in {'ANGLE', 'DEGREES'}:
                value = value * math.degrees(1)
            value = round(value, round_val)
        line = str(value)
        if len(line) == 0:
            line = 'No kb shortcut.'
        return line
    
