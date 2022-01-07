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
    __MODES = {'NONE', 'DELTA', 'DIGITS', 'LETTERS'}

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

    __MODAL_DIGITS_LIST = list(__MODAL_DIGITS) + list(__MODAL_DIGITS_NUMPAD)

    __MODAL_DIGITS_EDITING = ['PERIOD', 'BACK-SPACE']
    __MODAL_LETTERS_EDITING = ['SPACE', 'BACK-SPACE']

    __MODAL_LETTERS_LIST\
        = list(__MODAL_LETTERS)\
        + __MODAL_DIGITS_LIST

    __DIGITS_TYPES = {'INT', 'FLOAT'}
    __LETTERS_TYPES = {'STR', 'ENUM'}

    # Currently active mode.
    # TODO: should this really be here
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

    # TODO: this method duplicated in adaptive modifiers editor.
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

    def modal_digits(self, event, prop_def):  # {{{
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

    def modal_letters(self, event, prop_def):  # {{{
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

    def modal_input_mouse(self, attr_val, prop, event, sens=1):  # {{{
        if not isinstance(attr_val, bool)\
                and not isinstance(attr_val, int)\
                and not isinstance(attr_val, float):
            raise TypeError
        if event is None:
            raise TypeError
        if prop is None:
            raise TypeError

        # Delta percentage
        # 10
        delta_pct = self.__get_delta_pct(event)
        # normalized 0.1
        delta_pct_f = delta_pct/100
        # pow 0.001
        delta_pct_i = pow(delta_pct_f, 2)

        if delta_pct > 100:
            delta = delta_pct
        else:
            # This variable should be used when possible
            delta = delta_pct_i

        # Distance
        v = self.__get_view3d_window()
        distance = v.data.view_distance

        # Max value
        max_val = prop.soft_max

        # Info
        logger.debug(
                f'delta: {delta_pct}, {delta_pct_f}, {delta_pct_i}, {delta}')
        logger.debug(f'Distance: {distance}')
        logger.debug(' ')
        logger.debug(f'Prop: {prop.name}')
        logger.debug(f'Type: {prop.type}')
        logger.debug(f'Subtype: {prop.subtype}')
        logger.debug(f'Units: {prop.unit}')
        logger.debug(f'Step: {prop.step}')
        logger.debug(f'Max value: {max_val}')

        if prop.type == 'INT':
            # use max as max percentage
            max_val = prop.soft_max
            x = delta_pct_i*max_val
            x = int(x)

        elif prop.type == 'FLOAT':
            if prop.subtype == 'NONE':
                result = float(distance*delta)

            elif prop.subtype in {'ANGLE', 'DEGREES'}:
                x = delta*(max_val/100)
                x = x / math.degrees(1)
                result = x

            elif prop.subtype == 'PERCENTAGE':
                result = delta

            elif prop.subtype in {'DISTANCE'}:
                if prop.unit in {'LENGTH'}:
                    x = distance*delta_pct_i

                    # limit
                    if x > max_val:
                        x = max_val
                    result = x

                else:
                    raise TypeError(
                        f'Not implemented prop unit type "{prop.unit}"')
            else:
                raise TypeError(
                    f'Not implemented prop subtype "{prop.subtype}"')
        else:
            raise TypeError(
                    f'Not implemented prop type "{prop.subtype}"')

        logger.debug(f'Returning {x}')

        if result is None:
            raise TypeError

        return result

    # Vector length
    def __vec_len(self, x1, x2, y1, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
    # }}}

    # Utils {{{
    def __get_view3d(self):
        a = None
        for x in bpy.context.window.screen.areas:
            if x.type == 'VIEW_3D':
                if a is None:
                    a = x
                else:
                    raise ValueError
        if a is None:
            raise ValueError
        return a

    def __get_view3d_window(self, v=None):
        if v is None:
            v = self.__get_view3d()
        a = None
        for x in v.regions:
            if x.type == 'WINDOW':
                if a is None:
                    a = x
                else:
                    raise ValueError
        if a is None:
            raise ValueError
        return a

    def __get_delta_pct(self, event, bounds=0, limit=100):
        """
        Returns float between 0 and 100 for event.
        """
        v = self.__get_view3d_window()
        d = (v.width, v.height)
        c = (d[0]/2, d[1]/2)

        if c[0] > c[1]:
            m = c[1]
        else:
            m = c[0]
        m = m - bounds

        # vec = self.__vec_len(event.mouse_x, c[0], event.mouse_y, c[1])
        vec = self.__vec_len(c[0], event.mouse_x, c[1], event.mouse_y)
        result = vec/(m/100)

        # Limit
        if result > limit:
            result = limit
        return result
    # }}}
