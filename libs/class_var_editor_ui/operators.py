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

import re
import string

import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Panel, Operator


class EMTK_OT_emtk_invoke_operator_func(Operator):
    """Workaround to change panel class variables from button."""

    bl_idname = "emtk.emtk_invoke_operator_func"
    bl_label = "Invoke one of emtk operator functions."

    # Line to eval
    func: StringProperty("")

    # Variable to write result to
    returned_variable: StringProperty("")

    def execute(self, context):
        line = str(self.func)
        line_2 = str(self.returned_variable)
        if not isinstance(line, str):
            raise TypeError
        if not isinstance(line_2, str):
            raise TypeError
        if type(line) is not str:
            raise TypeError
        if type(line_2) is not str:
            raise TypeError

        if not re.search('bpy.types.', line)\
                and not re.search('bpy.ops.', line):
            a = f'''Expected "bpy.types. ..." \
                    or "bpy.ops. ...", got "{line[0:10]}. ..."'''
            a = re.sub('\n\s*', '', a)
            raise ValueError(a)

        for x in line[:]:
            if x not in string.ascii_letters\
                    and x not in string.digits\
                    and x not in list('()[]"\',._ =;'):
                a = f'Expected x in [A-Z][a-z][0-9], [[]()"\',._ ], got "{x}"'
                raise ValueError(a)

        if len(line_2) > 4:
            if not re.match('bpy.types.', line_2)\
                    and not re.match('bpy.ops.', line_2):
                a = f'''Expected "bpy.types. ..." or "bpy.ops. ...", \
                        got "{line_2[0:10]} ..."'''
                a = re.sub('\n\s*', '', a)
                raise ValueError(a)

            for x in line_2[:]:
                if x not in string.ascii_letters\
                        and x not in string.digits\
                        and x not in list('[]"\'._'):
                    a = f'''Expected x 
        in [A-Z][a-z][0-9], [[]"\',._ ], got "{x}"'''
                    a = re.sub('\n\s*', '', a)
                    raise ValueError(a)

        print(line)
        print(line_2)
        result = exec(line)
        if len(line_2) > 4:
            line_2 = line_2 + ' = result'
            eval(line_2)
        print(f"'{line}'")
        print(f"'{result}'")
        print(f"'{line_2}'")
        return {'FINISHED'}
