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

from .cluster_trait import ClusterTrait

from ..lists.modifiers_list import ModifiersList
from ..lists.traits.modifiers.active_modifier \
        import ActiveModifierTrait
from ..lists.traits.modifiers.object_modifiers_list \
        import ObjectModifiersListTrait

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False


class ModifiersCluster(
                       ClusterTrait,
                       ActiveModifierTrait,
                       ObjectModifiersListTrait,
                       ModifiersList
                       ):
    """
    Base class for modifiers cluster type
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _delete(self, action):
        if _WITH_BPY:
            mod_name = action.subject.name
            self._modifiers_list.remove(action.subject)
            bpy.ops.object.modifier_remove(modifier=mod_name)
        else:
            mod_name = action.subject.name
            self._modifiers_list.remove(action.subject)
            self._object.modifier_remove(modifier=mod_name)
