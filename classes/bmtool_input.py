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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMToolModalInput():

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

    __MODAL_LETTERS_AND_DIGITS_LIST\
        = list(__MODAL_LETTERS)\
        + list(__MODAL_DIGITS)\
        + list(__MODAL_DIGITS_NUMPAD)

    # Currently active mode.
    # modal_input_mode
    # }}}

    def __init__(self):
        self.modal_input_mode = self.__DEFAULT_MODE

    # Pop val {{{
    # This two methods are used to get variable value from modal input mode.
    def modal_digits_pop(self, number_type='ANY'):
        """Returns number that were typed in 'DIGITS' mode.
        number_type can be either 'ANY', 'INT' or 'FLOAT'.
        """
        result = self._modal_numbers_get_val(number_type)
        self.bmtool_modal_numbers_str = ''
        self.modal_input_mode = self.__DEFAULT_MODE
        return result

    def modal_str_pop(self):
        """Returns string that were typed in 'STRING' mode."""
        result = self.bmtool_modal_str
        self.bmtool_modal_str = ''
        self.modal_input_mode = self.__DEFAULT_MODE
        return result  # }}}

    def modal_digits(self, event):  # {{{
        """This thing writes a string that can be used in modal operator
        to get integer, float, or string.
        """
        for x in self.__MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.bmtool_modal_numbers_str\
                    = self.bmtool_modal_numbers_str + self.__MODAL_DIGITS[x]
                return True
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str + '.'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str[0:-1]
        elif event.type == 'RETURN' and event.value == 'PRESS':
            self.modal_input_mode = self._previous_mode
        else:
            return False
        return True  # }}}

    def modal_str(self, event):  # {{{
        """This thing writes a string that can be used in modal operator."""
        for x in self.__MODAL_LETTERS:
            if event.type == x and event.value == 'PRESS':
                if event.shift:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x
                else:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x.lower()
                return True
        for x in self.__MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.bmtool_modal_str = self.bmtool_modal_str + x
                return True
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str + '.'
        elif event.type == 'MINUS' and event.value == 'PRESS':
            if event.shift:
                self.bmtool_modal_numbers_str\
                        = self.bmtool_modal_numbers_str + '_'
            else:
                self.bmtool_modal_numbers_str\
                        = self.bmtool_modal_numbers_str + '-'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str[0:-1]
        elif event.type == 'RETURN' and event.value == 'PRESS':
            self.modal_input_mode = self._previous_mode
        else:
            return False
        return True  # }}}

    # Digits and letters input mode utils. {{{
    def __digits_get_val(self, t='ANY'):
        if len(self.bmtool_modal_numbers_str) == 0:
            return None

        if t == 'ANY':
            if '.' in self.bmtool_modal_numbers_str:
                return float(self.bmtool_modal_numbers_str)
            else:
                return int(self.bmtool_modal_numbers_str)
        elif t == 'INT':
            i = None
            for z, x in enumerate(self.bmtool_modal_numbers_str):
                if x == '.':
                    i = z
            return int(self.bmtool_modal_numbers_str[0:i])
        elif t == 'FLOAT':
            result = copy.copy(self.bmtool_modal_numbers_str)
            f = False
            for x in self.bmtool_modal_numbers_str:
                if x == '.':
                    f = True
            if f is False:
                result = result + '.0'
            return float(result)
    # }}}

    # delta_d {{{
    # TODO: should be in utils
    # Returns VL
    # VL = vector length
    # VL from object center (currently from initialisation)
    # TODO: should take into consideration distance to object center.
    # TODO: should use object center as center.
    # TODO: should not change settings when changing mode
    def delta_d(self, event):
        x = self.__vec_len(self.first_x, event.mouse_x,
                           self.first_y, event.mouse_y
                           )
        y = pow(x, 2)
        return y

    # Vector length
    def __vec_len(self, x1, x2, y1, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
    # }}}
