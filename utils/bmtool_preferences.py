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

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):
    bl_idname = "bmtools"

    save_clusters: BoolProperty(
            name="Save clusters on operator finish",
            default=True
            )

    save_clusters_backup: BoolProperty(
            name="Save clusters backup on operator finish",
            default=True
            )

    backup_mesh_on_modifier_apply_remove: BoolProperty(
            name="Backup mesh on modifier apply or remove.",
            default=True
            )

    backup_collection_name: StringProperty(
            name="Name of collection that will be used for mesh backup.",
            default='BMToolM mesh backup'
            )

    custom_cluster_types: BoolProperty(
            name="Use custom cluster types.",
            default=True
            )

    always_add_custom_cluster_types: BoolProperty(
            name="Always add custom cluster types.",
            default=True
            )

    cluster_types: StringProperty(
            name="ClusterTypes",
            default="[]"
            )

    # {{{
    bmtool_kbs_name: StringProperty(
            name="bmtool_kbs_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_name_shift: BoolProperty(
            name="bmtool_kbs_name_shift",
            default=False
            )

    bmtool_kbs_name_ctl: BoolProperty(
            name="bmtool_kbs_name_ctl",
            default=False
            )

    bmtool_kbs_name_alt: BoolProperty(
            name="bmtool_kbs_name_alt",
            default=False
            )

    bmtool_kbs_vertex_group: StringProperty(
            name="bmtool_kbs_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_vertex_group_shift",
            default=False
            )

    bmtool_kbs_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_vertex_group_alt",
            default=False
            )

    bmtool_kbs_filepath: StringProperty(
            name="bmtool_kbs_filepath",
            maxlen=1,
            default=''
            )

    bmtool_kbs_filepath_shift: BoolProperty(
            name="bmtool_kbs_filepath_shift",
            default=False
            )

    bmtool_kbs_filepath_ctl: BoolProperty(
            name="bmtool_kbs_filepath_ctl",
            default=False
            )

    bmtool_kbs_filepath_alt: BoolProperty(
            name="bmtool_kbs_filepath_alt",
            default=False
            )

    bmtool_kbs_object_path: StringProperty(
            name="bmtool_kbs_object_path",
            maxlen=1,
            default=''
            )

    bmtool_kbs_object_path_shift: BoolProperty(
            name="bmtool_kbs_object_path_shift",
            default=False
            )

    bmtool_kbs_object_path_ctl: BoolProperty(
            name="bmtool_kbs_object_path_ctl",
            default=False
            )

    bmtool_kbs_object_path_alt: BoolProperty(
            name="bmtool_kbs_object_path_alt",
            default=False
            )

    bmtool_kbs_uv_layer: StringProperty(
            name="bmtool_kbs_uv_layer",
            maxlen=1,
            default=''
            )

    bmtool_kbs_uv_layer_shift: BoolProperty(
            name="bmtool_kbs_uv_layer_shift",
            default=False
            )

    bmtool_kbs_uv_layer_ctl: BoolProperty(
            name="bmtool_kbs_uv_layer_ctl",
            default=False
            )

    bmtool_kbs_uv_layer_alt: BoolProperty(
            name="bmtool_kbs_uv_layer_alt",
            default=False
            )

    bmtool_kbs_bone_to: StringProperty(
            name="bmtool_kbs_bone_to",
            maxlen=1,
            default=''
            )

    bmtool_kbs_bone_to_shift: BoolProperty(
            name="bmtool_kbs_bone_to_shift",
            default=False
            )

    bmtool_kbs_bone_to_ctl: BoolProperty(
            name="bmtool_kbs_bone_to_ctl",
            default=False
            )

    bmtool_kbs_bone_to_alt: BoolProperty(
            name="bmtool_kbs_bone_to_alt",
            default=False
            )

    bmtool_kbs_bone_from: StringProperty(
            name="bmtool_kbs_bone_from",
            maxlen=1,
            default=''
            )

    bmtool_kbs_bone_from_shift: BoolProperty(
            name="bmtool_kbs_bone_from_shift",
            default=False
            )

    bmtool_kbs_bone_from_ctl: BoolProperty(
            name="bmtool_kbs_bone_from_ctl",
            default=False
            )

    bmtool_kbs_bone_from_alt: BoolProperty(
            name="bmtool_kbs_bone_from_alt",
            default=False
            )

    bmtool_kbs_mask_vertex_group: StringProperty(
            name="bmtool_kbs_mask_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_mask_vertex_group_shift",
            default=False
            )

    bmtool_kbs_mask_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_mask_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_mask_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_mask_vertex_group_alt",
            default=False
            )

    bmtool_kbs_mask_tex_map_bone: StringProperty(
            name="bmtool_kbs_mask_tex_map_bone",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_tex_map_bone_shift: BoolProperty(
            name="bmtool_kbs_mask_tex_map_bone_shift",
            default=False
            )

    bmtool_kbs_mask_tex_map_bone_ctl: BoolProperty(
            name="bmtool_kbs_mask_tex_map_bone_ctl",
            default=False
            )

    bmtool_kbs_mask_tex_map_bone_alt: BoolProperty(
            name="bmtool_kbs_mask_tex_map_bone_alt",
            default=False
            )

    bmtool_kbs_mask_tex_uv_layer: StringProperty(
            name="bmtool_kbs_mask_tex_uv_layer",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_tex_uv_layer_shift: BoolProperty(
            name="bmtool_kbs_mask_tex_uv_layer_shift",
            default=False
            )

    bmtool_kbs_mask_tex_uv_layer_ctl: BoolProperty(
            name="bmtool_kbs_mask_tex_uv_layer_ctl",
            default=False
            )

    bmtool_kbs_mask_tex_uv_layer_alt: BoolProperty(
            name="bmtool_kbs_mask_tex_uv_layer_alt",
            default=False
            )

    bmtool_kbs_vertex_group_a: StringProperty(
            name="bmtool_kbs_vertex_group_a",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vertex_group_a_shift: BoolProperty(
            name="bmtool_kbs_vertex_group_a_shift",
            default=False
            )

    bmtool_kbs_vertex_group_a_ctl: BoolProperty(
            name="bmtool_kbs_vertex_group_a_ctl",
            default=False
            )

    bmtool_kbs_vertex_group_a_alt: BoolProperty(
            name="bmtool_kbs_vertex_group_a_alt",
            default=False
            )

    bmtool_kbs_vertex_group_b: StringProperty(
            name="bmtool_kbs_vertex_group_b",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vertex_group_b_shift: BoolProperty(
            name="bmtool_kbs_vertex_group_b_shift",
            default=False
            )

    bmtool_kbs_vertex_group_b_ctl: BoolProperty(
            name="bmtool_kbs_vertex_group_b_ctl",
            default=False
            )

    bmtool_kbs_vertex_group_b_alt: BoolProperty(
            name="bmtool_kbs_vertex_group_b_alt",
            default=False
            )

    bmtool_kbs_rim_vertex_group: StringProperty(
            name="bmtool_kbs_rim_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_rim_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_rim_vertex_group_shift",
            default=False
            )

    bmtool_kbs_rim_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_rim_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_rim_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_rim_vertex_group_alt",
            default=False
            )

    bmtool_kbs_shell_vertex_group: StringProperty(
            name="bmtool_kbs_shell_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_shell_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_shell_vertex_group_shift",
            default=False
            )

    bmtool_kbs_shell_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_shell_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_shell_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_shell_vertex_group_alt",
            default=False
            )

    bmtool_kbs_grid_name: StringProperty(
            name="bmtool_kbs_grid_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_grid_name_shift: BoolProperty(
            name="bmtool_kbs_grid_name_shift",
            default=False
            )

    bmtool_kbs_grid_name_ctl: BoolProperty(
            name="bmtool_kbs_grid_name_ctl",
            default=False
            )

    bmtool_kbs_grid_name_alt: BoolProperty(
            name="bmtool_kbs_grid_name_alt",
            default=False
            )

    bmtool_kbs_texture_coords_bone: StringProperty(
            name="bmtool_kbs_texture_coords_bone",
            maxlen=1,
            default=''
            )

    bmtool_kbs_texture_coords_bone_shift: BoolProperty(
            name="bmtool_kbs_texture_coords_bone_shift",
            default=False
            )

    bmtool_kbs_texture_coords_bone_ctl: BoolProperty(
            name="bmtool_kbs_texture_coords_bone_ctl",
            default=False
            )

    bmtool_kbs_texture_coords_bone_alt: BoolProperty(
            name="bmtool_kbs_texture_coords_bone_alt",
            default=False
            )

    bmtool_kbs_subtarget: StringProperty(
            name="bmtool_kbs_subtarget",
            maxlen=1,
            default=''
            )

    bmtool_kbs_subtarget_shift: BoolProperty(
            name="bmtool_kbs_subtarget_shift",
            default=False
            )

    bmtool_kbs_subtarget_ctl: BoolProperty(
            name="bmtool_kbs_subtarget_ctl",
            default=False
            )

    bmtool_kbs_subtarget_alt: BoolProperty(
            name="bmtool_kbs_subtarget_alt",
            default=False
            )

    bmtool_kbs_particle_uv: StringProperty(
            name="bmtool_kbs_particle_uv",
            maxlen=1,
            default=''
            )

    bmtool_kbs_particle_uv_shift: BoolProperty(
            name="bmtool_kbs_particle_uv_shift",
            default=False
            )

    bmtool_kbs_particle_uv_ctl: BoolProperty(
            name="bmtool_kbs_particle_uv_ctl",
            default=False
            )

    bmtool_kbs_particle_uv_alt: BoolProperty(
            name="bmtool_kbs_particle_uv_alt",
            default=False
            )

    bmtool_kbs_foam_layer_name: StringProperty(
            name="bmtool_kbs_foam_layer_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_foam_layer_name_shift: BoolProperty(
            name="bmtool_kbs_foam_layer_name_shift",
            default=False
            )

    bmtool_kbs_foam_layer_name_ctl: BoolProperty(
            name="bmtool_kbs_foam_layer_name_ctl",
            default=False
            )

    bmtool_kbs_foam_layer_name_alt: BoolProperty(
            name="bmtool_kbs_foam_layer_name_alt",
            default=False
            )

    bmtool_kbs_spray_layer_name: StringProperty(
            name="bmtool_kbs_spray_layer_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_spray_layer_name_shift: BoolProperty(
            name="bmtool_kbs_spray_layer_name_shift",
            default=False
            )

    bmtool_kbs_spray_layer_name_ctl: BoolProperty(
            name="bmtool_kbs_spray_layer_name_ctl",
            default=False
            )

    bmtool_kbs_spray_layer_name_alt: BoolProperty(
            name="bmtool_kbs_spray_layer_name_alt",
            default=False
            )

    bmtool_kbs_value_layer_name: StringProperty(
            name="bmtool_kbs_value_layer_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_value_layer_name_shift: BoolProperty(
            name="bmtool_kbs_value_layer_name_shift",
            default=False
            )

    bmtool_kbs_value_layer_name_ctl: BoolProperty(
            name="bmtool_kbs_value_layer_name_ctl",
            default=False
            )

    bmtool_kbs_value_layer_name_alt: BoolProperty(
            name="bmtool_kbs_value_layer_name_alt",
            default=False
            )

    bmtool_kbs_index_layer_name: StringProperty(
            name="bmtool_kbs_index_layer_name",
            maxlen=1,
            default=''
            )

    bmtool_kbs_index_layer_name_shift: BoolProperty(
            name="bmtool_kbs_index_layer_name_shift",
            default=False
            )

    bmtool_kbs_index_layer_name_ctl: BoolProperty(
            name="bmtool_kbs_index_layer_name_ctl",
            default=False
            )

    bmtool_kbs_index_layer_name_alt: BoolProperty(
            name="bmtool_kbs_index_layer_name_alt",
            default=False
            )

    bmtool_kbs_use_apply_on_spline: StringProperty(
            name="bmtool_kbs_use_apply_on_spline",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_apply_on_spline_shift: BoolProperty(
            name="bmtool_kbs_use_apply_on_spline_shift",
            default=False
            )

    bmtool_kbs_use_apply_on_spline_ctl: BoolProperty(
            name="bmtool_kbs_use_apply_on_spline_ctl",
            default=False
            )

    bmtool_kbs_use_apply_on_spline_alt: BoolProperty(
            name="bmtool_kbs_use_apply_on_spline_alt",
            default=False
            )

    bmtool_kbs_use_poly_data: StringProperty(
            name="bmtool_kbs_use_poly_data",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_poly_data_shift: BoolProperty(
            name="bmtool_kbs_use_poly_data_shift",
            default=False
            )

    bmtool_kbs_use_poly_data_ctl: BoolProperty(
            name="bmtool_kbs_use_poly_data_ctl",
            default=False
            )

    bmtool_kbs_use_poly_data_alt: BoolProperty(
            name="bmtool_kbs_use_poly_data_alt",
            default=False
            )

    bmtool_kbs_show_render: StringProperty(
            name="bmtool_kbs_show_render",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_render_shift: BoolProperty(
            name="bmtool_kbs_show_render_shift",
            default=False
            )

    bmtool_kbs_show_render_ctl: BoolProperty(
            name="bmtool_kbs_show_render_ctl",
            default=False
            )

    bmtool_kbs_show_render_alt: BoolProperty(
            name="bmtool_kbs_show_render_alt",
            default=False
            )

    bmtool_kbs_show_in_editmode: StringProperty(
            name="bmtool_kbs_show_in_editmode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_in_editmode_shift: BoolProperty(
            name="bmtool_kbs_show_in_editmode_shift",
            default=False
            )

    bmtool_kbs_show_in_editmode_ctl: BoolProperty(
            name="bmtool_kbs_show_in_editmode_ctl",
            default=False
            )

    bmtool_kbs_show_in_editmode_alt: BoolProperty(
            name="bmtool_kbs_show_in_editmode_alt",
            default=False
            )

    bmtool_kbs_use_edge_data: StringProperty(
            name="bmtool_kbs_use_edge_data",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_edge_data_shift: BoolProperty(
            name="bmtool_kbs_use_edge_data_shift",
            default=False
            )

    bmtool_kbs_use_edge_data_ctl: BoolProperty(
            name="bmtool_kbs_use_edge_data_ctl",
            default=False
            )

    bmtool_kbs_use_edge_data_alt: BoolProperty(
            name="bmtool_kbs_use_edge_data_alt",
            default=False
            )

    bmtool_kbs_use_loop_data: StringProperty(
            name="bmtool_kbs_use_loop_data",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_loop_data_shift: BoolProperty(
            name="bmtool_kbs_use_loop_data_shift",
            default=False
            )

    bmtool_kbs_use_loop_data_ctl: BoolProperty(
            name="bmtool_kbs_use_loop_data_ctl",
            default=False
            )

    bmtool_kbs_use_loop_data_alt: BoolProperty(
            name="bmtool_kbs_use_loop_data_alt",
            default=False
            )

    bmtool_kbs_use_vert_data: StringProperty(
            name="bmtool_kbs_use_vert_data",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_vert_data_shift: BoolProperty(
            name="bmtool_kbs_use_vert_data_shift",
            default=False
            )

    bmtool_kbs_use_vert_data_ctl: BoolProperty(
            name="bmtool_kbs_use_vert_data_ctl",
            default=False
            )

    bmtool_kbs_use_vert_data_alt: BoolProperty(
            name="bmtool_kbs_use_vert_data_alt",
            default=False
            )

    bmtool_kbs_use_object_transform: StringProperty(
            name="bmtool_kbs_use_object_transform",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_object_transform_shift: BoolProperty(
            name="bmtool_kbs_use_object_transform_shift",
            default=False
            )

    bmtool_kbs_use_object_transform_ctl: BoolProperty(
            name="bmtool_kbs_use_object_transform_ctl",
            default=False
            )

    bmtool_kbs_use_object_transform_alt: BoolProperty(
            name="bmtool_kbs_use_object_transform_alt",
            default=False
            )

    bmtool_kbs_use_max_distance: StringProperty(
            name="bmtool_kbs_use_max_distance",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_max_distance_shift: BoolProperty(
            name="bmtool_kbs_use_max_distance_shift",
            default=False
            )

    bmtool_kbs_use_max_distance_ctl: BoolProperty(
            name="bmtool_kbs_use_max_distance_ctl",
            default=False
            )

    bmtool_kbs_use_max_distance_alt: BoolProperty(
            name="bmtool_kbs_use_max_distance_alt",
            default=False
            )

    bmtool_kbs_show_expanded: StringProperty(
            name="bmtool_kbs_show_expanded",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_expanded_shift: BoolProperty(
            name="bmtool_kbs_show_expanded_shift",
            default=False
            )

    bmtool_kbs_show_expanded_ctl: BoolProperty(
            name="bmtool_kbs_show_expanded_ctl",
            default=False
            )

    bmtool_kbs_show_expanded_alt: BoolProperty(
            name="bmtool_kbs_show_expanded_alt",
            default=False
            )

    bmtool_kbs_show_viewport: StringProperty(
            name="bmtool_kbs_show_viewport",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_viewport_shift: BoolProperty(
            name="bmtool_kbs_show_viewport_shift",
            default=False
            )

    bmtool_kbs_show_viewport_ctl: BoolProperty(
            name="bmtool_kbs_show_viewport_ctl",
            default=False
            )

    bmtool_kbs_show_viewport_alt: BoolProperty(
            name="bmtool_kbs_show_viewport_alt",
            default=False
            )

    bmtool_kbs_is_active: StringProperty(
            name="bmtool_kbs_is_active",
            maxlen=1,
            default=''
            )

    bmtool_kbs_is_active_shift: BoolProperty(
            name="bmtool_kbs_is_active_shift",
            default=False
            )

    bmtool_kbs_is_active_ctl: BoolProperty(
            name="bmtool_kbs_is_active_ctl",
            default=False
            )

    bmtool_kbs_is_active_alt: BoolProperty(
            name="bmtool_kbs_is_active_alt",
            default=False
            )

    bmtool_kbs_show_on_cage: StringProperty(
            name="bmtool_kbs_show_on_cage",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_on_cage_shift: BoolProperty(
            name="bmtool_kbs_show_on_cage_shift",
            default=False
            )

    bmtool_kbs_show_on_cage_ctl: BoolProperty(
            name="bmtool_kbs_show_on_cage_ctl",
            default=False
            )

    bmtool_kbs_show_on_cage_alt: BoolProperty(
            name="bmtool_kbs_show_on_cage_alt",
            default=False
            )

    bmtool_kbs_invert_vertex_group: StringProperty(
            name="bmtool_kbs_invert_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_shift",
            default=False
            )

    bmtool_kbs_invert_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_invert_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_alt",
            default=False
            )

    bmtool_kbs_use_vertex_interpolation: StringProperty(
            name="bmtool_kbs_use_vertex_interpolation",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_vertex_interpolation_shift: BoolProperty(
            name="bmtool_kbs_use_vertex_interpolation_shift",
            default=False
            )

    bmtool_kbs_use_vertex_interpolation_ctl: BoolProperty(
            name="bmtool_kbs_use_vertex_interpolation_ctl",
            default=False
            )

    bmtool_kbs_use_vertex_interpolation_alt: BoolProperty(
            name="bmtool_kbs_use_vertex_interpolation_alt",
            default=False
            )

    bmtool_kbs_use_direction_parallel: StringProperty(
            name="bmtool_kbs_use_direction_parallel",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_direction_parallel_shift: BoolProperty(
            name="bmtool_kbs_use_direction_parallel_shift",
            default=False
            )

    bmtool_kbs_use_direction_parallel_ctl: BoolProperty(
            name="bmtool_kbs_use_direction_parallel_ctl",
            default=False
            )

    bmtool_kbs_use_direction_parallel_alt: BoolProperty(
            name="bmtool_kbs_use_direction_parallel_alt",
            default=False
            )

    bmtool_kbs_no_polynors_fix: StringProperty(
            name="bmtool_kbs_no_polynors_fix",
            maxlen=1,
            default=''
            )

    bmtool_kbs_no_polynors_fix_shift: BoolProperty(
            name="bmtool_kbs_no_polynors_fix_shift",
            default=False
            )

    bmtool_kbs_no_polynors_fix_ctl: BoolProperty(
            name="bmtool_kbs_no_polynors_fix_ctl",
            default=False
            )

    bmtool_kbs_no_polynors_fix_alt: BoolProperty(
            name="bmtool_kbs_no_polynors_fix_alt",
            default=False
            )

    bmtool_kbs_keep_sharp: StringProperty(
            name="bmtool_kbs_keep_sharp",
            maxlen=1,
            default=''
            )

    bmtool_kbs_keep_sharp_shift: BoolProperty(
            name="bmtool_kbs_keep_sharp_shift",
            default=False
            )

    bmtool_kbs_keep_sharp_ctl: BoolProperty(
            name="bmtool_kbs_keep_sharp_ctl",
            default=False
            )

    bmtool_kbs_keep_sharp_alt: BoolProperty(
            name="bmtool_kbs_keep_sharp_alt",
            default=False
            )

    bmtool_kbs_use_face_influence: StringProperty(
            name="bmtool_kbs_use_face_influence",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_face_influence_shift: BoolProperty(
            name="bmtool_kbs_use_face_influence_shift",
            default=False
            )

    bmtool_kbs_use_face_influence_ctl: BoolProperty(
            name="bmtool_kbs_use_face_influence_ctl",
            default=False
            )

    bmtool_kbs_use_face_influence_alt: BoolProperty(
            name="bmtool_kbs_use_face_influence_alt",
            default=False
            )

    bmtool_kbs_use_add: StringProperty(
            name="bmtool_kbs_use_add",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_add_shift: BoolProperty(
            name="bmtool_kbs_use_add_shift",
            default=False
            )

    bmtool_kbs_use_add_ctl: BoolProperty(
            name="bmtool_kbs_use_add_ctl",
            default=False
            )

    bmtool_kbs_use_add_alt: BoolProperty(
            name="bmtool_kbs_use_add_alt",
            default=False
            )

    bmtool_kbs_invert_falloff: StringProperty(
            name="bmtool_kbs_invert_falloff",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_falloff_shift: BoolProperty(
            name="bmtool_kbs_invert_falloff_shift",
            default=False
            )

    bmtool_kbs_invert_falloff_ctl: BoolProperty(
            name="bmtool_kbs_invert_falloff_ctl",
            default=False
            )

    bmtool_kbs_invert_falloff_alt: BoolProperty(
            name="bmtool_kbs_invert_falloff_alt",
            default=False
            )

    bmtool_kbs_normalize: StringProperty(
            name="bmtool_kbs_normalize",
            maxlen=1,
            default=''
            )

    bmtool_kbs_normalize_shift: BoolProperty(
            name="bmtool_kbs_normalize_shift",
            default=False
            )

    bmtool_kbs_normalize_ctl: BoolProperty(
            name="bmtool_kbs_normalize_ctl",
            default=False
            )

    bmtool_kbs_normalize_alt: BoolProperty(
            name="bmtool_kbs_normalize_alt",
            default=False
            )

    bmtool_kbs_use_remove: StringProperty(
            name="bmtool_kbs_use_remove",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_remove_shift: BoolProperty(
            name="bmtool_kbs_use_remove_shift",
            default=False
            )

    bmtool_kbs_use_remove_ctl: BoolProperty(
            name="bmtool_kbs_use_remove_ctl",
            default=False
            )

    bmtool_kbs_use_remove_alt: BoolProperty(
            name="bmtool_kbs_use_remove_alt",
            default=False
            )

    bmtool_kbs_invert_mask_vertex_group: StringProperty(
            name="bmtool_kbs_invert_mask_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_mask_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_invert_mask_vertex_group_shift",
            default=False
            )

    bmtool_kbs_invert_mask_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_invert_mask_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_invert_mask_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_invert_mask_vertex_group_alt",
            default=False
            )

    bmtool_kbs_invert_vertex_group_a: StringProperty(
            name="bmtool_kbs_invert_vertex_group_a",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_vertex_group_a_shift: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_a_shift",
            default=False
            )

    bmtool_kbs_invert_vertex_group_a_ctl: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_a_ctl",
            default=False
            )

    bmtool_kbs_invert_vertex_group_a_alt: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_a_alt",
            default=False
            )

    bmtool_kbs_invert_vertex_group_b: StringProperty(
            name="bmtool_kbs_invert_vertex_group_b",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_vertex_group_b_shift: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_b_shift",
            default=False
            )

    bmtool_kbs_invert_vertex_group_b_ctl: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_b_ctl",
            default=False
            )

    bmtool_kbs_invert_vertex_group_b_alt: BoolProperty(
            name="bmtool_kbs_invert_vertex_group_b_alt",
            default=False
            )

    bmtool_kbs_use_object_offset: StringProperty(
            name="bmtool_kbs_use_object_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_object_offset_shift: BoolProperty(
            name="bmtool_kbs_use_object_offset_shift",
            default=False
            )

    bmtool_kbs_use_object_offset_ctl: BoolProperty(
            name="bmtool_kbs_use_object_offset_ctl",
            default=False
            )

    bmtool_kbs_use_object_offset_alt: BoolProperty(
            name="bmtool_kbs_use_object_offset_alt",
            default=False
            )

    bmtool_kbs_use_merge_vertices: StringProperty(
            name="bmtool_kbs_use_merge_vertices",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_merge_vertices_shift: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_shift",
            default=False
            )

    bmtool_kbs_use_merge_vertices_ctl: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_ctl",
            default=False
            )

    bmtool_kbs_use_merge_vertices_alt: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_alt",
            default=False
            )

    bmtool_kbs_use_constant_offset: StringProperty(
            name="bmtool_kbs_use_constant_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_constant_offset_shift: BoolProperty(
            name="bmtool_kbs_use_constant_offset_shift",
            default=False
            )

    bmtool_kbs_use_constant_offset_ctl: BoolProperty(
            name="bmtool_kbs_use_constant_offset_ctl",
            default=False
            )

    bmtool_kbs_use_constant_offset_alt: BoolProperty(
            name="bmtool_kbs_use_constant_offset_alt",
            default=False
            )

    bmtool_kbs_use_merge_vertices_cap: StringProperty(
            name="bmtool_kbs_use_merge_vertices_cap",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_merge_vertices_cap_shift: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_cap_shift",
            default=False
            )

    bmtool_kbs_use_merge_vertices_cap_ctl: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_cap_ctl",
            default=False
            )

    bmtool_kbs_use_merge_vertices_cap_alt: BoolProperty(
            name="bmtool_kbs_use_merge_vertices_cap_alt",
            default=False
            )

    bmtool_kbs_use_relative_offset: StringProperty(
            name="bmtool_kbs_use_relative_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_relative_offset_shift: BoolProperty(
            name="bmtool_kbs_use_relative_offset_shift",
            default=False
            )

    bmtool_kbs_use_relative_offset_ctl: BoolProperty(
            name="bmtool_kbs_use_relative_offset_ctl",
            default=False
            )

    bmtool_kbs_use_relative_offset_alt: BoolProperty(
            name="bmtool_kbs_use_relative_offset_alt",
            default=False
            )

    bmtool_kbs_use_clamp_overlap: StringProperty(
            name="bmtool_kbs_use_clamp_overlap",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_clamp_overlap_shift: BoolProperty(
            name="bmtool_kbs_use_clamp_overlap_shift",
            default=False
            )

    bmtool_kbs_use_clamp_overlap_ctl: BoolProperty(
            name="bmtool_kbs_use_clamp_overlap_ctl",
            default=False
            )

    bmtool_kbs_use_clamp_overlap_alt: BoolProperty(
            name="bmtool_kbs_use_clamp_overlap_alt",
            default=False
            )

    bmtool_kbs_loop_slide: StringProperty(
            name="bmtool_kbs_loop_slide",
            maxlen=1,
            default=''
            )

    bmtool_kbs_loop_slide_shift: BoolProperty(
            name="bmtool_kbs_loop_slide_shift",
            default=False
            )

    bmtool_kbs_loop_slide_ctl: BoolProperty(
            name="bmtool_kbs_loop_slide_ctl",
            default=False
            )

    bmtool_kbs_loop_slide_alt: BoolProperty(
            name="bmtool_kbs_loop_slide_alt",
            default=False
            )

    bmtool_kbs_mark_sharp: StringProperty(
            name="bmtool_kbs_mark_sharp",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mark_sharp_shift: BoolProperty(
            name="bmtool_kbs_mark_sharp_shift",
            default=False
            )

    bmtool_kbs_mark_sharp_ctl: BoolProperty(
            name="bmtool_kbs_mark_sharp_ctl",
            default=False
            )

    bmtool_kbs_mark_sharp_alt: BoolProperty(
            name="bmtool_kbs_mark_sharp_alt",
            default=False
            )

    bmtool_kbs_mark_seam: StringProperty(
            name="bmtool_kbs_mark_seam",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mark_seam_shift: BoolProperty(
            name="bmtool_kbs_mark_seam_shift",
            default=False
            )

    bmtool_kbs_mark_seam_ctl: BoolProperty(
            name="bmtool_kbs_mark_seam_ctl",
            default=False
            )

    bmtool_kbs_mark_seam_alt: BoolProperty(
            name="bmtool_kbs_mark_seam_alt",
            default=False
            )

    bmtool_kbs_harden_normals: StringProperty(
            name="bmtool_kbs_harden_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_harden_normals_shift: BoolProperty(
            name="bmtool_kbs_harden_normals_shift",
            default=False
            )

    bmtool_kbs_harden_normals_ctl: BoolProperty(
            name="bmtool_kbs_harden_normals_ctl",
            default=False
            )

    bmtool_kbs_harden_normals_alt: BoolProperty(
            name="bmtool_kbs_harden_normals_alt",
            default=False
            )

    bmtool_kbs_use_hole_tolerant: StringProperty(
            name="bmtool_kbs_use_hole_tolerant",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_hole_tolerant_shift: BoolProperty(
            name="bmtool_kbs_use_hole_tolerant_shift",
            default=False
            )

    bmtool_kbs_use_hole_tolerant_ctl: BoolProperty(
            name="bmtool_kbs_use_hole_tolerant_ctl",
            default=False
            )

    bmtool_kbs_use_hole_tolerant_alt: BoolProperty(
            name="bmtool_kbs_use_hole_tolerant_alt",
            default=False
            )

    bmtool_kbs_use_self: StringProperty(
            name="bmtool_kbs_use_self",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_self_shift: BoolProperty(
            name="bmtool_kbs_use_self_shift",
            default=False
            )

    bmtool_kbs_use_self_ctl: BoolProperty(
            name="bmtool_kbs_use_self_ctl",
            default=False
            )

    bmtool_kbs_use_self_alt: BoolProperty(
            name="bmtool_kbs_use_self_alt",
            default=False
            )

    bmtool_kbs_use_random_order: StringProperty(
            name="bmtool_kbs_use_random_order",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_random_order_shift: BoolProperty(
            name="bmtool_kbs_use_random_order_shift",
            default=False
            )

    bmtool_kbs_use_random_order_ctl: BoolProperty(
            name="bmtool_kbs_use_random_order_ctl",
            default=False
            )

    bmtool_kbs_use_random_order_alt: BoolProperty(
            name="bmtool_kbs_use_random_order_alt",
            default=False
            )

    bmtool_kbs_use_reverse: StringProperty(
            name="bmtool_kbs_use_reverse",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_reverse_shift: BoolProperty(
            name="bmtool_kbs_use_reverse_shift",
            default=False
            )

    bmtool_kbs_use_reverse_ctl: BoolProperty(
            name="bmtool_kbs_use_reverse_ctl",
            default=False
            )

    bmtool_kbs_use_reverse_alt: BoolProperty(
            name="bmtool_kbs_use_reverse_alt",
            default=False
            )

    bmtool_kbs_use_collapse_triangulate: StringProperty(
            name="bmtool_kbs_use_collapse_triangulate",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_collapse_triangulate_shift: BoolProperty(
            name="bmtool_kbs_use_collapse_triangulate_shift",
            default=False
            )

    bmtool_kbs_use_collapse_triangulate_ctl: BoolProperty(
            name="bmtool_kbs_use_collapse_triangulate_ctl",
            default=False
            )

    bmtool_kbs_use_collapse_triangulate_alt: BoolProperty(
            name="bmtool_kbs_use_collapse_triangulate_alt",
            default=False
            )

    bmtool_kbs_use_dissolve_boundaries: StringProperty(
            name="bmtool_kbs_use_dissolve_boundaries",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_dissolve_boundaries_shift: BoolProperty(
            name="bmtool_kbs_use_dissolve_boundaries_shift",
            default=False
            )

    bmtool_kbs_use_dissolve_boundaries_ctl: BoolProperty(
            name="bmtool_kbs_use_dissolve_boundaries_ctl",
            default=False
            )

    bmtool_kbs_use_dissolve_boundaries_alt: BoolProperty(
            name="bmtool_kbs_use_dissolve_boundaries_alt",
            default=False
            )

    bmtool_kbs_use_symmetry: StringProperty(
            name="bmtool_kbs_use_symmetry",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_symmetry_shift: BoolProperty(
            name="bmtool_kbs_use_symmetry_shift",
            default=False
            )

    bmtool_kbs_use_symmetry_ctl: BoolProperty(
            name="bmtool_kbs_use_symmetry_ctl",
            default=False
            )

    bmtool_kbs_use_symmetry_alt: BoolProperty(
            name="bmtool_kbs_use_symmetry_alt",
            default=False
            )

    bmtool_kbs_use_edge_sharp: StringProperty(
            name="bmtool_kbs_use_edge_sharp",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_edge_sharp_shift: BoolProperty(
            name="bmtool_kbs_use_edge_sharp_shift",
            default=False
            )

    bmtool_kbs_use_edge_sharp_ctl: BoolProperty(
            name="bmtool_kbs_use_edge_sharp_ctl",
            default=False
            )

    bmtool_kbs_use_edge_sharp_alt: BoolProperty(
            name="bmtool_kbs_use_edge_sharp_alt",
            default=False
            )

    bmtool_kbs_use_edge_angle: StringProperty(
            name="bmtool_kbs_use_edge_angle",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_edge_angle_shift: BoolProperty(
            name="bmtool_kbs_use_edge_angle_shift",
            default=False
            )

    bmtool_kbs_use_edge_angle_ctl: BoolProperty(
            name="bmtool_kbs_use_edge_angle_ctl",
            default=False
            )

    bmtool_kbs_use_edge_angle_alt: BoolProperty(
            name="bmtool_kbs_use_edge_angle_alt",
            default=False
            )

    bmtool_kbs_use_smooth: StringProperty(
            name="bmtool_kbs_use_smooth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_smooth_shift: BoolProperty(
            name="bmtool_kbs_use_smooth_shift",
            default=False
            )

    bmtool_kbs_use_smooth_ctl: BoolProperty(
            name="bmtool_kbs_use_smooth_ctl",
            default=False
            )

    bmtool_kbs_use_smooth_alt: BoolProperty(
            name="bmtool_kbs_use_smooth_alt",
            default=False
            )

    bmtool_kbs_use_mirror_merge: StringProperty(
            name="bmtool_kbs_use_mirror_merge",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_mirror_merge_shift: BoolProperty(
            name="bmtool_kbs_use_mirror_merge_shift",
            default=False
            )

    bmtool_kbs_use_mirror_merge_ctl: BoolProperty(
            name="bmtool_kbs_use_mirror_merge_ctl",
            default=False
            )

    bmtool_kbs_use_mirror_merge_alt: BoolProperty(
            name="bmtool_kbs_use_mirror_merge_alt",
            default=False
            )

    bmtool_kbs_use_mirror_v: StringProperty(
            name="bmtool_kbs_use_mirror_v",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_mirror_v_shift: BoolProperty(
            name="bmtool_kbs_use_mirror_v_shift",
            default=False
            )

    bmtool_kbs_use_mirror_v_ctl: BoolProperty(
            name="bmtool_kbs_use_mirror_v_ctl",
            default=False
            )

    bmtool_kbs_use_mirror_v_alt: BoolProperty(
            name="bmtool_kbs_use_mirror_v_alt",
            default=False
            )

    bmtool_kbs_use_mirror_udim: StringProperty(
            name="bmtool_kbs_use_mirror_udim",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_mirror_udim_shift: BoolProperty(
            name="bmtool_kbs_use_mirror_udim_shift",
            default=False
            )

    bmtool_kbs_use_mirror_udim_ctl: BoolProperty(
            name="bmtool_kbs_use_mirror_udim_ctl",
            default=False
            )

    bmtool_kbs_use_mirror_udim_alt: BoolProperty(
            name="bmtool_kbs_use_mirror_udim_alt",
            default=False
            )

    bmtool_kbs_use_bisect_flip_axis: StringProperty(
            name="bmtool_kbs_use_bisect_flip_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_bisect_flip_axis_shift: BoolProperty(
            name="bmtool_kbs_use_bisect_flip_axis_shift",
            default=False
            )

    bmtool_kbs_use_bisect_flip_axis_ctl: BoolProperty(
            name="bmtool_kbs_use_bisect_flip_axis_ctl",
            default=False
            )

    bmtool_kbs_use_bisect_flip_axis_alt: BoolProperty(
            name="bmtool_kbs_use_bisect_flip_axis_alt",
            default=False
            )

    bmtool_kbs_use_mirror_u: StringProperty(
            name="bmtool_kbs_use_mirror_u",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_mirror_u_shift: BoolProperty(
            name="bmtool_kbs_use_mirror_u_shift",
            default=False
            )

    bmtool_kbs_use_mirror_u_ctl: BoolProperty(
            name="bmtool_kbs_use_mirror_u_ctl",
            default=False
            )

    bmtool_kbs_use_mirror_u_alt: BoolProperty(
            name="bmtool_kbs_use_mirror_u_alt",
            default=False
            )

    bmtool_kbs_use_bisect_axis: StringProperty(
            name="bmtool_kbs_use_bisect_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_bisect_axis_shift: BoolProperty(
            name="bmtool_kbs_use_bisect_axis_shift",
            default=False
            )

    bmtool_kbs_use_bisect_axis_ctl: BoolProperty(
            name="bmtool_kbs_use_bisect_axis_ctl",
            default=False
            )

    bmtool_kbs_use_bisect_axis_alt: BoolProperty(
            name="bmtool_kbs_use_bisect_axis_alt",
            default=False
            )

    bmtool_kbs_use_mirror_vertex_groups: StringProperty(
            name="bmtool_kbs_use_mirror_vertex_groups",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_mirror_vertex_groups_shift: BoolProperty(
            name="bmtool_kbs_use_mirror_vertex_groups_shift",
            default=False
            )

    bmtool_kbs_use_mirror_vertex_groups_ctl: BoolProperty(
            name="bmtool_kbs_use_mirror_vertex_groups_ctl",
            default=False
            )

    bmtool_kbs_use_mirror_vertex_groups_alt: BoolProperty(
            name="bmtool_kbs_use_mirror_vertex_groups_alt",
            default=False
            )

    bmtool_kbs_use_axis: StringProperty(
            name="bmtool_kbs_use_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_axis_shift: BoolProperty(
            name="bmtool_kbs_use_axis_shift",
            default=False
            )

    bmtool_kbs_use_axis_ctl: BoolProperty(
            name="bmtool_kbs_use_axis_ctl",
            default=False
            )

    bmtool_kbs_use_axis_alt: BoolProperty(
            name="bmtool_kbs_use_axis_alt",
            default=False
            )

    bmtool_kbs_use_clip: StringProperty(
            name="bmtool_kbs_use_clip",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_clip_shift: BoolProperty(
            name="bmtool_kbs_use_clip_shift",
            default=False
            )

    bmtool_kbs_use_clip_ctl: BoolProperty(
            name="bmtool_kbs_use_clip_ctl",
            default=False
            )

    bmtool_kbs_use_clip_alt: BoolProperty(
            name="bmtool_kbs_use_clip_alt",
            default=False
            )

    bmtool_kbs_use_creases: StringProperty(
            name="bmtool_kbs_use_creases",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_creases_shift: BoolProperty(
            name="bmtool_kbs_use_creases_shift",
            default=False
            )

    bmtool_kbs_use_creases_ctl: BoolProperty(
            name="bmtool_kbs_use_creases_ctl",
            default=False
            )

    bmtool_kbs_use_creases_alt: BoolProperty(
            name="bmtool_kbs_use_creases_alt",
            default=False
            )

    bmtool_kbs_use_sculpt_base_mesh: StringProperty(
            name="bmtool_kbs_use_sculpt_base_mesh",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_sculpt_base_mesh_shift: BoolProperty(
            name="bmtool_kbs_use_sculpt_base_mesh_shift",
            default=False
            )

    bmtool_kbs_use_sculpt_base_mesh_ctl: BoolProperty(
            name="bmtool_kbs_use_sculpt_base_mesh_ctl",
            default=False
            )

    bmtool_kbs_use_sculpt_base_mesh_alt: BoolProperty(
            name="bmtool_kbs_use_sculpt_base_mesh_alt",
            default=False
            )

    bmtool_kbs_show_only_control_edges: StringProperty(
            name="bmtool_kbs_show_only_control_edges",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_only_control_edges_shift: BoolProperty(
            name="bmtool_kbs_show_only_control_edges_shift",
            default=False
            )

    bmtool_kbs_show_only_control_edges_ctl: BoolProperty(
            name="bmtool_kbs_show_only_control_edges_ctl",
            default=False
            )

    bmtool_kbs_show_only_control_edges_alt: BoolProperty(
            name="bmtool_kbs_show_only_control_edges_alt",
            default=False
            )

    bmtool_kbs_use_custom_normals: StringProperty(
            name="bmtool_kbs_use_custom_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_custom_normals_shift: BoolProperty(
            name="bmtool_kbs_use_custom_normals_shift",
            default=False
            )

    bmtool_kbs_use_custom_normals_ctl: BoolProperty(
            name="bmtool_kbs_use_custom_normals_ctl",
            default=False
            )

    bmtool_kbs_use_custom_normals_alt: BoolProperty(
            name="bmtool_kbs_use_custom_normals_alt",
            default=False
            )

    bmtool_kbs_use_remove_disconnected: StringProperty(
            name="bmtool_kbs_use_remove_disconnected",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_remove_disconnected_shift: BoolProperty(
            name="bmtool_kbs_use_remove_disconnected_shift",
            default=False
            )

    bmtool_kbs_use_remove_disconnected_ctl: BoolProperty(
            name="bmtool_kbs_use_remove_disconnected_ctl",
            default=False
            )

    bmtool_kbs_use_remove_disconnected_alt: BoolProperty(
            name="bmtool_kbs_use_remove_disconnected_alt",
            default=False
            )

    bmtool_kbs_use_smooth_shade: StringProperty(
            name="bmtool_kbs_use_smooth_shade",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_smooth_shade_shift: BoolProperty(
            name="bmtool_kbs_use_smooth_shade_shift",
            default=False
            )

    bmtool_kbs_use_smooth_shade_ctl: BoolProperty(
            name="bmtool_kbs_use_smooth_shade_ctl",
            default=False
            )

    bmtool_kbs_use_smooth_shade_alt: BoolProperty(
            name="bmtool_kbs_use_smooth_shade_alt",
            default=False
            )

    bmtool_kbs_use_normal_calculate: StringProperty(
            name="bmtool_kbs_use_normal_calculate",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_calculate_shift: BoolProperty(
            name="bmtool_kbs_use_normal_calculate_shift",
            default=False
            )

    bmtool_kbs_use_normal_calculate_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_calculate_ctl",
            default=False
            )

    bmtool_kbs_use_normal_calculate_alt: BoolProperty(
            name="bmtool_kbs_use_normal_calculate_alt",
            default=False
            )

    bmtool_kbs_use_normal_flip: StringProperty(
            name="bmtool_kbs_use_normal_flip",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_flip_shift: BoolProperty(
            name="bmtool_kbs_use_normal_flip_shift",
            default=False
            )

    bmtool_kbs_use_normal_flip_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_flip_ctl",
            default=False
            )

    bmtool_kbs_use_normal_flip_alt: BoolProperty(
            name="bmtool_kbs_use_normal_flip_alt",
            default=False
            )

    bmtool_kbs_use_stretch_u: StringProperty(
            name="bmtool_kbs_use_stretch_u",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_stretch_u_shift: BoolProperty(
            name="bmtool_kbs_use_stretch_u_shift",
            default=False
            )

    bmtool_kbs_use_stretch_u_ctl: BoolProperty(
            name="bmtool_kbs_use_stretch_u_ctl",
            default=False
            )

    bmtool_kbs_use_stretch_u_alt: BoolProperty(
            name="bmtool_kbs_use_stretch_u_alt",
            default=False
            )

    bmtool_kbs_use_object_screw_offset: StringProperty(
            name="bmtool_kbs_use_object_screw_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_object_screw_offset_shift: BoolProperty(
            name="bmtool_kbs_use_object_screw_offset_shift",
            default=False
            )

    bmtool_kbs_use_object_screw_offset_ctl: BoolProperty(
            name="bmtool_kbs_use_object_screw_offset_ctl",
            default=False
            )

    bmtool_kbs_use_object_screw_offset_alt: BoolProperty(
            name="bmtool_kbs_use_object_screw_offset_alt",
            default=False
            )

    bmtool_kbs_use_stretch_v: StringProperty(
            name="bmtool_kbs_use_stretch_v",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_stretch_v_shift: BoolProperty(
            name="bmtool_kbs_use_stretch_v_shift",
            default=False
            )

    bmtool_kbs_use_stretch_v_ctl: BoolProperty(
            name="bmtool_kbs_use_stretch_v_ctl",
            default=False
            )

    bmtool_kbs_use_stretch_v_alt: BoolProperty(
            name="bmtool_kbs_use_stretch_v_alt",
            default=False
            )

    bmtool_kbs_use_x_symmetry: StringProperty(
            name="bmtool_kbs_use_x_symmetry",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_x_symmetry_shift: BoolProperty(
            name="bmtool_kbs_use_x_symmetry_shift",
            default=False
            )

    bmtool_kbs_use_x_symmetry_ctl: BoolProperty(
            name="bmtool_kbs_use_x_symmetry_ctl",
            default=False
            )

    bmtool_kbs_use_x_symmetry_alt: BoolProperty(
            name="bmtool_kbs_use_x_symmetry_alt",
            default=False
            )

    bmtool_kbs_use_y_symmetry: StringProperty(
            name="bmtool_kbs_use_y_symmetry",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_y_symmetry_shift: BoolProperty(
            name="bmtool_kbs_use_y_symmetry_shift",
            default=False
            )

    bmtool_kbs_use_y_symmetry_ctl: BoolProperty(
            name="bmtool_kbs_use_y_symmetry_ctl",
            default=False
            )

    bmtool_kbs_use_y_symmetry_alt: BoolProperty(
            name="bmtool_kbs_use_y_symmetry_alt",
            default=False
            )

    bmtool_kbs_use_z_symmetry: StringProperty(
            name="bmtool_kbs_use_z_symmetry",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_z_symmetry_shift: BoolProperty(
            name="bmtool_kbs_use_z_symmetry_shift",
            default=False
            )

    bmtool_kbs_use_z_symmetry_ctl: BoolProperty(
            name="bmtool_kbs_use_z_symmetry_ctl",
            default=False
            )

    bmtool_kbs_use_z_symmetry_alt: BoolProperty(
            name="bmtool_kbs_use_z_symmetry_alt",
            default=False
            )

    bmtool_kbs_use_rim: StringProperty(
            name="bmtool_kbs_use_rim",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_rim_shift: BoolProperty(
            name="bmtool_kbs_use_rim_shift",
            default=False
            )

    bmtool_kbs_use_rim_ctl: BoolProperty(
            name="bmtool_kbs_use_rim_ctl",
            default=False
            )

    bmtool_kbs_use_rim_alt: BoolProperty(
            name="bmtool_kbs_use_rim_alt",
            default=False
            )

    bmtool_kbs_use_rim_only: StringProperty(
            name="bmtool_kbs_use_rim_only",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_rim_only_shift: BoolProperty(
            name="bmtool_kbs_use_rim_only_shift",
            default=False
            )

    bmtool_kbs_use_rim_only_ctl: BoolProperty(
            name="bmtool_kbs_use_rim_only_ctl",
            default=False
            )

    bmtool_kbs_use_rim_only_alt: BoolProperty(
            name="bmtool_kbs_use_rim_only_alt",
            default=False
            )

    bmtool_kbs_use_quality_normals: StringProperty(
            name="bmtool_kbs_use_quality_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_quality_normals_shift: BoolProperty(
            name="bmtool_kbs_use_quality_normals_shift",
            default=False
            )

    bmtool_kbs_use_quality_normals_ctl: BoolProperty(
            name="bmtool_kbs_use_quality_normals_ctl",
            default=False
            )

    bmtool_kbs_use_quality_normals_alt: BoolProperty(
            name="bmtool_kbs_use_quality_normals_alt",
            default=False
            )

    bmtool_kbs_use_flat_faces: StringProperty(
            name="bmtool_kbs_use_flat_faces",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_flat_faces_shift: BoolProperty(
            name="bmtool_kbs_use_flat_faces_shift",
            default=False
            )

    bmtool_kbs_use_flat_faces_ctl: BoolProperty(
            name="bmtool_kbs_use_flat_faces_ctl",
            default=False
            )

    bmtool_kbs_use_flat_faces_alt: BoolProperty(
            name="bmtool_kbs_use_flat_faces_alt",
            default=False
            )

    bmtool_kbs_use_even_offset: StringProperty(
            name="bmtool_kbs_use_even_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_even_offset_shift: BoolProperty(
            name="bmtool_kbs_use_even_offset_shift",
            default=False
            )

    bmtool_kbs_use_even_offset_ctl: BoolProperty(
            name="bmtool_kbs_use_even_offset_ctl",
            default=False
            )

    bmtool_kbs_use_even_offset_alt: BoolProperty(
            name="bmtool_kbs_use_even_offset_alt",
            default=False
            )

    bmtool_kbs_use_flip_normals: StringProperty(
            name="bmtool_kbs_use_flip_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_flip_normals_shift: BoolProperty(
            name="bmtool_kbs_use_flip_normals_shift",
            default=False
            )

    bmtool_kbs_use_flip_normals_ctl: BoolProperty(
            name="bmtool_kbs_use_flip_normals_ctl",
            default=False
            )

    bmtool_kbs_use_flip_normals_alt: BoolProperty(
            name="bmtool_kbs_use_flip_normals_alt",
            default=False
            )

    bmtool_kbs_use_thickness_angle_clamp: StringProperty(
            name="bmtool_kbs_use_thickness_angle_clamp",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_thickness_angle_clamp_shift: BoolProperty(
            name="bmtool_kbs_use_thickness_angle_clamp_shift",
            default=False
            )

    bmtool_kbs_use_thickness_angle_clamp_ctl: BoolProperty(
            name="bmtool_kbs_use_thickness_angle_clamp_ctl",
            default=False
            )

    bmtool_kbs_use_thickness_angle_clamp_alt: BoolProperty(
            name="bmtool_kbs_use_thickness_angle_clamp_alt",
            default=False
            )

    bmtool_kbs_use_limit_surface: StringProperty(
            name="bmtool_kbs_use_limit_surface",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_limit_surface_shift: BoolProperty(
            name="bmtool_kbs_use_limit_surface_shift",
            default=False
            )

    bmtool_kbs_use_limit_surface_ctl: BoolProperty(
            name="bmtool_kbs_use_limit_surface_ctl",
            default=False
            )

    bmtool_kbs_use_limit_surface_alt: BoolProperty(
            name="bmtool_kbs_use_limit_surface_alt",
            default=False
            )

    bmtool_kbs_keep_custom_normals: StringProperty(
            name="bmtool_kbs_keep_custom_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_keep_custom_normals_shift: BoolProperty(
            name="bmtool_kbs_keep_custom_normals_shift",
            default=False
            )

    bmtool_kbs_keep_custom_normals_ctl: BoolProperty(
            name="bmtool_kbs_keep_custom_normals_ctl",
            default=False
            )

    bmtool_kbs_keep_custom_normals_alt: BoolProperty(
            name="bmtool_kbs_keep_custom_normals_alt",
            default=False
            )

    bmtool_kbs_loose_edges: StringProperty(
            name="bmtool_kbs_loose_edges",
            maxlen=1,
            default=''
            )

    bmtool_kbs_loose_edges_shift: BoolProperty(
            name="bmtool_kbs_loose_edges_shift",
            default=False
            )

    bmtool_kbs_loose_edges_ctl: BoolProperty(
            name="bmtool_kbs_loose_edges_ctl",
            default=False
            )

    bmtool_kbs_loose_edges_alt: BoolProperty(
            name="bmtool_kbs_loose_edges_alt",
            default=False
            )

    bmtool_kbs_use_crease: StringProperty(
            name="bmtool_kbs_use_crease",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_crease_shift: BoolProperty(
            name="bmtool_kbs_use_crease_shift",
            default=False
            )

    bmtool_kbs_use_crease_ctl: BoolProperty(
            name="bmtool_kbs_use_crease_ctl",
            default=False
            )

    bmtool_kbs_use_crease_alt: BoolProperty(
            name="bmtool_kbs_use_crease_alt",
            default=False
            )

    bmtool_kbs_use_replace: StringProperty(
            name="bmtool_kbs_use_replace",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_replace_shift: BoolProperty(
            name="bmtool_kbs_use_replace_shift",
            default=False
            )

    bmtool_kbs_use_replace_ctl: BoolProperty(
            name="bmtool_kbs_use_replace_ctl",
            default=False
            )

    bmtool_kbs_use_replace_alt: BoolProperty(
            name="bmtool_kbs_use_replace_alt",
            default=False
            )

    bmtool_kbs_use_boundary: StringProperty(
            name="bmtool_kbs_use_boundary",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_boundary_shift: BoolProperty(
            name="bmtool_kbs_use_boundary_shift",
            default=False
            )

    bmtool_kbs_use_boundary_ctl: BoolProperty(
            name="bmtool_kbs_use_boundary_ctl",
            default=False
            )

    bmtool_kbs_use_boundary_alt: BoolProperty(
            name="bmtool_kbs_use_boundary_alt",
            default=False
            )

    bmtool_kbs_use_multi_modifier: StringProperty(
            name="bmtool_kbs_use_multi_modifier",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_multi_modifier_shift: BoolProperty(
            name="bmtool_kbs_use_multi_modifier_shift",
            default=False
            )

    bmtool_kbs_use_multi_modifier_ctl: BoolProperty(
            name="bmtool_kbs_use_multi_modifier_ctl",
            default=False
            )

    bmtool_kbs_use_multi_modifier_alt: BoolProperty(
            name="bmtool_kbs_use_multi_modifier_alt",
            default=False
            )

    bmtool_kbs_use_bone_envelopes: StringProperty(
            name="bmtool_kbs_use_bone_envelopes",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_bone_envelopes_shift: BoolProperty(
            name="bmtool_kbs_use_bone_envelopes_shift",
            default=False
            )

    bmtool_kbs_use_bone_envelopes_ctl: BoolProperty(
            name="bmtool_kbs_use_bone_envelopes_ctl",
            default=False
            )

    bmtool_kbs_use_bone_envelopes_alt: BoolProperty(
            name="bmtool_kbs_use_bone_envelopes_alt",
            default=False
            )

    bmtool_kbs_use_deform_preserve_volume: StringProperty(
            name="bmtool_kbs_use_deform_preserve_volume",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_deform_preserve_volume_shift: BoolProperty(
            name="bmtool_kbs_use_deform_preserve_volume_shift",
            default=False
            )

    bmtool_kbs_use_deform_preserve_volume_ctl: BoolProperty(
            name="bmtool_kbs_use_deform_preserve_volume_ctl",
            default=False
            )

    bmtool_kbs_use_deform_preserve_volume_alt: BoolProperty(
            name="bmtool_kbs_use_deform_preserve_volume_alt",
            default=False
            )

    bmtool_kbs_use_vertex_groups: StringProperty(
            name="bmtool_kbs_use_vertex_groups",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_vertex_groups_shift: BoolProperty(
            name="bmtool_kbs_use_vertex_groups_shift",
            default=False
            )

    bmtool_kbs_use_vertex_groups_ctl: BoolProperty(
            name="bmtool_kbs_use_vertex_groups_ctl",
            default=False
            )

    bmtool_kbs_use_vertex_groups_alt: BoolProperty(
            name="bmtool_kbs_use_vertex_groups_alt",
            default=False
            )

    bmtool_kbs_use_z: StringProperty(
            name="bmtool_kbs_use_z",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_z_shift: BoolProperty(
            name="bmtool_kbs_use_z_shift",
            default=False
            )

    bmtool_kbs_use_z_ctl: BoolProperty(
            name="bmtool_kbs_use_z_ctl",
            default=False
            )

    bmtool_kbs_use_z_alt: BoolProperty(
            name="bmtool_kbs_use_z_alt",
            default=False
            )

    bmtool_kbs_use_x: StringProperty(
            name="bmtool_kbs_use_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_x_shift: BoolProperty(
            name="bmtool_kbs_use_x_shift",
            default=False
            )

    bmtool_kbs_use_x_ctl: BoolProperty(
            name="bmtool_kbs_use_x_ctl",
            default=False
            )

    bmtool_kbs_use_x_alt: BoolProperty(
            name="bmtool_kbs_use_x_alt",
            default=False
            )

    bmtool_kbs_use_y: StringProperty(
            name="bmtool_kbs_use_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_y_shift: BoolProperty(
            name="bmtool_kbs_use_y_shift",
            default=False
            )

    bmtool_kbs_use_y_ctl: BoolProperty(
            name="bmtool_kbs_use_y_ctl",
            default=False
            )

    bmtool_kbs_use_y_alt: BoolProperty(
            name="bmtool_kbs_use_y_alt",
            default=False
            )

    bmtool_kbs_use_radius_as_size: StringProperty(
            name="bmtool_kbs_use_radius_as_size",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_radius_as_size_shift: BoolProperty(
            name="bmtool_kbs_use_radius_as_size_shift",
            default=False
            )

    bmtool_kbs_use_radius_as_size_ctl: BoolProperty(
            name="bmtool_kbs_use_radius_as_size_ctl",
            default=False
            )

    bmtool_kbs_use_radius_as_size_alt: BoolProperty(
            name="bmtool_kbs_use_radius_as_size_alt",
            default=False
            )

    bmtool_kbs_use_transform: StringProperty(
            name="bmtool_kbs_use_transform",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_transform_shift: BoolProperty(
            name="bmtool_kbs_use_transform_shift",
            default=False
            )

    bmtool_kbs_use_transform_ctl: BoolProperty(
            name="bmtool_kbs_use_transform_ctl",
            default=False
            )

    bmtool_kbs_use_transform_alt: BoolProperty(
            name="bmtool_kbs_use_transform_alt",
            default=False
            )

    bmtool_kbs_use_falloff_uniform: StringProperty(
            name="bmtool_kbs_use_falloff_uniform",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_falloff_uniform_shift: BoolProperty(
            name="bmtool_kbs_use_falloff_uniform_shift",
            default=False
            )

    bmtool_kbs_use_falloff_uniform_ctl: BoolProperty(
            name="bmtool_kbs_use_falloff_uniform_ctl",
            default=False
            )

    bmtool_kbs_use_falloff_uniform_alt: BoolProperty(
            name="bmtool_kbs_use_falloff_uniform_alt",
            default=False
            )

    bmtool_kbs_use_dynamic_bind: StringProperty(
            name="bmtool_kbs_use_dynamic_bind",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_dynamic_bind_shift: BoolProperty(
            name="bmtool_kbs_use_dynamic_bind_shift",
            default=False
            )

    bmtool_kbs_use_dynamic_bind_ctl: BoolProperty(
            name="bmtool_kbs_use_dynamic_bind_ctl",
            default=False
            )

    bmtool_kbs_use_dynamic_bind_alt: BoolProperty(
            name="bmtool_kbs_use_dynamic_bind_alt",
            default=False
            )

    bmtool_kbs_use_project_z: StringProperty(
            name="bmtool_kbs_use_project_z",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_project_z_shift: BoolProperty(
            name="bmtool_kbs_use_project_z_shift",
            default=False
            )

    bmtool_kbs_use_project_z_ctl: BoolProperty(
            name="bmtool_kbs_use_project_z_ctl",
            default=False
            )

    bmtool_kbs_use_project_z_alt: BoolProperty(
            name="bmtool_kbs_use_project_z_alt",
            default=False
            )

    bmtool_kbs_use_negative_direction: StringProperty(
            name="bmtool_kbs_use_negative_direction",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_negative_direction_shift: BoolProperty(
            name="bmtool_kbs_use_negative_direction_shift",
            default=False
            )

    bmtool_kbs_use_negative_direction_ctl: BoolProperty(
            name="bmtool_kbs_use_negative_direction_ctl",
            default=False
            )

    bmtool_kbs_use_negative_direction_alt: BoolProperty(
            name="bmtool_kbs_use_negative_direction_alt",
            default=False
            )

    bmtool_kbs_use_invert_cull: StringProperty(
            name="bmtool_kbs_use_invert_cull",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_invert_cull_shift: BoolProperty(
            name="bmtool_kbs_use_invert_cull_shift",
            default=False
            )

    bmtool_kbs_use_invert_cull_ctl: BoolProperty(
            name="bmtool_kbs_use_invert_cull_ctl",
            default=False
            )

    bmtool_kbs_use_invert_cull_alt: BoolProperty(
            name="bmtool_kbs_use_invert_cull_alt",
            default=False
            )

    bmtool_kbs_use_positive_direction: StringProperty(
            name="bmtool_kbs_use_positive_direction",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_positive_direction_shift: BoolProperty(
            name="bmtool_kbs_use_positive_direction_shift",
            default=False
            )

    bmtool_kbs_use_positive_direction_ctl: BoolProperty(
            name="bmtool_kbs_use_positive_direction_ctl",
            default=False
            )

    bmtool_kbs_use_positive_direction_alt: BoolProperty(
            name="bmtool_kbs_use_positive_direction_alt",
            default=False
            )

    bmtool_kbs_use_project_y: StringProperty(
            name="bmtool_kbs_use_project_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_project_y_shift: BoolProperty(
            name="bmtool_kbs_use_project_y_shift",
            default=False
            )

    bmtool_kbs_use_project_y_ctl: BoolProperty(
            name="bmtool_kbs_use_project_y_ctl",
            default=False
            )

    bmtool_kbs_use_project_y_alt: BoolProperty(
            name="bmtool_kbs_use_project_y_alt",
            default=False
            )

    bmtool_kbs_use_project_x: StringProperty(
            name="bmtool_kbs_use_project_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_project_x_shift: BoolProperty(
            name="bmtool_kbs_use_project_x_shift",
            default=False
            )

    bmtool_kbs_use_project_x_ctl: BoolProperty(
            name="bmtool_kbs_use_project_x_ctl",
            default=False
            )

    bmtool_kbs_use_project_x_alt: BoolProperty(
            name="bmtool_kbs_use_project_x_alt",
            default=False
            )

    bmtool_kbs_lock_z: StringProperty(
            name="bmtool_kbs_lock_z",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lock_z_shift: BoolProperty(
            name="bmtool_kbs_lock_z_shift",
            default=False
            )

    bmtool_kbs_lock_z_ctl: BoolProperty(
            name="bmtool_kbs_lock_z_ctl",
            default=False
            )

    bmtool_kbs_lock_z_alt: BoolProperty(
            name="bmtool_kbs_lock_z_alt",
            default=False
            )

    bmtool_kbs_lock_x: StringProperty(
            name="bmtool_kbs_lock_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lock_x_shift: BoolProperty(
            name="bmtool_kbs_lock_x_shift",
            default=False
            )

    bmtool_kbs_lock_x_ctl: BoolProperty(
            name="bmtool_kbs_lock_x_ctl",
            default=False
            )

    bmtool_kbs_lock_x_alt: BoolProperty(
            name="bmtool_kbs_lock_x_alt",
            default=False
            )

    bmtool_kbs_lock_y: StringProperty(
            name="bmtool_kbs_lock_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lock_y_shift: BoolProperty(
            name="bmtool_kbs_lock_y_shift",
            default=False
            )

    bmtool_kbs_lock_y_ctl: BoolProperty(
            name="bmtool_kbs_lock_y_ctl",
            default=False
            )

    bmtool_kbs_lock_y_alt: BoolProperty(
            name="bmtool_kbs_lock_y_alt",
            default=False
            )

    bmtool_kbs_use_only_smooth: StringProperty(
            name="bmtool_kbs_use_only_smooth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_only_smooth_shift: BoolProperty(
            name="bmtool_kbs_use_only_smooth_shift",
            default=False
            )

    bmtool_kbs_use_only_smooth_ctl: BoolProperty(
            name="bmtool_kbs_use_only_smooth_ctl",
            default=False
            )

    bmtool_kbs_use_only_smooth_alt: BoolProperty(
            name="bmtool_kbs_use_only_smooth_alt",
            default=False
            )

    bmtool_kbs_use_pin_boundary: StringProperty(
            name="bmtool_kbs_use_pin_boundary",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_pin_boundary_shift: BoolProperty(
            name="bmtool_kbs_use_pin_boundary_shift",
            default=False
            )

    bmtool_kbs_use_pin_boundary_ctl: BoolProperty(
            name="bmtool_kbs_use_pin_boundary_ctl",
            default=False
            )

    bmtool_kbs_use_pin_boundary_alt: BoolProperty(
            name="bmtool_kbs_use_pin_boundary_alt",
            default=False
            )

    bmtool_kbs_use_normalized: StringProperty(
            name="bmtool_kbs_use_normalized",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normalized_shift: BoolProperty(
            name="bmtool_kbs_use_normalized_shift",
            default=False
            )

    bmtool_kbs_use_normalized_ctl: BoolProperty(
            name="bmtool_kbs_use_normalized_ctl",
            default=False
            )

    bmtool_kbs_use_normalized_alt: BoolProperty(
            name="bmtool_kbs_use_normalized_alt",
            default=False
            )

    bmtool_kbs_use_volume_preserve: StringProperty(
            name="bmtool_kbs_use_volume_preserve",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_volume_preserve_shift: BoolProperty(
            name="bmtool_kbs_use_volume_preserve_shift",
            default=False
            )

    bmtool_kbs_use_volume_preserve_ctl: BoolProperty(
            name="bmtool_kbs_use_volume_preserve_ctl",
            default=False
            )

    bmtool_kbs_use_volume_preserve_alt: BoolProperty(
            name="bmtool_kbs_use_volume_preserve_alt",
            default=False
            )

    bmtool_kbs_use_sparse_bind: StringProperty(
            name="bmtool_kbs_use_sparse_bind",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_sparse_bind_shift: BoolProperty(
            name="bmtool_kbs_use_sparse_bind_shift",
            default=False
            )

    bmtool_kbs_use_sparse_bind_ctl: BoolProperty(
            name="bmtool_kbs_use_sparse_bind_ctl",
            default=False
            )

    bmtool_kbs_use_sparse_bind_alt: BoolProperty(
            name="bmtool_kbs_use_sparse_bind_alt",
            default=False
            )

    bmtool_kbs_use_normal: StringProperty(
            name="bmtool_kbs_use_normal",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_shift: BoolProperty(
            name="bmtool_kbs_use_normal_shift",
            default=False
            )

    bmtool_kbs_use_normal_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_ctl",
            default=False
            )

    bmtool_kbs_use_normal_alt: BoolProperty(
            name="bmtool_kbs_use_normal_alt",
            default=False
            )

    bmtool_kbs_use_normal_y: StringProperty(
            name="bmtool_kbs_use_normal_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_y_shift: BoolProperty(
            name="bmtool_kbs_use_normal_y_shift",
            default=False
            )

    bmtool_kbs_use_normal_y_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_y_ctl",
            default=False
            )

    bmtool_kbs_use_normal_y_alt: BoolProperty(
            name="bmtool_kbs_use_normal_y_alt",
            default=False
            )

    bmtool_kbs_use_cyclic: StringProperty(
            name="bmtool_kbs_use_cyclic",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_cyclic_shift: BoolProperty(
            name="bmtool_kbs_use_cyclic_shift",
            default=False
            )

    bmtool_kbs_use_cyclic_ctl: BoolProperty(
            name="bmtool_kbs_use_cyclic_ctl",
            default=False
            )

    bmtool_kbs_use_cyclic_alt: BoolProperty(
            name="bmtool_kbs_use_cyclic_alt",
            default=False
            )

    bmtool_kbs_use_normal_z: StringProperty(
            name="bmtool_kbs_use_normal_z",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_z_shift: BoolProperty(
            name="bmtool_kbs_use_normal_z_shift",
            default=False
            )

    bmtool_kbs_use_normal_z_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_z_ctl",
            default=False
            )

    bmtool_kbs_use_normal_z_alt: BoolProperty(
            name="bmtool_kbs_use_normal_z_alt",
            default=False
            )

    bmtool_kbs_use_normal_x: StringProperty(
            name="bmtool_kbs_use_normal_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normal_x_shift: BoolProperty(
            name="bmtool_kbs_use_normal_x_shift",
            default=False
            )

    bmtool_kbs_use_normal_x_ctl: BoolProperty(
            name="bmtool_kbs_use_normal_x_ctl",
            default=False
            )

    bmtool_kbs_use_normal_x_alt: BoolProperty(
            name="bmtool_kbs_use_normal_x_alt",
            default=False
            )

    bmtool_kbs_show_alive: StringProperty(
            name="bmtool_kbs_show_alive",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_alive_shift: BoolProperty(
            name="bmtool_kbs_show_alive_shift",
            default=False
            )

    bmtool_kbs_show_alive_ctl: BoolProperty(
            name="bmtool_kbs_show_alive_ctl",
            default=False
            )

    bmtool_kbs_show_alive_alt: BoolProperty(
            name="bmtool_kbs_show_alive_alt",
            default=False
            )

    bmtool_kbs_show_dead: StringProperty(
            name="bmtool_kbs_show_dead",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_dead_shift: BoolProperty(
            name="bmtool_kbs_show_dead_shift",
            default=False
            )

    bmtool_kbs_show_dead_ctl: BoolProperty(
            name="bmtool_kbs_show_dead_ctl",
            default=False
            )

    bmtool_kbs_show_dead_alt: BoolProperty(
            name="bmtool_kbs_show_dead_alt",
            default=False
            )

    bmtool_kbs_use_size: StringProperty(
            name="bmtool_kbs_use_size",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_size_shift: BoolProperty(
            name="bmtool_kbs_use_size_shift",
            default=False
            )

    bmtool_kbs_use_size_ctl: BoolProperty(
            name="bmtool_kbs_use_size_ctl",
            default=False
            )

    bmtool_kbs_use_size_alt: BoolProperty(
            name="bmtool_kbs_use_size_alt",
            default=False
            )

    bmtool_kbs_show_unborn: StringProperty(
            name="bmtool_kbs_show_unborn",
            maxlen=1,
            default=''
            )

    bmtool_kbs_show_unborn_shift: BoolProperty(
            name="bmtool_kbs_show_unborn_shift",
            default=False
            )

    bmtool_kbs_show_unborn_ctl: BoolProperty(
            name="bmtool_kbs_show_unborn_ctl",
            default=False
            )

    bmtool_kbs_show_unborn_alt: BoolProperty(
            name="bmtool_kbs_show_unborn_alt",
            default=False
            )

    bmtool_kbs_use_edge_cut: StringProperty(
            name="bmtool_kbs_use_edge_cut",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_edge_cut_shift: BoolProperty(
            name="bmtool_kbs_use_edge_cut_shift",
            default=False
            )

    bmtool_kbs_use_edge_cut_ctl: BoolProperty(
            name="bmtool_kbs_use_edge_cut_ctl",
            default=False
            )

    bmtool_kbs_use_edge_cut_alt: BoolProperty(
            name="bmtool_kbs_use_edge_cut_alt",
            default=False
            )

    bmtool_kbs_use_spray: StringProperty(
            name="bmtool_kbs_use_spray",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_spray_shift: BoolProperty(
            name="bmtool_kbs_use_spray_shift",
            default=False
            )

    bmtool_kbs_use_spray_ctl: BoolProperty(
            name="bmtool_kbs_use_spray_ctl",
            default=False
            )

    bmtool_kbs_use_spray_alt: BoolProperty(
            name="bmtool_kbs_use_spray_alt",
            default=False
            )

    bmtool_kbs_invert_spray: StringProperty(
            name="bmtool_kbs_invert_spray",
            maxlen=1,
            default=''
            )

    bmtool_kbs_invert_spray_shift: BoolProperty(
            name="bmtool_kbs_invert_spray_shift",
            default=False
            )

    bmtool_kbs_invert_spray_ctl: BoolProperty(
            name="bmtool_kbs_invert_spray_ctl",
            default=False
            )

    bmtool_kbs_invert_spray_alt: BoolProperty(
            name="bmtool_kbs_invert_spray_alt",
            default=False
            )

    bmtool_kbs_use_foam: StringProperty(
            name="bmtool_kbs_use_foam",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_foam_shift: BoolProperty(
            name="bmtool_kbs_use_foam_shift",
            default=False
            )

    bmtool_kbs_use_foam_ctl: BoolProperty(
            name="bmtool_kbs_use_foam_ctl",
            default=False
            )

    bmtool_kbs_use_foam_alt: BoolProperty(
            name="bmtool_kbs_use_foam_alt",
            default=False
            )

    bmtool_kbs_use_normals: StringProperty(
            name="bmtool_kbs_use_normals",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_normals_shift: BoolProperty(
            name="bmtool_kbs_use_normals_shift",
            default=False
            )

    bmtool_kbs_use_normals_ctl: BoolProperty(
            name="bmtool_kbs_use_normals_ctl",
            default=False
            )

    bmtool_kbs_use_normals_alt: BoolProperty(
            name="bmtool_kbs_use_normals_alt",
            default=False
            )

    bmtool_kbs_use_children: StringProperty(
            name="bmtool_kbs_use_children",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_children_shift: BoolProperty(
            name="bmtool_kbs_use_children_shift",
            default=False
            )

    bmtool_kbs_use_children_ctl: BoolProperty(
            name="bmtool_kbs_use_children_ctl",
            default=False
            )

    bmtool_kbs_use_children_alt: BoolProperty(
            name="bmtool_kbs_use_children_alt",
            default=False
            )

    bmtool_kbs_use_preserve_shape: StringProperty(
            name="bmtool_kbs_use_preserve_shape",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_preserve_shape_shift: BoolProperty(
            name="bmtool_kbs_use_preserve_shape_shift",
            default=False
            )

    bmtool_kbs_use_preserve_shape_ctl: BoolProperty(
            name="bmtool_kbs_use_preserve_shape_ctl",
            default=False
            )

    bmtool_kbs_use_preserve_shape_alt: BoolProperty(
            name="bmtool_kbs_use_preserve_shape_alt",
            default=False
            )

    bmtool_kbs_use_path: StringProperty(
            name="bmtool_kbs_use_path",
            maxlen=1,
            default=''
            )

    bmtool_kbs_use_path_shift: BoolProperty(
            name="bmtool_kbs_use_path_shift",
            default=False
            )

    bmtool_kbs_use_path_ctl: BoolProperty(
            name="bmtool_kbs_use_path_ctl",
            default=False
            )

    bmtool_kbs_use_path_alt: BoolProperty(
            name="bmtool_kbs_use_path_alt",
            default=False
            )

    bmtool_kbs_layers_vcol_select_src: StringProperty(
            name="bmtool_kbs_layers_vcol_select_src",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_vcol_select_src_shift: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_src_shift",
            default=False
            )

    bmtool_kbs_layers_vcol_select_src_ctl: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_src_ctl",
            default=False
            )

    bmtool_kbs_layers_vcol_select_src_alt: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_src_alt",
            default=False
            )

    bmtool_kbs_vert_mapping: StringProperty(
            name="bmtool_kbs_vert_mapping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vert_mapping_shift: BoolProperty(
            name="bmtool_kbs_vert_mapping_shift",
            default=False
            )

    bmtool_kbs_vert_mapping_ctl: BoolProperty(
            name="bmtool_kbs_vert_mapping_ctl",
            default=False
            )

    bmtool_kbs_vert_mapping_alt: BoolProperty(
            name="bmtool_kbs_vert_mapping_alt",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_src: StringProperty(
            name="bmtool_kbs_layers_vgroup_select_src",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_vgroup_select_src_shift: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_src_shift",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_src_ctl: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_src_ctl",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_src_alt: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_src_alt",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_dst: StringProperty(
            name="bmtool_kbs_layers_vgroup_select_dst",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_vgroup_select_dst_shift: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_dst_shift",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_dst_ctl: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_dst_ctl",
            default=False
            )

    bmtool_kbs_layers_vgroup_select_dst_alt: BoolProperty(
            name="bmtool_kbs_layers_vgroup_select_dst_alt",
            default=False
            )

    bmtool_kbs_layers_vcol_select_dst: StringProperty(
            name="bmtool_kbs_layers_vcol_select_dst",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_vcol_select_dst_shift: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_dst_shift",
            default=False
            )

    bmtool_kbs_layers_vcol_select_dst_ctl: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_dst_ctl",
            default=False
            )

    bmtool_kbs_layers_vcol_select_dst_alt: BoolProperty(
            name="bmtool_kbs_layers_vcol_select_dst_alt",
            default=False
            )

    bmtool_kbs_poly_mapping: StringProperty(
            name="bmtool_kbs_poly_mapping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_poly_mapping_shift: BoolProperty(
            name="bmtool_kbs_poly_mapping_shift",
            default=False
            )

    bmtool_kbs_poly_mapping_ctl: BoolProperty(
            name="bmtool_kbs_poly_mapping_ctl",
            default=False
            )

    bmtool_kbs_poly_mapping_alt: BoolProperty(
            name="bmtool_kbs_poly_mapping_alt",
            default=False
            )

    bmtool_kbs_mix_mode: StringProperty(
            name="bmtool_kbs_mix_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mix_mode_shift: BoolProperty(
            name="bmtool_kbs_mix_mode_shift",
            default=False
            )

    bmtool_kbs_mix_mode_ctl: BoolProperty(
            name="bmtool_kbs_mix_mode_ctl",
            default=False
            )

    bmtool_kbs_mix_mode_alt: BoolProperty(
            name="bmtool_kbs_mix_mode_alt",
            default=False
            )

    bmtool_kbs_data_types_edges: StringProperty(
            name="bmtool_kbs_data_types_edges",
            maxlen=1,
            default=''
            )

    bmtool_kbs_data_types_edges_shift: BoolProperty(
            name="bmtool_kbs_data_types_edges_shift",
            default=False
            )

    bmtool_kbs_data_types_edges_ctl: BoolProperty(
            name="bmtool_kbs_data_types_edges_ctl",
            default=False
            )

    bmtool_kbs_data_types_edges_alt: BoolProperty(
            name="bmtool_kbs_data_types_edges_alt",
            default=False
            )

    bmtool_kbs_layers_uv_select_src: StringProperty(
            name="bmtool_kbs_layers_uv_select_src",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_uv_select_src_shift: BoolProperty(
            name="bmtool_kbs_layers_uv_select_src_shift",
            default=False
            )

    bmtool_kbs_layers_uv_select_src_ctl: BoolProperty(
            name="bmtool_kbs_layers_uv_select_src_ctl",
            default=False
            )

    bmtool_kbs_layers_uv_select_src_alt: BoolProperty(
            name="bmtool_kbs_layers_uv_select_src_alt",
            default=False
            )

    bmtool_kbs_data_types_polys: StringProperty(
            name="bmtool_kbs_data_types_polys",
            maxlen=1,
            default=''
            )

    bmtool_kbs_data_types_polys_shift: BoolProperty(
            name="bmtool_kbs_data_types_polys_shift",
            default=False
            )

    bmtool_kbs_data_types_polys_ctl: BoolProperty(
            name="bmtool_kbs_data_types_polys_ctl",
            default=False
            )

    bmtool_kbs_data_types_polys_alt: BoolProperty(
            name="bmtool_kbs_data_types_polys_alt",
            default=False
            )

    bmtool_kbs_data_types_verts: StringProperty(
            name="bmtool_kbs_data_types_verts",
            maxlen=1,
            default=''
            )

    bmtool_kbs_data_types_verts_shift: BoolProperty(
            name="bmtool_kbs_data_types_verts_shift",
            default=False
            )

    bmtool_kbs_data_types_verts_ctl: BoolProperty(
            name="bmtool_kbs_data_types_verts_ctl",
            default=False
            )

    bmtool_kbs_data_types_verts_alt: BoolProperty(
            name="bmtool_kbs_data_types_verts_alt",
            default=False
            )

    bmtool_kbs_layers_uv_select_dst: StringProperty(
            name="bmtool_kbs_layers_uv_select_dst",
            maxlen=1,
            default=''
            )

    bmtool_kbs_layers_uv_select_dst_shift: BoolProperty(
            name="bmtool_kbs_layers_uv_select_dst_shift",
            default=False
            )

    bmtool_kbs_layers_uv_select_dst_ctl: BoolProperty(
            name="bmtool_kbs_layers_uv_select_dst_ctl",
            default=False
            )

    bmtool_kbs_layers_uv_select_dst_alt: BoolProperty(
            name="bmtool_kbs_layers_uv_select_dst_alt",
            default=False
            )

    bmtool_kbs_edge_mapping: StringProperty(
            name="bmtool_kbs_edge_mapping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_edge_mapping_shift: BoolProperty(
            name="bmtool_kbs_edge_mapping_shift",
            default=False
            )

    bmtool_kbs_edge_mapping_ctl: BoolProperty(
            name="bmtool_kbs_edge_mapping_ctl",
            default=False
            )

    bmtool_kbs_edge_mapping_alt: BoolProperty(
            name="bmtool_kbs_edge_mapping_alt",
            default=False
            )

    bmtool_kbs_loop_mapping: StringProperty(
            name="bmtool_kbs_loop_mapping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_loop_mapping_shift: BoolProperty(
            name="bmtool_kbs_loop_mapping_shift",
            default=False
            )

    bmtool_kbs_loop_mapping_ctl: BoolProperty(
            name="bmtool_kbs_loop_mapping_ctl",
            default=False
            )

    bmtool_kbs_loop_mapping_alt: BoolProperty(
            name="bmtool_kbs_loop_mapping_alt",
            default=False
            )

    bmtool_kbs_data_types_loops: StringProperty(
            name="bmtool_kbs_data_types_loops",
            maxlen=1,
            default=''
            )

    bmtool_kbs_data_types_loops_shift: BoolProperty(
            name="bmtool_kbs_data_types_loops_shift",
            default=False
            )

    bmtool_kbs_data_types_loops_ctl: BoolProperty(
            name="bmtool_kbs_data_types_loops_ctl",
            default=False
            )

    bmtool_kbs_data_types_loops_alt: BoolProperty(
            name="bmtool_kbs_data_types_loops_alt",
            default=False
            )

    bmtool_kbs_up_axis: StringProperty(
            name="bmtool_kbs_up_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_up_axis_shift: BoolProperty(
            name="bmtool_kbs_up_axis_shift",
            default=False
            )

    bmtool_kbs_up_axis_ctl: BoolProperty(
            name="bmtool_kbs_up_axis_ctl",
            default=False
            )

    bmtool_kbs_up_axis_alt: BoolProperty(
            name="bmtool_kbs_up_axis_alt",
            default=False
            )

    bmtool_kbs_cache_format: StringProperty(
            name="bmtool_kbs_cache_format",
            maxlen=1,
            default=''
            )

    bmtool_kbs_cache_format_shift: BoolProperty(
            name="bmtool_kbs_cache_format_shift",
            default=False
            )

    bmtool_kbs_cache_format_ctl: BoolProperty(
            name="bmtool_kbs_cache_format_ctl",
            default=False
            )

    bmtool_kbs_cache_format_alt: BoolProperty(
            name="bmtool_kbs_cache_format_alt",
            default=False
            )

    bmtool_kbs_deform_mode: StringProperty(
            name="bmtool_kbs_deform_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_deform_mode_shift: BoolProperty(
            name="bmtool_kbs_deform_mode_shift",
            default=False
            )

    bmtool_kbs_deform_mode_ctl: BoolProperty(
            name="bmtool_kbs_deform_mode_ctl",
            default=False
            )

    bmtool_kbs_deform_mode_alt: BoolProperty(
            name="bmtool_kbs_deform_mode_alt",
            default=False
            )

    bmtool_kbs_play_mode: StringProperty(
            name="bmtool_kbs_play_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_play_mode_shift: BoolProperty(
            name="bmtool_kbs_play_mode_shift",
            default=False
            )

    bmtool_kbs_play_mode_ctl: BoolProperty(
            name="bmtool_kbs_play_mode_ctl",
            default=False
            )

    bmtool_kbs_play_mode_alt: BoolProperty(
            name="bmtool_kbs_play_mode_alt",
            default=False
            )

    bmtool_kbs_interpolation: StringProperty(
            name="bmtool_kbs_interpolation",
            maxlen=1,
            default=''
            )

    bmtool_kbs_interpolation_shift: BoolProperty(
            name="bmtool_kbs_interpolation_shift",
            default=False
            )

    bmtool_kbs_interpolation_ctl: BoolProperty(
            name="bmtool_kbs_interpolation_ctl",
            default=False
            )

    bmtool_kbs_interpolation_alt: BoolProperty(
            name="bmtool_kbs_interpolation_alt",
            default=False
            )

    bmtool_kbs_forward_axis: StringProperty(
            name="bmtool_kbs_forward_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_forward_axis_shift: BoolProperty(
            name="bmtool_kbs_forward_axis_shift",
            default=False
            )

    bmtool_kbs_forward_axis_ctl: BoolProperty(
            name="bmtool_kbs_forward_axis_ctl",
            default=False
            )

    bmtool_kbs_forward_axis_alt: BoolProperty(
            name="bmtool_kbs_forward_axis_alt",
            default=False
            )

    bmtool_kbs_flip_axis: StringProperty(
            name="bmtool_kbs_flip_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_flip_axis_shift: BoolProperty(
            name="bmtool_kbs_flip_axis_shift",
            default=False
            )

    bmtool_kbs_flip_axis_ctl: BoolProperty(
            name="bmtool_kbs_flip_axis_ctl",
            default=False
            )

    bmtool_kbs_flip_axis_alt: BoolProperty(
            name="bmtool_kbs_flip_axis_alt",
            default=False
            )

    bmtool_kbs_time_mode: StringProperty(
            name="bmtool_kbs_time_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_time_mode_shift: BoolProperty(
            name="bmtool_kbs_time_mode_shift",
            default=False
            )

    bmtool_kbs_time_mode_ctl: BoolProperty(
            name="bmtool_kbs_time_mode_ctl",
            default=False
            )

    bmtool_kbs_time_mode_alt: BoolProperty(
            name="bmtool_kbs_time_mode_alt",
            default=False
            )

    bmtool_kbs_read_data: StringProperty(
            name="bmtool_kbs_read_data",
            maxlen=1,
            default=''
            )

    bmtool_kbs_read_data_shift: BoolProperty(
            name="bmtool_kbs_read_data_shift",
            default=False
            )

    bmtool_kbs_read_data_ctl: BoolProperty(
            name="bmtool_kbs_read_data_ctl",
            default=False
            )

    bmtool_kbs_read_data_alt: BoolProperty(
            name="bmtool_kbs_read_data_alt",
            default=False
            )

    bmtool_kbs_mode: StringProperty(
            name="bmtool_kbs_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mode_shift: BoolProperty(
            name="bmtool_kbs_mode_shift",
            default=False
            )

    bmtool_kbs_mode_ctl: BoolProperty(
            name="bmtool_kbs_mode_ctl",
            default=False
            )

    bmtool_kbs_mode_alt: BoolProperty(
            name="bmtool_kbs_mode_alt",
            default=False
            )

    bmtool_kbs_axis_v: StringProperty(
            name="bmtool_kbs_axis_v",
            maxlen=1,
            default=''
            )

    bmtool_kbs_axis_v_shift: BoolProperty(
            name="bmtool_kbs_axis_v_shift",
            default=False
            )

    bmtool_kbs_axis_v_ctl: BoolProperty(
            name="bmtool_kbs_axis_v_ctl",
            default=False
            )

    bmtool_kbs_axis_v_alt: BoolProperty(
            name="bmtool_kbs_axis_v_alt",
            default=False
            )

    bmtool_kbs_axis_u: StringProperty(
            name="bmtool_kbs_axis_u",
            maxlen=1,
            default=''
            )

    bmtool_kbs_axis_u_shift: BoolProperty(
            name="bmtool_kbs_axis_u_shift",
            default=False
            )

    bmtool_kbs_axis_u_ctl: BoolProperty(
            name="bmtool_kbs_axis_u_ctl",
            default=False
            )

    bmtool_kbs_axis_u_alt: BoolProperty(
            name="bmtool_kbs_axis_u_alt",
            default=False
            )

    bmtool_kbs_mask_tex_mapping: StringProperty(
            name="bmtool_kbs_mask_tex_mapping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_tex_mapping_shift: BoolProperty(
            name="bmtool_kbs_mask_tex_mapping_shift",
            default=False
            )

    bmtool_kbs_mask_tex_mapping_ctl: BoolProperty(
            name="bmtool_kbs_mask_tex_mapping_ctl",
            default=False
            )

    bmtool_kbs_mask_tex_mapping_alt: BoolProperty(
            name="bmtool_kbs_mask_tex_mapping_alt",
            default=False
            )

    bmtool_kbs_mask_tex_use_channel: StringProperty(
            name="bmtool_kbs_mask_tex_use_channel",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_tex_use_channel_shift: BoolProperty(
            name="bmtool_kbs_mask_tex_use_channel_shift",
            default=False
            )

    bmtool_kbs_mask_tex_use_channel_ctl: BoolProperty(
            name="bmtool_kbs_mask_tex_use_channel_ctl",
            default=False
            )

    bmtool_kbs_mask_tex_use_channel_alt: BoolProperty(
            name="bmtool_kbs_mask_tex_use_channel_alt",
            default=False
            )

    bmtool_kbs_falloff_type: StringProperty(
            name="bmtool_kbs_falloff_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_falloff_type_shift: BoolProperty(
            name="bmtool_kbs_falloff_type_shift",
            default=False
            )

    bmtool_kbs_falloff_type_ctl: BoolProperty(
            name="bmtool_kbs_falloff_type_ctl",
            default=False
            )

    bmtool_kbs_falloff_type_alt: BoolProperty(
            name="bmtool_kbs_falloff_type_alt",
            default=False
            )

    bmtool_kbs_mix_set: StringProperty(
            name="bmtool_kbs_mix_set",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mix_set_shift: BoolProperty(
            name="bmtool_kbs_mix_set_shift",
            default=False
            )

    bmtool_kbs_mix_set_ctl: BoolProperty(
            name="bmtool_kbs_mix_set_ctl",
            default=False
            )

    bmtool_kbs_mix_set_alt: BoolProperty(
            name="bmtool_kbs_mix_set_alt",
            default=False
            )

    bmtool_kbs_proximity_mode: StringProperty(
            name="bmtool_kbs_proximity_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_proximity_mode_shift: BoolProperty(
            name="bmtool_kbs_proximity_mode_shift",
            default=False
            )

    bmtool_kbs_proximity_mode_ctl: BoolProperty(
            name="bmtool_kbs_proximity_mode_ctl",
            default=False
            )

    bmtool_kbs_proximity_mode_alt: BoolProperty(
            name="bmtool_kbs_proximity_mode_alt",
            default=False
            )

    bmtool_kbs_proximity_geometry: StringProperty(
            name="bmtool_kbs_proximity_geometry",
            maxlen=1,
            default=''
            )

    bmtool_kbs_proximity_geometry_shift: BoolProperty(
            name="bmtool_kbs_proximity_geometry_shift",
            default=False
            )

    bmtool_kbs_proximity_geometry_ctl: BoolProperty(
            name="bmtool_kbs_proximity_geometry_ctl",
            default=False
            )

    bmtool_kbs_proximity_geometry_alt: BoolProperty(
            name="bmtool_kbs_proximity_geometry_alt",
            default=False
            )

    bmtool_kbs_fit_type: StringProperty(
            name="bmtool_kbs_fit_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_fit_type_shift: BoolProperty(
            name="bmtool_kbs_fit_type_shift",
            default=False
            )

    bmtool_kbs_fit_type_ctl: BoolProperty(
            name="bmtool_kbs_fit_type_ctl",
            default=False
            )

    bmtool_kbs_fit_type_alt: BoolProperty(
            name="bmtool_kbs_fit_type_alt",
            default=False
            )

    bmtool_kbs_face_strength_mode: StringProperty(
            name="bmtool_kbs_face_strength_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_face_strength_mode_shift: BoolProperty(
            name="bmtool_kbs_face_strength_mode_shift",
            default=False
            )

    bmtool_kbs_face_strength_mode_ctl: BoolProperty(
            name="bmtool_kbs_face_strength_mode_ctl",
            default=False
            )

    bmtool_kbs_face_strength_mode_alt: BoolProperty(
            name="bmtool_kbs_face_strength_mode_alt",
            default=False
            )

    bmtool_kbs_profile_type: StringProperty(
            name="bmtool_kbs_profile_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_profile_type_shift: BoolProperty(
            name="bmtool_kbs_profile_type_shift",
            default=False
            )

    bmtool_kbs_profile_type_ctl: BoolProperty(
            name="bmtool_kbs_profile_type_ctl",
            default=False
            )

    bmtool_kbs_profile_type_alt: BoolProperty(
            name="bmtool_kbs_profile_type_alt",
            default=False
            )

    bmtool_kbs_miter_inner: StringProperty(
            name="bmtool_kbs_miter_inner",
            maxlen=1,
            default=''
            )

    bmtool_kbs_miter_inner_shift: BoolProperty(
            name="bmtool_kbs_miter_inner_shift",
            default=False
            )

    bmtool_kbs_miter_inner_ctl: BoolProperty(
            name="bmtool_kbs_miter_inner_ctl",
            default=False
            )

    bmtool_kbs_miter_inner_alt: BoolProperty(
            name="bmtool_kbs_miter_inner_alt",
            default=False
            )

    bmtool_kbs_limit_method: StringProperty(
            name="bmtool_kbs_limit_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_limit_method_shift: BoolProperty(
            name="bmtool_kbs_limit_method_shift",
            default=False
            )

    bmtool_kbs_limit_method_ctl: BoolProperty(
            name="bmtool_kbs_limit_method_ctl",
            default=False
            )

    bmtool_kbs_limit_method_alt: BoolProperty(
            name="bmtool_kbs_limit_method_alt",
            default=False
            )

    bmtool_kbs_miter_outer: StringProperty(
            name="bmtool_kbs_miter_outer",
            maxlen=1,
            default=''
            )

    bmtool_kbs_miter_outer_shift: BoolProperty(
            name="bmtool_kbs_miter_outer_shift",
            default=False
            )

    bmtool_kbs_miter_outer_ctl: BoolProperty(
            name="bmtool_kbs_miter_outer_ctl",
            default=False
            )

    bmtool_kbs_miter_outer_alt: BoolProperty(
            name="bmtool_kbs_miter_outer_alt",
            default=False
            )

    bmtool_kbs_vmesh_method: StringProperty(
            name="bmtool_kbs_vmesh_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vmesh_method_shift: BoolProperty(
            name="bmtool_kbs_vmesh_method_shift",
            default=False
            )

    bmtool_kbs_vmesh_method_ctl: BoolProperty(
            name="bmtool_kbs_vmesh_method_ctl",
            default=False
            )

    bmtool_kbs_vmesh_method_alt: BoolProperty(
            name="bmtool_kbs_vmesh_method_alt",
            default=False
            )

    bmtool_kbs_affect: StringProperty(
            name="bmtool_kbs_affect",
            maxlen=1,
            default=''
            )

    bmtool_kbs_affect_shift: BoolProperty(
            name="bmtool_kbs_affect_shift",
            default=False
            )

    bmtool_kbs_affect_ctl: BoolProperty(
            name="bmtool_kbs_affect_ctl",
            default=False
            )

    bmtool_kbs_affect_alt: BoolProperty(
            name="bmtool_kbs_affect_alt",
            default=False
            )

    bmtool_kbs_offset_type: StringProperty(
            name="bmtool_kbs_offset_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_offset_type_shift: BoolProperty(
            name="bmtool_kbs_offset_type_shift",
            default=False
            )

    bmtool_kbs_offset_type_ctl: BoolProperty(
            name="bmtool_kbs_offset_type_ctl",
            default=False
            )

    bmtool_kbs_offset_type_alt: BoolProperty(
            name="bmtool_kbs_offset_type_alt",
            default=False
            )

    bmtool_kbs_debug_options: StringProperty(
            name="bmtool_kbs_debug_options",
            maxlen=1,
            default=''
            )

    bmtool_kbs_debug_options_shift: BoolProperty(
            name="bmtool_kbs_debug_options_shift",
            default=False
            )

    bmtool_kbs_debug_options_ctl: BoolProperty(
            name="bmtool_kbs_debug_options_ctl",
            default=False
            )

    bmtool_kbs_debug_options_alt: BoolProperty(
            name="bmtool_kbs_debug_options_alt",
            default=False
            )

    bmtool_kbs_solver: StringProperty(
            name="bmtool_kbs_solver",
            maxlen=1,
            default=''
            )

    bmtool_kbs_solver_shift: BoolProperty(
            name="bmtool_kbs_solver_shift",
            default=False
            )

    bmtool_kbs_solver_ctl: BoolProperty(
            name="bmtool_kbs_solver_ctl",
            default=False
            )

    bmtool_kbs_solver_alt: BoolProperty(
            name="bmtool_kbs_solver_alt",
            default=False
            )

    bmtool_kbs_operation: StringProperty(
            name="bmtool_kbs_operation",
            maxlen=1,
            default=''
            )

    bmtool_kbs_operation_shift: BoolProperty(
            name="bmtool_kbs_operation_shift",
            default=False
            )

    bmtool_kbs_operation_ctl: BoolProperty(
            name="bmtool_kbs_operation_ctl",
            default=False
            )

    bmtool_kbs_operation_alt: BoolProperty(
            name="bmtool_kbs_operation_alt",
            default=False
            )

    bmtool_kbs_operand_type: StringProperty(
            name="bmtool_kbs_operand_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_operand_type_shift: BoolProperty(
            name="bmtool_kbs_operand_type_shift",
            default=False
            )

    bmtool_kbs_operand_type_ctl: BoolProperty(
            name="bmtool_kbs_operand_type_ctl",
            default=False
            )

    bmtool_kbs_operand_type_alt: BoolProperty(
            name="bmtool_kbs_operand_type_alt",
            default=False
            )

    bmtool_kbs_symmetry_axis: StringProperty(
            name="bmtool_kbs_symmetry_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_symmetry_axis_shift: BoolProperty(
            name="bmtool_kbs_symmetry_axis_shift",
            default=False
            )

    bmtool_kbs_symmetry_axis_ctl: BoolProperty(
            name="bmtool_kbs_symmetry_axis_ctl",
            default=False
            )

    bmtool_kbs_symmetry_axis_alt: BoolProperty(
            name="bmtool_kbs_symmetry_axis_alt",
            default=False
            )

    bmtool_kbs_delimit: StringProperty(
            name="bmtool_kbs_delimit",
            maxlen=1,
            default=''
            )

    bmtool_kbs_delimit_shift: BoolProperty(
            name="bmtool_kbs_delimit_shift",
            default=False
            )

    bmtool_kbs_delimit_ctl: BoolProperty(
            name="bmtool_kbs_delimit_ctl",
            default=False
            )

    bmtool_kbs_delimit_alt: BoolProperty(
            name="bmtool_kbs_delimit_alt",
            default=False
            )

    bmtool_kbs_decimate_type: StringProperty(
            name="bmtool_kbs_decimate_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_decimate_type_shift: BoolProperty(
            name="bmtool_kbs_decimate_type_shift",
            default=False
            )

    bmtool_kbs_decimate_type_ctl: BoolProperty(
            name="bmtool_kbs_decimate_type_ctl",
            default=False
            )

    bmtool_kbs_decimate_type_alt: BoolProperty(
            name="bmtool_kbs_decimate_type_alt",
            default=False
            )

    bmtool_kbs_uv_smooth: StringProperty(
            name="bmtool_kbs_uv_smooth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_uv_smooth_shift: BoolProperty(
            name="bmtool_kbs_uv_smooth_shift",
            default=False
            )

    bmtool_kbs_uv_smooth_ctl: BoolProperty(
            name="bmtool_kbs_uv_smooth_ctl",
            default=False
            )

    bmtool_kbs_uv_smooth_alt: BoolProperty(
            name="bmtool_kbs_uv_smooth_alt",
            default=False
            )

    bmtool_kbs_boundary_smooth: StringProperty(
            name="bmtool_kbs_boundary_smooth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_boundary_smooth_shift: BoolProperty(
            name="bmtool_kbs_boundary_smooth_shift",
            default=False
            )

    bmtool_kbs_boundary_smooth_ctl: BoolProperty(
            name="bmtool_kbs_boundary_smooth_ctl",
            default=False
            )

    bmtool_kbs_boundary_smooth_alt: BoolProperty(
            name="bmtool_kbs_boundary_smooth_alt",
            default=False
            )

    bmtool_kbs_axis: StringProperty(
            name="bmtool_kbs_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_axis_shift: BoolProperty(
            name="bmtool_kbs_axis_shift",
            default=False
            )

    bmtool_kbs_axis_ctl: BoolProperty(
            name="bmtool_kbs_axis_ctl",
            default=False
            )

    bmtool_kbs_axis_alt: BoolProperty(
            name="bmtool_kbs_axis_alt",
            default=False
            )

    bmtool_kbs_nonmanifold_thickness_mode: StringProperty(
            name="bmtool_kbs_nonmanifold_thickness_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_nonmanifold_thickness_mode_shift: BoolProperty(
            name="bmtool_kbs_nonmanifold_thickness_mode_shift",
            default=False
            )

    bmtool_kbs_nonmanifold_thickness_mode_ctl: BoolProperty(
            name="bmtool_kbs_nonmanifold_thickness_mode_ctl",
            default=False
            )

    bmtool_kbs_nonmanifold_thickness_mode_alt: BoolProperty(
            name="bmtool_kbs_nonmanifold_thickness_mode_alt",
            default=False
            )

    bmtool_kbs_solidify_mode: StringProperty(
            name="bmtool_kbs_solidify_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_solidify_mode_shift: BoolProperty(
            name="bmtool_kbs_solidify_mode_shift",
            default=False
            )

    bmtool_kbs_solidify_mode_ctl: BoolProperty(
            name="bmtool_kbs_solidify_mode_ctl",
            default=False
            )

    bmtool_kbs_solidify_mode_alt: BoolProperty(
            name="bmtool_kbs_solidify_mode_alt",
            default=False
            )

    bmtool_kbs_nonmanifold_boundary_mode: StringProperty(
            name="bmtool_kbs_nonmanifold_boundary_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_nonmanifold_boundary_mode_shift: BoolProperty(
            name="bmtool_kbs_nonmanifold_boundary_mode_shift",
            default=False
            )

    bmtool_kbs_nonmanifold_boundary_mode_ctl: BoolProperty(
            name="bmtool_kbs_nonmanifold_boundary_mode_ctl",
            default=False
            )

    bmtool_kbs_nonmanifold_boundary_mode_alt: BoolProperty(
            name="bmtool_kbs_nonmanifold_boundary_mode_alt",
            default=False
            )

    bmtool_kbs_subdivision_type: StringProperty(
            name="bmtool_kbs_subdivision_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_subdivision_type_shift: BoolProperty(
            name="bmtool_kbs_subdivision_type_shift",
            default=False
            )

    bmtool_kbs_subdivision_type_ctl: BoolProperty(
            name="bmtool_kbs_subdivision_type_ctl",
            default=False
            )

    bmtool_kbs_subdivision_type_alt: BoolProperty(
            name="bmtool_kbs_subdivision_type_alt",
            default=False
            )

    bmtool_kbs_ngon_method: StringProperty(
            name="bmtool_kbs_ngon_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_ngon_method_shift: BoolProperty(
            name="bmtool_kbs_ngon_method_shift",
            default=False
            )

    bmtool_kbs_ngon_method_ctl: BoolProperty(
            name="bmtool_kbs_ngon_method_ctl",
            default=False
            )

    bmtool_kbs_ngon_method_alt: BoolProperty(
            name="bmtool_kbs_ngon_method_alt",
            default=False
            )

    bmtool_kbs_quad_method: StringProperty(
            name="bmtool_kbs_quad_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_quad_method_shift: BoolProperty(
            name="bmtool_kbs_quad_method_shift",
            default=False
            )

    bmtool_kbs_quad_method_ctl: BoolProperty(
            name="bmtool_kbs_quad_method_ctl",
            default=False
            )

    bmtool_kbs_quad_method_alt: BoolProperty(
            name="bmtool_kbs_quad_method_alt",
            default=False
            )

    bmtool_kbs_resolution_mode: StringProperty(
            name="bmtool_kbs_resolution_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_resolution_mode_shift: BoolProperty(
            name="bmtool_kbs_resolution_mode_shift",
            default=False
            )

    bmtool_kbs_resolution_mode_ctl: BoolProperty(
            name="bmtool_kbs_resolution_mode_ctl",
            default=False
            )

    bmtool_kbs_resolution_mode_alt: BoolProperty(
            name="bmtool_kbs_resolution_mode_alt",
            default=False
            )

    bmtool_kbs_cast_type: StringProperty(
            name="bmtool_kbs_cast_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_cast_type_shift: BoolProperty(
            name="bmtool_kbs_cast_type_shift",
            default=False
            )

    bmtool_kbs_cast_type_ctl: BoolProperty(
            name="bmtool_kbs_cast_type_ctl",
            default=False
            )

    bmtool_kbs_cast_type_alt: BoolProperty(
            name="bmtool_kbs_cast_type_alt",
            default=False
            )

    bmtool_kbs_deform_axis: StringProperty(
            name="bmtool_kbs_deform_axis",
            maxlen=1,
            default=''
            )

    bmtool_kbs_deform_axis_shift: BoolProperty(
            name="bmtool_kbs_deform_axis_shift",
            default=False
            )

    bmtool_kbs_deform_axis_ctl: BoolProperty(
            name="bmtool_kbs_deform_axis_ctl",
            default=False
            )

    bmtool_kbs_deform_axis_alt: BoolProperty(
            name="bmtool_kbs_deform_axis_alt",
            default=False
            )

    bmtool_kbs_space: StringProperty(
            name="bmtool_kbs_space",
            maxlen=1,
            default=''
            )

    bmtool_kbs_space_shift: BoolProperty(
            name="bmtool_kbs_space_shift",
            default=False
            )

    bmtool_kbs_space_ctl: BoolProperty(
            name="bmtool_kbs_space_ctl",
            default=False
            )

    bmtool_kbs_space_alt: BoolProperty(
            name="bmtool_kbs_space_alt",
            default=False
            )

    bmtool_kbs_direction: StringProperty(
            name="bmtool_kbs_direction",
            maxlen=1,
            default=''
            )

    bmtool_kbs_direction_shift: BoolProperty(
            name="bmtool_kbs_direction_shift",
            default=False
            )

    bmtool_kbs_direction_ctl: BoolProperty(
            name="bmtool_kbs_direction_ctl",
            default=False
            )

    bmtool_kbs_direction_alt: BoolProperty(
            name="bmtool_kbs_direction_alt",
            default=False
            )

    bmtool_kbs_texture_coords: StringProperty(
            name="bmtool_kbs_texture_coords",
            maxlen=1,
            default=''
            )

    bmtool_kbs_texture_coords_shift: BoolProperty(
            name="bmtool_kbs_texture_coords_shift",
            default=False
            )

    bmtool_kbs_texture_coords_ctl: BoolProperty(
            name="bmtool_kbs_texture_coords_ctl",
            default=False
            )

    bmtool_kbs_texture_coords_alt: BoolProperty(
            name="bmtool_kbs_texture_coords_alt",
            default=False
            )

    bmtool_kbs_wrap_method: StringProperty(
            name="bmtool_kbs_wrap_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wrap_method_shift: BoolProperty(
            name="bmtool_kbs_wrap_method_shift",
            default=False
            )

    bmtool_kbs_wrap_method_ctl: BoolProperty(
            name="bmtool_kbs_wrap_method_ctl",
            default=False
            )

    bmtool_kbs_wrap_method_alt: BoolProperty(
            name="bmtool_kbs_wrap_method_alt",
            default=False
            )

    bmtool_kbs_wrap_mode: StringProperty(
            name="bmtool_kbs_wrap_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wrap_mode_shift: BoolProperty(
            name="bmtool_kbs_wrap_mode_shift",
            default=False
            )

    bmtool_kbs_wrap_mode_ctl: BoolProperty(
            name="bmtool_kbs_wrap_mode_ctl",
            default=False
            )

    bmtool_kbs_wrap_mode_alt: BoolProperty(
            name="bmtool_kbs_wrap_mode_alt",
            default=False
            )

    bmtool_kbs_cull_face: StringProperty(
            name="bmtool_kbs_cull_face",
            maxlen=1,
            default=''
            )

    bmtool_kbs_cull_face_shift: BoolProperty(
            name="bmtool_kbs_cull_face_shift",
            default=False
            )

    bmtool_kbs_cull_face_ctl: BoolProperty(
            name="bmtool_kbs_cull_face_ctl",
            default=False
            )

    bmtool_kbs_cull_face_alt: BoolProperty(
            name="bmtool_kbs_cull_face_alt",
            default=False
            )

    bmtool_kbs_deform_method: StringProperty(
            name="bmtool_kbs_deform_method",
            maxlen=1,
            default=''
            )

    bmtool_kbs_deform_method_shift: BoolProperty(
            name="bmtool_kbs_deform_method_shift",
            default=False
            )

    bmtool_kbs_deform_method_ctl: BoolProperty(
            name="bmtool_kbs_deform_method_ctl",
            default=False
            )

    bmtool_kbs_deform_method_alt: BoolProperty(
            name="bmtool_kbs_deform_method_alt",
            default=False
            )

    bmtool_kbs_smooth_type: StringProperty(
            name="bmtool_kbs_smooth_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_smooth_type_shift: BoolProperty(
            name="bmtool_kbs_smooth_type_shift",
            default=False
            )

    bmtool_kbs_smooth_type_ctl: BoolProperty(
            name="bmtool_kbs_smooth_type_ctl",
            default=False
            )

    bmtool_kbs_smooth_type_alt: BoolProperty(
            name="bmtool_kbs_smooth_type_alt",
            default=False
            )

    bmtool_kbs_rest_source: StringProperty(
            name="bmtool_kbs_rest_source",
            maxlen=1,
            default=''
            )

    bmtool_kbs_rest_source_shift: BoolProperty(
            name="bmtool_kbs_rest_source_shift",
            default=False
            )

    bmtool_kbs_rest_source_ctl: BoolProperty(
            name="bmtool_kbs_rest_source_ctl",
            default=False
            )

    bmtool_kbs_rest_source_alt: BoolProperty(
            name="bmtool_kbs_rest_source_alt",
            default=False
            )

    bmtool_kbs_ui_type: StringProperty(
            name="bmtool_kbs_ui_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_ui_type_shift: BoolProperty(
            name="bmtool_kbs_ui_type_shift",
            default=False
            )

    bmtool_kbs_ui_type_ctl: BoolProperty(
            name="bmtool_kbs_ui_type_ctl",
            default=False
            )

    bmtool_kbs_ui_type_alt: BoolProperty(
            name="bmtool_kbs_ui_type_alt",
            default=False
            )

    bmtool_kbs_fluid_type: StringProperty(
            name="bmtool_kbs_fluid_type",
            maxlen=1,
            default=''
            )

    bmtool_kbs_fluid_type_shift: BoolProperty(
            name="bmtool_kbs_fluid_type_shift",
            default=False
            )

    bmtool_kbs_fluid_type_ctl: BoolProperty(
            name="bmtool_kbs_fluid_type_ctl",
            default=False
            )

    bmtool_kbs_fluid_type_alt: BoolProperty(
            name="bmtool_kbs_fluid_type_alt",
            default=False
            )

    bmtool_kbs_spectrum: StringProperty(
            name="bmtool_kbs_spectrum",
            maxlen=1,
            default=''
            )

    bmtool_kbs_spectrum_shift: BoolProperty(
            name="bmtool_kbs_spectrum_shift",
            default=False
            )

    bmtool_kbs_spectrum_ctl: BoolProperty(
            name="bmtool_kbs_spectrum_ctl",
            default=False
            )

    bmtool_kbs_spectrum_alt: BoolProperty(
            name="bmtool_kbs_spectrum_alt",
            default=False
            )

    bmtool_kbs_geometry_mode: StringProperty(
            name="bmtool_kbs_geometry_mode",
            maxlen=1,
            default=''
            )

    bmtool_kbs_geometry_mode_shift: BoolProperty(
            name="bmtool_kbs_geometry_mode_shift",
            default=False
            )

    bmtool_kbs_geometry_mode_ctl: BoolProperty(
            name="bmtool_kbs_geometry_mode_ctl",
            default=False
            )

    bmtool_kbs_geometry_mode_alt: BoolProperty(
            name="bmtool_kbs_geometry_mode_alt",
            default=False
            )

    bmtool_kbs_ray_radius: StringProperty(
            name="bmtool_kbs_ray_radius",
            maxlen=1,
            default=''
            )

    bmtool_kbs_ray_radius_shift: BoolProperty(
            name="bmtool_kbs_ray_radius_shift",
            default=False
            )

    bmtool_kbs_ray_radius_ctl: BoolProperty(
            name="bmtool_kbs_ray_radius_ctl",
            default=False
            )

    bmtool_kbs_ray_radius_alt: BoolProperty(
            name="bmtool_kbs_ray_radius_alt",
            default=False
            )

    bmtool_kbs_mix_factor: StringProperty(
            name="bmtool_kbs_mix_factor",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mix_factor_shift: BoolProperty(
            name="bmtool_kbs_mix_factor_shift",
            default=False
            )

    bmtool_kbs_mix_factor_ctl: BoolProperty(
            name="bmtool_kbs_mix_factor_ctl",
            default=False
            )

    bmtool_kbs_mix_factor_alt: BoolProperty(
            name="bmtool_kbs_mix_factor_alt",
            default=False
            )

    bmtool_kbs_islands_precision: StringProperty(
            name="bmtool_kbs_islands_precision",
            maxlen=1,
            default=''
            )

    bmtool_kbs_islands_precision_shift: BoolProperty(
            name="bmtool_kbs_islands_precision_shift",
            default=False
            )

    bmtool_kbs_islands_precision_ctl: BoolProperty(
            name="bmtool_kbs_islands_precision_ctl",
            default=False
            )

    bmtool_kbs_islands_precision_alt: BoolProperty(
            name="bmtool_kbs_islands_precision_alt",
            default=False
            )

    bmtool_kbs_max_distance: StringProperty(
            name="bmtool_kbs_max_distance",
            maxlen=1,
            default=''
            )

    bmtool_kbs_max_distance_shift: BoolProperty(
            name="bmtool_kbs_max_distance_shift",
            default=False
            )

    bmtool_kbs_max_distance_ctl: BoolProperty(
            name="bmtool_kbs_max_distance_ctl",
            default=False
            )

    bmtool_kbs_max_distance_alt: BoolProperty(
            name="bmtool_kbs_max_distance_alt",
            default=False
            )

    bmtool_kbs_frame_scale: StringProperty(
            name="bmtool_kbs_frame_scale",
            maxlen=1,
            default=''
            )

    bmtool_kbs_frame_scale_shift: BoolProperty(
            name="bmtool_kbs_frame_scale_shift",
            default=False
            )

    bmtool_kbs_frame_scale_ctl: BoolProperty(
            name="bmtool_kbs_frame_scale_ctl",
            default=False
            )

    bmtool_kbs_frame_scale_alt: BoolProperty(
            name="bmtool_kbs_frame_scale_alt",
            default=False
            )

    bmtool_kbs_eval_frame: StringProperty(
            name="bmtool_kbs_eval_frame",
            maxlen=1,
            default=''
            )

    bmtool_kbs_eval_frame_shift: BoolProperty(
            name="bmtool_kbs_eval_frame_shift",
            default=False
            )

    bmtool_kbs_eval_frame_ctl: BoolProperty(
            name="bmtool_kbs_eval_frame_ctl",
            default=False
            )

    bmtool_kbs_eval_frame_alt: BoolProperty(
            name="bmtool_kbs_eval_frame_alt",
            default=False
            )

    bmtool_kbs_eval_time: StringProperty(
            name="bmtool_kbs_eval_time",
            maxlen=1,
            default=''
            )

    bmtool_kbs_eval_time_shift: BoolProperty(
            name="bmtool_kbs_eval_time_shift",
            default=False
            )

    bmtool_kbs_eval_time_ctl: BoolProperty(
            name="bmtool_kbs_eval_time_ctl",
            default=False
            )

    bmtool_kbs_eval_time_alt: BoolProperty(
            name="bmtool_kbs_eval_time_alt",
            default=False
            )

    bmtool_kbs_frame_start: StringProperty(
            name="bmtool_kbs_frame_start",
            maxlen=1,
            default=''
            )

    bmtool_kbs_frame_start_shift: BoolProperty(
            name="bmtool_kbs_frame_start_shift",
            default=False
            )

    bmtool_kbs_frame_start_ctl: BoolProperty(
            name="bmtool_kbs_frame_start_ctl",
            default=False
            )

    bmtool_kbs_frame_start_alt: BoolProperty(
            name="bmtool_kbs_frame_start_alt",
            default=False
            )

    bmtool_kbs_eval_factor: StringProperty(
            name="bmtool_kbs_eval_factor",
            maxlen=1,
            default=''
            )

    bmtool_kbs_eval_factor_shift: BoolProperty(
            name="bmtool_kbs_eval_factor_shift",
            default=False
            )

    bmtool_kbs_eval_factor_ctl: BoolProperty(
            name="bmtool_kbs_eval_factor_ctl",
            default=False
            )

    bmtool_kbs_eval_factor_alt: BoolProperty(
            name="bmtool_kbs_eval_factor_alt",
            default=False
            )

    bmtool_kbs_factor: StringProperty(
            name="bmtool_kbs_factor",
            maxlen=1,
            default=''
            )

    bmtool_kbs_factor_shift: BoolProperty(
            name="bmtool_kbs_factor_shift",
            default=False
            )

    bmtool_kbs_factor_ctl: BoolProperty(
            name="bmtool_kbs_factor_ctl",
            default=False
            )

    bmtool_kbs_factor_alt: BoolProperty(
            name="bmtool_kbs_factor_alt",
            default=False
            )

    bmtool_kbs_velocity_scale: StringProperty(
            name="bmtool_kbs_velocity_scale",
            maxlen=1,
            default=''
            )

    bmtool_kbs_velocity_scale_shift: BoolProperty(
            name="bmtool_kbs_velocity_scale_shift",
            default=False
            )

    bmtool_kbs_velocity_scale_ctl: BoolProperty(
            name="bmtool_kbs_velocity_scale_ctl",
            default=False
            )

    bmtool_kbs_velocity_scale_alt: BoolProperty(
            name="bmtool_kbs_velocity_scale_alt",
            default=False
            )

    bmtool_kbs_mix_limit: StringProperty(
            name="bmtool_kbs_mix_limit",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mix_limit_shift: BoolProperty(
            name="bmtool_kbs_mix_limit_shift",
            default=False
            )

    bmtool_kbs_mix_limit_ctl: BoolProperty(
            name="bmtool_kbs_mix_limit_ctl",
            default=False
            )

    bmtool_kbs_mix_limit_alt: BoolProperty(
            name="bmtool_kbs_mix_limit_alt",
            default=False
            )

    bmtool_kbs_offset: StringProperty(
            name="bmtool_kbs_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_offset_shift: BoolProperty(
            name="bmtool_kbs_offset_shift",
            default=False
            )

    bmtool_kbs_offset_ctl: BoolProperty(
            name="bmtool_kbs_offset_ctl",
            default=False
            )

    bmtool_kbs_offset_alt: BoolProperty(
            name="bmtool_kbs_offset_alt",
            default=False
            )

    bmtool_kbs_thresh: StringProperty(
            name="bmtool_kbs_thresh",
            maxlen=1,
            default=''
            )

    bmtool_kbs_thresh_shift: BoolProperty(
            name="bmtool_kbs_thresh_shift",
            default=False
            )

    bmtool_kbs_thresh_ctl: BoolProperty(
            name="bmtool_kbs_thresh_ctl",
            default=False
            )

    bmtool_kbs_thresh_alt: BoolProperty(
            name="bmtool_kbs_thresh_alt",
            default=False
            )

    bmtool_kbs_aspect_y: StringProperty(
            name="bmtool_kbs_aspect_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_aspect_y_shift: BoolProperty(
            name="bmtool_kbs_aspect_y_shift",
            default=False
            )

    bmtool_kbs_aspect_y_ctl: BoolProperty(
            name="bmtool_kbs_aspect_y_ctl",
            default=False
            )

    bmtool_kbs_aspect_y_alt: BoolProperty(
            name="bmtool_kbs_aspect_y_alt",
            default=False
            )

    bmtool_kbs_aspect_x: StringProperty(
            name="bmtool_kbs_aspect_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_aspect_x_shift: BoolProperty(
            name="bmtool_kbs_aspect_x_shift",
            default=False
            )

    bmtool_kbs_aspect_x_ctl: BoolProperty(
            name="bmtool_kbs_aspect_x_ctl",
            default=False
            )

    bmtool_kbs_aspect_x_alt: BoolProperty(
            name="bmtool_kbs_aspect_x_alt",
            default=False
            )

    bmtool_kbs_scale_y: StringProperty(
            name="bmtool_kbs_scale_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_scale_y_shift: BoolProperty(
            name="bmtool_kbs_scale_y_shift",
            default=False
            )

    bmtool_kbs_scale_y_ctl: BoolProperty(
            name="bmtool_kbs_scale_y_ctl",
            default=False
            )

    bmtool_kbs_scale_y_alt: BoolProperty(
            name="bmtool_kbs_scale_y_alt",
            default=False
            )

    bmtool_kbs_scale_x: StringProperty(
            name="bmtool_kbs_scale_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_scale_x_shift: BoolProperty(
            name="bmtool_kbs_scale_x_shift",
            default=False
            )

    bmtool_kbs_scale_x_ctl: BoolProperty(
            name="bmtool_kbs_scale_x_ctl",
            default=False
            )

    bmtool_kbs_scale_x_alt: BoolProperty(
            name="bmtool_kbs_scale_x_alt",
            default=False
            )

    bmtool_kbs_rotation: StringProperty(
            name="bmtool_kbs_rotation",
            maxlen=1,
            default=''
            )

    bmtool_kbs_rotation_shift: BoolProperty(
            name="bmtool_kbs_rotation_shift",
            default=False
            )

    bmtool_kbs_rotation_ctl: BoolProperty(
            name="bmtool_kbs_rotation_ctl",
            default=False
            )

    bmtool_kbs_rotation_alt: BoolProperty(
            name="bmtool_kbs_rotation_alt",
            default=False
            )

    bmtool_kbs_center: StringProperty(
            name="bmtool_kbs_center",
            maxlen=1,
            default=''
            )

    bmtool_kbs_center_shift: BoolProperty(
            name="bmtool_kbs_center_shift",
            default=False
            )

    bmtool_kbs_center_ctl: BoolProperty(
            name="bmtool_kbs_center_ctl",
            default=False
            )

    bmtool_kbs_center_alt: BoolProperty(
            name="bmtool_kbs_center_alt",
            default=False
            )

    bmtool_kbs_scale: StringProperty(
            name="bmtool_kbs_scale",
            maxlen=1,
            default=''
            )

    bmtool_kbs_scale_shift: BoolProperty(
            name="bmtool_kbs_scale_shift",
            default=False
            )

    bmtool_kbs_scale_ctl: BoolProperty(
            name="bmtool_kbs_scale_ctl",
            default=False
            )

    bmtool_kbs_scale_alt: BoolProperty(
            name="bmtool_kbs_scale_alt",
            default=False
            )

    bmtool_kbs_mask_constant: StringProperty(
            name="bmtool_kbs_mask_constant",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mask_constant_shift: BoolProperty(
            name="bmtool_kbs_mask_constant_shift",
            default=False
            )

    bmtool_kbs_mask_constant_ctl: BoolProperty(
            name="bmtool_kbs_mask_constant_ctl",
            default=False
            )

    bmtool_kbs_mask_constant_alt: BoolProperty(
            name="bmtool_kbs_mask_constant_alt",
            default=False
            )

    bmtool_kbs_add_threshold: StringProperty(
            name="bmtool_kbs_add_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_add_threshold_shift: BoolProperty(
            name="bmtool_kbs_add_threshold_shift",
            default=False
            )

    bmtool_kbs_add_threshold_ctl: BoolProperty(
            name="bmtool_kbs_add_threshold_ctl",
            default=False
            )

    bmtool_kbs_add_threshold_alt: BoolProperty(
            name="bmtool_kbs_add_threshold_alt",
            default=False
            )

    bmtool_kbs_default_weight: StringProperty(
            name="bmtool_kbs_default_weight",
            maxlen=1,
            default=''
            )

    bmtool_kbs_default_weight_shift: BoolProperty(
            name="bmtool_kbs_default_weight_shift",
            default=False
            )

    bmtool_kbs_default_weight_ctl: BoolProperty(
            name="bmtool_kbs_default_weight_ctl",
            default=False
            )

    bmtool_kbs_default_weight_alt: BoolProperty(
            name="bmtool_kbs_default_weight_alt",
            default=False
            )

    bmtool_kbs_remove_threshold: StringProperty(
            name="bmtool_kbs_remove_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_remove_threshold_shift: BoolProperty(
            name="bmtool_kbs_remove_threshold_shift",
            default=False
            )

    bmtool_kbs_remove_threshold_ctl: BoolProperty(
            name="bmtool_kbs_remove_threshold_ctl",
            default=False
            )

    bmtool_kbs_remove_threshold_alt: BoolProperty(
            name="bmtool_kbs_remove_threshold_alt",
            default=False
            )

    bmtool_kbs_default_weight_a: StringProperty(
            name="bmtool_kbs_default_weight_a",
            maxlen=1,
            default=''
            )

    bmtool_kbs_default_weight_a_shift: BoolProperty(
            name="bmtool_kbs_default_weight_a_shift",
            default=False
            )

    bmtool_kbs_default_weight_a_ctl: BoolProperty(
            name="bmtool_kbs_default_weight_a_ctl",
            default=False
            )

    bmtool_kbs_default_weight_a_alt: BoolProperty(
            name="bmtool_kbs_default_weight_a_alt",
            default=False
            )

    bmtool_kbs_default_weight_b: StringProperty(
            name="bmtool_kbs_default_weight_b",
            maxlen=1,
            default=''
            )

    bmtool_kbs_default_weight_b_shift: BoolProperty(
            name="bmtool_kbs_default_weight_b_shift",
            default=False
            )

    bmtool_kbs_default_weight_b_ctl: BoolProperty(
            name="bmtool_kbs_default_weight_b_ctl",
            default=False
            )

    bmtool_kbs_default_weight_b_alt: BoolProperty(
            name="bmtool_kbs_default_weight_b_alt",
            default=False
            )

    bmtool_kbs_max_dist: StringProperty(
            name="bmtool_kbs_max_dist",
            maxlen=1,
            default=''
            )

    bmtool_kbs_max_dist_shift: BoolProperty(
            name="bmtool_kbs_max_dist_shift",
            default=False
            )

    bmtool_kbs_max_dist_ctl: BoolProperty(
            name="bmtool_kbs_max_dist_ctl",
            default=False
            )

    bmtool_kbs_max_dist_alt: BoolProperty(
            name="bmtool_kbs_max_dist_alt",
            default=False
            )

    bmtool_kbs_min_dist: StringProperty(
            name="bmtool_kbs_min_dist",
            maxlen=1,
            default=''
            )

    bmtool_kbs_min_dist_shift: BoolProperty(
            name="bmtool_kbs_min_dist_shift",
            default=False
            )

    bmtool_kbs_min_dist_ctl: BoolProperty(
            name="bmtool_kbs_min_dist_ctl",
            default=False
            )

    bmtool_kbs_min_dist_alt: BoolProperty(
            name="bmtool_kbs_min_dist_alt",
            default=False
            )

    bmtool_kbs_relative_offset_displace: StringProperty(
            name="bmtool_kbs_relative_offset_displace",
            maxlen=1,
            default=''
            )

    bmtool_kbs_relative_offset_displace_shift: BoolProperty(
            name="bmtool_kbs_relative_offset_displace_shift",
            default=False
            )

    bmtool_kbs_relative_offset_displace_ctl: BoolProperty(
            name="bmtool_kbs_relative_offset_displace_ctl",
            default=False
            )

    bmtool_kbs_relative_offset_displace_alt: BoolProperty(
            name="bmtool_kbs_relative_offset_displace_alt",
            default=False
            )

    bmtool_kbs_constant_offset_displace: StringProperty(
            name="bmtool_kbs_constant_offset_displace",
            maxlen=1,
            default=''
            )

    bmtool_kbs_constant_offset_displace_shift: BoolProperty(
            name="bmtool_kbs_constant_offset_displace_shift",
            default=False
            )

    bmtool_kbs_constant_offset_displace_ctl: BoolProperty(
            name="bmtool_kbs_constant_offset_displace_ctl",
            default=False
            )

    bmtool_kbs_constant_offset_displace_alt: BoolProperty(
            name="bmtool_kbs_constant_offset_displace_alt",
            default=False
            )

    bmtool_kbs_fit_length: StringProperty(
            name="bmtool_kbs_fit_length",
            maxlen=1,
            default=''
            )

    bmtool_kbs_fit_length_shift: BoolProperty(
            name="bmtool_kbs_fit_length_shift",
            default=False
            )

    bmtool_kbs_fit_length_ctl: BoolProperty(
            name="bmtool_kbs_fit_length_ctl",
            default=False
            )

    bmtool_kbs_fit_length_alt: BoolProperty(
            name="bmtool_kbs_fit_length_alt",
            default=False
            )

    bmtool_kbs_merge_threshold: StringProperty(
            name="bmtool_kbs_merge_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_merge_threshold_shift: BoolProperty(
            name="bmtool_kbs_merge_threshold_shift",
            default=False
            )

    bmtool_kbs_merge_threshold_ctl: BoolProperty(
            name="bmtool_kbs_merge_threshold_ctl",
            default=False
            )

    bmtool_kbs_merge_threshold_alt: BoolProperty(
            name="bmtool_kbs_merge_threshold_alt",
            default=False
            )

    bmtool_kbs_offset_v: StringProperty(
            name="bmtool_kbs_offset_v",
            maxlen=1,
            default=''
            )

    bmtool_kbs_offset_v_shift: BoolProperty(
            name="bmtool_kbs_offset_v_shift",
            default=False
            )

    bmtool_kbs_offset_v_ctl: BoolProperty(
            name="bmtool_kbs_offset_v_ctl",
            default=False
            )

    bmtool_kbs_offset_v_alt: BoolProperty(
            name="bmtool_kbs_offset_v_alt",
            default=False
            )

    bmtool_kbs_offset_u: StringProperty(
            name="bmtool_kbs_offset_u",
            maxlen=1,
            default=''
            )

    bmtool_kbs_offset_u_shift: BoolProperty(
            name="bmtool_kbs_offset_u_shift",
            default=False
            )

    bmtool_kbs_offset_u_ctl: BoolProperty(
            name="bmtool_kbs_offset_u_ctl",
            default=False
            )

    bmtool_kbs_offset_u_alt: BoolProperty(
            name="bmtool_kbs_offset_u_alt",
            default=False
            )

    bmtool_kbs_angle_limit: StringProperty(
            name="bmtool_kbs_angle_limit",
            maxlen=1,
            default=''
            )

    bmtool_kbs_angle_limit_shift: BoolProperty(
            name="bmtool_kbs_angle_limit_shift",
            default=False
            )

    bmtool_kbs_angle_limit_ctl: BoolProperty(
            name="bmtool_kbs_angle_limit_ctl",
            default=False
            )

    bmtool_kbs_angle_limit_alt: BoolProperty(
            name="bmtool_kbs_angle_limit_alt",
            default=False
            )

    bmtool_kbs_spread: StringProperty(
            name="bmtool_kbs_spread",
            maxlen=1,
            default=''
            )

    bmtool_kbs_spread_shift: BoolProperty(
            name="bmtool_kbs_spread_shift",
            default=False
            )

    bmtool_kbs_spread_ctl: BoolProperty(
            name="bmtool_kbs_spread_ctl",
            default=False
            )

    bmtool_kbs_spread_alt: BoolProperty(
            name="bmtool_kbs_spread_alt",
            default=False
            )

    bmtool_kbs_width: StringProperty(
            name="bmtool_kbs_width",
            maxlen=1,
            default=''
            )

    bmtool_kbs_width_shift: BoolProperty(
            name="bmtool_kbs_width_shift",
            default=False
            )

    bmtool_kbs_width_ctl: BoolProperty(
            name="bmtool_kbs_width_ctl",
            default=False
            )

    bmtool_kbs_width_alt: BoolProperty(
            name="bmtool_kbs_width_alt",
            default=False
            )

    bmtool_kbs_width_pct: StringProperty(
            name="bmtool_kbs_width_pct",
            maxlen=1,
            default=''
            )

    bmtool_kbs_width_pct_shift: BoolProperty(
            name="bmtool_kbs_width_pct_shift",
            default=False
            )

    bmtool_kbs_width_pct_ctl: BoolProperty(
            name="bmtool_kbs_width_pct_ctl",
            default=False
            )

    bmtool_kbs_width_pct_alt: BoolProperty(
            name="bmtool_kbs_width_pct_alt",
            default=False
            )

    bmtool_kbs_profile: StringProperty(
            name="bmtool_kbs_profile",
            maxlen=1,
            default=''
            )

    bmtool_kbs_profile_shift: BoolProperty(
            name="bmtool_kbs_profile_shift",
            default=False
            )

    bmtool_kbs_profile_ctl: BoolProperty(
            name="bmtool_kbs_profile_ctl",
            default=False
            )

    bmtool_kbs_profile_alt: BoolProperty(
            name="bmtool_kbs_profile_alt",
            default=False
            )

    bmtool_kbs_double_threshold: StringProperty(
            name="bmtool_kbs_double_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_double_threshold_shift: BoolProperty(
            name="bmtool_kbs_double_threshold_shift",
            default=False
            )

    bmtool_kbs_double_threshold_ctl: BoolProperty(
            name="bmtool_kbs_double_threshold_ctl",
            default=False
            )

    bmtool_kbs_double_threshold_alt: BoolProperty(
            name="bmtool_kbs_double_threshold_alt",
            default=False
            )

    bmtool_kbs_frame_duration: StringProperty(
            name="bmtool_kbs_frame_duration",
            maxlen=1,
            default=''
            )

    bmtool_kbs_frame_duration_shift: BoolProperty(
            name="bmtool_kbs_frame_duration_shift",
            default=False
            )

    bmtool_kbs_frame_duration_ctl: BoolProperty(
            name="bmtool_kbs_frame_duration_ctl",
            default=False
            )

    bmtool_kbs_frame_duration_alt: BoolProperty(
            name="bmtool_kbs_frame_duration_alt",
            default=False
            )

    bmtool_kbs_vertex_group_factor: StringProperty(
            name="bmtool_kbs_vertex_group_factor",
            maxlen=1,
            default=''
            )

    bmtool_kbs_vertex_group_factor_shift: BoolProperty(
            name="bmtool_kbs_vertex_group_factor_shift",
            default=False
            )

    bmtool_kbs_vertex_group_factor_ctl: BoolProperty(
            name="bmtool_kbs_vertex_group_factor_ctl",
            default=False
            )

    bmtool_kbs_vertex_group_factor_alt: BoolProperty(
            name="bmtool_kbs_vertex_group_factor_alt",
            default=False
            )

    bmtool_kbs_ratio: StringProperty(
            name="bmtool_kbs_ratio",
            maxlen=1,
            default=''
            )

    bmtool_kbs_ratio_shift: BoolProperty(
            name="bmtool_kbs_ratio_shift",
            default=False
            )

    bmtool_kbs_ratio_ctl: BoolProperty(
            name="bmtool_kbs_ratio_ctl",
            default=False
            )

    bmtool_kbs_ratio_alt: BoolProperty(
            name="bmtool_kbs_ratio_alt",
            default=False
            )

    bmtool_kbs_split_angle: StringProperty(
            name="bmtool_kbs_split_angle",
            maxlen=1,
            default=''
            )

    bmtool_kbs_split_angle_shift: BoolProperty(
            name="bmtool_kbs_split_angle_shift",
            default=False
            )

    bmtool_kbs_split_angle_ctl: BoolProperty(
            name="bmtool_kbs_split_angle_ctl",
            default=False
            )

    bmtool_kbs_split_angle_alt: BoolProperty(
            name="bmtool_kbs_split_angle_alt",
            default=False
            )

    bmtool_kbs_threshold: StringProperty(
            name="bmtool_kbs_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_threshold_shift: BoolProperty(
            name="bmtool_kbs_threshold_shift",
            default=False
            )

    bmtool_kbs_threshold_ctl: BoolProperty(
            name="bmtool_kbs_threshold_ctl",
            default=False
            )

    bmtool_kbs_threshold_alt: BoolProperty(
            name="bmtool_kbs_threshold_alt",
            default=False
            )

    bmtool_kbs_mirror_offset_v: StringProperty(
            name="bmtool_kbs_mirror_offset_v",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mirror_offset_v_shift: BoolProperty(
            name="bmtool_kbs_mirror_offset_v_shift",
            default=False
            )

    bmtool_kbs_mirror_offset_v_ctl: BoolProperty(
            name="bmtool_kbs_mirror_offset_v_ctl",
            default=False
            )

    bmtool_kbs_mirror_offset_v_alt: BoolProperty(
            name="bmtool_kbs_mirror_offset_v_alt",
            default=False
            )

    bmtool_kbs_bisect_threshold: StringProperty(
            name="bmtool_kbs_bisect_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_bisect_threshold_shift: BoolProperty(
            name="bmtool_kbs_bisect_threshold_shift",
            default=False
            )

    bmtool_kbs_bisect_threshold_ctl: BoolProperty(
            name="bmtool_kbs_bisect_threshold_ctl",
            default=False
            )

    bmtool_kbs_bisect_threshold_alt: BoolProperty(
            name="bmtool_kbs_bisect_threshold_alt",
            default=False
            )

    bmtool_kbs_mirror_offset_u: StringProperty(
            name="bmtool_kbs_mirror_offset_u",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mirror_offset_u_shift: BoolProperty(
            name="bmtool_kbs_mirror_offset_u_shift",
            default=False
            )

    bmtool_kbs_mirror_offset_u_ctl: BoolProperty(
            name="bmtool_kbs_mirror_offset_u_ctl",
            default=False
            )

    bmtool_kbs_mirror_offset_u_alt: BoolProperty(
            name="bmtool_kbs_mirror_offset_u_alt",
            default=False
            )

    bmtool_kbs_sharpness: StringProperty(
            name="bmtool_kbs_sharpness",
            maxlen=1,
            default=''
            )

    bmtool_kbs_sharpness_shift: BoolProperty(
            name="bmtool_kbs_sharpness_shift",
            default=False
            )

    bmtool_kbs_sharpness_ctl: BoolProperty(
            name="bmtool_kbs_sharpness_ctl",
            default=False
            )

    bmtool_kbs_sharpness_alt: BoolProperty(
            name="bmtool_kbs_sharpness_alt",
            default=False
            )

    bmtool_kbs_adaptivity: StringProperty(
            name="bmtool_kbs_adaptivity",
            maxlen=1,
            default=''
            )

    bmtool_kbs_adaptivity_shift: BoolProperty(
            name="bmtool_kbs_adaptivity_shift",
            default=False
            )

    bmtool_kbs_adaptivity_ctl: BoolProperty(
            name="bmtool_kbs_adaptivity_ctl",
            default=False
            )

    bmtool_kbs_adaptivity_alt: BoolProperty(
            name="bmtool_kbs_adaptivity_alt",
            default=False
            )

    bmtool_kbs_voxel_size: StringProperty(
            name="bmtool_kbs_voxel_size",
            maxlen=1,
            default=''
            )

    bmtool_kbs_voxel_size_shift: BoolProperty(
            name="bmtool_kbs_voxel_size_shift",
            default=False
            )

    bmtool_kbs_voxel_size_ctl: BoolProperty(
            name="bmtool_kbs_voxel_size_ctl",
            default=False
            )

    bmtool_kbs_voxel_size_alt: BoolProperty(
            name="bmtool_kbs_voxel_size_alt",
            default=False
            )

    bmtool_kbs_screw_offset: StringProperty(
            name="bmtool_kbs_screw_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_screw_offset_shift: BoolProperty(
            name="bmtool_kbs_screw_offset_shift",
            default=False
            )

    bmtool_kbs_screw_offset_ctl: BoolProperty(
            name="bmtool_kbs_screw_offset_ctl",
            default=False
            )

    bmtool_kbs_screw_offset_alt: BoolProperty(
            name="bmtool_kbs_screw_offset_alt",
            default=False
            )

    bmtool_kbs_angle: StringProperty(
            name="bmtool_kbs_angle",
            maxlen=1,
            default=''
            )

    bmtool_kbs_angle_shift: BoolProperty(
            name="bmtool_kbs_angle_shift",
            default=False
            )

    bmtool_kbs_angle_ctl: BoolProperty(
            name="bmtool_kbs_angle_ctl",
            default=False
            )

    bmtool_kbs_angle_alt: BoolProperty(
            name="bmtool_kbs_angle_alt",
            default=False
            )

    bmtool_kbs_branch_smoothing: StringProperty(
            name="bmtool_kbs_branch_smoothing",
            maxlen=1,
            default=''
            )

    bmtool_kbs_branch_smoothing_shift: BoolProperty(
            name="bmtool_kbs_branch_smoothing_shift",
            default=False
            )

    bmtool_kbs_branch_smoothing_ctl: BoolProperty(
            name="bmtool_kbs_branch_smoothing_ctl",
            default=False
            )

    bmtool_kbs_branch_smoothing_alt: BoolProperty(
            name="bmtool_kbs_branch_smoothing_alt",
            default=False
            )

    bmtool_kbs_edge_crease_inner: StringProperty(
            name="bmtool_kbs_edge_crease_inner",
            maxlen=1,
            default=''
            )

    bmtool_kbs_edge_crease_inner_shift: BoolProperty(
            name="bmtool_kbs_edge_crease_inner_shift",
            default=False
            )

    bmtool_kbs_edge_crease_inner_ctl: BoolProperty(
            name="bmtool_kbs_edge_crease_inner_ctl",
            default=False
            )

    bmtool_kbs_edge_crease_inner_alt: BoolProperty(
            name="bmtool_kbs_edge_crease_inner_alt",
            default=False
            )

    bmtool_kbs_nonmanifold_merge_threshold: StringProperty(
            name="bmtool_kbs_nonmanifold_merge_threshold",
            maxlen=1,
            default=''
            )

    bmtool_kbs_nonmanifold_merge_threshold_shift: BoolProperty(
            name="bmtool_kbs_nonmanifold_merge_threshold_shift",
            default=False
            )

    bmtool_kbs_nonmanifold_merge_threshold_ctl: BoolProperty(
            name="bmtool_kbs_nonmanifold_merge_threshold_ctl",
            default=False
            )

    bmtool_kbs_nonmanifold_merge_threshold_alt: BoolProperty(
            name="bmtool_kbs_nonmanifold_merge_threshold_alt",
            default=False
            )

    bmtool_kbs_thickness_vertex_group: StringProperty(
            name="bmtool_kbs_thickness_vertex_group",
            maxlen=1,
            default=''
            )

    bmtool_kbs_thickness_vertex_group_shift: BoolProperty(
            name="bmtool_kbs_thickness_vertex_group_shift",
            default=False
            )

    bmtool_kbs_thickness_vertex_group_ctl: BoolProperty(
            name="bmtool_kbs_thickness_vertex_group_ctl",
            default=False
            )

    bmtool_kbs_thickness_vertex_group_alt: BoolProperty(
            name="bmtool_kbs_thickness_vertex_group_alt",
            default=False
            )

    bmtool_kbs_thickness: StringProperty(
            name="bmtool_kbs_thickness",
            maxlen=1,
            default=''
            )

    bmtool_kbs_thickness_shift: BoolProperty(
            name="bmtool_kbs_thickness_shift",
            default=False
            )

    bmtool_kbs_thickness_ctl: BoolProperty(
            name="bmtool_kbs_thickness_ctl",
            default=False
            )

    bmtool_kbs_thickness_alt: BoolProperty(
            name="bmtool_kbs_thickness_alt",
            default=False
            )

    bmtool_kbs_edge_crease_rim: StringProperty(
            name="bmtool_kbs_edge_crease_rim",
            maxlen=1,
            default=''
            )

    bmtool_kbs_edge_crease_rim_shift: BoolProperty(
            name="bmtool_kbs_edge_crease_rim_shift",
            default=False
            )

    bmtool_kbs_edge_crease_rim_ctl: BoolProperty(
            name="bmtool_kbs_edge_crease_rim_ctl",
            default=False
            )

    bmtool_kbs_edge_crease_rim_alt: BoolProperty(
            name="bmtool_kbs_edge_crease_rim_alt",
            default=False
            )

    bmtool_kbs_bevel_convex: StringProperty(
            name="bmtool_kbs_bevel_convex",
            maxlen=1,
            default=''
            )

    bmtool_kbs_bevel_convex_shift: BoolProperty(
            name="bmtool_kbs_bevel_convex_shift",
            default=False
            )

    bmtool_kbs_bevel_convex_ctl: BoolProperty(
            name="bmtool_kbs_bevel_convex_ctl",
            default=False
            )

    bmtool_kbs_bevel_convex_alt: BoolProperty(
            name="bmtool_kbs_bevel_convex_alt",
            default=False
            )

    bmtool_kbs_thickness_clamp: StringProperty(
            name="bmtool_kbs_thickness_clamp",
            maxlen=1,
            default=''
            )

    bmtool_kbs_thickness_clamp_shift: BoolProperty(
            name="bmtool_kbs_thickness_clamp_shift",
            default=False
            )

    bmtool_kbs_thickness_clamp_ctl: BoolProperty(
            name="bmtool_kbs_thickness_clamp_ctl",
            default=False
            )

    bmtool_kbs_thickness_clamp_alt: BoolProperty(
            name="bmtool_kbs_thickness_clamp_alt",
            default=False
            )

    bmtool_kbs_edge_crease_outer: StringProperty(
            name="bmtool_kbs_edge_crease_outer",
            maxlen=1,
            default=''
            )

    bmtool_kbs_edge_crease_outer_shift: BoolProperty(
            name="bmtool_kbs_edge_crease_outer_shift",
            default=False
            )

    bmtool_kbs_edge_crease_outer_ctl: BoolProperty(
            name="bmtool_kbs_edge_crease_outer_ctl",
            default=False
            )

    bmtool_kbs_edge_crease_outer_alt: BoolProperty(
            name="bmtool_kbs_edge_crease_outer_alt",
            default=False
            )

    bmtool_kbs_crease_weight: StringProperty(
            name="bmtool_kbs_crease_weight",
            maxlen=1,
            default=''
            )

    bmtool_kbs_crease_weight_shift: BoolProperty(
            name="bmtool_kbs_crease_weight_shift",
            default=False
            )

    bmtool_kbs_crease_weight_ctl: BoolProperty(
            name="bmtool_kbs_crease_weight_ctl",
            default=False
            )

    bmtool_kbs_crease_weight_alt: BoolProperty(
            name="bmtool_kbs_crease_weight_alt",
            default=False
            )

    bmtool_kbs_size: StringProperty(
            name="bmtool_kbs_size",
            maxlen=1,
            default=''
            )

    bmtool_kbs_size_shift: BoolProperty(
            name="bmtool_kbs_size_shift",
            default=False
            )

    bmtool_kbs_size_ctl: BoolProperty(
            name="bmtool_kbs_size_ctl",
            default=False
            )

    bmtool_kbs_size_alt: BoolProperty(
            name="bmtool_kbs_size_alt",
            default=False
            )

    bmtool_kbs_radius: StringProperty(
            name="bmtool_kbs_radius",
            maxlen=1,
            default=''
            )

    bmtool_kbs_radius_shift: BoolProperty(
            name="bmtool_kbs_radius_shift",
            default=False
            )

    bmtool_kbs_radius_ctl: BoolProperty(
            name="bmtool_kbs_radius_ctl",
            default=False
            )

    bmtool_kbs_radius_alt: BoolProperty(
            name="bmtool_kbs_radius_alt",
            default=False
            )

    bmtool_kbs_mid_level: StringProperty(
            name="bmtool_kbs_mid_level",
            maxlen=1,
            default=''
            )

    bmtool_kbs_mid_level_shift: BoolProperty(
            name="bmtool_kbs_mid_level_shift",
            default=False
            )

    bmtool_kbs_mid_level_ctl: BoolProperty(
            name="bmtool_kbs_mid_level_ctl",
            default=False
            )

    bmtool_kbs_mid_level_alt: BoolProperty(
            name="bmtool_kbs_mid_level_alt",
            default=False
            )

    bmtool_kbs_strength: StringProperty(
            name="bmtool_kbs_strength",
            maxlen=1,
            default=''
            )

    bmtool_kbs_strength_shift: BoolProperty(
            name="bmtool_kbs_strength_shift",
            default=False
            )

    bmtool_kbs_strength_ctl: BoolProperty(
            name="bmtool_kbs_strength_ctl",
            default=False
            )

    bmtool_kbs_strength_alt: BoolProperty(
            name="bmtool_kbs_strength_alt",
            default=False
            )

    bmtool_kbs_matrix_inverse: StringProperty(
            name="bmtool_kbs_matrix_inverse",
            maxlen=1,
            default=''
            )

    bmtool_kbs_matrix_inverse_shift: BoolProperty(
            name="bmtool_kbs_matrix_inverse_shift",
            default=False
            )

    bmtool_kbs_matrix_inverse_ctl: BoolProperty(
            name="bmtool_kbs_matrix_inverse_ctl",
            default=False
            )

    bmtool_kbs_matrix_inverse_alt: BoolProperty(
            name="bmtool_kbs_matrix_inverse_alt",
            default=False
            )

    bmtool_kbs_falloff_radius: StringProperty(
            name="bmtool_kbs_falloff_radius",
            maxlen=1,
            default=''
            )

    bmtool_kbs_falloff_radius_shift: BoolProperty(
            name="bmtool_kbs_falloff_radius_shift",
            default=False
            )

    bmtool_kbs_falloff_radius_ctl: BoolProperty(
            name="bmtool_kbs_falloff_radius_ctl",
            default=False
            )

    bmtool_kbs_falloff_radius_alt: BoolProperty(
            name="bmtool_kbs_falloff_radius_alt",
            default=False
            )

    bmtool_kbs_project_limit: StringProperty(
            name="bmtool_kbs_project_limit",
            maxlen=1,
            default=''
            )

    bmtool_kbs_project_limit_shift: BoolProperty(
            name="bmtool_kbs_project_limit_shift",
            default=False
            )

    bmtool_kbs_project_limit_ctl: BoolProperty(
            name="bmtool_kbs_project_limit_ctl",
            default=False
            )

    bmtool_kbs_project_limit_alt: BoolProperty(
            name="bmtool_kbs_project_limit_alt",
            default=False
            )

    bmtool_kbs_limits: StringProperty(
            name="bmtool_kbs_limits",
            maxlen=1,
            default=''
            )

    bmtool_kbs_limits_shift: BoolProperty(
            name="bmtool_kbs_limits_shift",
            default=False
            )

    bmtool_kbs_limits_ctl: BoolProperty(
            name="bmtool_kbs_limits_ctl",
            default=False
            )

    bmtool_kbs_limits_alt: BoolProperty(
            name="bmtool_kbs_limits_alt",
            default=False
            )

    bmtool_kbs_lambda_border: StringProperty(
            name="bmtool_kbs_lambda_border",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lambda_border_shift: BoolProperty(
            name="bmtool_kbs_lambda_border_shift",
            default=False
            )

    bmtool_kbs_lambda_border_ctl: BoolProperty(
            name="bmtool_kbs_lambda_border_ctl",
            default=False
            )

    bmtool_kbs_lambda_border_alt: BoolProperty(
            name="bmtool_kbs_lambda_border_alt",
            default=False
            )

    bmtool_kbs_lambda_factor: StringProperty(
            name="bmtool_kbs_lambda_factor",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lambda_factor_shift: BoolProperty(
            name="bmtool_kbs_lambda_factor_shift",
            default=False
            )

    bmtool_kbs_lambda_factor_ctl: BoolProperty(
            name="bmtool_kbs_lambda_factor_ctl",
            default=False
            )

    bmtool_kbs_lambda_factor_alt: BoolProperty(
            name="bmtool_kbs_lambda_factor_alt",
            default=False
            )

    bmtool_kbs_falloff: StringProperty(
            name="bmtool_kbs_falloff",
            maxlen=1,
            default=''
            )

    bmtool_kbs_falloff_shift: BoolProperty(
            name="bmtool_kbs_falloff_shift",
            default=False
            )

    bmtool_kbs_falloff_ctl: BoolProperty(
            name="bmtool_kbs_falloff_ctl",
            default=False
            )

    bmtool_kbs_falloff_alt: BoolProperty(
            name="bmtool_kbs_falloff_alt",
            default=False
            )

    bmtool_kbs_damping_time: StringProperty(
            name="bmtool_kbs_damping_time",
            maxlen=1,
            default=''
            )

    bmtool_kbs_damping_time_shift: BoolProperty(
            name="bmtool_kbs_damping_time_shift",
            default=False
            )

    bmtool_kbs_damping_time_ctl: BoolProperty(
            name="bmtool_kbs_damping_time_ctl",
            default=False
            )

    bmtool_kbs_damping_time_alt: BoolProperty(
            name="bmtool_kbs_damping_time_alt",
            default=False
            )

    bmtool_kbs_lifetime: StringProperty(
            name="bmtool_kbs_lifetime",
            maxlen=1,
            default=''
            )

    bmtool_kbs_lifetime_shift: BoolProperty(
            name="bmtool_kbs_lifetime_shift",
            default=False
            )

    bmtool_kbs_lifetime_ctl: BoolProperty(
            name="bmtool_kbs_lifetime_ctl",
            default=False
            )

    bmtool_kbs_lifetime_alt: BoolProperty(
            name="bmtool_kbs_lifetime_alt",
            default=False
            )

    bmtool_kbs_narrowness: StringProperty(
            name="bmtool_kbs_narrowness",
            maxlen=1,
            default=''
            )

    bmtool_kbs_narrowness_shift: BoolProperty(
            name="bmtool_kbs_narrowness_shift",
            default=False
            )

    bmtool_kbs_narrowness_ctl: BoolProperty(
            name="bmtool_kbs_narrowness_ctl",
            default=False
            )

    bmtool_kbs_narrowness_alt: BoolProperty(
            name="bmtool_kbs_narrowness_alt",
            default=False
            )

    bmtool_kbs_time_offset: StringProperty(
            name="bmtool_kbs_time_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_time_offset_shift: BoolProperty(
            name="bmtool_kbs_time_offset_shift",
            default=False
            )

    bmtool_kbs_time_offset_ctl: BoolProperty(
            name="bmtool_kbs_time_offset_ctl",
            default=False
            )

    bmtool_kbs_time_offset_alt: BoolProperty(
            name="bmtool_kbs_time_offset_alt",
            default=False
            )

    bmtool_kbs_start_position_y: StringProperty(
            name="bmtool_kbs_start_position_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_start_position_y_shift: BoolProperty(
            name="bmtool_kbs_start_position_y_shift",
            default=False
            )

    bmtool_kbs_start_position_y_ctl: BoolProperty(
            name="bmtool_kbs_start_position_y_ctl",
            default=False
            )

    bmtool_kbs_start_position_y_alt: BoolProperty(
            name="bmtool_kbs_start_position_y_alt",
            default=False
            )

    bmtool_kbs_height: StringProperty(
            name="bmtool_kbs_height",
            maxlen=1,
            default=''
            )

    bmtool_kbs_height_shift: BoolProperty(
            name="bmtool_kbs_height_shift",
            default=False
            )

    bmtool_kbs_height_ctl: BoolProperty(
            name="bmtool_kbs_height_ctl",
            default=False
            )

    bmtool_kbs_height_alt: BoolProperty(
            name="bmtool_kbs_height_alt",
            default=False
            )

    bmtool_kbs_start_position_x: StringProperty(
            name="bmtool_kbs_start_position_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_start_position_x_shift: BoolProperty(
            name="bmtool_kbs_start_position_x_shift",
            default=False
            )

    bmtool_kbs_start_position_x_ctl: BoolProperty(
            name="bmtool_kbs_start_position_x_ctl",
            default=False
            )

    bmtool_kbs_start_position_x_alt: BoolProperty(
            name="bmtool_kbs_start_position_x_alt",
            default=False
            )

    bmtool_kbs_speed: StringProperty(
            name="bmtool_kbs_speed",
            maxlen=1,
            default=''
            )

    bmtool_kbs_speed_shift: BoolProperty(
            name="bmtool_kbs_speed_shift",
            default=False
            )

    bmtool_kbs_speed_ctl: BoolProperty(
            name="bmtool_kbs_speed_ctl",
            default=False
            )

    bmtool_kbs_speed_alt: BoolProperty(
            name="bmtool_kbs_speed_alt",
            default=False
            )

    bmtool_kbs_protect: StringProperty(
            name="bmtool_kbs_protect",
            maxlen=1,
            default=''
            )

    bmtool_kbs_protect_shift: BoolProperty(
            name="bmtool_kbs_protect_shift",
            default=False
            )

    bmtool_kbs_protect_ctl: BoolProperty(
            name="bmtool_kbs_protect_ctl",
            default=False
            )

    bmtool_kbs_protect_alt: BoolProperty(
            name="bmtool_kbs_protect_alt",
            default=False
            )

    bmtool_kbs_sharpen_peak_jonswap: StringProperty(
            name="bmtool_kbs_sharpen_peak_jonswap",
            maxlen=1,
            default=''
            )

    bmtool_kbs_sharpen_peak_jonswap_shift: BoolProperty(
            name="bmtool_kbs_sharpen_peak_jonswap_shift",
            default=False
            )

    bmtool_kbs_sharpen_peak_jonswap_ctl: BoolProperty(
            name="bmtool_kbs_sharpen_peak_jonswap_ctl",
            default=False
            )

    bmtool_kbs_sharpen_peak_jonswap_alt: BoolProperty(
            name="bmtool_kbs_sharpen_peak_jonswap_alt",
            default=False
            )

    bmtool_kbs_wave_scale_min: StringProperty(
            name="bmtool_kbs_wave_scale_min",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wave_scale_min_shift: BoolProperty(
            name="bmtool_kbs_wave_scale_min_shift",
            default=False
            )

    bmtool_kbs_wave_scale_min_ctl: BoolProperty(
            name="bmtool_kbs_wave_scale_min_ctl",
            default=False
            )

    bmtool_kbs_wave_scale_min_alt: BoolProperty(
            name="bmtool_kbs_wave_scale_min_alt",
            default=False
            )

    bmtool_kbs_wave_scale: StringProperty(
            name="bmtool_kbs_wave_scale",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wave_scale_shift: BoolProperty(
            name="bmtool_kbs_wave_scale_shift",
            default=False
            )

    bmtool_kbs_wave_scale_ctl: BoolProperty(
            name="bmtool_kbs_wave_scale_ctl",
            default=False
            )

    bmtool_kbs_wave_scale_alt: BoolProperty(
            name="bmtool_kbs_wave_scale_alt",
            default=False
            )

    bmtool_kbs_wave_alignment: StringProperty(
            name="bmtool_kbs_wave_alignment",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wave_alignment_shift: BoolProperty(
            name="bmtool_kbs_wave_alignment_shift",
            default=False
            )

    bmtool_kbs_wave_alignment_ctl: BoolProperty(
            name="bmtool_kbs_wave_alignment_ctl",
            default=False
            )

    bmtool_kbs_wave_alignment_alt: BoolProperty(
            name="bmtool_kbs_wave_alignment_alt",
            default=False
            )

    bmtool_kbs_choppiness: StringProperty(
            name="bmtool_kbs_choppiness",
            maxlen=1,
            default=''
            )

    bmtool_kbs_choppiness_shift: BoolProperty(
            name="bmtool_kbs_choppiness_shift",
            default=False
            )

    bmtool_kbs_choppiness_ctl: BoolProperty(
            name="bmtool_kbs_choppiness_ctl",
            default=False
            )

    bmtool_kbs_choppiness_alt: BoolProperty(
            name="bmtool_kbs_choppiness_alt",
            default=False
            )

    bmtool_kbs_time: StringProperty(
            name="bmtool_kbs_time",
            maxlen=1,
            default=''
            )

    bmtool_kbs_time_shift: BoolProperty(
            name="bmtool_kbs_time_shift",
            default=False
            )

    bmtool_kbs_time_ctl: BoolProperty(
            name="bmtool_kbs_time_ctl",
            default=False
            )

    bmtool_kbs_time_alt: BoolProperty(
            name="bmtool_kbs_time_alt",
            default=False
            )

    bmtool_kbs_damping: StringProperty(
            name="bmtool_kbs_damping",
            maxlen=1,
            default=''
            )

    bmtool_kbs_damping_shift: BoolProperty(
            name="bmtool_kbs_damping_shift",
            default=False
            )

    bmtool_kbs_damping_ctl: BoolProperty(
            name="bmtool_kbs_damping_ctl",
            default=False
            )

    bmtool_kbs_damping_alt: BoolProperty(
            name="bmtool_kbs_damping_alt",
            default=False
            )

    bmtool_kbs_wave_direction: StringProperty(
            name="bmtool_kbs_wave_direction",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wave_direction_shift: BoolProperty(
            name="bmtool_kbs_wave_direction_shift",
            default=False
            )

    bmtool_kbs_wave_direction_ctl: BoolProperty(
            name="bmtool_kbs_wave_direction_ctl",
            default=False
            )

    bmtool_kbs_wave_direction_alt: BoolProperty(
            name="bmtool_kbs_wave_direction_alt",
            default=False
            )

    bmtool_kbs_wind_velocity: StringProperty(
            name="bmtool_kbs_wind_velocity",
            maxlen=1,
            default=''
            )

    bmtool_kbs_wind_velocity_shift: BoolProperty(
            name="bmtool_kbs_wind_velocity_shift",
            default=False
            )

    bmtool_kbs_wind_velocity_ctl: BoolProperty(
            name="bmtool_kbs_wind_velocity_ctl",
            default=False
            )

    bmtool_kbs_wind_velocity_alt: BoolProperty(
            name="bmtool_kbs_wind_velocity_alt",
            default=False
            )

    bmtool_kbs_depth: StringProperty(
            name="bmtool_kbs_depth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_depth_shift: BoolProperty(
            name="bmtool_kbs_depth_shift",
            default=False
            )

    bmtool_kbs_depth_ctl: BoolProperty(
            name="bmtool_kbs_depth_ctl",
            default=False
            )

    bmtool_kbs_depth_alt: BoolProperty(
            name="bmtool_kbs_depth_alt",
            default=False
            )

    bmtool_kbs_foam_coverage: StringProperty(
            name="bmtool_kbs_foam_coverage",
            maxlen=1,
            default=''
            )

    bmtool_kbs_foam_coverage_shift: BoolProperty(
            name="bmtool_kbs_foam_coverage_shift",
            default=False
            )

    bmtool_kbs_foam_coverage_ctl: BoolProperty(
            name="bmtool_kbs_foam_coverage_ctl",
            default=False
            )

    bmtool_kbs_foam_coverage_alt: BoolProperty(
            name="bmtool_kbs_foam_coverage_alt",
            default=False
            )

    bmtool_kbs_fetch_jonswap: StringProperty(
            name="bmtool_kbs_fetch_jonswap",
            maxlen=1,
            default=''
            )

    bmtool_kbs_fetch_jonswap_shift: BoolProperty(
            name="bmtool_kbs_fetch_jonswap_shift",
            default=False
            )

    bmtool_kbs_fetch_jonswap_ctl: BoolProperty(
            name="bmtool_kbs_fetch_jonswap_ctl",
            default=False
            )

    bmtool_kbs_fetch_jonswap_alt: BoolProperty(
            name="bmtool_kbs_fetch_jonswap_alt",
            default=False
            )

    bmtool_kbs_bake_foam_fade: StringProperty(
            name="bmtool_kbs_bake_foam_fade",
            maxlen=1,
            default=''
            )

    bmtool_kbs_bake_foam_fade_shift: BoolProperty(
            name="bmtool_kbs_bake_foam_fade_shift",
            default=False
            )

    bmtool_kbs_bake_foam_fade_ctl: BoolProperty(
            name="bmtool_kbs_bake_foam_fade_ctl",
            default=False
            )

    bmtool_kbs_bake_foam_fade_alt: BoolProperty(
            name="bmtool_kbs_bake_foam_fade_alt",
            default=False
            )

    bmtool_kbs_particle_amount: StringProperty(
            name="bmtool_kbs_particle_amount",
            maxlen=1,
            default=''
            )

    bmtool_kbs_particle_amount_shift: BoolProperty(
            name="bmtool_kbs_particle_amount_shift",
            default=False
            )

    bmtool_kbs_particle_amount_ctl: BoolProperty(
            name="bmtool_kbs_particle_amount_ctl",
            default=False
            )

    bmtool_kbs_particle_amount_alt: BoolProperty(
            name="bmtool_kbs_particle_amount_alt",
            default=False
            )

    bmtool_kbs_random_rotation: StringProperty(
            name="bmtool_kbs_random_rotation",
            maxlen=1,
            default=''
            )

    bmtool_kbs_random_rotation_shift: BoolProperty(
            name="bmtool_kbs_random_rotation_shift",
            default=False
            )

    bmtool_kbs_random_rotation_ctl: BoolProperty(
            name="bmtool_kbs_random_rotation_ctl",
            default=False
            )

    bmtool_kbs_random_rotation_alt: BoolProperty(
            name="bmtool_kbs_random_rotation_alt",
            default=False
            )

    bmtool_kbs_particle_offset: StringProperty(
            name="bmtool_kbs_particle_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_particle_offset_shift: BoolProperty(
            name="bmtool_kbs_particle_offset_shift",
            default=False
            )

    bmtool_kbs_particle_offset_ctl: BoolProperty(
            name="bmtool_kbs_particle_offset_ctl",
            default=False
            )

    bmtool_kbs_particle_offset_alt: BoolProperty(
            name="bmtool_kbs_particle_offset_alt",
            default=False
            )

    bmtool_kbs_random_position: StringProperty(
            name="bmtool_kbs_random_position",
            maxlen=1,
            default=''
            )

    bmtool_kbs_random_position_shift: BoolProperty(
            name="bmtool_kbs_random_position_shift",
            default=False
            )

    bmtool_kbs_random_position_ctl: BoolProperty(
            name="bmtool_kbs_random_position_ctl",
            default=False
            )

    bmtool_kbs_random_position_alt: BoolProperty(
            name="bmtool_kbs_random_position_alt",
            default=False
            )

    bmtool_kbs_position: StringProperty(
            name="bmtool_kbs_position",
            maxlen=1,
            default=''
            )

    bmtool_kbs_position_shift: BoolProperty(
            name="bmtool_kbs_position_shift",
            default=False
            )

    bmtool_kbs_position_ctl: BoolProperty(
            name="bmtool_kbs_position_ctl",
            default=False
            )

    bmtool_kbs_position_alt: BoolProperty(
            name="bmtool_kbs_position_alt",
            default=False
            )

    bmtool_kbs_weight: StringProperty(
            name="bmtool_kbs_weight",
            maxlen=1,
            default=''
            )

    bmtool_kbs_weight_shift: BoolProperty(
            name="bmtool_kbs_weight_shift",
            default=False
            )

    bmtool_kbs_weight_ctl: BoolProperty(
            name="bmtool_kbs_weight_ctl",
            default=False
            )

    bmtool_kbs_weight_alt: BoolProperty(
            name="bmtool_kbs_weight_alt",
            default=False
            )

    bmtool_kbs_projector_count: StringProperty(
            name="bmtool_kbs_projector_count",
            maxlen=1,
            default=''
            )

    bmtool_kbs_projector_count_shift: BoolProperty(
            name="bmtool_kbs_projector_count_shift",
            default=False
            )

    bmtool_kbs_projector_count_ctl: BoolProperty(
            name="bmtool_kbs_projector_count_ctl",
            default=False
            )

    bmtool_kbs_projector_count_alt: BoolProperty(
            name="bmtool_kbs_projector_count_alt",
            default=False
            )

    bmtool_kbs_count: StringProperty(
            name="bmtool_kbs_count",
            maxlen=1,
            default=''
            )

    bmtool_kbs_count_shift: BoolProperty(
            name="bmtool_kbs_count_shift",
            default=False
            )

    bmtool_kbs_count_ctl: BoolProperty(
            name="bmtool_kbs_count_ctl",
            default=False
            )

    bmtool_kbs_count_alt: BoolProperty(
            name="bmtool_kbs_count_alt",
            default=False
            )

    bmtool_kbs_segments: StringProperty(
            name="bmtool_kbs_segments",
            maxlen=1,
            default=''
            )

    bmtool_kbs_segments_shift: BoolProperty(
            name="bmtool_kbs_segments_shift",
            default=False
            )

    bmtool_kbs_segments_ctl: BoolProperty(
            name="bmtool_kbs_segments_ctl",
            default=False
            )

    bmtool_kbs_segments_alt: BoolProperty(
            name="bmtool_kbs_segments_alt",
            default=False
            )

    bmtool_kbs_material: StringProperty(
            name="bmtool_kbs_material",
            maxlen=1,
            default=''
            )

    bmtool_kbs_material_shift: BoolProperty(
            name="bmtool_kbs_material_shift",
            default=False
            )

    bmtool_kbs_material_ctl: BoolProperty(
            name="bmtool_kbs_material_ctl",
            default=False
            )

    bmtool_kbs_material_alt: BoolProperty(
            name="bmtool_kbs_material_alt",
            default=False
            )

    bmtool_kbs_seed: StringProperty(
            name="bmtool_kbs_seed",
            maxlen=1,
            default=''
            )

    bmtool_kbs_seed_shift: BoolProperty(
            name="bmtool_kbs_seed_shift",
            default=False
            )

    bmtool_kbs_seed_ctl: BoolProperty(
            name="bmtool_kbs_seed_ctl",
            default=False
            )

    bmtool_kbs_seed_alt: BoolProperty(
            name="bmtool_kbs_seed_alt",
            default=False
            )

    bmtool_kbs_iterations: StringProperty(
            name="bmtool_kbs_iterations",
            maxlen=1,
            default=''
            )

    bmtool_kbs_iterations_shift: BoolProperty(
            name="bmtool_kbs_iterations_shift",
            default=False
            )

    bmtool_kbs_iterations_ctl: BoolProperty(
            name="bmtool_kbs_iterations_ctl",
            default=False
            )

    bmtool_kbs_iterations_alt: BoolProperty(
            name="bmtool_kbs_iterations_alt",
            default=False
            )

    bmtool_kbs_levels: StringProperty(
            name="bmtool_kbs_levels",
            maxlen=1,
            default=''
            )

    bmtool_kbs_levels_shift: BoolProperty(
            name="bmtool_kbs_levels_shift",
            default=False
            )

    bmtool_kbs_levels_ctl: BoolProperty(
            name="bmtool_kbs_levels_ctl",
            default=False
            )

    bmtool_kbs_levels_alt: BoolProperty(
            name="bmtool_kbs_levels_alt",
            default=False
            )

    bmtool_kbs_quality: StringProperty(
            name="bmtool_kbs_quality",
            maxlen=1,
            default=''
            )

    bmtool_kbs_quality_shift: BoolProperty(
            name="bmtool_kbs_quality_shift",
            default=False
            )

    bmtool_kbs_quality_ctl: BoolProperty(
            name="bmtool_kbs_quality_ctl",
            default=False
            )

    bmtool_kbs_quality_alt: BoolProperty(
            name="bmtool_kbs_quality_alt",
            default=False
            )

    bmtool_kbs_sculpt_levels: StringProperty(
            name="bmtool_kbs_sculpt_levels",
            maxlen=1,
            default=''
            )

    bmtool_kbs_sculpt_levels_shift: BoolProperty(
            name="bmtool_kbs_sculpt_levels_shift",
            default=False
            )

    bmtool_kbs_sculpt_levels_ctl: BoolProperty(
            name="bmtool_kbs_sculpt_levels_ctl",
            default=False
            )

    bmtool_kbs_sculpt_levels_alt: BoolProperty(
            name="bmtool_kbs_sculpt_levels_alt",
            default=False
            )

    bmtool_kbs_render_levels: StringProperty(
            name="bmtool_kbs_render_levels",
            maxlen=1,
            default=''
            )

    bmtool_kbs_render_levels_shift: BoolProperty(
            name="bmtool_kbs_render_levels_shift",
            default=False
            )

    bmtool_kbs_render_levels_ctl: BoolProperty(
            name="bmtool_kbs_render_levels_ctl",
            default=False
            )

    bmtool_kbs_render_levels_alt: BoolProperty(
            name="bmtool_kbs_render_levels_alt",
            default=False
            )

    bmtool_kbs_octree_depth: StringProperty(
            name="bmtool_kbs_octree_depth",
            maxlen=1,
            default=''
            )

    bmtool_kbs_octree_depth_shift: BoolProperty(
            name="bmtool_kbs_octree_depth_shift",
            default=False
            )

    bmtool_kbs_octree_depth_ctl: BoolProperty(
            name="bmtool_kbs_octree_depth_ctl",
            default=False
            )

    bmtool_kbs_octree_depth_alt: BoolProperty(
            name="bmtool_kbs_octree_depth_alt",
            default=False
            )

    bmtool_kbs_render_steps: StringProperty(
            name="bmtool_kbs_render_steps",
            maxlen=1,
            default=''
            )

    bmtool_kbs_render_steps_shift: BoolProperty(
            name="bmtool_kbs_render_steps_shift",
            default=False
            )

    bmtool_kbs_render_steps_ctl: BoolProperty(
            name="bmtool_kbs_render_steps_ctl",
            default=False
            )

    bmtool_kbs_render_steps_alt: BoolProperty(
            name="bmtool_kbs_render_steps_alt",
            default=False
            )

    bmtool_kbs_steps: StringProperty(
            name="bmtool_kbs_steps",
            maxlen=1,
            default=''
            )

    bmtool_kbs_steps_shift: BoolProperty(
            name="bmtool_kbs_steps_shift",
            default=False
            )

    bmtool_kbs_steps_ctl: BoolProperty(
            name="bmtool_kbs_steps_ctl",
            default=False
            )

    bmtool_kbs_steps_alt: BoolProperty(
            name="bmtool_kbs_steps_alt",
            default=False
            )

    bmtool_kbs_material_offset: StringProperty(
            name="bmtool_kbs_material_offset",
            maxlen=1,
            default=''
            )

    bmtool_kbs_material_offset_shift: BoolProperty(
            name="bmtool_kbs_material_offset_shift",
            default=False
            )

    bmtool_kbs_material_offset_ctl: BoolProperty(
            name="bmtool_kbs_material_offset_ctl",
            default=False
            )

    bmtool_kbs_material_offset_alt: BoolProperty(
            name="bmtool_kbs_material_offset_alt",
            default=False
            )

    bmtool_kbs_material_offset_rim: StringProperty(
            name="bmtool_kbs_material_offset_rim",
            maxlen=1,
            default=''
            )

    bmtool_kbs_material_offset_rim_shift: BoolProperty(
            name="bmtool_kbs_material_offset_rim_shift",
            default=False
            )

    bmtool_kbs_material_offset_rim_ctl: BoolProperty(
            name="bmtool_kbs_material_offset_rim_ctl",
            default=False
            )

    bmtool_kbs_material_offset_rim_alt: BoolProperty(
            name="bmtool_kbs_material_offset_rim_alt",
            default=False
            )

    bmtool_kbs_min_vertices: StringProperty(
            name="bmtool_kbs_min_vertices",
            maxlen=1,
            default=''
            )

    bmtool_kbs_min_vertices_shift: BoolProperty(
            name="bmtool_kbs_min_vertices_shift",
            default=False
            )

    bmtool_kbs_min_vertices_ctl: BoolProperty(
            name="bmtool_kbs_min_vertices_ctl",
            default=False
            )

    bmtool_kbs_min_vertices_alt: BoolProperty(
            name="bmtool_kbs_min_vertices_alt",
            default=False
            )

    bmtool_kbs_voxel_amount: StringProperty(
            name="bmtool_kbs_voxel_amount",
            maxlen=1,
            default=''
            )

    bmtool_kbs_voxel_amount_shift: BoolProperty(
            name="bmtool_kbs_voxel_amount_shift",
            default=False
            )

    bmtool_kbs_voxel_amount_ctl: BoolProperty(
            name="bmtool_kbs_voxel_amount_ctl",
            default=False
            )

    bmtool_kbs_voxel_amount_alt: BoolProperty(
            name="bmtool_kbs_voxel_amount_alt",
            default=False
            )

    bmtool_kbs_precision: StringProperty(
            name="bmtool_kbs_precision",
            maxlen=1,
            default=''
            )

    bmtool_kbs_precision_shift: BoolProperty(
            name="bmtool_kbs_precision_shift",
            default=False
            )

    bmtool_kbs_precision_ctl: BoolProperty(
            name="bmtool_kbs_precision_ctl",
            default=False
            )

    bmtool_kbs_precision_alt: BoolProperty(
            name="bmtool_kbs_precision_alt",
            default=False
            )

    bmtool_kbs_subsurf_levels: StringProperty(
            name="bmtool_kbs_subsurf_levels",
            maxlen=1,
            default=''
            )

    bmtool_kbs_subsurf_levels_shift: BoolProperty(
            name="bmtool_kbs_subsurf_levels_shift",
            default=False
            )

    bmtool_kbs_subsurf_levels_ctl: BoolProperty(
            name="bmtool_kbs_subsurf_levels_ctl",
            default=False
            )

    bmtool_kbs_subsurf_levels_alt: BoolProperty(
            name="bmtool_kbs_subsurf_levels_alt",
            default=False
            )

    bmtool_kbs_resolution: StringProperty(
            name="bmtool_kbs_resolution",
            maxlen=1,
            default=''
            )

    bmtool_kbs_resolution_shift: BoolProperty(
            name="bmtool_kbs_resolution_shift",
            default=False
            )

    bmtool_kbs_resolution_ctl: BoolProperty(
            name="bmtool_kbs_resolution_ctl",
            default=False
            )

    bmtool_kbs_resolution_alt: BoolProperty(
            name="bmtool_kbs_resolution_alt",
            default=False
            )

    bmtool_kbs_repeat_x: StringProperty(
            name="bmtool_kbs_repeat_x",
            maxlen=1,
            default=''
            )

    bmtool_kbs_repeat_x_shift: BoolProperty(
            name="bmtool_kbs_repeat_x_shift",
            default=False
            )

    bmtool_kbs_repeat_x_ctl: BoolProperty(
            name="bmtool_kbs_repeat_x_ctl",
            default=False
            )

    bmtool_kbs_repeat_x_alt: BoolProperty(
            name="bmtool_kbs_repeat_x_alt",
            default=False
            )

    bmtool_kbs_spatial_size: StringProperty(
            name="bmtool_kbs_spatial_size",
            maxlen=1,
            default=''
            )

    bmtool_kbs_spatial_size_shift: BoolProperty(
            name="bmtool_kbs_spatial_size_shift",
            default=False
            )

    bmtool_kbs_spatial_size_ctl: BoolProperty(
            name="bmtool_kbs_spatial_size_ctl",
            default=False
            )

    bmtool_kbs_spatial_size_alt: BoolProperty(
            name="bmtool_kbs_spatial_size_alt",
            default=False
            )

    bmtool_kbs_viewport_resolution: StringProperty(
            name="bmtool_kbs_viewport_resolution",
            maxlen=1,
            default=''
            )

    bmtool_kbs_viewport_resolution_shift: BoolProperty(
            name="bmtool_kbs_viewport_resolution_shift",
            default=False
            )

    bmtool_kbs_viewport_resolution_ctl: BoolProperty(
            name="bmtool_kbs_viewport_resolution_ctl",
            default=False
            )

    bmtool_kbs_viewport_resolution_alt: BoolProperty(
            name="bmtool_kbs_viewport_resolution_alt",
            default=False
            )

    bmtool_kbs_frame_end: StringProperty(
            name="bmtool_kbs_frame_end",
            maxlen=1,
            default=''
            )

    bmtool_kbs_frame_end_shift: BoolProperty(
            name="bmtool_kbs_frame_end_shift",
            default=False
            )

    bmtool_kbs_frame_end_ctl: BoolProperty(
            name="bmtool_kbs_frame_end_ctl",
            default=False
            )

    bmtool_kbs_frame_end_alt: BoolProperty(
            name="bmtool_kbs_frame_end_alt",
            default=False
            )

    bmtool_kbs_repeat_y: StringProperty(
            name="bmtool_kbs_repeat_y",
            maxlen=1,
            default=''
            )

    bmtool_kbs_repeat_y_shift: BoolProperty(
            name="bmtool_kbs_repeat_y_shift",
            default=False
            )

    bmtool_kbs_repeat_y_ctl: BoolProperty(
            name="bmtool_kbs_repeat_y_ctl",
            default=False
            )

    bmtool_kbs_repeat_y_alt: BoolProperty(
            name="bmtool_kbs_repeat_y_alt",
            default=False
            )

    bmtool_kbs_random_seed: StringProperty(
            name="bmtool_kbs_random_seed",
            maxlen=1,
            default=''
            )

    bmtool_kbs_random_seed_shift: BoolProperty(
            name="bmtool_kbs_random_seed_shift",
            default=False
            )

    bmtool_kbs_random_seed_ctl: BoolProperty(
            name="bmtool_kbs_random_seed_ctl",
            default=False
            )

    bmtool_kbs_random_seed_alt: BoolProperty(
            name="bmtool_kbs_random_seed_alt",
            default=False
            )

    bmtool_kbs_particle_system_index: StringProperty(
            name="bmtool_kbs_particle_system_index"
            maxlen=1,
            default=''
            )

    bmtool_kbs_particle_system_index_shift: BoolProperty(
            name="bmtool_kbs_particle_system_index_shift",
            default=False
            )

    bmtool_kbs_particle_system_index_ctl: BoolProperty(
            name="bmtool_kbs_particle_system_index_ctl",
            default=False
            )

    bmtool_kbs_particle_system_index_alt: BoolProperty(
            name="bmtool_kbs_particle_system_index_alt",
            default=False
            )
    # }}}

    def draw(self, context):
        layout = self.layout
        layout.label(text="BMTool options")
        layout.prop(self, "save_clusters")
        if self.save_clusters_backup:
            layout.prop(self, "save_clusters_backup")
        layout.prop(self, "backup_mesh_on_modifier_apply_remove")
        if self.backup_mesh_on_modifier_apply_remove:
            layout.prop(self, "backup_collection_name")
        layout.prop(self, "custom_cluster_types")
        if self.custom_cluster_types:
            layout.prop(self, "always_add_custom_cluster_types")
            layout.prop(self, "saved_cluster_types")
            layout.prop(self, "cluster_types")
