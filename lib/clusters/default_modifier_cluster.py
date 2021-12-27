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

from .modifiers_cluster import ModifiersCluster

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False


class DefaultModifierCluster(
                             ModifiersCluster
                             ):
    """
    Cluster type for default modifiers without custom behaviour, tags, or name.
    Consist of one modifier. Returns actual Blender modifier name and type to
    clusters list.
    """

    def __init__(self):
        x = {
             'type': "DEFAULT_MODIFIER_CLUSTER",
             'name': "Default Modifier",
             'by_type': ['ANY'],
             'by_name': ['ANY'],
             'is_sane': True,
             'createable': True,
             'dynamic': True,
             }
        super().__init__(cluster_definition=x)

    def get_this_cluster_name(self):
        if not self._cluster_props['initialized']\
                or len(self._modifiers_list) == 0:
            return self.get_this_cluster_default_name()
        else:
            return self._modifiers_list[0].name

    def get_this_cluster_type(self):
        if not self._cluster_props['initialized']\
                or len(self._modifiers_list) == 0:
            return self._cluster_definition['type']
        else:
            return self._modifiers_list[0].type

    # Check if passed argument are actually Blender modifier
    def modcluster_extra_availability_check(self, mod):
        if len(mod) > 1:
            return False
        if _WITH_BPY:
            if not isinstance(mod[0], bpy.types.Modifier):
                return False
        elif not _WITH_BPY:
            if not isinstance(mod[0], DummyBlenderModifier):
                return False
        return 'FOUND'

    # ===========================
    # Initializing cluster
    # ===========================
    def set_this_cluster_modifiers(self, modifiers):
        """
        Replaces list of modifiers with modifiers.
        For this type of clusters, it checks that there is only one modifier.
        Returns True or False, if cluster is not editable
        """

        # If not a list
        if not isinstance(modifiers, list):
            modifiers = [modifiers]

        # If there is not exactly one modifier
        if len(modifiers) != 1:
            return ValueError(
                    'DefaultModifierCluster can work only with one modifier.')

        # If it is not an actual modifier
        if _WITH_BPY:
            if not isinstance(modifiers[0], bpy.types.Modifier):
                raise TypeError('Cluster needs actual Blender modifier.')
        elif not _WITH_BPY:
            if not isinstance(modifiers[0], DummyBlenderModifier):
                raise TypeError('Cluster needs actual Blender modifier.')

        # If havent set modifiers already
        if self._cluster_props['initialized'] is False:
            self._modifiers_list = modifiers
            self._cluster_props['initialized'] = True
            return True

        # If allowed to reset modifiers
        elif self._cluster_definition['dynamic']:
            self._modifiers_list = modifiers
            return True
        else:
            raise ValueError('Cant change modifiers, cluster is not dynamic')
