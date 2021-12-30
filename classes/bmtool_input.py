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

import copy
import logging
import string

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMToolModalInput():

    # Constants {{{
    _MODAL_LETTERS = string.ascii_uppercase

    _MODAL_DIGITS = {
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

    _MODAL_DIGITS_NUMPAD = {
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
    # }}}

    # Pop val {{{
    # This two methods are used to get variable value from modal input mode.
    def modal_digits_pop(self, number_type='ANY'):
        """Returns number that were typed in 'DIGITS' mode.
        number_type can be either 'ANY', 'INT' or 'FLOAT'.
        """
        result = self._modal_numbers_get_val(number_type)
        self._modal_numbers_clear()
        return result

    def modal_str_pop(self):
        """Returns string that were typed in 'STRING' mode."""
        result = self.bmtool_modal_str
        self._modal_str_clear()
        return result  # }}}

    def modal_digits(self, event):  # {{{
        """This thing writes a string that can be used in modal operator
        to get integer, float, or string.
        """
        for x in self._MODAL_DIGITS:
            if event.type == x and event.value == 'PRESS':
                self.bmtool_modal_numbers_str\
                    = self.bmtool_modal_numbers_str + self._MODAL_DIGITS[x]
                return True
        if event.type == 'PERIOD' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str + '.'
        elif event.type == 'BACK-SPACE' and event.value == 'PRESS':
            self.bmtool_modal_numbers_str = self.bmtool_modal_numbers_str[0:-1]
        elif event.type == 'RETURN' and event.value == 'PRESS':
            self._mode = self._previous_mode
        else:
            return False
        return True  # }}}

    def modal_str(self, event):  # {{{
        """This thing writes a string that can be used in modal operator."""
        for x in self._MODAL_LETTERS:
            if event.type == x and event.value == 'PRESS':
                if event.shift:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x
                else:
                    self.bmtool_modal_str\
                            = self.bmtool_modal_str + x.lower()
                return True
        for x in self._MODAL_DIGITS:
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
            self._mode = self._previous_mode
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

    def __str_get(self):
        return self.bmtool_modal_str

    def __digits_clear(self):
        self.bmtool_modal_numbers_str = ''

    def __str_clear(self):
        self.bmtool_modal_str = ''  # }}}
