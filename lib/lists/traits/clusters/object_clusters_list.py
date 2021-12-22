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

from ...modifiers_list import ModifiersList

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ....dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False

from ....controller.actions import (
                                    ClusterRequest,
                                    ClustersAction
                                    )


class ObjectClustersListTrait():
    """
    This is class that can be used to add methods
    for editing object's modifiers to ClustersList.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if not no_obj:
        #     if obj is None:
        #         raise ValueError

        # self._object = obj
