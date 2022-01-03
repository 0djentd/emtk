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

import json
from bpy.types import Operator
from bpy.props import StringProperty


class BMTOOL_OT_add_cluster_type_object(Operator):
    """
    Adds serialized_cluster_type to an object props.
    """
    bl_idname = "object.add_cluster_type"
    bl_label = "Add cluster type to an object"
    bl_description = "Add cluster type to an object"
    bl_options = {'REGISTER', 'UNDO'}

    serialized_cluster_type: StringProperty(
                                            name='Cluster Type',
                                            default=''
                                            )

    obj_prop_name: StringProperty(
                                  name='Cluster Types Prop Name',
                                  default='BMTool'
                                  )

    obj_prop_group: StringProperty(
                                  name='Cluster Types Prop Group',
                                  default='ClusterTypes'
                                  )

    def execute(self, context):
        # Dont do anything if operator properties are not correct.
        if self.serialized_cluster_type == '':
            return {'FINISHED'}
        if self.obj_prop_name == '':
            return {'FINISHED'}
        if self.obj_prop_group == '':
            return {'FINISHED'}

        cluster_type_to_add = json.loads(
                self.serialized_cluster_type)

        prop_name = f'{self.obj_prop_name}{self.obj_prop_group}'

        for obj in context.selected_objects:

            # Check if there is cluster types already.
            # Create cluster types prop.
            try:
                obj_cluster_types = obj[prop_name]
            except KeyError:
                e = json.dumps({})
                obj[prop_name] = e
                obj_cluster_types = obj[prop_name]

            clusters = json.loads(obj_cluster_types)

            # Check if replacing existing one.
            already_existing_type = False
            try:
                a = clusters[cluster_type_to_add['name']]
            except KeyError:
                already_existing_type = True
            if already_existing_type:
                self.report(
                        {'INFO'},
                        f'Cluster type {cluster_type_to_add["name"]} already exists, replacing.')

            self.report(
                    {'INFO'},
                    f'Adding cluster type {cluster_type_to_add["name"]} to {obj}.')

            clusters.update(
                    {cluster_type_to_add['name']: cluster_type_to_add})
            obj[prop_name] = json.dumps(clusters)
        return {'FINISHED'}
