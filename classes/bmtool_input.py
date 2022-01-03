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
import copy
import logging
import string

import bpy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMToolModalInput():
    """Base class for modal operators and editors."""

    # Constants {{{
    __MODES = {'NONE', 'DELTA_D', 'DIGITS', 'LETTERS'}

    __DEFAULT_MODE = 'NONE'

    __MODAL_LETTERS = list(string.ascii_uppercase)

    __MODAL_DIGITS = {
                     'ZERO': '0',
                     'ONE': '1',
                     'TWO': '2',
                     'THREE': '3',
                     'FOUR': '4',
                     'FIVE': '5',
                     'SIX': '6',
                     'SEVEN': '7',
                     'EIGHT': '8',
                     'NINE': '9',
                     }

    __MODAL_DIGITS_NUMPAD = {
                            'NUMPAD_0': '0',
                            'NUMPAD_1': '1',
                            'NUMPAD_2': '2',
                            'NUMPAD_3': '3',
                            'NUMPAD_4': '4',
                            'NUMPAD_5': '5',
                            'NUMPAD_6': '6',
                            'NUMPAD_7': '7',
                            'NUMPAD_8': '8',
                            'NUMPAD_9': '9',
                            }

    __MODAL_DIGITS_EDITING = ['PERIOD', 'BACK-SPACE']
    __MODAL_LETTERS_EDITING = ['SPACE', 'BACK-SPACE']

    __MODAL_DIGITS_LIST = list(__MODAL_DIGITS) + list(__MODAL_DIGITS_NUMPAD)

    __MODAL_LETTERS_LIST\
        = list(__MODAL_LETTERS)\
        + __MODAL_DIGITS_LIST

    # Currently active mode.
    # modal_input_mode
    # }}}

    # Variables {{{
    sens = {
            'INT': {
                    'UNSIGNED': 1,
                    'NONE': 0.5,
                    },

            'FLOAT': {
                      'UNSIGNED': 0.0005,
                      'ANGLE': 0.01,
                      'DEGREES': 0.01,
                      'DISTANCE': 0.005,
                      'NONE': 0.005,
                      },
            }
    # }}}

    # Properties {{{
    @property
    def modal_input_mode(self):
        if self.__editor_removed:
            raise ValueError

        return self.__modal_input_mode

    @modal_input_mode.setter
    def modal_input_mode(self, mode):
        if mode not in self.__MODES:
            raise TypeError

        self.__prop = None
        self.__modal_digits_str = ''
        self.__modal_letters_str = ''
        self.__modal_input_mode = mode
    # }}}

    def switch_mode(self, mode: str, prop_def=None):
        """
        This method should be used instead of modal_input_mode property
        when possbile.
        """
        self.modal_input_mode = mode
        if prop_def is not None and mode != self.__DEFAULT_MODE:
            self.__prop = prop_def
        else:
            self.__prop = None

    def __init__(self):
        # Mode
        self.__modal_input_mode = self.__DEFAULT_MODE

        # Property rna_type struct
        self.__prop = None

        # Str
        self.__modal_digits_str = ''
        self.__modal_letters_str = ''

        self.__editor_removed = False

    # Pop val {{{
    # This two methods are used to get variable value from modal input mode.
    def modal_digits_pop(self, number_type='ANY'):
        """Returns number that were typed in 'DIGITS' mode.

        number_type can be either 'ANY', 'INT' or 'FLOAT'.
        """

        result = self.modal_digits_get(number_type)
        self.__modal_digits_str = ''
        self.modal_input_mode = self.__DEFAULT_MODE
        return result

    def modal_letters_pop(self):
        """Returns string that were typed in 'STRING' mode."""

        result = self.__modal_letters_str
        self.__modal_letters_str = ''
        self.modal_input_mode = self.__DEFAULT_MODE
        return result
    # }}}

    # Get val {{{
    def modal_digits_get(self, number_type='ANY'):
        """Returns number or str."""
        if len(self.__modal_digits_str) == 0:
            return None

        if number_type == 'ANY':
            if '.' in self.__modal_digits_str:
                return float(self.__modal_digits_str)
            else:
                return int(self.__modal_digits_str)
        elif number_type == 'INT':
            i = None
            for z, x in enumerate(self.__modal_digits_str):
                if x == '.':
                    i = z
            return int(self.__modal_digits_str[0:i])
        elif number_type == 'FLOAT':
            result = copy.copy(self.__modal_digits_str)
            f = False
            for x in self.__modal_digits_str:
                if x == '.':
                    f = True
            if f is False:
                result = result + '.0'
            return float(result)

    def modal_letters_get(self) -> str:
        """Returns str."""
        return copy.copy(self.__modal_letters_str)
    # }}}

    def modal_digits(self, event):  # {{{
        """Writes a string that can be used to get integer or float."""

        if self.modal_input_mode != 'DIGITS':
            raise ValueError

        # Digits
        for x in self.__MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.__modal_digits_str\
                    = self.__modal_digits_str + self.__MODAL_DIGITS[x]
                return True

        for x in self.__MODAL_DIGITS_NUMPAD:
            if event.type == x and event.value == 'PRESS':
                self.__modal_digits_str\
                    = self.__modal_digits_str + self.__MODAL_DIGITS_NUMPAD[x]
                return True

        # Anything else
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.__modal_digits_str = self.__modal_digits_str + '.'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.__modal_digits_str = self.__modal_digits_str[0:-1]
        else:
            return False
        return True
    # }}}

    def modal_letters(self, event):  # {{{
        """This thing writes a string that can be used in modal operator."""

        if self.modal_input_mode != 'LETTERS':
            raise ValueError

        # Letters
        for x in self.__MODAL_LETTERS:
            if event.type == x and event.value == 'PRESS':
                if event.shift:
                    self.__modal_letters_str\
                            = self.__modal_letters_str + x
                else:
                    self.__modal_letters_str\
                            = self.__modal_letters_str + x.lower()
                return True

        # Digits
        for x in self.__MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.__modal_letters_str\
                        = self.__modal_letters_str\
                        + self.__MODAL_DIGITS[x]
                return True

        # Digits 2
        for x in self.__MODAL_DIGITS_NUMPAD:
            if event.type == x and event.value == 'PRESS':
                self.__modal_letters_str\
                        = self.__modal_letters_str\
                        + self.__MODAL_DIGITS_NUMPAD[x]
                return True

        # Anything else
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.__modal_letters_str = self.__modal_letters_str + '.'
        elif event.type == 'MINUS' and event.value == 'PRESS':
            if event.shift:
                self.__modal_letters_str\
                        = self.__modal_letters_str + '_'
            else:
                self.__modal_letters_str\
                        = self.__modal_letters_str + '-'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.__modal_letters_str = self.__modal_letters_str[0:-1]
        else:
            return False
        return True
    # }}}

    def modal_input_mouse(self, attr_val, prop, event):  # {{{
        if not isinstance(attr_val, bool)\
                and not isinstance(attr_val, int)\
                and not isinstance(attr_val, float):
            raise TypeError
        if event is None:
            raise TypeError
        if prop is None:
            raise TypeError

        x = self.__vec_len(self.first_x, event.mouse_x,
                           self.first_y, event.mouse_y
                           )

        if prop.subtype == 'UNSIGNED':
            raise ValueError('Not implemented')

        try:
            z = self.sens[prop.type][prop.subtype]
        except KeyError:
            print(f'No sens for {prop.name}, {prop.type}, {prop.subtype}')
            z = 1

        x = x * prop.step * z

        if prop.type == 'INT':
            x = int(x)

        elif prop.type == 'FLOAT':
            if prop.subtype in {'ANGLE', 'DEGREES'}:
                x = x / math.degrees(1)

            # # TODO: calculate distance to obj
            # elif prop.subtype in {'LENGTH', 'DISTANCE'}:
            #     x = x * distance_to_object
            else:
                x = float(x)
        else:
            raise TypeError

        y = pow(x, 2)
        return y

    # Vector length
    def __vec_len(self, x1, x2, y1, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
    # }}}


# Shortcuts utils {{{
def get_custom_modal_kbs(addon='bmtools'):
    if not isinstance(addon, str):
        raise TypeError

    addon_prefs\
        = bpy.context.preferences.addons[addon].preferences

    result = []
    for x in addon_prefs.props_names:
        kbs_1 = get_kbs(addon, x)
        kbs_2 = get_default_kbs(addon, x)
        if not compare_kbs(kbs_1, kbs_2):
            result.append(kbs_1)
    return result


def get_kbs(addon, kbs_name):
    addon_prefs\
        = bpy.context.preferences.addons[addon].preferences
    kbs = (
           getattr(addon_prefs, f'{kbs_name}'),
           getattr(addon_prefs, f'{kbs_name}_shift'),
           getattr(addon_prefs, f'{kbs_name}_ctl'),
           getattr(addon_prefs, f'{kbs_name}_alt'),
           )
    return kbs


def get_default_kbs(addon, kbs_name):
    addon_prefs\
        = bpy.context.preferences.addons[addon].preferences
    kbs = (
           getattr(addon_prefs, f'{kbs_name}.default'),
           getattr(addon_prefs, f'{kbs_name}_shift.default'),
           getattr(addon_prefs, f'{kbs_name}_ctl.default'),
           getattr(addon_prefs, f'{kbs_name}_alt.default'),
           )
    return kbs


def compare_kbs(kbs_1, kbs_2):
    if not isinstance(kbs_1, tuple):
        raise TypeError
    if not isinstance(kbs_2, tuple):
        raise TypeError
    if len(kbs_1) != 4:
        raise ValueError
    if len(kbs_2) != 4:
        raise ValueError
    if kbs_1[0] != kbs_2[0]\
            or kbs_1[1] != kbs_2[1]\
            or kbs_1[2] != kbs_2[2]\
            or kbs_1[3] != kbs_2[3]:
        return False
    return True
# }}}
