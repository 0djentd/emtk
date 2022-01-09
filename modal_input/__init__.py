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

"""
This module provides some utility for modal operators.

Features:
    Editing using mouse input.

    Editing using digits or letters input.

    Correct (?) interpretation of property subtype and units
    (using rna_type, or manually).

    Modal keyboard shortcuts.

    AddonPreferences mix-in class with shortcuts editor and cache.

    Automatic generation of new shortcuts without duplicates in
    name or definition.

TODO Planned features:
    Correct UI property value display.
"""
