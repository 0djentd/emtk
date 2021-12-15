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

from .lists.extended_modifiers_list import ExtendedModifiersList
from .lists.object_modifiers_clusters_list import ObjectModifiersClustersList
from .lists.object_modifiers_list import ObjectModifiersList
from .clusters import ModifiersCluster, ClustersLayer, DefaultModifierCluster


class ModifiersOperator():
    """
    Base class for operators that use Blender modifiers stack
    Have methods for selecting objects in view layer,
    switching active object, selecting objects by properties.
    """

    # Reference to active object's ModifierList()
    # m_list

    # Selected objects is a list of ModifierList objects for all
    # selected objects, including active object
    selected_objects = None

    # Can be used with modifiers clusters
    _MODIFIERS_OPERATOR_MODIFIER_CLUSTERS = True

    # Dont use extended modifiers list, use object modifiers list
    _MODIFIERS_OPERATOR_DONT_USE_EXTENDED = False

    def create_objects_modifiers_lists(self, context, cluster_types=None):
        """
        Updates lists of modifiers for selected objects
        on active view layer.
        Should be used on operator initialisation and
        after changing selected objects/switching active object
        Returns False if no objects selected
        """

        for x in range(50):
            self.report({'INFO'}, " ")

        if cluster_types is None:
            clusters = []
        elif isinstance(cluster_types, list):
            for x in cluster_types:
                if isinstance(x, ModifiersCluster):
                    clusters.append(x)
                else:
                    raise TypeError
        else:
            TypeError

        self.report({'INFO'}, "================================")
        self.report({'INFO'}, "  MODIFIERS OPERATOR STARTED")
        self.report({'INFO'}, "================================")
        self.report({'INFO'}, " ")
        self.report({'INFO'}, " ")
        self.report({'INFO'}, "================================")
        self.report({'INFO'}, "Trying to create modifier lists")
        self.report({'INFO'}, "================================")

        if len(context.view_layer.objects.selected) != 0:
            self.selected_objects = []
            x = 0

            # TODO: this shouldnt be here.
            # Available cluster types
            clusters = []
            cluster = DefaultModifierCluster()
            clusters.append(cluster)

            cluster = ModifiersCluster(cluster_name='Beveled Boolean',
                                       cluster_type='BEVELED_BOOLEAN',
                                       modifiers_by_type=[
                                           ['BOOLEAN'], ['BEVEL']],
                                       modifiers_by_name=[['ANY'], ['ANY']],
                                       cluster_priority=0,
                                       cluster_createable=True,
                                       )
            clusters.append(cluster)

            cluster = ModifiersCluster(cluster_name='Triple Bevel',
                                       cluster_type='TRIPLE_BEVEL',
                                       modifiers_by_type=[
                                           ['BEVEL'], ['BEVEL'], ['BEVEL']],
                                       modifiers_by_name=[
                                           ['ANY'], ['ANY'], ['ANY']],
                                       cluster_priority=0,
                                       cluster_createable=True,
                                       )
            clusters.append(cluster)

            cluster = ClustersLayer(cluster_name='Double Triple Bevel Cluster',
                                    cluster_type='BEVEL_CLUSTER',
                                    modifiers_by_type=[
                                        ['TRIPLE_BEVEL'], ['TRIPLE_BEVEL']],
                                    modifiers_by_name=[['ANY'], ['ANY']],
                                    cluster_priority=0,
                                    cluster_createable=True,
                                    )
            clusters.append(cluster)

            for b_obj in context.view_layer.objects.selected:

                # Create extended modlist for active object
                if b_obj == context.view_layer.objects.active:

                    # Create extended modifiers list and initialize it for obj
                    obj_mod_list = ExtendedModifiersList(obj=b_obj)

                    # If using clusters
                    if self._MODIFIERS_OPERATOR_MODIFIER_CLUSTERS:

                        for y in clusters:
                            if not obj_mod_list.update_cluster_types_list(y):
                                self.report(
                                        {'INFO'},
                                        "Failed to add new modcluster type")

                    # Create modifiers list for object and parse it
                    result = obj_mod_list.create_modifiers_list()

                    # Add modifiers list references
                    self.selected_objects.append(obj_mod_list)
                    self.m_list = self.selected_objects[x]
                    if result is False or result is None:
                        return False
                # else:
                    # if self._MODIFIERS_OPERATOR_MODIFIER_CLUSTERS:

                    #     # Create clusters list
                    #     obj_mod_list = ObjectModifiersClustersList(obj)
                    #     obj_mod_list._MODIFIER_CLUSTERS = True
                    #     for y in clusters:
                    #         if not obj_mod_list.update_cluster_types_list(y):
                    #             self.report(
                    #                     {'INFO'},
                    #                     "Failed to add new modcluster type")
                    # else:
                    #     # Create usual modifiers list
                    #     obj_mod_list = ObjectModifiersList(obj)

                    # # Create modifiers list for object and parse it
                    # result = obj_mod_list.create_modifiers_list(obj)
                    # if result is False or result is None:
                    #     return False
                    # self.selected_objects.append(obj_mod_list)
                x += 1
            self.report({'INFO'}, "Finished creating modifier lists")
            return True
        else:
            # for finishing modal operators
            return False

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
