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

import logging

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    _WITH_BPY = False

from .lists.extended_modifiers_list import ExtendedModifiersList

from .clusters.cluster_trait import ClusterTrait
from .clusters.modifiers_cluster import ModifiersCluster
from .clusters.clusters_layer import ClustersLayer

from .utils.clusters import (get_cluster_types_definitions_from_settings,
                             save_cluster_type_definition_to_settings,
                             instantiate_clusters_from_definitions)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ModifiersOperator():
    """
    Base class for operators that use Blender modifiers stack
    Have methods for selecting objects in view layer,
    switching active object, selecting objects by properties.
    """

    def create_objects_modifiers_lists(self, context,
                                       cluster_types=None,
                                       *args, **kwargs):
        """
        Updates lists of modifiers for selected objects
        on active view layer.
        Should be used on operator initialisation and
        after changing selected objects/switching active object
        Returns False if no objects selected
        """

        for x in range(50):
            logger.info(" ")

        if cluster_types is None:
            clusters = []
        elif isinstance(cluster_types, list):
            for x in cluster_types:
                if isinstance(x, ClusterTrait):
                    clusters.append(x)
                else:
                    raise TypeError
        else:
            TypeError

        logger.info("================================")
        logger.info("  MODIFIERS OPERATOR STARTED")
        logger.info("================================")
        logger.info(" ")
        logger.info(" ")
        logger.info("================================")
        logger.info("Trying to create modifier lists")
        logger.info("================================")

        if len(context.view_layer.objects.selected) == 0:
            return False

        # # Add some cluster types
        # default_clusters = self._default_cluster_types()
        # for x in default_clusters:
        #     y = x.get_this_cluster_definition()
        #     if y not in clusters:
        #         save_cluster_type_definition_to_settings(y, 'bmtools')

        if bpy.context.preferences.addons[
                'bmtools'].preferences.custom_cluster_types\
                and bpy.context.preferences.addons[
                        'bmtools'].preferences.always_add_custom_cluster_types\
                and _WITH_BPY:
            clusters = get_cluster_types_definitions_from_settings('bmtools')
            clusters = instantiate_clusters_from_definitions(clusters)
        else:
            clusters = []

        # Create extended modifiers lists and initialize
        # it for selected objects
        self.selected_objects = []
        for obj in context.view_layer.objects.selected:
            obj_mod_list = ExtendedModifiersList(
                    obj, cluster_types=clusters)
            if not obj_mod_list.create_modifiers_list(obj):
                return False

            # Add modifiers list references
            self.selected_objects.append(obj_mod_list)
            if obj == context.view_layer.objects.active:
                self.m_list = obj_mod_list
        return True

    def select_object(self, context, obj):
        """
        Add object to selected objects list
        without changing active object
        """

        active_obj = context.view_layer.objects.active
        obj.select_set(True)
        context.view_layer.objects.active = active_obj
        self.update_object_list(context)

    def select_objects_by_name(self, context, name):
        """
        Add objects to selected objects list by name
        without changing active object
        """

        active_obj = context.view_layer.objects.active
        for obj in context.view_layer.objects:
            if name in obj.name:
                obj.select_set(True)
                break
        context.view_layer.objects.active = active_obj
        self.update_object_list(context)

    def deselect_object(self, context, obj):
        """
        Remove object from selected objects list
        If removing active object select first object
        """

        objs = context.view_layer.objects
        active_obj = objs.active
        if active_obj is not obj:
            obj.select_set(False)
            objs.active = active_obj
        elif active_obj is obj:
            if len(context.view_layer.selected) > 1:
                obj.select_set(False)
                objs.active = objs.selected[0]
            else:
                obj.select_set(False)
        self.update_object_list(context)

    def switch_active_object(self, context, modifiers_list):
        """
        Switch active object to modifiers_list's object
        """

        context.view_layer.objects.active = modifiers_list._object
        self.m_list = modifiers_list
        self.update_object_list(context)

    def _default_cluster_types(self):
        """
        Some cluster types to add to addon settings or use without bpy.
        """
        clusters = []
        cluster = ModifiersCluster(
                                   cluster_name='Beveled Boolean',
                                   cluster_type='BEVELED_BOOLEAN',
                                   modifiers_by_type=[
                                       ['BOOLEAN'], ['BEVEL']],
                                   modifiers_by_name=[
                                       ['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ModifiersCluster(
                                   cluster_name='Triple Bevel',
                                   cluster_type='TRIPLE_BEVEL',
                                   modifiers_by_type=[['BEVEL'],
                                                      ['BEVEL'],
                                                      ['BEVEL']],
                                   modifiers_by_name=[
                                       ['ANY'], ['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ClustersLayer(
                                cluster_name='Double Bevel Cluster',
                                cluster_type='BEVEL_CLUSTER',
                                modifiers_by_type=[
                                    ['TRIPLE_BEVEL'],
                                    ['TRIPLE_BEVEL']],
                                modifiers_by_name=[['ANY'], ['ANY']],
                                cluster_priority=0,
                                cluster_createable=True,
                                )
        clusters.append(cluster)
        return clusters
