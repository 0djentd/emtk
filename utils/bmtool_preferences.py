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

import re

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):
    bl_idname = "bmtools"
    
    # Properties names list {{{
    props_names = [
                   "bmtools_name",
                   "bmtools_vertex_group",
                   "bmtools_filepath",
                   "bmtools_object_path",
                   "bmtools_uv_layer",
                   "bmtools_bone_to",
                   "bmtools_bone_from",
                   "bmtools_mask_vertex_group",
                   "bmtools_mask_tex_map_bone",
                   "bmtools_mask_tex_uv_layer",
                   "bmtools_vertex_group_a",
                   "bmtools_vertex_group_b",
                   "bmtools_rim_vertex_group",
                   "bmtools_shell_vertex_group",
                   "bmtools_grid_name",
                   "bmtools_texture_coords_bone",
                   "bmtools_subtarget",
                   "bmtools_particle_uv",
                   "bmtools_foam_layer_name",
                   "bmtools_spray_layer_name",
                   "bmtools_value_layer_name",
                   "bmtools_index_layer_name",
                   "bmtools_use_apply_on_spline",
                   "bmtools_use_poly_data",
                   "bmtools_show_render",
                   "bmtools_show_in_editmode",
                   "bmtools_use_edge_data",
                   "bmtools_use_loop_data",
                   "bmtools_use_vert_data",
                   "bmtools_use_object_transform",
                   "bmtools_use_max_distance",
                   "bmtools_show_expanded",
                   "bmtools_show_viewport",
                   "bmtools_is_active",
                   "bmtools_show_on_cage",
                   "bmtools_invert_vertex_group",
                   "bmtools_use_vertex_interpolation",
                   "bmtools_use_direction_parallel",
                   "bmtools_no_polynors_fix",
                   "bmtools_keep_sharp",
                   "bmtools_use_face_influence",
                   "bmtools_use_add",
                   "bmtools_invert_falloff",
                   "bmtools_normalize",
                   "bmtools_use_remove",
                   "bmtools_invert_mask_vertex_group",
                   "bmtools_invert_vertex_group_a",
                   "bmtools_invert_vertex_group_b",
                   "bmtools_use_object_offset",
                   "bmtools_use_merge_vertices",
                   "bmtools_use_constant_offset",
                   "bmtools_use_merge_vertices_cap",
                   "bmtools_use_relative_offset",
                   "bmtools_use_clamp_overlap",
                   "bmtools_loop_slide",
                   "bmtools_mark_sharp",
                   "bmtools_mark_seam",
                   "bmtools_harden_normals",
                   "bmtools_use_hole_tolerant",
                   "bmtools_use_self",
                   "bmtools_use_random_order",
                   "bmtools_use_reverse",
                   "bmtools_use_collapse_triangulate",
                   "bmtools_use_dissolve_boundaries",
                   "bmtools_use_symmetry",
                   "bmtools_use_edge_sharp",
                   "bmtools_use_edge_angle",
                   "bmtools_use_smooth",
                   "bmtools_use_mirror_merge",
                   "bmtools_use_mirror_v",
                   "bmtools_use_mirror_udim",
                   "bmtools_use_bisect_flip_axis",
                   "bmtools_use_mirror_u",
                   "bmtools_use_bisect_axis",
                   "bmtools_use_mirror_vertex_groups",
                   "bmtools_use_axis",
                   "bmtools_use_clip",
                   "bmtools_use_creases",
                   "bmtools_use_sculpt_base_mesh",
                   "bmtools_show_only_control_edges",
                   "bmtools_use_custom_normals",
                   "bmtools_use_remove_disconnected",
                   "bmtools_use_smooth_shade",
                   "bmtools_use_normal_calculate",
                   "bmtools_use_normal_flip",
                   "bmtools_use_stretch_u",
                   "bmtools_use_object_screw_offset",
                   "bmtools_use_stretch_v",
                   "bmtools_use_x_symmetry",
                   "bmtools_use_y_symmetry",
                   "bmtools_use_z_symmetry",
                   "bmtools_use_rim",
                   "bmtools_use_rim_only",
                   "bmtools_use_quality_normals",
                   "bmtools_use_flat_faces",
                   "bmtools_use_even_offset",
                   "bmtools_use_flip_normals",
                   "bmtools_use_thickness_angle_clamp",
                   "bmtools_use_limit_surface",
                   "bmtools_keep_custom_normals",
                   "bmtools_loose_edges",
                   "bmtools_use_crease",
                   "bmtools_use_replace",
                   "bmtools_use_boundary",
                   "bmtools_use_multi_modifier",
                   "bmtools_use_bone_envelopes",
                   "bmtools_use_deform_preserve_volume",
                   "bmtools_use_vertex_groups",
                   "bmtools_use_z",
                   "bmtools_use_x",
                   "bmtools_use_y",
                   "bmtools_use_radius_as_size",
                   "bmtools_use_transform",
                   "bmtools_use_falloff_uniform",
                   "bmtools_use_dynamic_bind",
                   "bmtools_use_project_z",
                   "bmtools_use_negative_direction",
                   "bmtools_use_invert_cull",
                   "bmtools_use_positive_direction",
                   "bmtools_use_project_y",
                   "bmtools_use_project_x",
                   "bmtools_lock_z",
                   "bmtools_lock_x",
                   "bmtools_lock_y",
                   "bmtools_use_only_smooth",
                   "bmtools_use_pin_boundary",
                   "bmtools_use_normalized",
                   "bmtools_use_volume_preserve",
                   "bmtools_use_sparse_bind",
                   "bmtools_use_normal",
                   "bmtools_use_normal_y",
                   "bmtools_use_cyclic",
                   "bmtools_use_normal_z",
                   "bmtools_use_normal_x",
                   "bmtools_show_alive",
                   "bmtools_show_dead",
                   "bmtools_use_size",
                   "bmtools_show_unborn",
                   "bmtools_use_edge_cut",
                   "bmtools_use_spray",
                   "bmtools_invert_spray",
                   "bmtools_use_foam",
                   "bmtools_use_normals",
                   "bmtools_use_children",
                   "bmtools_use_preserve_shape",
                   "bmtools_use_path",
                   "bmtools_layers_vcol_select_src",
                   "bmtools_vert_mapping",
                   "bmtools_layers_vgroup_select_src",
                   "bmtools_layers_vgroup_select_dst",
                   "bmtools_layers_vcol_select_dst",
                   "bmtools_poly_mapping",
                   "bmtools_mix_mode",
                   "bmtools_data_types_edges",
                   "bmtools_layers_uv_select_src",
                   "bmtools_data_types_polys",
                   "bmtools_data_types_verts",
                   "bmtools_layers_uv_select_dst",
                   "bmtools_edge_mapping",
                   "bmtools_loop_mapping",
                   "bmtools_data_types_loops",
                   "bmtools_up_axis",
                   "bmtools_cache_format",
                   "bmtools_deform_mode",
                   "bmtools_play_mode",
                   "bmtools_interpolation",
                   "bmtools_forward_axis",
                   "bmtools_flip_axis",
                   "bmtools_time_mode",
                   "bmtools_read_data",
                   "bmtools_mode",
                   "bmtools_axis_v",
                   "bmtools_axis_u",
                   "bmtools_mask_tex_mapping",
                   "bmtools_mask_tex_use_channel",
                   "bmtools_falloff_type",
                   "bmtools_mix_set",
                   "bmtools_proximity_mode",
                   "bmtools_proximity_geometry",
                   "bmtools_fit_type",
                   "bmtools_face_strength_mode",
                   "bmtools_profile_type",
                   "bmtools_miter_inner",
                   "bmtools_limit_method",
                   "bmtools_miter_outer",
                   "bmtools_vmesh_method",
                   "bmtools_affect",
                   "bmtools_offset_type",
                   "bmtools_debug_options",
                   "bmtools_solver",
                   "bmtools_operation",
                   "bmtools_operand_type",
                   "bmtools_symmetry_axis",
                   "bmtools_delimit",
                   "bmtools_decimate_type",
                   "bmtools_uv_smooth",
                   "bmtools_boundary_smooth",
                   "bmtools_axis",
                   "bmtools_nonmanifold_thickness_mode",
                   "bmtools_solidify_mode",
                   "bmtools_nonmanifold_boundary_mode",
                   "bmtools_subdivision_type",
                   "bmtools_ngon_method",
                   "bmtools_quad_method",
                   "bmtools_resolution_mode",
                   "bmtools_cast_type",
                   "bmtools_deform_axis",
                   "bmtools_space",
                   "bmtools_direction",
                   "bmtools_texture_coords",
                   "bmtools_wrap_method",
                   "bmtools_wrap_mode",
                   "bmtools_cull_face",
                   "bmtools_deform_method",
                   "bmtools_smooth_type",
                   "bmtools_rest_source",
                   "bmtools_ui_type",
                   "bmtools_fluid_type",
                   "bmtools_spectrum",
                   "bmtools_geometry_mode",
                   "bmtools_ray_radius",
                   "bmtools_mix_factor",
                   "bmtools_islands_precision",
                   "bmtools_max_distance",
                   "bmtools_frame_scale",
                   "bmtools_eval_frame",
                   "bmtools_eval_time",
                   "bmtools_frame_start",
                   "bmtools_eval_factor",
                   "bmtools_factor",
                   "bmtools_velocity_scale",
                   "bmtools_mix_limit",
                   "bmtools_offset",
                   "bmtools_thresh",
                   "bmtools_aspect_y",
                   "bmtools_aspect_x",
                   "bmtools_scale_y",
                   "bmtools_scale_x",
                   "bmtools_rotation",
                   "bmtools_center",
                   "bmtools_scale",
                   "bmtools_mask_constant",
                   "bmtools_add_threshold",
                   "bmtools_default_weight",
                   "bmtools_remove_threshold",
                   "bmtools_default_weight_a",
                   "bmtools_default_weight_b",
                   "bmtools_max_dist",
                   "bmtools_min_dist",
                   "bmtools_relative_offset_displace",
                   "bmtools_constant_offset_displace",
                   "bmtools_fit_length",
                   "bmtools_merge_threshold",
                   "bmtools_offset_v",
                   "bmtools_offset_u",
                   "bmtools_angle_limit",
                   "bmtools_spread",
                   "bmtools_width",
                   "bmtools_width_pct",
                   "bmtools_profile",
                   "bmtools_double_threshold",
                   "bmtools_frame_duration",
                   "bmtools_vertex_group_factor",
                   "bmtools_ratio",
                   "bmtools_split_angle",
                   "bmtools_threshold",
                   "bmtools_mirror_offset_v",
                   "bmtools_bisect_threshold",
                   "bmtools_mirror_offset_u",
                   "bmtools_sharpness",
                   "bmtools_adaptivity",
                   "bmtools_voxel_size",
                   "bmtools_screw_offset",
                   "bmtools_angle",
                   "bmtools_branch_smoothing",
                   "bmtools_edge_crease_inner",
                   "bmtools_nonmanifold_merge_threshold",
                   "bmtools_thickness_vertex_group",
                   "bmtools_thickness",
                   "bmtools_edge_crease_rim",
                   "bmtools_bevel_convex",
                   "bmtools_thickness_clamp",
                   "bmtools_edge_crease_outer",
                   "bmtools_crease_weight",
                   "bmtools_size",
                   "bmtools_radius",
                   "bmtools_mid_level",
                   "bmtools_strength",
                   "bmtools_matrix_inverse",
                   "bmtools_falloff_radius",
                   "bmtools_project_limit",
                   "bmtools_limits",
                   "bmtools_lambda_border",
                   "bmtools_lambda_factor",
                   "bmtools_falloff",
                   "bmtools_damping_time",
                   "bmtools_lifetime",
                   "bmtools_narrowness",
                   "bmtools_time_offset",
                   "bmtools_start_position_y",
                   "bmtools_height",
                   "bmtools_start_position_x",
                   "bmtools_speed",
                   "bmtools_protect",
                   "bmtools_sharpen_peak_jonswap",
                   "bmtools_wave_scale_min",
                   "bmtools_wave_scale",
                   "bmtools_wave_alignment",
                   "bmtools_choppiness",
                   "bmtools_time",
                   "bmtools_damping",
                   "bmtools_wave_direction",
                   "bmtools_wind_velocity",
                   "bmtools_depth",
                   "bmtools_foam_coverage",
                   "bmtools_fetch_jonswap",
                   "bmtools_bake_foam_fade",
                   "bmtools_particle_amount",
                   "bmtools_random_rotation",
                   "bmtools_particle_offset",
                   "bmtools_random_position",
                   "bmtools_position",
                   "bmtools_weight",
                   "bmtools_projector_count",
                   "bmtools_count",
                   "bmtools_segments",
                   "bmtools_material",
                   "bmtools_seed",
                   "bmtools_iterations",
                   "bmtools_levels",
                   "bmtools_quality",
                   "bmtools_sculpt_levels",
                   "bmtools_render_levels",
                   "bmtools_octree_depth",
                   "bmtools_render_steps",
                   "bmtools_steps",
                   "bmtools_material_offset",
                   "bmtools_material_offset_rim",
                   "bmtools_min_vertices",
                   "bmtools_voxel_amount",
                   "bmtools_precision",
                   "bmtools_subsurf_levels",
                   "bmtools_resolution",
                   "bmtools_repeat_x",
                   "bmtools_spatial_size",
                   "bmtools_viewport_resolution",
                   "bmtools_frame_end",
                   "bmtools_repeat_y",
                   "bmtools_random_seed",
                   "bmtools_particle_system_index",
                   ]
    # }}}
    
    # Properties {{{
    
    # Name {{{
    bmtools_name: StringProperty(
        name="bmtools_name",
        maxlen=1,
        default='',
        )
    
    bmtools_name_shift: BoolProperty(
        name="bmtools_name_shift",
        default=False,
        )
    
    bmtools_name_ctl: BoolProperty(
        name="bmtools_name_ctl",
        default=False,
        )
    
    bmtools_name_alt: BoolProperty(
        name="bmtools_name_alt",
        default=False,
        )
    # }}}
    
    # Vertex Group {{{
    bmtools_vertex_group: StringProperty(
        name="bmtools_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_vertex_group_shift: BoolProperty(
        name="bmtools_vertex_group_shift",
        default=False,
        )
    
    bmtools_vertex_group_ctl: BoolProperty(
        name="bmtools_vertex_group_ctl",
        default=False,
        )
    
    bmtools_vertex_group_alt: BoolProperty(
        name="bmtools_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Filepath {{{
    bmtools_filepath: StringProperty(
        name="bmtools_filepath",
        maxlen=1,
        default='',
        )
    
    bmtools_filepath_shift: BoolProperty(
        name="bmtools_filepath_shift",
        default=False,
        )
    
    bmtools_filepath_ctl: BoolProperty(
        name="bmtools_filepath_ctl",
        default=False,
        )
    
    bmtools_filepath_alt: BoolProperty(
        name="bmtools_filepath_alt",
        default=False,
        )
    # }}}
    
    # Object Path {{{
    bmtools_object_path: StringProperty(
        name="bmtools_object_path",
        maxlen=1,
        default='',
        )
    
    bmtools_object_path_shift: BoolProperty(
        name="bmtools_object_path_shift",
        default=False,
        )
    
    bmtools_object_path_ctl: BoolProperty(
        name="bmtools_object_path_ctl",
        default=False,
        )
    
    bmtools_object_path_alt: BoolProperty(
        name="bmtools_object_path_alt",
        default=False,
        )
    # }}}
    
    # Uv Layer {{{
    bmtools_uv_layer: StringProperty(
        name="bmtools_uv_layer",
        maxlen=1,
        default='',
        )
    
    bmtools_uv_layer_shift: BoolProperty(
        name="bmtools_uv_layer_shift",
        default=False,
        )
    
    bmtools_uv_layer_ctl: BoolProperty(
        name="bmtools_uv_layer_ctl",
        default=False,
        )
    
    bmtools_uv_layer_alt: BoolProperty(
        name="bmtools_uv_layer_alt",
        default=False,
        )
    # }}}
    
    # Bone To {{{
    bmtools_bone_to: StringProperty(
        name="bmtools_bone_to",
        maxlen=1,
        default='',
        )
    
    bmtools_bone_to_shift: BoolProperty(
        name="bmtools_bone_to_shift",
        default=False,
        )
    
    bmtools_bone_to_ctl: BoolProperty(
        name="bmtools_bone_to_ctl",
        default=False,
        )
    
    bmtools_bone_to_alt: BoolProperty(
        name="bmtools_bone_to_alt",
        default=False,
        )
    # }}}
    
    # Bone From {{{
    bmtools_bone_from: StringProperty(
        name="bmtools_bone_from",
        maxlen=1,
        default='',
        )
    
    bmtools_bone_from_shift: BoolProperty(
        name="bmtools_bone_from_shift",
        default=False,
        )
    
    bmtools_bone_from_ctl: BoolProperty(
        name="bmtools_bone_from_ctl",
        default=False,
        )
    
    bmtools_bone_from_alt: BoolProperty(
        name="bmtools_bone_from_alt",
        default=False,
        )
    # }}}
    
    # Mask Vertex Group {{{
    bmtools_mask_vertex_group: StringProperty(
        name="bmtools_mask_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_vertex_group_shift: BoolProperty(
        name="bmtools_mask_vertex_group_shift",
        default=False,
        )
    
    bmtools_mask_vertex_group_ctl: BoolProperty(
        name="bmtools_mask_vertex_group_ctl",
        default=False,
        )
    
    bmtools_mask_vertex_group_alt: BoolProperty(
        name="bmtools_mask_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Mask Tex Map Bone {{{
    bmtools_mask_tex_map_bone: StringProperty(
        name="bmtools_mask_tex_map_bone",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_tex_map_bone_shift: BoolProperty(
        name="bmtools_mask_tex_map_bone_shift",
        default=False,
        )
    
    bmtools_mask_tex_map_bone_ctl: BoolProperty(
        name="bmtools_mask_tex_map_bone_ctl",
        default=False,
        )
    
    bmtools_mask_tex_map_bone_alt: BoolProperty(
        name="bmtools_mask_tex_map_bone_alt",
        default=False,
        )
    # }}}
    
    # Mask Tex Uv Layer {{{
    bmtools_mask_tex_uv_layer: StringProperty(
        name="bmtools_mask_tex_uv_layer",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_tex_uv_layer_shift: BoolProperty(
        name="bmtools_mask_tex_uv_layer_shift",
        default=False,
        )
    
    bmtools_mask_tex_uv_layer_ctl: BoolProperty(
        name="bmtools_mask_tex_uv_layer_ctl",
        default=False,
        )
    
    bmtools_mask_tex_uv_layer_alt: BoolProperty(
        name="bmtools_mask_tex_uv_layer_alt",
        default=False,
        )
    # }}}
    
    # Vertex Group A {{{
    bmtools_vertex_group_a: StringProperty(
        name="bmtools_vertex_group_a",
        maxlen=1,
        default='',
        )
    
    bmtools_vertex_group_a_shift: BoolProperty(
        name="bmtools_vertex_group_a_shift",
        default=False,
        )
    
    bmtools_vertex_group_a_ctl: BoolProperty(
        name="bmtools_vertex_group_a_ctl",
        default=False,
        )
    
    bmtools_vertex_group_a_alt: BoolProperty(
        name="bmtools_vertex_group_a_alt",
        default=False,
        )
    # }}}
    
    # Vertex Group B {{{
    bmtools_vertex_group_b: StringProperty(
        name="bmtools_vertex_group_b",
        maxlen=1,
        default='',
        )
    
    bmtools_vertex_group_b_shift: BoolProperty(
        name="bmtools_vertex_group_b_shift",
        default=False,
        )
    
    bmtools_vertex_group_b_ctl: BoolProperty(
        name="bmtools_vertex_group_b_ctl",
        default=False,
        )
    
    bmtools_vertex_group_b_alt: BoolProperty(
        name="bmtools_vertex_group_b_alt",
        default=False,
        )
    # }}}
    
    # Rim Vertex Group {{{
    bmtools_rim_vertex_group: StringProperty(
        name="bmtools_rim_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_rim_vertex_group_shift: BoolProperty(
        name="bmtools_rim_vertex_group_shift",
        default=False,
        )
    
    bmtools_rim_vertex_group_ctl: BoolProperty(
        name="bmtools_rim_vertex_group_ctl",
        default=False,
        )
    
    bmtools_rim_vertex_group_alt: BoolProperty(
        name="bmtools_rim_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Shell Vertex Group {{{
    bmtools_shell_vertex_group: StringProperty(
        name="bmtools_shell_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_shell_vertex_group_shift: BoolProperty(
        name="bmtools_shell_vertex_group_shift",
        default=False,
        )
    
    bmtools_shell_vertex_group_ctl: BoolProperty(
        name="bmtools_shell_vertex_group_ctl",
        default=False,
        )
    
    bmtools_shell_vertex_group_alt: BoolProperty(
        name="bmtools_shell_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Grid Name {{{
    bmtools_grid_name: StringProperty(
        name="bmtools_grid_name",
        maxlen=1,
        default='',
        )
    
    bmtools_grid_name_shift: BoolProperty(
        name="bmtools_grid_name_shift",
        default=False,
        )
    
    bmtools_grid_name_ctl: BoolProperty(
        name="bmtools_grid_name_ctl",
        default=False,
        )
    
    bmtools_grid_name_alt: BoolProperty(
        name="bmtools_grid_name_alt",
        default=False,
        )
    # }}}
    
    # Texture Coords Bone {{{
    bmtools_texture_coords_bone: StringProperty(
        name="bmtools_texture_coords_bone",
        maxlen=1,
        default='',
        )
    
    bmtools_texture_coords_bone_shift: BoolProperty(
        name="bmtools_texture_coords_bone_shift",
        default=False,
        )
    
    bmtools_texture_coords_bone_ctl: BoolProperty(
        name="bmtools_texture_coords_bone_ctl",
        default=False,
        )
    
    bmtools_texture_coords_bone_alt: BoolProperty(
        name="bmtools_texture_coords_bone_alt",
        default=False,
        )
    # }}}
    
    # Subtarget {{{
    bmtools_subtarget: StringProperty(
        name="bmtools_subtarget",
        maxlen=1,
        default='',
        )
    
    bmtools_subtarget_shift: BoolProperty(
        name="bmtools_subtarget_shift",
        default=False,
        )
    
    bmtools_subtarget_ctl: BoolProperty(
        name="bmtools_subtarget_ctl",
        default=False,
        )
    
    bmtools_subtarget_alt: BoolProperty(
        name="bmtools_subtarget_alt",
        default=False,
        )
    # }}}
    
    # Particle Uv {{{
    bmtools_particle_uv: StringProperty(
        name="bmtools_particle_uv",
        maxlen=1,
        default='',
        )
    
    bmtools_particle_uv_shift: BoolProperty(
        name="bmtools_particle_uv_shift",
        default=False,
        )
    
    bmtools_particle_uv_ctl: BoolProperty(
        name="bmtools_particle_uv_ctl",
        default=False,
        )
    
    bmtools_particle_uv_alt: BoolProperty(
        name="bmtools_particle_uv_alt",
        default=False,
        )
    # }}}
    
    # Foam Layer Name {{{
    bmtools_foam_layer_name: StringProperty(
        name="bmtools_foam_layer_name",
        maxlen=1,
        default='',
        )
    
    bmtools_foam_layer_name_shift: BoolProperty(
        name="bmtools_foam_layer_name_shift",
        default=False,
        )
    
    bmtools_foam_layer_name_ctl: BoolProperty(
        name="bmtools_foam_layer_name_ctl",
        default=False,
        )
    
    bmtools_foam_layer_name_alt: BoolProperty(
        name="bmtools_foam_layer_name_alt",
        default=False,
        )
    # }}}
    
    # Spray Layer Name {{{
    bmtools_spray_layer_name: StringProperty(
        name="bmtools_spray_layer_name",
        maxlen=1,
        default='',
        )
    
    bmtools_spray_layer_name_shift: BoolProperty(
        name="bmtools_spray_layer_name_shift",
        default=False,
        )
    
    bmtools_spray_layer_name_ctl: BoolProperty(
        name="bmtools_spray_layer_name_ctl",
        default=False,
        )
    
    bmtools_spray_layer_name_alt: BoolProperty(
        name="bmtools_spray_layer_name_alt",
        default=False,
        )
    # }}}
    
    # Value Layer Name {{{
    bmtools_value_layer_name: StringProperty(
        name="bmtools_value_layer_name",
        maxlen=1,
        default='',
        )
    
    bmtools_value_layer_name_shift: BoolProperty(
        name="bmtools_value_layer_name_shift",
        default=False,
        )
    
    bmtools_value_layer_name_ctl: BoolProperty(
        name="bmtools_value_layer_name_ctl",
        default=False,
        )
    
    bmtools_value_layer_name_alt: BoolProperty(
        name="bmtools_value_layer_name_alt",
        default=False,
        )
    # }}}
    
    # Index Layer Name {{{
    bmtools_index_layer_name: StringProperty(
        name="bmtools_index_layer_name",
        maxlen=1,
        default='',
        )
    
    bmtools_index_layer_name_shift: BoolProperty(
        name="bmtools_index_layer_name_shift",
        default=False,
        )
    
    bmtools_index_layer_name_ctl: BoolProperty(
        name="bmtools_index_layer_name_ctl",
        default=False,
        )
    
    bmtools_index_layer_name_alt: BoolProperty(
        name="bmtools_index_layer_name_alt",
        default=False,
        )
    # }}}
    
    # Use Apply On Spline {{{
    bmtools_use_apply_on_spline: StringProperty(
        name="bmtools_use_apply_on_spline",
        maxlen=1,
        default='',
        )
    
    bmtools_use_apply_on_spline_shift: BoolProperty(
        name="bmtools_use_apply_on_spline_shift",
        default=False,
        )
    
    bmtools_use_apply_on_spline_ctl: BoolProperty(
        name="bmtools_use_apply_on_spline_ctl",
        default=False,
        )
    
    bmtools_use_apply_on_spline_alt: BoolProperty(
        name="bmtools_use_apply_on_spline_alt",
        default=False,
        )
    # }}}
    
    # Use Poly Data {{{
    bmtools_use_poly_data: StringProperty(
        name="bmtools_use_poly_data",
        maxlen=1,
        default='',
        )
    
    bmtools_use_poly_data_shift: BoolProperty(
        name="bmtools_use_poly_data_shift",
        default=False,
        )
    
    bmtools_use_poly_data_ctl: BoolProperty(
        name="bmtools_use_poly_data_ctl",
        default=False,
        )
    
    bmtools_use_poly_data_alt: BoolProperty(
        name="bmtools_use_poly_data_alt",
        default=False,
        )
    # }}}
    
    # Show Render {{{
    bmtools_show_render: StringProperty(
        name="bmtools_show_render",
        maxlen=1,
        default='',
        )
    
    bmtools_show_render_shift: BoolProperty(
        name="bmtools_show_render_shift",
        default=False,
        )
    
    bmtools_show_render_ctl: BoolProperty(
        name="bmtools_show_render_ctl",
        default=False,
        )
    
    bmtools_show_render_alt: BoolProperty(
        name="bmtools_show_render_alt",
        default=False,
        )
    # }}}
    
    # Show In Editmode {{{
    bmtools_show_in_editmode: StringProperty(
        name="bmtools_show_in_editmode",
        maxlen=1,
        default='',
        )
    
    bmtools_show_in_editmode_shift: BoolProperty(
        name="bmtools_show_in_editmode_shift",
        default=False,
        )
    
    bmtools_show_in_editmode_ctl: BoolProperty(
        name="bmtools_show_in_editmode_ctl",
        default=False,
        )
    
    bmtools_show_in_editmode_alt: BoolProperty(
        name="bmtools_show_in_editmode_alt",
        default=False,
        )
    # }}}
    
    # Use Edge Data {{{
    bmtools_use_edge_data: StringProperty(
        name="bmtools_use_edge_data",
        maxlen=1,
        default='',
        )
    
    bmtools_use_edge_data_shift: BoolProperty(
        name="bmtools_use_edge_data_shift",
        default=False,
        )
    
    bmtools_use_edge_data_ctl: BoolProperty(
        name="bmtools_use_edge_data_ctl",
        default=False,
        )
    
    bmtools_use_edge_data_alt: BoolProperty(
        name="bmtools_use_edge_data_alt",
        default=False,
        )
    # }}}
    
    # Use Loop Data {{{
    bmtools_use_loop_data: StringProperty(
        name="bmtools_use_loop_data",
        maxlen=1,
        default='',
        )
    
    bmtools_use_loop_data_shift: BoolProperty(
        name="bmtools_use_loop_data_shift",
        default=False,
        )
    
    bmtools_use_loop_data_ctl: BoolProperty(
        name="bmtools_use_loop_data_ctl",
        default=False,
        )
    
    bmtools_use_loop_data_alt: BoolProperty(
        name="bmtools_use_loop_data_alt",
        default=False,
        )
    # }}}
    
    # Use Vert Data {{{
    bmtools_use_vert_data: StringProperty(
        name="bmtools_use_vert_data",
        maxlen=1,
        default='',
        )
    
    bmtools_use_vert_data_shift: BoolProperty(
        name="bmtools_use_vert_data_shift",
        default=False,
        )
    
    bmtools_use_vert_data_ctl: BoolProperty(
        name="bmtools_use_vert_data_ctl",
        default=False,
        )
    
    bmtools_use_vert_data_alt: BoolProperty(
        name="bmtools_use_vert_data_alt",
        default=False,
        )
    # }}}
    
    # Use Object Transform {{{
    bmtools_use_object_transform: StringProperty(
        name="bmtools_use_object_transform",
        maxlen=1,
        default='',
        )
    
    bmtools_use_object_transform_shift: BoolProperty(
        name="bmtools_use_object_transform_shift",
        default=False,
        )
    
    bmtools_use_object_transform_ctl: BoolProperty(
        name="bmtools_use_object_transform_ctl",
        default=False,
        )
    
    bmtools_use_object_transform_alt: BoolProperty(
        name="bmtools_use_object_transform_alt",
        default=False,
        )
    # }}}
    
    # Use Max Distance {{{
    bmtools_use_max_distance: StringProperty(
        name="bmtools_use_max_distance",
        maxlen=1,
        default='',
        )
    
    bmtools_use_max_distance_shift: BoolProperty(
        name="bmtools_use_max_distance_shift",
        default=False,
        )
    
    bmtools_use_max_distance_ctl: BoolProperty(
        name="bmtools_use_max_distance_ctl",
        default=False,
        )
    
    bmtools_use_max_distance_alt: BoolProperty(
        name="bmtools_use_max_distance_alt",
        default=False,
        )
    # }}}
    
    # Show Expanded {{{
    bmtools_show_expanded: StringProperty(
        name="bmtools_show_expanded",
        maxlen=1,
        default='',
        )
    
    bmtools_show_expanded_shift: BoolProperty(
        name="bmtools_show_expanded_shift",
        default=False,
        )
    
    bmtools_show_expanded_ctl: BoolProperty(
        name="bmtools_show_expanded_ctl",
        default=False,
        )
    
    bmtools_show_expanded_alt: BoolProperty(
        name="bmtools_show_expanded_alt",
        default=False,
        )
    # }}}
    
    # Show Viewport {{{
    bmtools_show_viewport: StringProperty(
        name="bmtools_show_viewport",
        maxlen=1,
        default='',
        )
    
    bmtools_show_viewport_shift: BoolProperty(
        name="bmtools_show_viewport_shift",
        default=False,
        )
    
    bmtools_show_viewport_ctl: BoolProperty(
        name="bmtools_show_viewport_ctl",
        default=False,
        )
    
    bmtools_show_viewport_alt: BoolProperty(
        name="bmtools_show_viewport_alt",
        default=False,
        )
    # }}}
    
    # Is Active {{{
    bmtools_is_active: StringProperty(
        name="bmtools_is_active",
        maxlen=1,
        default='',
        )
    
    bmtools_is_active_shift: BoolProperty(
        name="bmtools_is_active_shift",
        default=False,
        )
    
    bmtools_is_active_ctl: BoolProperty(
        name="bmtools_is_active_ctl",
        default=False,
        )
    
    bmtools_is_active_alt: BoolProperty(
        name="bmtools_is_active_alt",
        default=False,
        )
    # }}}
    
    # Show On Cage {{{
    bmtools_show_on_cage: StringProperty(
        name="bmtools_show_on_cage",
        maxlen=1,
        default='',
        )
    
    bmtools_show_on_cage_shift: BoolProperty(
        name="bmtools_show_on_cage_shift",
        default=False,
        )
    
    bmtools_show_on_cage_ctl: BoolProperty(
        name="bmtools_show_on_cage_ctl",
        default=False,
        )
    
    bmtools_show_on_cage_alt: BoolProperty(
        name="bmtools_show_on_cage_alt",
        default=False,
        )
    # }}}
    
    # Invert Vertex Group {{{
    bmtools_invert_vertex_group: StringProperty(
        name="bmtools_invert_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_vertex_group_shift: BoolProperty(
        name="bmtools_invert_vertex_group_shift",
        default=False,
        )
    
    bmtools_invert_vertex_group_ctl: BoolProperty(
        name="bmtools_invert_vertex_group_ctl",
        default=False,
        )
    
    bmtools_invert_vertex_group_alt: BoolProperty(
        name="bmtools_invert_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Use Vertex Interpolation {{{
    bmtools_use_vertex_interpolation: StringProperty(
        name="bmtools_use_vertex_interpolation",
        maxlen=1,
        default='',
        )
    
    bmtools_use_vertex_interpolation_shift: BoolProperty(
        name="bmtools_use_vertex_interpolation_shift",
        default=False,
        )
    
    bmtools_use_vertex_interpolation_ctl: BoolProperty(
        name="bmtools_use_vertex_interpolation_ctl",
        default=False,
        )
    
    bmtools_use_vertex_interpolation_alt: BoolProperty(
        name="bmtools_use_vertex_interpolation_alt",
        default=False,
        )
    # }}}
    
    # Use Direction Parallel {{{
    bmtools_use_direction_parallel: StringProperty(
        name="bmtools_use_direction_parallel",
        maxlen=1,
        default='',
        )
    
    bmtools_use_direction_parallel_shift: BoolProperty(
        name="bmtools_use_direction_parallel_shift",
        default=False,
        )
    
    bmtools_use_direction_parallel_ctl: BoolProperty(
        name="bmtools_use_direction_parallel_ctl",
        default=False,
        )
    
    bmtools_use_direction_parallel_alt: BoolProperty(
        name="bmtools_use_direction_parallel_alt",
        default=False,
        )
    # }}}
    
    # No Polynors Fix {{{
    bmtools_no_polynors_fix: StringProperty(
        name="bmtools_no_polynors_fix",
        maxlen=1,
        default='',
        )
    
    bmtools_no_polynors_fix_shift: BoolProperty(
        name="bmtools_no_polynors_fix_shift",
        default=False,
        )
    
    bmtools_no_polynors_fix_ctl: BoolProperty(
        name="bmtools_no_polynors_fix_ctl",
        default=False,
        )
    
    bmtools_no_polynors_fix_alt: BoolProperty(
        name="bmtools_no_polynors_fix_alt",
        default=False,
        )
    # }}}
    
    # Keep Sharp {{{
    bmtools_keep_sharp: StringProperty(
        name="bmtools_keep_sharp",
        maxlen=1,
        default='',
        )
    
    bmtools_keep_sharp_shift: BoolProperty(
        name="bmtools_keep_sharp_shift",
        default=False,
        )
    
    bmtools_keep_sharp_ctl: BoolProperty(
        name="bmtools_keep_sharp_ctl",
        default=False,
        )
    
    bmtools_keep_sharp_alt: BoolProperty(
        name="bmtools_keep_sharp_alt",
        default=False,
        )
    # }}}
    
    # Use Face Influence {{{
    bmtools_use_face_influence: StringProperty(
        name="bmtools_use_face_influence",
        maxlen=1,
        default='',
        )
    
    bmtools_use_face_influence_shift: BoolProperty(
        name="bmtools_use_face_influence_shift",
        default=False,
        )
    
    bmtools_use_face_influence_ctl: BoolProperty(
        name="bmtools_use_face_influence_ctl",
        default=False,
        )
    
    bmtools_use_face_influence_alt: BoolProperty(
        name="bmtools_use_face_influence_alt",
        default=False,
        )
    # }}}
    
    # Use Add {{{
    bmtools_use_add: StringProperty(
        name="bmtools_use_add",
        maxlen=1,
        default='',
        )
    
    bmtools_use_add_shift: BoolProperty(
        name="bmtools_use_add_shift",
        default=False,
        )
    
    bmtools_use_add_ctl: BoolProperty(
        name="bmtools_use_add_ctl",
        default=False,
        )
    
    bmtools_use_add_alt: BoolProperty(
        name="bmtools_use_add_alt",
        default=False,
        )
    # }}}
    
    # Invert Falloff {{{
    bmtools_invert_falloff: StringProperty(
        name="bmtools_invert_falloff",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_falloff_shift: BoolProperty(
        name="bmtools_invert_falloff_shift",
        default=False,
        )
    
    bmtools_invert_falloff_ctl: BoolProperty(
        name="bmtools_invert_falloff_ctl",
        default=False,
        )
    
    bmtools_invert_falloff_alt: BoolProperty(
        name="bmtools_invert_falloff_alt",
        default=False,
        )
    # }}}
    
    # Normalize {{{
    bmtools_normalize: StringProperty(
        name="bmtools_normalize",
        maxlen=1,
        default='',
        )
    
    bmtools_normalize_shift: BoolProperty(
        name="bmtools_normalize_shift",
        default=False,
        )
    
    bmtools_normalize_ctl: BoolProperty(
        name="bmtools_normalize_ctl",
        default=False,
        )
    
    bmtools_normalize_alt: BoolProperty(
        name="bmtools_normalize_alt",
        default=False,
        )
    # }}}
    
    # Use Remove {{{
    bmtools_use_remove: StringProperty(
        name="bmtools_use_remove",
        maxlen=1,
        default='',
        )
    
    bmtools_use_remove_shift: BoolProperty(
        name="bmtools_use_remove_shift",
        default=False,
        )
    
    bmtools_use_remove_ctl: BoolProperty(
        name="bmtools_use_remove_ctl",
        default=False,
        )
    
    bmtools_use_remove_alt: BoolProperty(
        name="bmtools_use_remove_alt",
        default=False,
        )
    # }}}
    
    # Invert Mask Vertex Group {{{
    bmtools_invert_mask_vertex_group: StringProperty(
        name="bmtools_invert_mask_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_mask_vertex_group_shift: BoolProperty(
        name="bmtools_invert_mask_vertex_group_shift",
        default=False,
        )
    
    bmtools_invert_mask_vertex_group_ctl: BoolProperty(
        name="bmtools_invert_mask_vertex_group_ctl",
        default=False,
        )
    
    bmtools_invert_mask_vertex_group_alt: BoolProperty(
        name="bmtools_invert_mask_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Invert Vertex Group A {{{
    bmtools_invert_vertex_group_a: StringProperty(
        name="bmtools_invert_vertex_group_a",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_vertex_group_a_shift: BoolProperty(
        name="bmtools_invert_vertex_group_a_shift",
        default=False,
        )
    
    bmtools_invert_vertex_group_a_ctl: BoolProperty(
        name="bmtools_invert_vertex_group_a_ctl",
        default=False,
        )
    
    bmtools_invert_vertex_group_a_alt: BoolProperty(
        name="bmtools_invert_vertex_group_a_alt",
        default=False,
        )
    # }}}
    
    # Invert Vertex Group B {{{
    bmtools_invert_vertex_group_b: StringProperty(
        name="bmtools_invert_vertex_group_b",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_vertex_group_b_shift: BoolProperty(
        name="bmtools_invert_vertex_group_b_shift",
        default=False,
        )
    
    bmtools_invert_vertex_group_b_ctl: BoolProperty(
        name="bmtools_invert_vertex_group_b_ctl",
        default=False,
        )
    
    bmtools_invert_vertex_group_b_alt: BoolProperty(
        name="bmtools_invert_vertex_group_b_alt",
        default=False,
        )
    # }}}
    
    # Use Object Offset {{{
    bmtools_use_object_offset: StringProperty(
        name="bmtools_use_object_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_use_object_offset_shift: BoolProperty(
        name="bmtools_use_object_offset_shift",
        default=False,
        )
    
    bmtools_use_object_offset_ctl: BoolProperty(
        name="bmtools_use_object_offset_ctl",
        default=False,
        )
    
    bmtools_use_object_offset_alt: BoolProperty(
        name="bmtools_use_object_offset_alt",
        default=False,
        )
    # }}}
    
    # Use Merge Vertices {{{
    bmtools_use_merge_vertices: StringProperty(
        name="bmtools_use_merge_vertices",
        maxlen=1,
        default='',
        )
    
    bmtools_use_merge_vertices_shift: BoolProperty(
        name="bmtools_use_merge_vertices_shift",
        default=False,
        )
    
    bmtools_use_merge_vertices_ctl: BoolProperty(
        name="bmtools_use_merge_vertices_ctl",
        default=False,
        )
    
    bmtools_use_merge_vertices_alt: BoolProperty(
        name="bmtools_use_merge_vertices_alt",
        default=False,
        )
    # }}}
    
    # Use Constant Offset {{{
    bmtools_use_constant_offset: StringProperty(
        name="bmtools_use_constant_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_use_constant_offset_shift: BoolProperty(
        name="bmtools_use_constant_offset_shift",
        default=False,
        )
    
    bmtools_use_constant_offset_ctl: BoolProperty(
        name="bmtools_use_constant_offset_ctl",
        default=False,
        )
    
    bmtools_use_constant_offset_alt: BoolProperty(
        name="bmtools_use_constant_offset_alt",
        default=False,
        )
    # }}}
    
    # Use Merge Vertices Cap {{{
    bmtools_use_merge_vertices_cap: StringProperty(
        name="bmtools_use_merge_vertices_cap",
        maxlen=1,
        default='',
        )
    
    bmtools_use_merge_vertices_cap_shift: BoolProperty(
        name="bmtools_use_merge_vertices_cap_shift",
        default=False,
        )
    
    bmtools_use_merge_vertices_cap_ctl: BoolProperty(
        name="bmtools_use_merge_vertices_cap_ctl",
        default=False,
        )
    
    bmtools_use_merge_vertices_cap_alt: BoolProperty(
        name="bmtools_use_merge_vertices_cap_alt",
        default=False,
        )
    # }}}
    
    # Use Relative Offset {{{
    bmtools_use_relative_offset: StringProperty(
        name="bmtools_use_relative_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_use_relative_offset_shift: BoolProperty(
        name="bmtools_use_relative_offset_shift",
        default=False,
        )
    
    bmtools_use_relative_offset_ctl: BoolProperty(
        name="bmtools_use_relative_offset_ctl",
        default=False,
        )
    
    bmtools_use_relative_offset_alt: BoolProperty(
        name="bmtools_use_relative_offset_alt",
        default=False,
        )
    # }}}
    
    # Use Clamp Overlap {{{
    bmtools_use_clamp_overlap: StringProperty(
        name="bmtools_use_clamp_overlap",
        maxlen=1,
        default='',
        )
    
    bmtools_use_clamp_overlap_shift: BoolProperty(
        name="bmtools_use_clamp_overlap_shift",
        default=False,
        )
    
    bmtools_use_clamp_overlap_ctl: BoolProperty(
        name="bmtools_use_clamp_overlap_ctl",
        default=False,
        )
    
    bmtools_use_clamp_overlap_alt: BoolProperty(
        name="bmtools_use_clamp_overlap_alt",
        default=False,
        )
    # }}}
    
    # Loop Slide {{{
    bmtools_loop_slide: StringProperty(
        name="bmtools_loop_slide",
        maxlen=1,
        default='',
        )
    
    bmtools_loop_slide_shift: BoolProperty(
        name="bmtools_loop_slide_shift",
        default=False,
        )
    
    bmtools_loop_slide_ctl: BoolProperty(
        name="bmtools_loop_slide_ctl",
        default=False,
        )
    
    bmtools_loop_slide_alt: BoolProperty(
        name="bmtools_loop_slide_alt",
        default=False,
        )
    # }}}
    
    # Mark Sharp {{{
    bmtools_mark_sharp: StringProperty(
        name="bmtools_mark_sharp",
        maxlen=1,
        default='',
        )
    
    bmtools_mark_sharp_shift: BoolProperty(
        name="bmtools_mark_sharp_shift",
        default=False,
        )
    
    bmtools_mark_sharp_ctl: BoolProperty(
        name="bmtools_mark_sharp_ctl",
        default=False,
        )
    
    bmtools_mark_sharp_alt: BoolProperty(
        name="bmtools_mark_sharp_alt",
        default=False,
        )
    # }}}
    
    # Mark Seam {{{
    bmtools_mark_seam: StringProperty(
        name="bmtools_mark_seam",
        maxlen=1,
        default='',
        )
    
    bmtools_mark_seam_shift: BoolProperty(
        name="bmtools_mark_seam_shift",
        default=False,
        )
    
    bmtools_mark_seam_ctl: BoolProperty(
        name="bmtools_mark_seam_ctl",
        default=False,
        )
    
    bmtools_mark_seam_alt: BoolProperty(
        name="bmtools_mark_seam_alt",
        default=False,
        )
    # }}}
    
    # Harden Normals {{{
    bmtools_harden_normals: StringProperty(
        name="bmtools_harden_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_harden_normals_shift: BoolProperty(
        name="bmtools_harden_normals_shift",
        default=False,
        )
    
    bmtools_harden_normals_ctl: BoolProperty(
        name="bmtools_harden_normals_ctl",
        default=False,
        )
    
    bmtools_harden_normals_alt: BoolProperty(
        name="bmtools_harden_normals_alt",
        default=False,
        )
    # }}}
    
    # Use Hole Tolerant {{{
    bmtools_use_hole_tolerant: StringProperty(
        name="bmtools_use_hole_tolerant",
        maxlen=1,
        default='',
        )
    
    bmtools_use_hole_tolerant_shift: BoolProperty(
        name="bmtools_use_hole_tolerant_shift",
        default=False,
        )
    
    bmtools_use_hole_tolerant_ctl: BoolProperty(
        name="bmtools_use_hole_tolerant_ctl",
        default=False,
        )
    
    bmtools_use_hole_tolerant_alt: BoolProperty(
        name="bmtools_use_hole_tolerant_alt",
        default=False,
        )
    # }}}
    
    # Use Self {{{
    bmtools_use_self: StringProperty(
        name="bmtools_use_self",
        maxlen=1,
        default='',
        )
    
    bmtools_use_self_shift: BoolProperty(
        name="bmtools_use_self_shift",
        default=False,
        )
    
    bmtools_use_self_ctl: BoolProperty(
        name="bmtools_use_self_ctl",
        default=False,
        )
    
    bmtools_use_self_alt: BoolProperty(
        name="bmtools_use_self_alt",
        default=False,
        )
    # }}}
    
    # Use Random Order {{{
    bmtools_use_random_order: StringProperty(
        name="bmtools_use_random_order",
        maxlen=1,
        default='',
        )
    
    bmtools_use_random_order_shift: BoolProperty(
        name="bmtools_use_random_order_shift",
        default=False,
        )
    
    bmtools_use_random_order_ctl: BoolProperty(
        name="bmtools_use_random_order_ctl",
        default=False,
        )
    
    bmtools_use_random_order_alt: BoolProperty(
        name="bmtools_use_random_order_alt",
        default=False,
        )
    # }}}
    
    # Use Reverse {{{
    bmtools_use_reverse: StringProperty(
        name="bmtools_use_reverse",
        maxlen=1,
        default='',
        )
    
    bmtools_use_reverse_shift: BoolProperty(
        name="bmtools_use_reverse_shift",
        default=False,
        )
    
    bmtools_use_reverse_ctl: BoolProperty(
        name="bmtools_use_reverse_ctl",
        default=False,
        )
    
    bmtools_use_reverse_alt: BoolProperty(
        name="bmtools_use_reverse_alt",
        default=False,
        )
    # }}}
    
    # Use Collapse Triangulate {{{
    bmtools_use_collapse_triangulate: StringProperty(
        name="bmtools_use_collapse_triangulate",
        maxlen=1,
        default='',
        )
    
    bmtools_use_collapse_triangulate_shift: BoolProperty(
        name="bmtools_use_collapse_triangulate_shift",
        default=False,
        )
    
    bmtools_use_collapse_triangulate_ctl: BoolProperty(
        name="bmtools_use_collapse_triangulate_ctl",
        default=False,
        )
    
    bmtools_use_collapse_triangulate_alt: BoolProperty(
        name="bmtools_use_collapse_triangulate_alt",
        default=False,
        )
    # }}}
    
    # Use Dissolve Boundaries {{{
    bmtools_use_dissolve_boundaries: StringProperty(
        name="bmtools_use_dissolve_boundaries",
        maxlen=1,
        default='',
        )
    
    bmtools_use_dissolve_boundaries_shift: BoolProperty(
        name="bmtools_use_dissolve_boundaries_shift",
        default=False,
        )
    
    bmtools_use_dissolve_boundaries_ctl: BoolProperty(
        name="bmtools_use_dissolve_boundaries_ctl",
        default=False,
        )
    
    bmtools_use_dissolve_boundaries_alt: BoolProperty(
        name="bmtools_use_dissolve_boundaries_alt",
        default=False,
        )
    # }}}
    
    # Use Symmetry {{{
    bmtools_use_symmetry: StringProperty(
        name="bmtools_use_symmetry",
        maxlen=1,
        default='',
        )
    
    bmtools_use_symmetry_shift: BoolProperty(
        name="bmtools_use_symmetry_shift",
        default=False,
        )
    
    bmtools_use_symmetry_ctl: BoolProperty(
        name="bmtools_use_symmetry_ctl",
        default=False,
        )
    
    bmtools_use_symmetry_alt: BoolProperty(
        name="bmtools_use_symmetry_alt",
        default=False,
        )
    # }}}
    
    # Use Edge Sharp {{{
    bmtools_use_edge_sharp: StringProperty(
        name="bmtools_use_edge_sharp",
        maxlen=1,
        default='',
        )
    
    bmtools_use_edge_sharp_shift: BoolProperty(
        name="bmtools_use_edge_sharp_shift",
        default=False,
        )
    
    bmtools_use_edge_sharp_ctl: BoolProperty(
        name="bmtools_use_edge_sharp_ctl",
        default=False,
        )
    
    bmtools_use_edge_sharp_alt: BoolProperty(
        name="bmtools_use_edge_sharp_alt",
        default=False,
        )
    # }}}
    
    # Use Edge Angle {{{
    bmtools_use_edge_angle: StringProperty(
        name="bmtools_use_edge_angle",
        maxlen=1,
        default='',
        )
    
    bmtools_use_edge_angle_shift: BoolProperty(
        name="bmtools_use_edge_angle_shift",
        default=False,
        )
    
    bmtools_use_edge_angle_ctl: BoolProperty(
        name="bmtools_use_edge_angle_ctl",
        default=False,
        )
    
    bmtools_use_edge_angle_alt: BoolProperty(
        name="bmtools_use_edge_angle_alt",
        default=False,
        )
    # }}}
    
    # Use Smooth {{{
    bmtools_use_smooth: StringProperty(
        name="bmtools_use_smooth",
        maxlen=1,
        default='',
        )
    
    bmtools_use_smooth_shift: BoolProperty(
        name="bmtools_use_smooth_shift",
        default=False,
        )
    
    bmtools_use_smooth_ctl: BoolProperty(
        name="bmtools_use_smooth_ctl",
        default=False,
        )
    
    bmtools_use_smooth_alt: BoolProperty(
        name="bmtools_use_smooth_alt",
        default=False,
        )
    # }}}
    
    # Use Mirror Merge {{{
    bmtools_use_mirror_merge: StringProperty(
        name="bmtools_use_mirror_merge",
        maxlen=1,
        default='',
        )
    
    bmtools_use_mirror_merge_shift: BoolProperty(
        name="bmtools_use_mirror_merge_shift",
        default=False,
        )
    
    bmtools_use_mirror_merge_ctl: BoolProperty(
        name="bmtools_use_mirror_merge_ctl",
        default=False,
        )
    
    bmtools_use_mirror_merge_alt: BoolProperty(
        name="bmtools_use_mirror_merge_alt",
        default=False,
        )
    # }}}
    
    # Use Mirror V {{{
    bmtools_use_mirror_v: StringProperty(
        name="bmtools_use_mirror_v",
        maxlen=1,
        default='',
        )
    
    bmtools_use_mirror_v_shift: BoolProperty(
        name="bmtools_use_mirror_v_shift",
        default=False,
        )
    
    bmtools_use_mirror_v_ctl: BoolProperty(
        name="bmtools_use_mirror_v_ctl",
        default=False,
        )
    
    bmtools_use_mirror_v_alt: BoolProperty(
        name="bmtools_use_mirror_v_alt",
        default=False,
        )
    # }}}
    
    # Use Mirror Udim {{{
    bmtools_use_mirror_udim: StringProperty(
        name="bmtools_use_mirror_udim",
        maxlen=1,
        default='',
        )
    
    bmtools_use_mirror_udim_shift: BoolProperty(
        name="bmtools_use_mirror_udim_shift",
        default=False,
        )
    
    bmtools_use_mirror_udim_ctl: BoolProperty(
        name="bmtools_use_mirror_udim_ctl",
        default=False,
        )
    
    bmtools_use_mirror_udim_alt: BoolProperty(
        name="bmtools_use_mirror_udim_alt",
        default=False,
        )
    # }}}
    
    # Use Bisect Flip Axis {{{
    bmtools_use_bisect_flip_axis: StringProperty(
        name="bmtools_use_bisect_flip_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_use_bisect_flip_axis_shift: BoolProperty(
        name="bmtools_use_bisect_flip_axis_shift",
        default=False,
        )
    
    bmtools_use_bisect_flip_axis_ctl: BoolProperty(
        name="bmtools_use_bisect_flip_axis_ctl",
        default=False,
        )
    
    bmtools_use_bisect_flip_axis_alt: BoolProperty(
        name="bmtools_use_bisect_flip_axis_alt",
        default=False,
        )
    # }}}
    
    # Use Mirror U {{{
    bmtools_use_mirror_u: StringProperty(
        name="bmtools_use_mirror_u",
        maxlen=1,
        default='',
        )
    
    bmtools_use_mirror_u_shift: BoolProperty(
        name="bmtools_use_mirror_u_shift",
        default=False,
        )
    
    bmtools_use_mirror_u_ctl: BoolProperty(
        name="bmtools_use_mirror_u_ctl",
        default=False,
        )
    
    bmtools_use_mirror_u_alt: BoolProperty(
        name="bmtools_use_mirror_u_alt",
        default=False,
        )
    # }}}
    
    # Use Bisect Axis {{{
    bmtools_use_bisect_axis: StringProperty(
        name="bmtools_use_bisect_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_use_bisect_axis_shift: BoolProperty(
        name="bmtools_use_bisect_axis_shift",
        default=False,
        )
    
    bmtools_use_bisect_axis_ctl: BoolProperty(
        name="bmtools_use_bisect_axis_ctl",
        default=False,
        )
    
    bmtools_use_bisect_axis_alt: BoolProperty(
        name="bmtools_use_bisect_axis_alt",
        default=False,
        )
    # }}}
    
    # Use Mirror Vertex Groups {{{
    bmtools_use_mirror_vertex_groups: StringProperty(
        name="bmtools_use_mirror_vertex_groups",
        maxlen=1,
        default='',
        )
    
    bmtools_use_mirror_vertex_groups_shift: BoolProperty(
        name="bmtools_use_mirror_vertex_groups_shift",
        default=False,
        )
    
    bmtools_use_mirror_vertex_groups_ctl: BoolProperty(
        name="bmtools_use_mirror_vertex_groups_ctl",
        default=False,
        )
    
    bmtools_use_mirror_vertex_groups_alt: BoolProperty(
        name="bmtools_use_mirror_vertex_groups_alt",
        default=False,
        )
    # }}}
    
    # Use Axis {{{
    bmtools_use_axis: StringProperty(
        name="bmtools_use_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_use_axis_shift: BoolProperty(
        name="bmtools_use_axis_shift",
        default=False,
        )
    
    bmtools_use_axis_ctl: BoolProperty(
        name="bmtools_use_axis_ctl",
        default=False,
        )
    
    bmtools_use_axis_alt: BoolProperty(
        name="bmtools_use_axis_alt",
        default=False,
        )
    # }}}
    
    # Use Clip {{{
    bmtools_use_clip: StringProperty(
        name="bmtools_use_clip",
        maxlen=1,
        default='',
        )
    
    bmtools_use_clip_shift: BoolProperty(
        name="bmtools_use_clip_shift",
        default=False,
        )
    
    bmtools_use_clip_ctl: BoolProperty(
        name="bmtools_use_clip_ctl",
        default=False,
        )
    
    bmtools_use_clip_alt: BoolProperty(
        name="bmtools_use_clip_alt",
        default=False,
        )
    # }}}
    
    # Use Creases {{{
    bmtools_use_creases: StringProperty(
        name="bmtools_use_creases",
        maxlen=1,
        default='',
        )
    
    bmtools_use_creases_shift: BoolProperty(
        name="bmtools_use_creases_shift",
        default=False,
        )
    
    bmtools_use_creases_ctl: BoolProperty(
        name="bmtools_use_creases_ctl",
        default=False,
        )
    
    bmtools_use_creases_alt: BoolProperty(
        name="bmtools_use_creases_alt",
        default=False,
        )
    # }}}
    
    # Use Sculpt Base Mesh {{{
    bmtools_use_sculpt_base_mesh: StringProperty(
        name="bmtools_use_sculpt_base_mesh",
        maxlen=1,
        default='',
        )
    
    bmtools_use_sculpt_base_mesh_shift: BoolProperty(
        name="bmtools_use_sculpt_base_mesh_shift",
        default=False,
        )
    
    bmtools_use_sculpt_base_mesh_ctl: BoolProperty(
        name="bmtools_use_sculpt_base_mesh_ctl",
        default=False,
        )
    
    bmtools_use_sculpt_base_mesh_alt: BoolProperty(
        name="bmtools_use_sculpt_base_mesh_alt",
        default=False,
        )
    # }}}
    
    # Show Only Control Edges {{{
    bmtools_show_only_control_edges: StringProperty(
        name="bmtools_show_only_control_edges",
        maxlen=1,
        default='',
        )
    
    bmtools_show_only_control_edges_shift: BoolProperty(
        name="bmtools_show_only_control_edges_shift",
        default=False,
        )
    
    bmtools_show_only_control_edges_ctl: BoolProperty(
        name="bmtools_show_only_control_edges_ctl",
        default=False,
        )
    
    bmtools_show_only_control_edges_alt: BoolProperty(
        name="bmtools_show_only_control_edges_alt",
        default=False,
        )
    # }}}
    
    # Use Custom Normals {{{
    bmtools_use_custom_normals: StringProperty(
        name="bmtools_use_custom_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_use_custom_normals_shift: BoolProperty(
        name="bmtools_use_custom_normals_shift",
        default=False,
        )
    
    bmtools_use_custom_normals_ctl: BoolProperty(
        name="bmtools_use_custom_normals_ctl",
        default=False,
        )
    
    bmtools_use_custom_normals_alt: BoolProperty(
        name="bmtools_use_custom_normals_alt",
        default=False,
        )
    # }}}
    
    # Use Remove Disconnected {{{
    bmtools_use_remove_disconnected: StringProperty(
        name="bmtools_use_remove_disconnected",
        maxlen=1,
        default='',
        )
    
    bmtools_use_remove_disconnected_shift: BoolProperty(
        name="bmtools_use_remove_disconnected_shift",
        default=False,
        )
    
    bmtools_use_remove_disconnected_ctl: BoolProperty(
        name="bmtools_use_remove_disconnected_ctl",
        default=False,
        )
    
    bmtools_use_remove_disconnected_alt: BoolProperty(
        name="bmtools_use_remove_disconnected_alt",
        default=False,
        )
    # }}}
    
    # Use Smooth Shade {{{
    bmtools_use_smooth_shade: StringProperty(
        name="bmtools_use_smooth_shade",
        maxlen=1,
        default='',
        )
    
    bmtools_use_smooth_shade_shift: BoolProperty(
        name="bmtools_use_smooth_shade_shift",
        default=False,
        )
    
    bmtools_use_smooth_shade_ctl: BoolProperty(
        name="bmtools_use_smooth_shade_ctl",
        default=False,
        )
    
    bmtools_use_smooth_shade_alt: BoolProperty(
        name="bmtools_use_smooth_shade_alt",
        default=False,
        )
    # }}}
    
    # Use Normal Calculate {{{
    bmtools_use_normal_calculate: StringProperty(
        name="bmtools_use_normal_calculate",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_calculate_shift: BoolProperty(
        name="bmtools_use_normal_calculate_shift",
        default=False,
        )
    
    bmtools_use_normal_calculate_ctl: BoolProperty(
        name="bmtools_use_normal_calculate_ctl",
        default=False,
        )
    
    bmtools_use_normal_calculate_alt: BoolProperty(
        name="bmtools_use_normal_calculate_alt",
        default=False,
        )
    # }}}
    
    # Use Normal Flip {{{
    bmtools_use_normal_flip: StringProperty(
        name="bmtools_use_normal_flip",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_flip_shift: BoolProperty(
        name="bmtools_use_normal_flip_shift",
        default=False,
        )
    
    bmtools_use_normal_flip_ctl: BoolProperty(
        name="bmtools_use_normal_flip_ctl",
        default=False,
        )
    
    bmtools_use_normal_flip_alt: BoolProperty(
        name="bmtools_use_normal_flip_alt",
        default=False,
        )
    # }}}
    
    # Use Stretch U {{{
    bmtools_use_stretch_u: StringProperty(
        name="bmtools_use_stretch_u",
        maxlen=1,
        default='',
        )
    
    bmtools_use_stretch_u_shift: BoolProperty(
        name="bmtools_use_stretch_u_shift",
        default=False,
        )
    
    bmtools_use_stretch_u_ctl: BoolProperty(
        name="bmtools_use_stretch_u_ctl",
        default=False,
        )
    
    bmtools_use_stretch_u_alt: BoolProperty(
        name="bmtools_use_stretch_u_alt",
        default=False,
        )
    # }}}
    
    # Use Object Screw Offset {{{
    bmtools_use_object_screw_offset: StringProperty(
        name="bmtools_use_object_screw_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_use_object_screw_offset_shift: BoolProperty(
        name="bmtools_use_object_screw_offset_shift",
        default=False,
        )
    
    bmtools_use_object_screw_offset_ctl: BoolProperty(
        name="bmtools_use_object_screw_offset_ctl",
        default=False,
        )
    
    bmtools_use_object_screw_offset_alt: BoolProperty(
        name="bmtools_use_object_screw_offset_alt",
        default=False,
        )
    # }}}
    
    # Use Stretch V {{{
    bmtools_use_stretch_v: StringProperty(
        name="bmtools_use_stretch_v",
        maxlen=1,
        default='',
        )
    
    bmtools_use_stretch_v_shift: BoolProperty(
        name="bmtools_use_stretch_v_shift",
        default=False,
        )
    
    bmtools_use_stretch_v_ctl: BoolProperty(
        name="bmtools_use_stretch_v_ctl",
        default=False,
        )
    
    bmtools_use_stretch_v_alt: BoolProperty(
        name="bmtools_use_stretch_v_alt",
        default=False,
        )
    # }}}
    
    # Use X Symmetry {{{
    bmtools_use_x_symmetry: StringProperty(
        name="bmtools_use_x_symmetry",
        maxlen=1,
        default='',
        )
    
    bmtools_use_x_symmetry_shift: BoolProperty(
        name="bmtools_use_x_symmetry_shift",
        default=False,
        )
    
    bmtools_use_x_symmetry_ctl: BoolProperty(
        name="bmtools_use_x_symmetry_ctl",
        default=False,
        )
    
    bmtools_use_x_symmetry_alt: BoolProperty(
        name="bmtools_use_x_symmetry_alt",
        default=False,
        )
    # }}}
    
    # Use Y Symmetry {{{
    bmtools_use_y_symmetry: StringProperty(
        name="bmtools_use_y_symmetry",
        maxlen=1,
        default='',
        )
    
    bmtools_use_y_symmetry_shift: BoolProperty(
        name="bmtools_use_y_symmetry_shift",
        default=False,
        )
    
    bmtools_use_y_symmetry_ctl: BoolProperty(
        name="bmtools_use_y_symmetry_ctl",
        default=False,
        )
    
    bmtools_use_y_symmetry_alt: BoolProperty(
        name="bmtools_use_y_symmetry_alt",
        default=False,
        )
    # }}}
    
    # Use Z Symmetry {{{
    bmtools_use_z_symmetry: StringProperty(
        name="bmtools_use_z_symmetry",
        maxlen=1,
        default='',
        )
    
    bmtools_use_z_symmetry_shift: BoolProperty(
        name="bmtools_use_z_symmetry_shift",
        default=False,
        )
    
    bmtools_use_z_symmetry_ctl: BoolProperty(
        name="bmtools_use_z_symmetry_ctl",
        default=False,
        )
    
    bmtools_use_z_symmetry_alt: BoolProperty(
        name="bmtools_use_z_symmetry_alt",
        default=False,
        )
    # }}}
    
    # Use Rim {{{
    bmtools_use_rim: StringProperty(
        name="bmtools_use_rim",
        maxlen=1,
        default='',
        )
    
    bmtools_use_rim_shift: BoolProperty(
        name="bmtools_use_rim_shift",
        default=False,
        )
    
    bmtools_use_rim_ctl: BoolProperty(
        name="bmtools_use_rim_ctl",
        default=False,
        )
    
    bmtools_use_rim_alt: BoolProperty(
        name="bmtools_use_rim_alt",
        default=False,
        )
    # }}}
    
    # Use Rim Only {{{
    bmtools_use_rim_only: StringProperty(
        name="bmtools_use_rim_only",
        maxlen=1,
        default='',
        )
    
    bmtools_use_rim_only_shift: BoolProperty(
        name="bmtools_use_rim_only_shift",
        default=False,
        )
    
    bmtools_use_rim_only_ctl: BoolProperty(
        name="bmtools_use_rim_only_ctl",
        default=False,
        )
    
    bmtools_use_rim_only_alt: BoolProperty(
        name="bmtools_use_rim_only_alt",
        default=False,
        )
    # }}}
    
    # Use Quality Normals {{{
    bmtools_use_quality_normals: StringProperty(
        name="bmtools_use_quality_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_use_quality_normals_shift: BoolProperty(
        name="bmtools_use_quality_normals_shift",
        default=False,
        )
    
    bmtools_use_quality_normals_ctl: BoolProperty(
        name="bmtools_use_quality_normals_ctl",
        default=False,
        )
    
    bmtools_use_quality_normals_alt: BoolProperty(
        name="bmtools_use_quality_normals_alt",
        default=False,
        )
    # }}}
    
    # Use Flat Faces {{{
    bmtools_use_flat_faces: StringProperty(
        name="bmtools_use_flat_faces",
        maxlen=1,
        default='',
        )
    
    bmtools_use_flat_faces_shift: BoolProperty(
        name="bmtools_use_flat_faces_shift",
        default=False,
        )
    
    bmtools_use_flat_faces_ctl: BoolProperty(
        name="bmtools_use_flat_faces_ctl",
        default=False,
        )
    
    bmtools_use_flat_faces_alt: BoolProperty(
        name="bmtools_use_flat_faces_alt",
        default=False,
        )
    # }}}
    
    # Use Even Offset {{{
    bmtools_use_even_offset: StringProperty(
        name="bmtools_use_even_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_use_even_offset_shift: BoolProperty(
        name="bmtools_use_even_offset_shift",
        default=False,
        )
    
    bmtools_use_even_offset_ctl: BoolProperty(
        name="bmtools_use_even_offset_ctl",
        default=False,
        )
    
    bmtools_use_even_offset_alt: BoolProperty(
        name="bmtools_use_even_offset_alt",
        default=False,
        )
    # }}}
    
    # Use Flip Normals {{{
    bmtools_use_flip_normals: StringProperty(
        name="bmtools_use_flip_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_use_flip_normals_shift: BoolProperty(
        name="bmtools_use_flip_normals_shift",
        default=False,
        )
    
    bmtools_use_flip_normals_ctl: BoolProperty(
        name="bmtools_use_flip_normals_ctl",
        default=False,
        )
    
    bmtools_use_flip_normals_alt: BoolProperty(
        name="bmtools_use_flip_normals_alt",
        default=False,
        )
    # }}}
    
    # Use Thickness Angle Clamp {{{
    bmtools_use_thickness_angle_clamp: StringProperty(
        name="bmtools_use_thickness_angle_clamp",
        maxlen=1,
        default='',
        )
    
    bmtools_use_thickness_angle_clamp_shift: BoolProperty(
        name="bmtools_use_thickness_angle_clamp_shift",
        default=False,
        )
    
    bmtools_use_thickness_angle_clamp_ctl: BoolProperty(
        name="bmtools_use_thickness_angle_clamp_ctl",
        default=False,
        )
    
    bmtools_use_thickness_angle_clamp_alt: BoolProperty(
        name="bmtools_use_thickness_angle_clamp_alt",
        default=False,
        )
    # }}}
    
    # Use Limit Surface {{{
    bmtools_use_limit_surface: StringProperty(
        name="bmtools_use_limit_surface",
        maxlen=1,
        default='',
        )
    
    bmtools_use_limit_surface_shift: BoolProperty(
        name="bmtools_use_limit_surface_shift",
        default=False,
        )
    
    bmtools_use_limit_surface_ctl: BoolProperty(
        name="bmtools_use_limit_surface_ctl",
        default=False,
        )
    
    bmtools_use_limit_surface_alt: BoolProperty(
        name="bmtools_use_limit_surface_alt",
        default=False,
        )
    # }}}
    
    # Keep Custom Normals {{{
    bmtools_keep_custom_normals: StringProperty(
        name="bmtools_keep_custom_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_keep_custom_normals_shift: BoolProperty(
        name="bmtools_keep_custom_normals_shift",
        default=False,
        )
    
    bmtools_keep_custom_normals_ctl: BoolProperty(
        name="bmtools_keep_custom_normals_ctl",
        default=False,
        )
    
    bmtools_keep_custom_normals_alt: BoolProperty(
        name="bmtools_keep_custom_normals_alt",
        default=False,
        )
    # }}}
    
    # Loose Edges {{{
    bmtools_loose_edges: StringProperty(
        name="bmtools_loose_edges",
        maxlen=1,
        default='',
        )
    
    bmtools_loose_edges_shift: BoolProperty(
        name="bmtools_loose_edges_shift",
        default=False,
        )
    
    bmtools_loose_edges_ctl: BoolProperty(
        name="bmtools_loose_edges_ctl",
        default=False,
        )
    
    bmtools_loose_edges_alt: BoolProperty(
        name="bmtools_loose_edges_alt",
        default=False,
        )
    # }}}
    
    # Use Crease {{{
    bmtools_use_crease: StringProperty(
        name="bmtools_use_crease",
        maxlen=1,
        default='',
        )
    
    bmtools_use_crease_shift: BoolProperty(
        name="bmtools_use_crease_shift",
        default=False,
        )
    
    bmtools_use_crease_ctl: BoolProperty(
        name="bmtools_use_crease_ctl",
        default=False,
        )
    
    bmtools_use_crease_alt: BoolProperty(
        name="bmtools_use_crease_alt",
        default=False,
        )
    # }}}
    
    # Use Replace {{{
    bmtools_use_replace: StringProperty(
        name="bmtools_use_replace",
        maxlen=1,
        default='',
        )
    
    bmtools_use_replace_shift: BoolProperty(
        name="bmtools_use_replace_shift",
        default=False,
        )
    
    bmtools_use_replace_ctl: BoolProperty(
        name="bmtools_use_replace_ctl",
        default=False,
        )
    
    bmtools_use_replace_alt: BoolProperty(
        name="bmtools_use_replace_alt",
        default=False,
        )
    # }}}
    
    # Use Boundary {{{
    bmtools_use_boundary: StringProperty(
        name="bmtools_use_boundary",
        maxlen=1,
        default='',
        )
    
    bmtools_use_boundary_shift: BoolProperty(
        name="bmtools_use_boundary_shift",
        default=False,
        )
    
    bmtools_use_boundary_ctl: BoolProperty(
        name="bmtools_use_boundary_ctl",
        default=False,
        )
    
    bmtools_use_boundary_alt: BoolProperty(
        name="bmtools_use_boundary_alt",
        default=False,
        )
    # }}}
    
    # Use Multi Modifier {{{
    bmtools_use_multi_modifier: StringProperty(
        name="bmtools_use_multi_modifier",
        maxlen=1,
        default='',
        )
    
    bmtools_use_multi_modifier_shift: BoolProperty(
        name="bmtools_use_multi_modifier_shift",
        default=False,
        )
    
    bmtools_use_multi_modifier_ctl: BoolProperty(
        name="bmtools_use_multi_modifier_ctl",
        default=False,
        )
    
    bmtools_use_multi_modifier_alt: BoolProperty(
        name="bmtools_use_multi_modifier_alt",
        default=False,
        )
    # }}}
    
    # Use Bone Envelopes {{{
    bmtools_use_bone_envelopes: StringProperty(
        name="bmtools_use_bone_envelopes",
        maxlen=1,
        default='',
        )
    
    bmtools_use_bone_envelopes_shift: BoolProperty(
        name="bmtools_use_bone_envelopes_shift",
        default=False,
        )
    
    bmtools_use_bone_envelopes_ctl: BoolProperty(
        name="bmtools_use_bone_envelopes_ctl",
        default=False,
        )
    
    bmtools_use_bone_envelopes_alt: BoolProperty(
        name="bmtools_use_bone_envelopes_alt",
        default=False,
        )
    # }}}
    
    # Use Deform Preserve Volume {{{
    bmtools_use_deform_preserve_volume: StringProperty(
        name="bmtools_use_deform_preserve_volume",
        maxlen=1,
        default='',
        )
    
    bmtools_use_deform_preserve_volume_shift: BoolProperty(
        name="bmtools_use_deform_preserve_volume_shift",
        default=False,
        )
    
    bmtools_use_deform_preserve_volume_ctl: BoolProperty(
        name="bmtools_use_deform_preserve_volume_ctl",
        default=False,
        )
    
    bmtools_use_deform_preserve_volume_alt: BoolProperty(
        name="bmtools_use_deform_preserve_volume_alt",
        default=False,
        )
    # }}}
    
    # Use Vertex Groups {{{
    bmtools_use_vertex_groups: StringProperty(
        name="bmtools_use_vertex_groups",
        maxlen=1,
        default='',
        )
    
    bmtools_use_vertex_groups_shift: BoolProperty(
        name="bmtools_use_vertex_groups_shift",
        default=False,
        )
    
    bmtools_use_vertex_groups_ctl: BoolProperty(
        name="bmtools_use_vertex_groups_ctl",
        default=False,
        )
    
    bmtools_use_vertex_groups_alt: BoolProperty(
        name="bmtools_use_vertex_groups_alt",
        default=False,
        )
    # }}}
    
    # Use Z {{{
    bmtools_use_z: StringProperty(
        name="bmtools_use_z",
        maxlen=1,
        default='',
        )
    
    bmtools_use_z_shift: BoolProperty(
        name="bmtools_use_z_shift",
        default=False,
        )
    
    bmtools_use_z_ctl: BoolProperty(
        name="bmtools_use_z_ctl",
        default=False,
        )
    
    bmtools_use_z_alt: BoolProperty(
        name="bmtools_use_z_alt",
        default=False,
        )
    # }}}
    
    # Use X {{{
    bmtools_use_x: StringProperty(
        name="bmtools_use_x",
        maxlen=1,
        default='',
        )
    
    bmtools_use_x_shift: BoolProperty(
        name="bmtools_use_x_shift",
        default=False,
        )
    
    bmtools_use_x_ctl: BoolProperty(
        name="bmtools_use_x_ctl",
        default=False,
        )
    
    bmtools_use_x_alt: BoolProperty(
        name="bmtools_use_x_alt",
        default=False,
        )
    # }}}
    
    # Use Y {{{
    bmtools_use_y: StringProperty(
        name="bmtools_use_y",
        maxlen=1,
        default='',
        )
    
    bmtools_use_y_shift: BoolProperty(
        name="bmtools_use_y_shift",
        default=False,
        )
    
    bmtools_use_y_ctl: BoolProperty(
        name="bmtools_use_y_ctl",
        default=False,
        )
    
    bmtools_use_y_alt: BoolProperty(
        name="bmtools_use_y_alt",
        default=False,
        )
    # }}}
    
    # Use Radius As Size {{{
    bmtools_use_radius_as_size: StringProperty(
        name="bmtools_use_radius_as_size",
        maxlen=1,
        default='',
        )
    
    bmtools_use_radius_as_size_shift: BoolProperty(
        name="bmtools_use_radius_as_size_shift",
        default=False,
        )
    
    bmtools_use_radius_as_size_ctl: BoolProperty(
        name="bmtools_use_radius_as_size_ctl",
        default=False,
        )
    
    bmtools_use_radius_as_size_alt: BoolProperty(
        name="bmtools_use_radius_as_size_alt",
        default=False,
        )
    # }}}
    
    # Use Transform {{{
    bmtools_use_transform: StringProperty(
        name="bmtools_use_transform",
        maxlen=1,
        default='',
        )
    
    bmtools_use_transform_shift: BoolProperty(
        name="bmtools_use_transform_shift",
        default=False,
        )
    
    bmtools_use_transform_ctl: BoolProperty(
        name="bmtools_use_transform_ctl",
        default=False,
        )
    
    bmtools_use_transform_alt: BoolProperty(
        name="bmtools_use_transform_alt",
        default=False,
        )
    # }}}
    
    # Use Falloff Uniform {{{
    bmtools_use_falloff_uniform: StringProperty(
        name="bmtools_use_falloff_uniform",
        maxlen=1,
        default='',
        )
    
    bmtools_use_falloff_uniform_shift: BoolProperty(
        name="bmtools_use_falloff_uniform_shift",
        default=False,
        )
    
    bmtools_use_falloff_uniform_ctl: BoolProperty(
        name="bmtools_use_falloff_uniform_ctl",
        default=False,
        )
    
    bmtools_use_falloff_uniform_alt: BoolProperty(
        name="bmtools_use_falloff_uniform_alt",
        default=False,
        )
    # }}}
    
    # Use Dynamic Bind {{{
    bmtools_use_dynamic_bind: StringProperty(
        name="bmtools_use_dynamic_bind",
        maxlen=1,
        default='',
        )
    
    bmtools_use_dynamic_bind_shift: BoolProperty(
        name="bmtools_use_dynamic_bind_shift",
        default=False,
        )
    
    bmtools_use_dynamic_bind_ctl: BoolProperty(
        name="bmtools_use_dynamic_bind_ctl",
        default=False,
        )
    
    bmtools_use_dynamic_bind_alt: BoolProperty(
        name="bmtools_use_dynamic_bind_alt",
        default=False,
        )
    # }}}
    
    # Use Project Z {{{
    bmtools_use_project_z: StringProperty(
        name="bmtools_use_project_z",
        maxlen=1,
        default='',
        )
    
    bmtools_use_project_z_shift: BoolProperty(
        name="bmtools_use_project_z_shift",
        default=False,
        )
    
    bmtools_use_project_z_ctl: BoolProperty(
        name="bmtools_use_project_z_ctl",
        default=False,
        )
    
    bmtools_use_project_z_alt: BoolProperty(
        name="bmtools_use_project_z_alt",
        default=False,
        )
    # }}}
    
    # Use Negative Direction {{{
    bmtools_use_negative_direction: StringProperty(
        name="bmtools_use_negative_direction",
        maxlen=1,
        default='',
        )
    
    bmtools_use_negative_direction_shift: BoolProperty(
        name="bmtools_use_negative_direction_shift",
        default=False,
        )
    
    bmtools_use_negative_direction_ctl: BoolProperty(
        name="bmtools_use_negative_direction_ctl",
        default=False,
        )
    
    bmtools_use_negative_direction_alt: BoolProperty(
        name="bmtools_use_negative_direction_alt",
        default=False,
        )
    # }}}
    
    # Use Invert Cull {{{
    bmtools_use_invert_cull: StringProperty(
        name="bmtools_use_invert_cull",
        maxlen=1,
        default='',
        )
    
    bmtools_use_invert_cull_shift: BoolProperty(
        name="bmtools_use_invert_cull_shift",
        default=False,
        )
    
    bmtools_use_invert_cull_ctl: BoolProperty(
        name="bmtools_use_invert_cull_ctl",
        default=False,
        )
    
    bmtools_use_invert_cull_alt: BoolProperty(
        name="bmtools_use_invert_cull_alt",
        default=False,
        )
    # }}}
    
    # Use Positive Direction {{{
    bmtools_use_positive_direction: StringProperty(
        name="bmtools_use_positive_direction",
        maxlen=1,
        default='',
        )
    
    bmtools_use_positive_direction_shift: BoolProperty(
        name="bmtools_use_positive_direction_shift",
        default=False,
        )
    
    bmtools_use_positive_direction_ctl: BoolProperty(
        name="bmtools_use_positive_direction_ctl",
        default=False,
        )
    
    bmtools_use_positive_direction_alt: BoolProperty(
        name="bmtools_use_positive_direction_alt",
        default=False,
        )
    # }}}
    
    # Use Project Y {{{
    bmtools_use_project_y: StringProperty(
        name="bmtools_use_project_y",
        maxlen=1,
        default='',
        )
    
    bmtools_use_project_y_shift: BoolProperty(
        name="bmtools_use_project_y_shift",
        default=False,
        )
    
    bmtools_use_project_y_ctl: BoolProperty(
        name="bmtools_use_project_y_ctl",
        default=False,
        )
    
    bmtools_use_project_y_alt: BoolProperty(
        name="bmtools_use_project_y_alt",
        default=False,
        )
    # }}}
    
    # Use Project X {{{
    bmtools_use_project_x: StringProperty(
        name="bmtools_use_project_x",
        maxlen=1,
        default='',
        )
    
    bmtools_use_project_x_shift: BoolProperty(
        name="bmtools_use_project_x_shift",
        default=False,
        )
    
    bmtools_use_project_x_ctl: BoolProperty(
        name="bmtools_use_project_x_ctl",
        default=False,
        )
    
    bmtools_use_project_x_alt: BoolProperty(
        name="bmtools_use_project_x_alt",
        default=False,
        )
    # }}}
    
    # Lock Z {{{
    bmtools_lock_z: StringProperty(
        name="bmtools_lock_z",
        maxlen=1,
        default='',
        )
    
    bmtools_lock_z_shift: BoolProperty(
        name="bmtools_lock_z_shift",
        default=False,
        )
    
    bmtools_lock_z_ctl: BoolProperty(
        name="bmtools_lock_z_ctl",
        default=False,
        )
    
    bmtools_lock_z_alt: BoolProperty(
        name="bmtools_lock_z_alt",
        default=False,
        )
    # }}}
    
    # Lock X {{{
    bmtools_lock_x: StringProperty(
        name="bmtools_lock_x",
        maxlen=1,
        default='',
        )
    
    bmtools_lock_x_shift: BoolProperty(
        name="bmtools_lock_x_shift",
        default=False,
        )
    
    bmtools_lock_x_ctl: BoolProperty(
        name="bmtools_lock_x_ctl",
        default=False,
        )
    
    bmtools_lock_x_alt: BoolProperty(
        name="bmtools_lock_x_alt",
        default=False,
        )
    # }}}
    
    # Lock Y {{{
    bmtools_lock_y: StringProperty(
        name="bmtools_lock_y",
        maxlen=1,
        default='',
        )
    
    bmtools_lock_y_shift: BoolProperty(
        name="bmtools_lock_y_shift",
        default=False,
        )
    
    bmtools_lock_y_ctl: BoolProperty(
        name="bmtools_lock_y_ctl",
        default=False,
        )
    
    bmtools_lock_y_alt: BoolProperty(
        name="bmtools_lock_y_alt",
        default=False,
        )
    # }}}
    
    # Use Only Smooth {{{
    bmtools_use_only_smooth: StringProperty(
        name="bmtools_use_only_smooth",
        maxlen=1,
        default='',
        )
    
    bmtools_use_only_smooth_shift: BoolProperty(
        name="bmtools_use_only_smooth_shift",
        default=False,
        )
    
    bmtools_use_only_smooth_ctl: BoolProperty(
        name="bmtools_use_only_smooth_ctl",
        default=False,
        )
    
    bmtools_use_only_smooth_alt: BoolProperty(
        name="bmtools_use_only_smooth_alt",
        default=False,
        )
    # }}}
    
    # Use Pin Boundary {{{
    bmtools_use_pin_boundary: StringProperty(
        name="bmtools_use_pin_boundary",
        maxlen=1,
        default='',
        )
    
    bmtools_use_pin_boundary_shift: BoolProperty(
        name="bmtools_use_pin_boundary_shift",
        default=False,
        )
    
    bmtools_use_pin_boundary_ctl: BoolProperty(
        name="bmtools_use_pin_boundary_ctl",
        default=False,
        )
    
    bmtools_use_pin_boundary_alt: BoolProperty(
        name="bmtools_use_pin_boundary_alt",
        default=False,
        )
    # }}}
    
    # Use Normalized {{{
    bmtools_use_normalized: StringProperty(
        name="bmtools_use_normalized",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normalized_shift: BoolProperty(
        name="bmtools_use_normalized_shift",
        default=False,
        )
    
    bmtools_use_normalized_ctl: BoolProperty(
        name="bmtools_use_normalized_ctl",
        default=False,
        )
    
    bmtools_use_normalized_alt: BoolProperty(
        name="bmtools_use_normalized_alt",
        default=False,
        )
    # }}}
    
    # Use Volume Preserve {{{
    bmtools_use_volume_preserve: StringProperty(
        name="bmtools_use_volume_preserve",
        maxlen=1,
        default='',
        )
    
    bmtools_use_volume_preserve_shift: BoolProperty(
        name="bmtools_use_volume_preserve_shift",
        default=False,
        )
    
    bmtools_use_volume_preserve_ctl: BoolProperty(
        name="bmtools_use_volume_preserve_ctl",
        default=False,
        )
    
    bmtools_use_volume_preserve_alt: BoolProperty(
        name="bmtools_use_volume_preserve_alt",
        default=False,
        )
    # }}}
    
    # Use Sparse Bind {{{
    bmtools_use_sparse_bind: StringProperty(
        name="bmtools_use_sparse_bind",
        maxlen=1,
        default='',
        )
    
    bmtools_use_sparse_bind_shift: BoolProperty(
        name="bmtools_use_sparse_bind_shift",
        default=False,
        )
    
    bmtools_use_sparse_bind_ctl: BoolProperty(
        name="bmtools_use_sparse_bind_ctl",
        default=False,
        )
    
    bmtools_use_sparse_bind_alt: BoolProperty(
        name="bmtools_use_sparse_bind_alt",
        default=False,
        )
    # }}}
    
    # Use Normal {{{
    bmtools_use_normal: StringProperty(
        name="bmtools_use_normal",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_shift: BoolProperty(
        name="bmtools_use_normal_shift",
        default=False,
        )
    
    bmtools_use_normal_ctl: BoolProperty(
        name="bmtools_use_normal_ctl",
        default=False,
        )
    
    bmtools_use_normal_alt: BoolProperty(
        name="bmtools_use_normal_alt",
        default=False,
        )
    # }}}
    
    # Use Normal Y {{{
    bmtools_use_normal_y: StringProperty(
        name="bmtools_use_normal_y",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_y_shift: BoolProperty(
        name="bmtools_use_normal_y_shift",
        default=False,
        )
    
    bmtools_use_normal_y_ctl: BoolProperty(
        name="bmtools_use_normal_y_ctl",
        default=False,
        )
    
    bmtools_use_normal_y_alt: BoolProperty(
        name="bmtools_use_normal_y_alt",
        default=False,
        )
    # }}}
    
    # Use Cyclic {{{
    bmtools_use_cyclic: StringProperty(
        name="bmtools_use_cyclic",
        maxlen=1,
        default='',
        )
    
    bmtools_use_cyclic_shift: BoolProperty(
        name="bmtools_use_cyclic_shift",
        default=False,
        )
    
    bmtools_use_cyclic_ctl: BoolProperty(
        name="bmtools_use_cyclic_ctl",
        default=False,
        )
    
    bmtools_use_cyclic_alt: BoolProperty(
        name="bmtools_use_cyclic_alt",
        default=False,
        )
    # }}}
    
    # Use Normal Z {{{
    bmtools_use_normal_z: StringProperty(
        name="bmtools_use_normal_z",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_z_shift: BoolProperty(
        name="bmtools_use_normal_z_shift",
        default=False,
        )
    
    bmtools_use_normal_z_ctl: BoolProperty(
        name="bmtools_use_normal_z_ctl",
        default=False,
        )
    
    bmtools_use_normal_z_alt: BoolProperty(
        name="bmtools_use_normal_z_alt",
        default=False,
        )
    # }}}
    
    # Use Normal X {{{
    bmtools_use_normal_x: StringProperty(
        name="bmtools_use_normal_x",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normal_x_shift: BoolProperty(
        name="bmtools_use_normal_x_shift",
        default=False,
        )
    
    bmtools_use_normal_x_ctl: BoolProperty(
        name="bmtools_use_normal_x_ctl",
        default=False,
        )
    
    bmtools_use_normal_x_alt: BoolProperty(
        name="bmtools_use_normal_x_alt",
        default=False,
        )
    # }}}
    
    # Show Alive {{{
    bmtools_show_alive: StringProperty(
        name="bmtools_show_alive",
        maxlen=1,
        default='',
        )
    
    bmtools_show_alive_shift: BoolProperty(
        name="bmtools_show_alive_shift",
        default=False,
        )
    
    bmtools_show_alive_ctl: BoolProperty(
        name="bmtools_show_alive_ctl",
        default=False,
        )
    
    bmtools_show_alive_alt: BoolProperty(
        name="bmtools_show_alive_alt",
        default=False,
        )
    # }}}
    
    # Show Dead {{{
    bmtools_show_dead: StringProperty(
        name="bmtools_show_dead",
        maxlen=1,
        default='',
        )
    
    bmtools_show_dead_shift: BoolProperty(
        name="bmtools_show_dead_shift",
        default=False,
        )
    
    bmtools_show_dead_ctl: BoolProperty(
        name="bmtools_show_dead_ctl",
        default=False,
        )
    
    bmtools_show_dead_alt: BoolProperty(
        name="bmtools_show_dead_alt",
        default=False,
        )
    # }}}
    
    # Use Size {{{
    bmtools_use_size: StringProperty(
        name="bmtools_use_size",
        maxlen=1,
        default='',
        )
    
    bmtools_use_size_shift: BoolProperty(
        name="bmtools_use_size_shift",
        default=False,
        )
    
    bmtools_use_size_ctl: BoolProperty(
        name="bmtools_use_size_ctl",
        default=False,
        )
    
    bmtools_use_size_alt: BoolProperty(
        name="bmtools_use_size_alt",
        default=False,
        )
    # }}}
    
    # Show Unborn {{{
    bmtools_show_unborn: StringProperty(
        name="bmtools_show_unborn",
        maxlen=1,
        default='',
        )
    
    bmtools_show_unborn_shift: BoolProperty(
        name="bmtools_show_unborn_shift",
        default=False,
        )
    
    bmtools_show_unborn_ctl: BoolProperty(
        name="bmtools_show_unborn_ctl",
        default=False,
        )
    
    bmtools_show_unborn_alt: BoolProperty(
        name="bmtools_show_unborn_alt",
        default=False,
        )
    # }}}
    
    # Use Edge Cut {{{
    bmtools_use_edge_cut: StringProperty(
        name="bmtools_use_edge_cut",
        maxlen=1,
        default='',
        )
    
    bmtools_use_edge_cut_shift: BoolProperty(
        name="bmtools_use_edge_cut_shift",
        default=False,
        )
    
    bmtools_use_edge_cut_ctl: BoolProperty(
        name="bmtools_use_edge_cut_ctl",
        default=False,
        )
    
    bmtools_use_edge_cut_alt: BoolProperty(
        name="bmtools_use_edge_cut_alt",
        default=False,
        )
    # }}}
    
    # Use Spray {{{
    bmtools_use_spray: StringProperty(
        name="bmtools_use_spray",
        maxlen=1,
        default='',
        )
    
    bmtools_use_spray_shift: BoolProperty(
        name="bmtools_use_spray_shift",
        default=False,
        )
    
    bmtools_use_spray_ctl: BoolProperty(
        name="bmtools_use_spray_ctl",
        default=False,
        )
    
    bmtools_use_spray_alt: BoolProperty(
        name="bmtools_use_spray_alt",
        default=False,
        )
    # }}}
    
    # Invert Spray {{{
    bmtools_invert_spray: StringProperty(
        name="bmtools_invert_spray",
        maxlen=1,
        default='',
        )
    
    bmtools_invert_spray_shift: BoolProperty(
        name="bmtools_invert_spray_shift",
        default=False,
        )
    
    bmtools_invert_spray_ctl: BoolProperty(
        name="bmtools_invert_spray_ctl",
        default=False,
        )
    
    bmtools_invert_spray_alt: BoolProperty(
        name="bmtools_invert_spray_alt",
        default=False,
        )
    # }}}
    
    # Use Foam {{{
    bmtools_use_foam: StringProperty(
        name="bmtools_use_foam",
        maxlen=1,
        default='',
        )
    
    bmtools_use_foam_shift: BoolProperty(
        name="bmtools_use_foam_shift",
        default=False,
        )
    
    bmtools_use_foam_ctl: BoolProperty(
        name="bmtools_use_foam_ctl",
        default=False,
        )
    
    bmtools_use_foam_alt: BoolProperty(
        name="bmtools_use_foam_alt",
        default=False,
        )
    # }}}
    
    # Use Normals {{{
    bmtools_use_normals: StringProperty(
        name="bmtools_use_normals",
        maxlen=1,
        default='',
        )
    
    bmtools_use_normals_shift: BoolProperty(
        name="bmtools_use_normals_shift",
        default=False,
        )
    
    bmtools_use_normals_ctl: BoolProperty(
        name="bmtools_use_normals_ctl",
        default=False,
        )
    
    bmtools_use_normals_alt: BoolProperty(
        name="bmtools_use_normals_alt",
        default=False,
        )
    # }}}
    
    # Use Children {{{
    bmtools_use_children: StringProperty(
        name="bmtools_use_children",
        maxlen=1,
        default='',
        )
    
    bmtools_use_children_shift: BoolProperty(
        name="bmtools_use_children_shift",
        default=False,
        )
    
    bmtools_use_children_ctl: BoolProperty(
        name="bmtools_use_children_ctl",
        default=False,
        )
    
    bmtools_use_children_alt: BoolProperty(
        name="bmtools_use_children_alt",
        default=False,
        )
    # }}}
    
    # Use Preserve Shape {{{
    bmtools_use_preserve_shape: StringProperty(
        name="bmtools_use_preserve_shape",
        maxlen=1,
        default='',
        )
    
    bmtools_use_preserve_shape_shift: BoolProperty(
        name="bmtools_use_preserve_shape_shift",
        default=False,
        )
    
    bmtools_use_preserve_shape_ctl: BoolProperty(
        name="bmtools_use_preserve_shape_ctl",
        default=False,
        )
    
    bmtools_use_preserve_shape_alt: BoolProperty(
        name="bmtools_use_preserve_shape_alt",
        default=False,
        )
    # }}}
    
    # Use Path {{{
    bmtools_use_path: StringProperty(
        name="bmtools_use_path",
        maxlen=1,
        default='',
        )
    
    bmtools_use_path_shift: BoolProperty(
        name="bmtools_use_path_shift",
        default=False,
        )
    
    bmtools_use_path_ctl: BoolProperty(
        name="bmtools_use_path_ctl",
        default=False,
        )
    
    bmtools_use_path_alt: BoolProperty(
        name="bmtools_use_path_alt",
        default=False,
        )
    # }}}
    
    # Layers Vcol Select Src {{{
    bmtools_layers_vcol_select_src: StringProperty(
        name="bmtools_layers_vcol_select_src",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_vcol_select_src_shift: BoolProperty(
        name="bmtools_layers_vcol_select_src_shift",
        default=False,
        )
    
    bmtools_layers_vcol_select_src_ctl: BoolProperty(
        name="bmtools_layers_vcol_select_src_ctl",
        default=False,
        )
    
    bmtools_layers_vcol_select_src_alt: BoolProperty(
        name="bmtools_layers_vcol_select_src_alt",
        default=False,
        )
    # }}}
    
    # Vert Mapping {{{
    bmtools_vert_mapping: StringProperty(
        name="bmtools_vert_mapping",
        maxlen=1,
        default='',
        )
    
    bmtools_vert_mapping_shift: BoolProperty(
        name="bmtools_vert_mapping_shift",
        default=False,
        )
    
    bmtools_vert_mapping_ctl: BoolProperty(
        name="bmtools_vert_mapping_ctl",
        default=False,
        )
    
    bmtools_vert_mapping_alt: BoolProperty(
        name="bmtools_vert_mapping_alt",
        default=False,
        )
    # }}}
    
    # Layers Vgroup Select Src {{{
    bmtools_layers_vgroup_select_src: StringProperty(
        name="bmtools_layers_vgroup_select_src",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_vgroup_select_src_shift: BoolProperty(
        name="bmtools_layers_vgroup_select_src_shift",
        default=False,
        )
    
    bmtools_layers_vgroup_select_src_ctl: BoolProperty(
        name="bmtools_layers_vgroup_select_src_ctl",
        default=False,
        )
    
    bmtools_layers_vgroup_select_src_alt: BoolProperty(
        name="bmtools_layers_vgroup_select_src_alt",
        default=False,
        )
    # }}}
    
    # Layers Vgroup Select Dst {{{
    bmtools_layers_vgroup_select_dst: StringProperty(
        name="bmtools_layers_vgroup_select_dst",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_vgroup_select_dst_shift: BoolProperty(
        name="bmtools_layers_vgroup_select_dst_shift",
        default=False,
        )
    
    bmtools_layers_vgroup_select_dst_ctl: BoolProperty(
        name="bmtools_layers_vgroup_select_dst_ctl",
        default=False,
        )
    
    bmtools_layers_vgroup_select_dst_alt: BoolProperty(
        name="bmtools_layers_vgroup_select_dst_alt",
        default=False,
        )
    # }}}
    
    # Layers Vcol Select Dst {{{
    bmtools_layers_vcol_select_dst: StringProperty(
        name="bmtools_layers_vcol_select_dst",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_vcol_select_dst_shift: BoolProperty(
        name="bmtools_layers_vcol_select_dst_shift",
        default=False,
        )
    
    bmtools_layers_vcol_select_dst_ctl: BoolProperty(
        name="bmtools_layers_vcol_select_dst_ctl",
        default=False,
        )
    
    bmtools_layers_vcol_select_dst_alt: BoolProperty(
        name="bmtools_layers_vcol_select_dst_alt",
        default=False,
        )
    # }}}
    
    # Poly Mapping {{{
    bmtools_poly_mapping: StringProperty(
        name="bmtools_poly_mapping",
        maxlen=1,
        default='',
        )
    
    bmtools_poly_mapping_shift: BoolProperty(
        name="bmtools_poly_mapping_shift",
        default=False,
        )
    
    bmtools_poly_mapping_ctl: BoolProperty(
        name="bmtools_poly_mapping_ctl",
        default=False,
        )
    
    bmtools_poly_mapping_alt: BoolProperty(
        name="bmtools_poly_mapping_alt",
        default=False,
        )
    # }}}
    
    # Mix Mode {{{
    bmtools_mix_mode: StringProperty(
        name="bmtools_mix_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_mix_mode_shift: BoolProperty(
        name="bmtools_mix_mode_shift",
        default=False,
        )
    
    bmtools_mix_mode_ctl: BoolProperty(
        name="bmtools_mix_mode_ctl",
        default=False,
        )
    
    bmtools_mix_mode_alt: BoolProperty(
        name="bmtools_mix_mode_alt",
        default=False,
        )
    # }}}
    
    # Data Types Edges {{{
    bmtools_data_types_edges: StringProperty(
        name="bmtools_data_types_edges",
        maxlen=1,
        default='',
        )
    
    bmtools_data_types_edges_shift: BoolProperty(
        name="bmtools_data_types_edges_shift",
        default=False,
        )
    
    bmtools_data_types_edges_ctl: BoolProperty(
        name="bmtools_data_types_edges_ctl",
        default=False,
        )
    
    bmtools_data_types_edges_alt: BoolProperty(
        name="bmtools_data_types_edges_alt",
        default=False,
        )
    # }}}
    
    # Layers Uv Select Src {{{
    bmtools_layers_uv_select_src: StringProperty(
        name="bmtools_layers_uv_select_src",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_uv_select_src_shift: BoolProperty(
        name="bmtools_layers_uv_select_src_shift",
        default=False,
        )
    
    bmtools_layers_uv_select_src_ctl: BoolProperty(
        name="bmtools_layers_uv_select_src_ctl",
        default=False,
        )
    
    bmtools_layers_uv_select_src_alt: BoolProperty(
        name="bmtools_layers_uv_select_src_alt",
        default=False,
        )
    # }}}
    
    # Data Types Polys {{{
    bmtools_data_types_polys: StringProperty(
        name="bmtools_data_types_polys",
        maxlen=1,
        default='',
        )
    
    bmtools_data_types_polys_shift: BoolProperty(
        name="bmtools_data_types_polys_shift",
        default=False,
        )
    
    bmtools_data_types_polys_ctl: BoolProperty(
        name="bmtools_data_types_polys_ctl",
        default=False,
        )
    
    bmtools_data_types_polys_alt: BoolProperty(
        name="bmtools_data_types_polys_alt",
        default=False,
        )
    # }}}
    
    # Data Types Verts {{{
    bmtools_data_types_verts: StringProperty(
        name="bmtools_data_types_verts",
        maxlen=1,
        default='',
        )
    
    bmtools_data_types_verts_shift: BoolProperty(
        name="bmtools_data_types_verts_shift",
        default=False,
        )
    
    bmtools_data_types_verts_ctl: BoolProperty(
        name="bmtools_data_types_verts_ctl",
        default=False,
        )
    
    bmtools_data_types_verts_alt: BoolProperty(
        name="bmtools_data_types_verts_alt",
        default=False,
        )
    # }}}
    
    # Layers Uv Select Dst {{{
    bmtools_layers_uv_select_dst: StringProperty(
        name="bmtools_layers_uv_select_dst",
        maxlen=1,
        default='',
        )
    
    bmtools_layers_uv_select_dst_shift: BoolProperty(
        name="bmtools_layers_uv_select_dst_shift",
        default=False,
        )
    
    bmtools_layers_uv_select_dst_ctl: BoolProperty(
        name="bmtools_layers_uv_select_dst_ctl",
        default=False,
        )
    
    bmtools_layers_uv_select_dst_alt: BoolProperty(
        name="bmtools_layers_uv_select_dst_alt",
        default=False,
        )
    # }}}
    
    # Edge Mapping {{{
    bmtools_edge_mapping: StringProperty(
        name="bmtools_edge_mapping",
        maxlen=1,
        default='',
        )
    
    bmtools_edge_mapping_shift: BoolProperty(
        name="bmtools_edge_mapping_shift",
        default=False,
        )
    
    bmtools_edge_mapping_ctl: BoolProperty(
        name="bmtools_edge_mapping_ctl",
        default=False,
        )
    
    bmtools_edge_mapping_alt: BoolProperty(
        name="bmtools_edge_mapping_alt",
        default=False,
        )
    # }}}
    
    # Loop Mapping {{{
    bmtools_loop_mapping: StringProperty(
        name="bmtools_loop_mapping",
        maxlen=1,
        default='',
        )
    
    bmtools_loop_mapping_shift: BoolProperty(
        name="bmtools_loop_mapping_shift",
        default=False,
        )
    
    bmtools_loop_mapping_ctl: BoolProperty(
        name="bmtools_loop_mapping_ctl",
        default=False,
        )
    
    bmtools_loop_mapping_alt: BoolProperty(
        name="bmtools_loop_mapping_alt",
        default=False,
        )
    # }}}
    
    # Data Types Loops {{{
    bmtools_data_types_loops: StringProperty(
        name="bmtools_data_types_loops",
        maxlen=1,
        default='',
        )
    
    bmtools_data_types_loops_shift: BoolProperty(
        name="bmtools_data_types_loops_shift",
        default=False,
        )
    
    bmtools_data_types_loops_ctl: BoolProperty(
        name="bmtools_data_types_loops_ctl",
        default=False,
        )
    
    bmtools_data_types_loops_alt: BoolProperty(
        name="bmtools_data_types_loops_alt",
        default=False,
        )
    # }}}
    
    # Up Axis {{{
    bmtools_up_axis: StringProperty(
        name="bmtools_up_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_up_axis_shift: BoolProperty(
        name="bmtools_up_axis_shift",
        default=False,
        )
    
    bmtools_up_axis_ctl: BoolProperty(
        name="bmtools_up_axis_ctl",
        default=False,
        )
    
    bmtools_up_axis_alt: BoolProperty(
        name="bmtools_up_axis_alt",
        default=False,
        )
    # }}}
    
    # Cache Format {{{
    bmtools_cache_format: StringProperty(
        name="bmtools_cache_format",
        maxlen=1,
        default='',
        )
    
    bmtools_cache_format_shift: BoolProperty(
        name="bmtools_cache_format_shift",
        default=False,
        )
    
    bmtools_cache_format_ctl: BoolProperty(
        name="bmtools_cache_format_ctl",
        default=False,
        )
    
    bmtools_cache_format_alt: BoolProperty(
        name="bmtools_cache_format_alt",
        default=False,
        )
    # }}}
    
    # Deform Mode {{{
    bmtools_deform_mode: StringProperty(
        name="bmtools_deform_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_deform_mode_shift: BoolProperty(
        name="bmtools_deform_mode_shift",
        default=False,
        )
    
    bmtools_deform_mode_ctl: BoolProperty(
        name="bmtools_deform_mode_ctl",
        default=False,
        )
    
    bmtools_deform_mode_alt: BoolProperty(
        name="bmtools_deform_mode_alt",
        default=False,
        )
    # }}}
    
    # Play Mode {{{
    bmtools_play_mode: StringProperty(
        name="bmtools_play_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_play_mode_shift: BoolProperty(
        name="bmtools_play_mode_shift",
        default=False,
        )
    
    bmtools_play_mode_ctl: BoolProperty(
        name="bmtools_play_mode_ctl",
        default=False,
        )
    
    bmtools_play_mode_alt: BoolProperty(
        name="bmtools_play_mode_alt",
        default=False,
        )
    # }}}
    
    # Interpolation {{{
    bmtools_interpolation: StringProperty(
        name="bmtools_interpolation",
        maxlen=1,
        default='',
        )
    
    bmtools_interpolation_shift: BoolProperty(
        name="bmtools_interpolation_shift",
        default=False,
        )
    
    bmtools_interpolation_ctl: BoolProperty(
        name="bmtools_interpolation_ctl",
        default=False,
        )
    
    bmtools_interpolation_alt: BoolProperty(
        name="bmtools_interpolation_alt",
        default=False,
        )
    # }}}
    
    # Forward Axis {{{
    bmtools_forward_axis: StringProperty(
        name="bmtools_forward_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_forward_axis_shift: BoolProperty(
        name="bmtools_forward_axis_shift",
        default=False,
        )
    
    bmtools_forward_axis_ctl: BoolProperty(
        name="bmtools_forward_axis_ctl",
        default=False,
        )
    
    bmtools_forward_axis_alt: BoolProperty(
        name="bmtools_forward_axis_alt",
        default=False,
        )
    # }}}
    
    # Flip Axis {{{
    bmtools_flip_axis: StringProperty(
        name="bmtools_flip_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_flip_axis_shift: BoolProperty(
        name="bmtools_flip_axis_shift",
        default=False,
        )
    
    bmtools_flip_axis_ctl: BoolProperty(
        name="bmtools_flip_axis_ctl",
        default=False,
        )
    
    bmtools_flip_axis_alt: BoolProperty(
        name="bmtools_flip_axis_alt",
        default=False,
        )
    # }}}
    
    # Time Mode {{{
    bmtools_time_mode: StringProperty(
        name="bmtools_time_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_time_mode_shift: BoolProperty(
        name="bmtools_time_mode_shift",
        default=False,
        )
    
    bmtools_time_mode_ctl: BoolProperty(
        name="bmtools_time_mode_ctl",
        default=False,
        )
    
    bmtools_time_mode_alt: BoolProperty(
        name="bmtools_time_mode_alt",
        default=False,
        )
    # }}}
    
    # Read Data {{{
    bmtools_read_data: StringProperty(
        name="bmtools_read_data",
        maxlen=1,
        default='',
        )
    
    bmtools_read_data_shift: BoolProperty(
        name="bmtools_read_data_shift",
        default=False,
        )
    
    bmtools_read_data_ctl: BoolProperty(
        name="bmtools_read_data_ctl",
        default=False,
        )
    
    bmtools_read_data_alt: BoolProperty(
        name="bmtools_read_data_alt",
        default=False,
        )
    # }}}
    
    # Mode {{{
    bmtools_mode: StringProperty(
        name="bmtools_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_mode_shift: BoolProperty(
        name="bmtools_mode_shift",
        default=False,
        )
    
    bmtools_mode_ctl: BoolProperty(
        name="bmtools_mode_ctl",
        default=False,
        )
    
    bmtools_mode_alt: BoolProperty(
        name="bmtools_mode_alt",
        default=False,
        )
    # }}}
    
    # Axis V {{{
    bmtools_axis_v: StringProperty(
        name="bmtools_axis_v",
        maxlen=1,
        default='',
        )
    
    bmtools_axis_v_shift: BoolProperty(
        name="bmtools_axis_v_shift",
        default=False,
        )
    
    bmtools_axis_v_ctl: BoolProperty(
        name="bmtools_axis_v_ctl",
        default=False,
        )
    
    bmtools_axis_v_alt: BoolProperty(
        name="bmtools_axis_v_alt",
        default=False,
        )
    # }}}
    
    # Axis U {{{
    bmtools_axis_u: StringProperty(
        name="bmtools_axis_u",
        maxlen=1,
        default='',
        )
    
    bmtools_axis_u_shift: BoolProperty(
        name="bmtools_axis_u_shift",
        default=False,
        )
    
    bmtools_axis_u_ctl: BoolProperty(
        name="bmtools_axis_u_ctl",
        default=False,
        )
    
    bmtools_axis_u_alt: BoolProperty(
        name="bmtools_axis_u_alt",
        default=False,
        )
    # }}}
    
    # Mask Tex Mapping {{{
    bmtools_mask_tex_mapping: StringProperty(
        name="bmtools_mask_tex_mapping",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_tex_mapping_shift: BoolProperty(
        name="bmtools_mask_tex_mapping_shift",
        default=False,
        )
    
    bmtools_mask_tex_mapping_ctl: BoolProperty(
        name="bmtools_mask_tex_mapping_ctl",
        default=False,
        )
    
    bmtools_mask_tex_mapping_alt: BoolProperty(
        name="bmtools_mask_tex_mapping_alt",
        default=False,
        )
    # }}}
    
    # Mask Tex Use Channel {{{
    bmtools_mask_tex_use_channel: StringProperty(
        name="bmtools_mask_tex_use_channel",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_tex_use_channel_shift: BoolProperty(
        name="bmtools_mask_tex_use_channel_shift",
        default=False,
        )
    
    bmtools_mask_tex_use_channel_ctl: BoolProperty(
        name="bmtools_mask_tex_use_channel_ctl",
        default=False,
        )
    
    bmtools_mask_tex_use_channel_alt: BoolProperty(
        name="bmtools_mask_tex_use_channel_alt",
        default=False,
        )
    # }}}
    
    # Falloff Type {{{
    bmtools_falloff_type: StringProperty(
        name="bmtools_falloff_type",
        maxlen=1,
        default='',
        )
    
    bmtools_falloff_type_shift: BoolProperty(
        name="bmtools_falloff_type_shift",
        default=False,
        )
    
    bmtools_falloff_type_ctl: BoolProperty(
        name="bmtools_falloff_type_ctl",
        default=False,
        )
    
    bmtools_falloff_type_alt: BoolProperty(
        name="bmtools_falloff_type_alt",
        default=False,
        )
    # }}}
    
    # Mix Set {{{
    bmtools_mix_set: StringProperty(
        name="bmtools_mix_set",
        maxlen=1,
        default='',
        )
    
    bmtools_mix_set_shift: BoolProperty(
        name="bmtools_mix_set_shift",
        default=False,
        )
    
    bmtools_mix_set_ctl: BoolProperty(
        name="bmtools_mix_set_ctl",
        default=False,
        )
    
    bmtools_mix_set_alt: BoolProperty(
        name="bmtools_mix_set_alt",
        default=False,
        )
    # }}}
    
    # Proximity Mode {{{
    bmtools_proximity_mode: StringProperty(
        name="bmtools_proximity_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_proximity_mode_shift: BoolProperty(
        name="bmtools_proximity_mode_shift",
        default=False,
        )
    
    bmtools_proximity_mode_ctl: BoolProperty(
        name="bmtools_proximity_mode_ctl",
        default=False,
        )
    
    bmtools_proximity_mode_alt: BoolProperty(
        name="bmtools_proximity_mode_alt",
        default=False,
        )
    # }}}
    
    # Proximity Geometry {{{
    bmtools_proximity_geometry: StringProperty(
        name="bmtools_proximity_geometry",
        maxlen=1,
        default='',
        )
    
    bmtools_proximity_geometry_shift: BoolProperty(
        name="bmtools_proximity_geometry_shift",
        default=False,
        )
    
    bmtools_proximity_geometry_ctl: BoolProperty(
        name="bmtools_proximity_geometry_ctl",
        default=False,
        )
    
    bmtools_proximity_geometry_alt: BoolProperty(
        name="bmtools_proximity_geometry_alt",
        default=False,
        )
    # }}}
    
    # Fit Type {{{
    bmtools_fit_type: StringProperty(
        name="bmtools_fit_type",
        maxlen=1,
        default='',
        )
    
    bmtools_fit_type_shift: BoolProperty(
        name="bmtools_fit_type_shift",
        default=False,
        )
    
    bmtools_fit_type_ctl: BoolProperty(
        name="bmtools_fit_type_ctl",
        default=False,
        )
    
    bmtools_fit_type_alt: BoolProperty(
        name="bmtools_fit_type_alt",
        default=False,
        )
    # }}}
    
    # Face Strength Mode {{{
    bmtools_face_strength_mode: StringProperty(
        name="bmtools_face_strength_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_face_strength_mode_shift: BoolProperty(
        name="bmtools_face_strength_mode_shift",
        default=False,
        )
    
    bmtools_face_strength_mode_ctl: BoolProperty(
        name="bmtools_face_strength_mode_ctl",
        default=False,
        )
    
    bmtools_face_strength_mode_alt: BoolProperty(
        name="bmtools_face_strength_mode_alt",
        default=False,
        )
    # }}}
    
    # Profile Type {{{
    bmtools_profile_type: StringProperty(
        name="bmtools_profile_type",
        maxlen=1,
        default='',
        )
    
    bmtools_profile_type_shift: BoolProperty(
        name="bmtools_profile_type_shift",
        default=False,
        )
    
    bmtools_profile_type_ctl: BoolProperty(
        name="bmtools_profile_type_ctl",
        default=False,
        )
    
    bmtools_profile_type_alt: BoolProperty(
        name="bmtools_profile_type_alt",
        default=False,
        )
    # }}}
    
    # Miter Inner {{{
    bmtools_miter_inner: StringProperty(
        name="bmtools_miter_inner",
        maxlen=1,
        default='',
        )
    
    bmtools_miter_inner_shift: BoolProperty(
        name="bmtools_miter_inner_shift",
        default=False,
        )
    
    bmtools_miter_inner_ctl: BoolProperty(
        name="bmtools_miter_inner_ctl",
        default=False,
        )
    
    bmtools_miter_inner_alt: BoolProperty(
        name="bmtools_miter_inner_alt",
        default=False,
        )
    # }}}
    
    # Limit Method {{{
    bmtools_limit_method: StringProperty(
        name="bmtools_limit_method",
        maxlen=1,
        default='',
        )
    
    bmtools_limit_method_shift: BoolProperty(
        name="bmtools_limit_method_shift",
        default=False,
        )
    
    bmtools_limit_method_ctl: BoolProperty(
        name="bmtools_limit_method_ctl",
        default=False,
        )
    
    bmtools_limit_method_alt: BoolProperty(
        name="bmtools_limit_method_alt",
        default=False,
        )
    # }}}
    
    # Miter Outer {{{
    bmtools_miter_outer: StringProperty(
        name="bmtools_miter_outer",
        maxlen=1,
        default='',
        )
    
    bmtools_miter_outer_shift: BoolProperty(
        name="bmtools_miter_outer_shift",
        default=False,
        )
    
    bmtools_miter_outer_ctl: BoolProperty(
        name="bmtools_miter_outer_ctl",
        default=False,
        )
    
    bmtools_miter_outer_alt: BoolProperty(
        name="bmtools_miter_outer_alt",
        default=False,
        )
    # }}}
    
    # Vmesh Method {{{
    bmtools_vmesh_method: StringProperty(
        name="bmtools_vmesh_method",
        maxlen=1,
        default='',
        )
    
    bmtools_vmesh_method_shift: BoolProperty(
        name="bmtools_vmesh_method_shift",
        default=False,
        )
    
    bmtools_vmesh_method_ctl: BoolProperty(
        name="bmtools_vmesh_method_ctl",
        default=False,
        )
    
    bmtools_vmesh_method_alt: BoolProperty(
        name="bmtools_vmesh_method_alt",
        default=False,
        )
    # }}}
    
    # Affect {{{
    bmtools_affect: StringProperty(
        name="bmtools_affect",
        maxlen=1,
        default='',
        )
    
    bmtools_affect_shift: BoolProperty(
        name="bmtools_affect_shift",
        default=False,
        )
    
    bmtools_affect_ctl: BoolProperty(
        name="bmtools_affect_ctl",
        default=False,
        )
    
    bmtools_affect_alt: BoolProperty(
        name="bmtools_affect_alt",
        default=False,
        )
    # }}}
    
    # Offset Type {{{
    bmtools_offset_type: StringProperty(
        name="bmtools_offset_type",
        maxlen=1,
        default='',
        )
    
    bmtools_offset_type_shift: BoolProperty(
        name="bmtools_offset_type_shift",
        default=False,
        )
    
    bmtools_offset_type_ctl: BoolProperty(
        name="bmtools_offset_type_ctl",
        default=False,
        )
    
    bmtools_offset_type_alt: BoolProperty(
        name="bmtools_offset_type_alt",
        default=False,
        )
    # }}}
    
    # Debug Options {{{
    bmtools_debug_options: StringProperty(
        name="bmtools_debug_options",
        maxlen=1,
        default='',
        )
    
    bmtools_debug_options_shift: BoolProperty(
        name="bmtools_debug_options_shift",
        default=False,
        )
    
    bmtools_debug_options_ctl: BoolProperty(
        name="bmtools_debug_options_ctl",
        default=False,
        )
    
    bmtools_debug_options_alt: BoolProperty(
        name="bmtools_debug_options_alt",
        default=False,
        )
    # }}}
    
    # Solver {{{
    bmtools_solver: StringProperty(
        name="bmtools_solver",
        maxlen=1,
        default='',
        )
    
    bmtools_solver_shift: BoolProperty(
        name="bmtools_solver_shift",
        default=False,
        )
    
    bmtools_solver_ctl: BoolProperty(
        name="bmtools_solver_ctl",
        default=False,
        )
    
    bmtools_solver_alt: BoolProperty(
        name="bmtools_solver_alt",
        default=False,
        )
    # }}}
    
    # Operation {{{
    bmtools_operation: StringProperty(
        name="bmtools_operation",
        maxlen=1,
        default='',
        )
    
    bmtools_operation_shift: BoolProperty(
        name="bmtools_operation_shift",
        default=False,
        )
    
    bmtools_operation_ctl: BoolProperty(
        name="bmtools_operation_ctl",
        default=False,
        )
    
    bmtools_operation_alt: BoolProperty(
        name="bmtools_operation_alt",
        default=False,
        )
    # }}}
    
    # Operand Type {{{
    bmtools_operand_type: StringProperty(
        name="bmtools_operand_type",
        maxlen=1,
        default='',
        )
    
    bmtools_operand_type_shift: BoolProperty(
        name="bmtools_operand_type_shift",
        default=False,
        )
    
    bmtools_operand_type_ctl: BoolProperty(
        name="bmtools_operand_type_ctl",
        default=False,
        )
    
    bmtools_operand_type_alt: BoolProperty(
        name="bmtools_operand_type_alt",
        default=False,
        )
    # }}}
    
    # Symmetry Axis {{{
    bmtools_symmetry_axis: StringProperty(
        name="bmtools_symmetry_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_symmetry_axis_shift: BoolProperty(
        name="bmtools_symmetry_axis_shift",
        default=False,
        )
    
    bmtools_symmetry_axis_ctl: BoolProperty(
        name="bmtools_symmetry_axis_ctl",
        default=False,
        )
    
    bmtools_symmetry_axis_alt: BoolProperty(
        name="bmtools_symmetry_axis_alt",
        default=False,
        )
    # }}}
    
    # Delimit {{{
    bmtools_delimit: StringProperty(
        name="bmtools_delimit",
        maxlen=1,
        default='',
        )
    
    bmtools_delimit_shift: BoolProperty(
        name="bmtools_delimit_shift",
        default=False,
        )
    
    bmtools_delimit_ctl: BoolProperty(
        name="bmtools_delimit_ctl",
        default=False,
        )
    
    bmtools_delimit_alt: BoolProperty(
        name="bmtools_delimit_alt",
        default=False,
        )
    # }}}
    
    # Decimate Type {{{
    bmtools_decimate_type: StringProperty(
        name="bmtools_decimate_type",
        maxlen=1,
        default='',
        )
    
    bmtools_decimate_type_shift: BoolProperty(
        name="bmtools_decimate_type_shift",
        default=False,
        )
    
    bmtools_decimate_type_ctl: BoolProperty(
        name="bmtools_decimate_type_ctl",
        default=False,
        )
    
    bmtools_decimate_type_alt: BoolProperty(
        name="bmtools_decimate_type_alt",
        default=False,
        )
    # }}}
    
    # Uv Smooth {{{
    bmtools_uv_smooth: StringProperty(
        name="bmtools_uv_smooth",
        maxlen=1,
        default='',
        )
    
    bmtools_uv_smooth_shift: BoolProperty(
        name="bmtools_uv_smooth_shift",
        default=False,
        )
    
    bmtools_uv_smooth_ctl: BoolProperty(
        name="bmtools_uv_smooth_ctl",
        default=False,
        )
    
    bmtools_uv_smooth_alt: BoolProperty(
        name="bmtools_uv_smooth_alt",
        default=False,
        )
    # }}}
    
    # Boundary Smooth {{{
    bmtools_boundary_smooth: StringProperty(
        name="bmtools_boundary_smooth",
        maxlen=1,
        default='',
        )
    
    bmtools_boundary_smooth_shift: BoolProperty(
        name="bmtools_boundary_smooth_shift",
        default=False,
        )
    
    bmtools_boundary_smooth_ctl: BoolProperty(
        name="bmtools_boundary_smooth_ctl",
        default=False,
        )
    
    bmtools_boundary_smooth_alt: BoolProperty(
        name="bmtools_boundary_smooth_alt",
        default=False,
        )
    # }}}
    
    # Axis {{{
    bmtools_axis: StringProperty(
        name="bmtools_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_axis_shift: BoolProperty(
        name="bmtools_axis_shift",
        default=False,
        )
    
    bmtools_axis_ctl: BoolProperty(
        name="bmtools_axis_ctl",
        default=False,
        )
    
    bmtools_axis_alt: BoolProperty(
        name="bmtools_axis_alt",
        default=False,
        )
    # }}}
    
    # Nonmanifold Thickness Mode {{{
    bmtools_nonmanifold_thickness_mode: StringProperty(
        name="bmtools_nonmanifold_thickness_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_nonmanifold_thickness_mode_shift: BoolProperty(
        name="bmtools_nonmanifold_thickness_mode_shift",
        default=False,
        )
    
    bmtools_nonmanifold_thickness_mode_ctl: BoolProperty(
        name="bmtools_nonmanifold_thickness_mode_ctl",
        default=False,
        )
    
    bmtools_nonmanifold_thickness_mode_alt: BoolProperty(
        name="bmtools_nonmanifold_thickness_mode_alt",
        default=False,
        )
    # }}}
    
    # Solidify Mode {{{
    bmtools_solidify_mode: StringProperty(
        name="bmtools_solidify_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_solidify_mode_shift: BoolProperty(
        name="bmtools_solidify_mode_shift",
        default=False,
        )
    
    bmtools_solidify_mode_ctl: BoolProperty(
        name="bmtools_solidify_mode_ctl",
        default=False,
        )
    
    bmtools_solidify_mode_alt: BoolProperty(
        name="bmtools_solidify_mode_alt",
        default=False,
        )
    # }}}
    
    # Nonmanifold Boundary Mode {{{
    bmtools_nonmanifold_boundary_mode: StringProperty(
        name="bmtools_nonmanifold_boundary_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_nonmanifold_boundary_mode_shift: BoolProperty(
        name="bmtools_nonmanifold_boundary_mode_shift",
        default=False,
        )
    
    bmtools_nonmanifold_boundary_mode_ctl: BoolProperty(
        name="bmtools_nonmanifold_boundary_mode_ctl",
        default=False,
        )
    
    bmtools_nonmanifold_boundary_mode_alt: BoolProperty(
        name="bmtools_nonmanifold_boundary_mode_alt",
        default=False,
        )
    # }}}
    
    # Subdivision Type {{{
    bmtools_subdivision_type: StringProperty(
        name="bmtools_subdivision_type",
        maxlen=1,
        default='',
        )
    
    bmtools_subdivision_type_shift: BoolProperty(
        name="bmtools_subdivision_type_shift",
        default=False,
        )
    
    bmtools_subdivision_type_ctl: BoolProperty(
        name="bmtools_subdivision_type_ctl",
        default=False,
        )
    
    bmtools_subdivision_type_alt: BoolProperty(
        name="bmtools_subdivision_type_alt",
        default=False,
        )
    # }}}
    
    # Ngon Method {{{
    bmtools_ngon_method: StringProperty(
        name="bmtools_ngon_method",
        maxlen=1,
        default='',
        )
    
    bmtools_ngon_method_shift: BoolProperty(
        name="bmtools_ngon_method_shift",
        default=False,
        )
    
    bmtools_ngon_method_ctl: BoolProperty(
        name="bmtools_ngon_method_ctl",
        default=False,
        )
    
    bmtools_ngon_method_alt: BoolProperty(
        name="bmtools_ngon_method_alt",
        default=False,
        )
    # }}}
    
    # Quad Method {{{
    bmtools_quad_method: StringProperty(
        name="bmtools_quad_method",
        maxlen=1,
        default='',
        )
    
    bmtools_quad_method_shift: BoolProperty(
        name="bmtools_quad_method_shift",
        default=False,
        )
    
    bmtools_quad_method_ctl: BoolProperty(
        name="bmtools_quad_method_ctl",
        default=False,
        )
    
    bmtools_quad_method_alt: BoolProperty(
        name="bmtools_quad_method_alt",
        default=False,
        )
    # }}}
    
    # Resolution Mode {{{
    bmtools_resolution_mode: StringProperty(
        name="bmtools_resolution_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_resolution_mode_shift: BoolProperty(
        name="bmtools_resolution_mode_shift",
        default=False,
        )
    
    bmtools_resolution_mode_ctl: BoolProperty(
        name="bmtools_resolution_mode_ctl",
        default=False,
        )
    
    bmtools_resolution_mode_alt: BoolProperty(
        name="bmtools_resolution_mode_alt",
        default=False,
        )
    # }}}
    
    # Cast Type {{{
    bmtools_cast_type: StringProperty(
        name="bmtools_cast_type",
        maxlen=1,
        default='',
        )
    
    bmtools_cast_type_shift: BoolProperty(
        name="bmtools_cast_type_shift",
        default=False,
        )
    
    bmtools_cast_type_ctl: BoolProperty(
        name="bmtools_cast_type_ctl",
        default=False,
        )
    
    bmtools_cast_type_alt: BoolProperty(
        name="bmtools_cast_type_alt",
        default=False,
        )
    # }}}
    
    # Deform Axis {{{
    bmtools_deform_axis: StringProperty(
        name="bmtools_deform_axis",
        maxlen=1,
        default='',
        )
    
    bmtools_deform_axis_shift: BoolProperty(
        name="bmtools_deform_axis_shift",
        default=False,
        )
    
    bmtools_deform_axis_ctl: BoolProperty(
        name="bmtools_deform_axis_ctl",
        default=False,
        )
    
    bmtools_deform_axis_alt: BoolProperty(
        name="bmtools_deform_axis_alt",
        default=False,
        )
    # }}}
    
    # Space {{{
    bmtools_space: StringProperty(
        name="bmtools_space",
        maxlen=1,
        default='',
        )
    
    bmtools_space_shift: BoolProperty(
        name="bmtools_space_shift",
        default=False,
        )
    
    bmtools_space_ctl: BoolProperty(
        name="bmtools_space_ctl",
        default=False,
        )
    
    bmtools_space_alt: BoolProperty(
        name="bmtools_space_alt",
        default=False,
        )
    # }}}
    
    # Direction {{{
    bmtools_direction: StringProperty(
        name="bmtools_direction",
        maxlen=1,
        default='',
        )
    
    bmtools_direction_shift: BoolProperty(
        name="bmtools_direction_shift",
        default=False,
        )
    
    bmtools_direction_ctl: BoolProperty(
        name="bmtools_direction_ctl",
        default=False,
        )
    
    bmtools_direction_alt: BoolProperty(
        name="bmtools_direction_alt",
        default=False,
        )
    # }}}
    
    # Texture Coords {{{
    bmtools_texture_coords: StringProperty(
        name="bmtools_texture_coords",
        maxlen=1,
        default='',
        )
    
    bmtools_texture_coords_shift: BoolProperty(
        name="bmtools_texture_coords_shift",
        default=False,
        )
    
    bmtools_texture_coords_ctl: BoolProperty(
        name="bmtools_texture_coords_ctl",
        default=False,
        )
    
    bmtools_texture_coords_alt: BoolProperty(
        name="bmtools_texture_coords_alt",
        default=False,
        )
    # }}}
    
    # Wrap Method {{{
    bmtools_wrap_method: StringProperty(
        name="bmtools_wrap_method",
        maxlen=1,
        default='',
        )
    
    bmtools_wrap_method_shift: BoolProperty(
        name="bmtools_wrap_method_shift",
        default=False,
        )
    
    bmtools_wrap_method_ctl: BoolProperty(
        name="bmtools_wrap_method_ctl",
        default=False,
        )
    
    bmtools_wrap_method_alt: BoolProperty(
        name="bmtools_wrap_method_alt",
        default=False,
        )
    # }}}
    
    # Wrap Mode {{{
    bmtools_wrap_mode: StringProperty(
        name="bmtools_wrap_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_wrap_mode_shift: BoolProperty(
        name="bmtools_wrap_mode_shift",
        default=False,
        )
    
    bmtools_wrap_mode_ctl: BoolProperty(
        name="bmtools_wrap_mode_ctl",
        default=False,
        )
    
    bmtools_wrap_mode_alt: BoolProperty(
        name="bmtools_wrap_mode_alt",
        default=False,
        )
    # }}}
    
    # Cull Face {{{
    bmtools_cull_face: StringProperty(
        name="bmtools_cull_face",
        maxlen=1,
        default='',
        )
    
    bmtools_cull_face_shift: BoolProperty(
        name="bmtools_cull_face_shift",
        default=False,
        )
    
    bmtools_cull_face_ctl: BoolProperty(
        name="bmtools_cull_face_ctl",
        default=False,
        )
    
    bmtools_cull_face_alt: BoolProperty(
        name="bmtools_cull_face_alt",
        default=False,
        )
    # }}}
    
    # Deform Method {{{
    bmtools_deform_method: StringProperty(
        name="bmtools_deform_method",
        maxlen=1,
        default='',
        )
    
    bmtools_deform_method_shift: BoolProperty(
        name="bmtools_deform_method_shift",
        default=False,
        )
    
    bmtools_deform_method_ctl: BoolProperty(
        name="bmtools_deform_method_ctl",
        default=False,
        )
    
    bmtools_deform_method_alt: BoolProperty(
        name="bmtools_deform_method_alt",
        default=False,
        )
    # }}}
    
    # Smooth Type {{{
    bmtools_smooth_type: StringProperty(
        name="bmtools_smooth_type",
        maxlen=1,
        default='',
        )
    
    bmtools_smooth_type_shift: BoolProperty(
        name="bmtools_smooth_type_shift",
        default=False,
        )
    
    bmtools_smooth_type_ctl: BoolProperty(
        name="bmtools_smooth_type_ctl",
        default=False,
        )
    
    bmtools_smooth_type_alt: BoolProperty(
        name="bmtools_smooth_type_alt",
        default=False,
        )
    # }}}
    
    # Rest Source {{{
    bmtools_rest_source: StringProperty(
        name="bmtools_rest_source",
        maxlen=1,
        default='',
        )
    
    bmtools_rest_source_shift: BoolProperty(
        name="bmtools_rest_source_shift",
        default=False,
        )
    
    bmtools_rest_source_ctl: BoolProperty(
        name="bmtools_rest_source_ctl",
        default=False,
        )
    
    bmtools_rest_source_alt: BoolProperty(
        name="bmtools_rest_source_alt",
        default=False,
        )
    # }}}
    
    # Ui Type {{{
    bmtools_ui_type: StringProperty(
        name="bmtools_ui_type",
        maxlen=1,
        default='',
        )
    
    bmtools_ui_type_shift: BoolProperty(
        name="bmtools_ui_type_shift",
        default=False,
        )
    
    bmtools_ui_type_ctl: BoolProperty(
        name="bmtools_ui_type_ctl",
        default=False,
        )
    
    bmtools_ui_type_alt: BoolProperty(
        name="bmtools_ui_type_alt",
        default=False,
        )
    # }}}
    
    # Fluid Type {{{
    bmtools_fluid_type: StringProperty(
        name="bmtools_fluid_type",
        maxlen=1,
        default='',
        )
    
    bmtools_fluid_type_shift: BoolProperty(
        name="bmtools_fluid_type_shift",
        default=False,
        )
    
    bmtools_fluid_type_ctl: BoolProperty(
        name="bmtools_fluid_type_ctl",
        default=False,
        )
    
    bmtools_fluid_type_alt: BoolProperty(
        name="bmtools_fluid_type_alt",
        default=False,
        )
    # }}}
    
    # Spectrum {{{
    bmtools_spectrum: StringProperty(
        name="bmtools_spectrum",
        maxlen=1,
        default='',
        )
    
    bmtools_spectrum_shift: BoolProperty(
        name="bmtools_spectrum_shift",
        default=False,
        )
    
    bmtools_spectrum_ctl: BoolProperty(
        name="bmtools_spectrum_ctl",
        default=False,
        )
    
    bmtools_spectrum_alt: BoolProperty(
        name="bmtools_spectrum_alt",
        default=False,
        )
    # }}}
    
    # Geometry Mode {{{
    bmtools_geometry_mode: StringProperty(
        name="bmtools_geometry_mode",
        maxlen=1,
        default='',
        )
    
    bmtools_geometry_mode_shift: BoolProperty(
        name="bmtools_geometry_mode_shift",
        default=False,
        )
    
    bmtools_geometry_mode_ctl: BoolProperty(
        name="bmtools_geometry_mode_ctl",
        default=False,
        )
    
    bmtools_geometry_mode_alt: BoolProperty(
        name="bmtools_geometry_mode_alt",
        default=False,
        )
    # }}}
    
    # Ray Radius {{{
    bmtools_ray_radius: StringProperty(
        name="bmtools_ray_radius",
        maxlen=1,
        default='',
        )
    
    bmtools_ray_radius_shift: BoolProperty(
        name="bmtools_ray_radius_shift",
        default=False,
        )
    
    bmtools_ray_radius_ctl: BoolProperty(
        name="bmtools_ray_radius_ctl",
        default=False,
        )
    
    bmtools_ray_radius_alt: BoolProperty(
        name="bmtools_ray_radius_alt",
        default=False,
        )
    # }}}
    
    # Mix Factor {{{
    bmtools_mix_factor: StringProperty(
        name="bmtools_mix_factor",
        maxlen=1,
        default='',
        )
    
    bmtools_mix_factor_shift: BoolProperty(
        name="bmtools_mix_factor_shift",
        default=False,
        )
    
    bmtools_mix_factor_ctl: BoolProperty(
        name="bmtools_mix_factor_ctl",
        default=False,
        )
    
    bmtools_mix_factor_alt: BoolProperty(
        name="bmtools_mix_factor_alt",
        default=False,
        )
    # }}}
    
    # Islands Precision {{{
    bmtools_islands_precision: StringProperty(
        name="bmtools_islands_precision",
        maxlen=1,
        default='',
        )
    
    bmtools_islands_precision_shift: BoolProperty(
        name="bmtools_islands_precision_shift",
        default=False,
        )
    
    bmtools_islands_precision_ctl: BoolProperty(
        name="bmtools_islands_precision_ctl",
        default=False,
        )
    
    bmtools_islands_precision_alt: BoolProperty(
        name="bmtools_islands_precision_alt",
        default=False,
        )
    # }}}
    
    # Max Distance {{{
    bmtools_max_distance: StringProperty(
        name="bmtools_max_distance",
        maxlen=1,
        default='',
        )
    
    bmtools_max_distance_shift: BoolProperty(
        name="bmtools_max_distance_shift",
        default=False,
        )
    
    bmtools_max_distance_ctl: BoolProperty(
        name="bmtools_max_distance_ctl",
        default=False,
        )
    
    bmtools_max_distance_alt: BoolProperty(
        name="bmtools_max_distance_alt",
        default=False,
        )
    # }}}
    
    # Frame Scale {{{
    bmtools_frame_scale: StringProperty(
        name="bmtools_frame_scale",
        maxlen=1,
        default='',
        )
    
    bmtools_frame_scale_shift: BoolProperty(
        name="bmtools_frame_scale_shift",
        default=False,
        )
    
    bmtools_frame_scale_ctl: BoolProperty(
        name="bmtools_frame_scale_ctl",
        default=False,
        )
    
    bmtools_frame_scale_alt: BoolProperty(
        name="bmtools_frame_scale_alt",
        default=False,
        )
    # }}}
    
    # Eval Frame {{{
    bmtools_eval_frame: StringProperty(
        name="bmtools_eval_frame",
        maxlen=1,
        default='',
        )
    
    bmtools_eval_frame_shift: BoolProperty(
        name="bmtools_eval_frame_shift",
        default=False,
        )
    
    bmtools_eval_frame_ctl: BoolProperty(
        name="bmtools_eval_frame_ctl",
        default=False,
        )
    
    bmtools_eval_frame_alt: BoolProperty(
        name="bmtools_eval_frame_alt",
        default=False,
        )
    # }}}
    
    # Eval Time {{{
    bmtools_eval_time: StringProperty(
        name="bmtools_eval_time",
        maxlen=1,
        default='',
        )
    
    bmtools_eval_time_shift: BoolProperty(
        name="bmtools_eval_time_shift",
        default=False,
        )
    
    bmtools_eval_time_ctl: BoolProperty(
        name="bmtools_eval_time_ctl",
        default=False,
        )
    
    bmtools_eval_time_alt: BoolProperty(
        name="bmtools_eval_time_alt",
        default=False,
        )
    # }}}
    
    # Frame Start {{{
    bmtools_frame_start: StringProperty(
        name="bmtools_frame_start",
        maxlen=1,
        default='',
        )
    
    bmtools_frame_start_shift: BoolProperty(
        name="bmtools_frame_start_shift",
        default=False,
        )
    
    bmtools_frame_start_ctl: BoolProperty(
        name="bmtools_frame_start_ctl",
        default=False,
        )
    
    bmtools_frame_start_alt: BoolProperty(
        name="bmtools_frame_start_alt",
        default=False,
        )
    # }}}
    
    # Eval Factor {{{
    bmtools_eval_factor: StringProperty(
        name="bmtools_eval_factor",
        maxlen=1,
        default='',
        )
    
    bmtools_eval_factor_shift: BoolProperty(
        name="bmtools_eval_factor_shift",
        default=False,
        )
    
    bmtools_eval_factor_ctl: BoolProperty(
        name="bmtools_eval_factor_ctl",
        default=False,
        )
    
    bmtools_eval_factor_alt: BoolProperty(
        name="bmtools_eval_factor_alt",
        default=False,
        )
    # }}}
    
    # Factor {{{
    bmtools_factor: StringProperty(
        name="bmtools_factor",
        maxlen=1,
        default='',
        )
    
    bmtools_factor_shift: BoolProperty(
        name="bmtools_factor_shift",
        default=False,
        )
    
    bmtools_factor_ctl: BoolProperty(
        name="bmtools_factor_ctl",
        default=False,
        )
    
    bmtools_factor_alt: BoolProperty(
        name="bmtools_factor_alt",
        default=False,
        )
    # }}}
    
    # Velocity Scale {{{
    bmtools_velocity_scale: StringProperty(
        name="bmtools_velocity_scale",
        maxlen=1,
        default='',
        )
    
    bmtools_velocity_scale_shift: BoolProperty(
        name="bmtools_velocity_scale_shift",
        default=False,
        )
    
    bmtools_velocity_scale_ctl: BoolProperty(
        name="bmtools_velocity_scale_ctl",
        default=False,
        )
    
    bmtools_velocity_scale_alt: BoolProperty(
        name="bmtools_velocity_scale_alt",
        default=False,
        )
    # }}}
    
    # Mix Limit {{{
    bmtools_mix_limit: StringProperty(
        name="bmtools_mix_limit",
        maxlen=1,
        default='',
        )
    
    bmtools_mix_limit_shift: BoolProperty(
        name="bmtools_mix_limit_shift",
        default=False,
        )
    
    bmtools_mix_limit_ctl: BoolProperty(
        name="bmtools_mix_limit_ctl",
        default=False,
        )
    
    bmtools_mix_limit_alt: BoolProperty(
        name="bmtools_mix_limit_alt",
        default=False,
        )
    # }}}
    
    # Offset {{{
    bmtools_offset: StringProperty(
        name="bmtools_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_offset_shift: BoolProperty(
        name="bmtools_offset_shift",
        default=False,
        )
    
    bmtools_offset_ctl: BoolProperty(
        name="bmtools_offset_ctl",
        default=False,
        )
    
    bmtools_offset_alt: BoolProperty(
        name="bmtools_offset_alt",
        default=False,
        )
    # }}}
    
    # Thresh {{{
    bmtools_thresh: StringProperty(
        name="bmtools_thresh",
        maxlen=1,
        default='',
        )
    
    bmtools_thresh_shift: BoolProperty(
        name="bmtools_thresh_shift",
        default=False,
        )
    
    bmtools_thresh_ctl: BoolProperty(
        name="bmtools_thresh_ctl",
        default=False,
        )
    
    bmtools_thresh_alt: BoolProperty(
        name="bmtools_thresh_alt",
        default=False,
        )
    # }}}
    
    # Aspect Y {{{
    bmtools_aspect_y: StringProperty(
        name="bmtools_aspect_y",
        maxlen=1,
        default='',
        )
    
    bmtools_aspect_y_shift: BoolProperty(
        name="bmtools_aspect_y_shift",
        default=False,
        )
    
    bmtools_aspect_y_ctl: BoolProperty(
        name="bmtools_aspect_y_ctl",
        default=False,
        )
    
    bmtools_aspect_y_alt: BoolProperty(
        name="bmtools_aspect_y_alt",
        default=False,
        )
    # }}}
    
    # Aspect X {{{
    bmtools_aspect_x: StringProperty(
        name="bmtools_aspect_x",
        maxlen=1,
        default='',
        )
    
    bmtools_aspect_x_shift: BoolProperty(
        name="bmtools_aspect_x_shift",
        default=False,
        )
    
    bmtools_aspect_x_ctl: BoolProperty(
        name="bmtools_aspect_x_ctl",
        default=False,
        )
    
    bmtools_aspect_x_alt: BoolProperty(
        name="bmtools_aspect_x_alt",
        default=False,
        )
    # }}}
    
    # Scale Y {{{
    bmtools_scale_y: StringProperty(
        name="bmtools_scale_y",
        maxlen=1,
        default='',
        )
    
    bmtools_scale_y_shift: BoolProperty(
        name="bmtools_scale_y_shift",
        default=False,
        )
    
    bmtools_scale_y_ctl: BoolProperty(
        name="bmtools_scale_y_ctl",
        default=False,
        )
    
    bmtools_scale_y_alt: BoolProperty(
        name="bmtools_scale_y_alt",
        default=False,
        )
    # }}}
    
    # Scale X {{{
    bmtools_scale_x: StringProperty(
        name="bmtools_scale_x",
        maxlen=1,
        default='',
        )
    
    bmtools_scale_x_shift: BoolProperty(
        name="bmtools_scale_x_shift",
        default=False,
        )
    
    bmtools_scale_x_ctl: BoolProperty(
        name="bmtools_scale_x_ctl",
        default=False,
        )
    
    bmtools_scale_x_alt: BoolProperty(
        name="bmtools_scale_x_alt",
        default=False,
        )
    # }}}
    
    # Rotation {{{
    bmtools_rotation: StringProperty(
        name="bmtools_rotation",
        maxlen=1,
        default='',
        )
    
    bmtools_rotation_shift: BoolProperty(
        name="bmtools_rotation_shift",
        default=False,
        )
    
    bmtools_rotation_ctl: BoolProperty(
        name="bmtools_rotation_ctl",
        default=False,
        )
    
    bmtools_rotation_alt: BoolProperty(
        name="bmtools_rotation_alt",
        default=False,
        )
    # }}}
    
    # Center {{{
    bmtools_center: StringProperty(
        name="bmtools_center",
        maxlen=1,
        default='',
        )
    
    bmtools_center_shift: BoolProperty(
        name="bmtools_center_shift",
        default=False,
        )
    
    bmtools_center_ctl: BoolProperty(
        name="bmtools_center_ctl",
        default=False,
        )
    
    bmtools_center_alt: BoolProperty(
        name="bmtools_center_alt",
        default=False,
        )
    # }}}
    
    # Scale {{{
    bmtools_scale: StringProperty(
        name="bmtools_scale",
        maxlen=1,
        default='',
        )
    
    bmtools_scale_shift: BoolProperty(
        name="bmtools_scale_shift",
        default=False,
        )
    
    bmtools_scale_ctl: BoolProperty(
        name="bmtools_scale_ctl",
        default=False,
        )
    
    bmtools_scale_alt: BoolProperty(
        name="bmtools_scale_alt",
        default=False,
        )
    # }}}
    
    # Mask Constant {{{
    bmtools_mask_constant: StringProperty(
        name="bmtools_mask_constant",
        maxlen=1,
        default='',
        )
    
    bmtools_mask_constant_shift: BoolProperty(
        name="bmtools_mask_constant_shift",
        default=False,
        )
    
    bmtools_mask_constant_ctl: BoolProperty(
        name="bmtools_mask_constant_ctl",
        default=False,
        )
    
    bmtools_mask_constant_alt: BoolProperty(
        name="bmtools_mask_constant_alt",
        default=False,
        )
    # }}}
    
    # Add Threshold {{{
    bmtools_add_threshold: StringProperty(
        name="bmtools_add_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_add_threshold_shift: BoolProperty(
        name="bmtools_add_threshold_shift",
        default=False,
        )
    
    bmtools_add_threshold_ctl: BoolProperty(
        name="bmtools_add_threshold_ctl",
        default=False,
        )
    
    bmtools_add_threshold_alt: BoolProperty(
        name="bmtools_add_threshold_alt",
        default=False,
        )
    # }}}
    
    # Default Weight {{{
    bmtools_default_weight: StringProperty(
        name="bmtools_default_weight",
        maxlen=1,
        default='',
        )
    
    bmtools_default_weight_shift: BoolProperty(
        name="bmtools_default_weight_shift",
        default=False,
        )
    
    bmtools_default_weight_ctl: BoolProperty(
        name="bmtools_default_weight_ctl",
        default=False,
        )
    
    bmtools_default_weight_alt: BoolProperty(
        name="bmtools_default_weight_alt",
        default=False,
        )
    # }}}
    
    # Remove Threshold {{{
    bmtools_remove_threshold: StringProperty(
        name="bmtools_remove_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_remove_threshold_shift: BoolProperty(
        name="bmtools_remove_threshold_shift",
        default=False,
        )
    
    bmtools_remove_threshold_ctl: BoolProperty(
        name="bmtools_remove_threshold_ctl",
        default=False,
        )
    
    bmtools_remove_threshold_alt: BoolProperty(
        name="bmtools_remove_threshold_alt",
        default=False,
        )
    # }}}
    
    # Default Weight A {{{
    bmtools_default_weight_a: StringProperty(
        name="bmtools_default_weight_a",
        maxlen=1,
        default='',
        )
    
    bmtools_default_weight_a_shift: BoolProperty(
        name="bmtools_default_weight_a_shift",
        default=False,
        )
    
    bmtools_default_weight_a_ctl: BoolProperty(
        name="bmtools_default_weight_a_ctl",
        default=False,
        )
    
    bmtools_default_weight_a_alt: BoolProperty(
        name="bmtools_default_weight_a_alt",
        default=False,
        )
    # }}}
    
    # Default Weight B {{{
    bmtools_default_weight_b: StringProperty(
        name="bmtools_default_weight_b",
        maxlen=1,
        default='',
        )
    
    bmtools_default_weight_b_shift: BoolProperty(
        name="bmtools_default_weight_b_shift",
        default=False,
        )
    
    bmtools_default_weight_b_ctl: BoolProperty(
        name="bmtools_default_weight_b_ctl",
        default=False,
        )
    
    bmtools_default_weight_b_alt: BoolProperty(
        name="bmtools_default_weight_b_alt",
        default=False,
        )
    # }}}
    
    # Max Dist {{{
    bmtools_max_dist: StringProperty(
        name="bmtools_max_dist",
        maxlen=1,
        default='',
        )
    
    bmtools_max_dist_shift: BoolProperty(
        name="bmtools_max_dist_shift",
        default=False,
        )
    
    bmtools_max_dist_ctl: BoolProperty(
        name="bmtools_max_dist_ctl",
        default=False,
        )
    
    bmtools_max_dist_alt: BoolProperty(
        name="bmtools_max_dist_alt",
        default=False,
        )
    # }}}
    
    # Min Dist {{{
    bmtools_min_dist: StringProperty(
        name="bmtools_min_dist",
        maxlen=1,
        default='',
        )
    
    bmtools_min_dist_shift: BoolProperty(
        name="bmtools_min_dist_shift",
        default=False,
        )
    
    bmtools_min_dist_ctl: BoolProperty(
        name="bmtools_min_dist_ctl",
        default=False,
        )
    
    bmtools_min_dist_alt: BoolProperty(
        name="bmtools_min_dist_alt",
        default=False,
        )
    # }}}
    
    # Relative Offset Displace {{{
    bmtools_relative_offset_displace: StringProperty(
        name="bmtools_relative_offset_displace",
        maxlen=1,
        default='',
        )
    
    bmtools_relative_offset_displace_shift: BoolProperty(
        name="bmtools_relative_offset_displace_shift",
        default=False,
        )
    
    bmtools_relative_offset_displace_ctl: BoolProperty(
        name="bmtools_relative_offset_displace_ctl",
        default=False,
        )
    
    bmtools_relative_offset_displace_alt: BoolProperty(
        name="bmtools_relative_offset_displace_alt",
        default=False,
        )
    # }}}
    
    # Constant Offset Displace {{{
    bmtools_constant_offset_displace: StringProperty(
        name="bmtools_constant_offset_displace",
        maxlen=1,
        default='',
        )
    
    bmtools_constant_offset_displace_shift: BoolProperty(
        name="bmtools_constant_offset_displace_shift",
        default=False,
        )
    
    bmtools_constant_offset_displace_ctl: BoolProperty(
        name="bmtools_constant_offset_displace_ctl",
        default=False,
        )
    
    bmtools_constant_offset_displace_alt: BoolProperty(
        name="bmtools_constant_offset_displace_alt",
        default=False,
        )
    # }}}
    
    # Fit Length {{{
    bmtools_fit_length: StringProperty(
        name="bmtools_fit_length",
        maxlen=1,
        default='',
        )
    
    bmtools_fit_length_shift: BoolProperty(
        name="bmtools_fit_length_shift",
        default=False,
        )
    
    bmtools_fit_length_ctl: BoolProperty(
        name="bmtools_fit_length_ctl",
        default=False,
        )
    
    bmtools_fit_length_alt: BoolProperty(
        name="bmtools_fit_length_alt",
        default=False,
        )
    # }}}
    
    # Merge Threshold {{{
    bmtools_merge_threshold: StringProperty(
        name="bmtools_merge_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_merge_threshold_shift: BoolProperty(
        name="bmtools_merge_threshold_shift",
        default=False,
        )
    
    bmtools_merge_threshold_ctl: BoolProperty(
        name="bmtools_merge_threshold_ctl",
        default=False,
        )
    
    bmtools_merge_threshold_alt: BoolProperty(
        name="bmtools_merge_threshold_alt",
        default=False,
        )
    # }}}
    
    # Offset V {{{
    bmtools_offset_v: StringProperty(
        name="bmtools_offset_v",
        maxlen=1,
        default='',
        )
    
    bmtools_offset_v_shift: BoolProperty(
        name="bmtools_offset_v_shift",
        default=False,
        )
    
    bmtools_offset_v_ctl: BoolProperty(
        name="bmtools_offset_v_ctl",
        default=False,
        )
    
    bmtools_offset_v_alt: BoolProperty(
        name="bmtools_offset_v_alt",
        default=False,
        )
    # }}}
    
    # Offset U {{{
    bmtools_offset_u: StringProperty(
        name="bmtools_offset_u",
        maxlen=1,
        default='',
        )
    
    bmtools_offset_u_shift: BoolProperty(
        name="bmtools_offset_u_shift",
        default=False,
        )
    
    bmtools_offset_u_ctl: BoolProperty(
        name="bmtools_offset_u_ctl",
        default=False,
        )
    
    bmtools_offset_u_alt: BoolProperty(
        name="bmtools_offset_u_alt",
        default=False,
        )
    # }}}
    
    # Angle Limit {{{
    bmtools_angle_limit: StringProperty(
        name="bmtools_angle_limit",
        maxlen=1,
        default='',
        )
    
    bmtools_angle_limit_shift: BoolProperty(
        name="bmtools_angle_limit_shift",
        default=False,
        )
    
    bmtools_angle_limit_ctl: BoolProperty(
        name="bmtools_angle_limit_ctl",
        default=False,
        )
    
    bmtools_angle_limit_alt: BoolProperty(
        name="bmtools_angle_limit_alt",
        default=False,
        )
    # }}}
    
    # Spread {{{
    bmtools_spread: StringProperty(
        name="bmtools_spread",
        maxlen=1,
        default='',
        )
    
    bmtools_spread_shift: BoolProperty(
        name="bmtools_spread_shift",
        default=False,
        )
    
    bmtools_spread_ctl: BoolProperty(
        name="bmtools_spread_ctl",
        default=False,
        )
    
    bmtools_spread_alt: BoolProperty(
        name="bmtools_spread_alt",
        default=False,
        )
    # }}}
    
    # Width {{{
    bmtools_width: StringProperty(
        name="bmtools_width",
        maxlen=1,
        default='',
        )
    
    bmtools_width_shift: BoolProperty(
        name="bmtools_width_shift",
        default=False,
        )
    
    bmtools_width_ctl: BoolProperty(
        name="bmtools_width_ctl",
        default=False,
        )
    
    bmtools_width_alt: BoolProperty(
        name="bmtools_width_alt",
        default=False,
        )
    # }}}
    
    # Width Pct {{{
    bmtools_width_pct: StringProperty(
        name="bmtools_width_pct",
        maxlen=1,
        default='',
        )
    
    bmtools_width_pct_shift: BoolProperty(
        name="bmtools_width_pct_shift",
        default=False,
        )
    
    bmtools_width_pct_ctl: BoolProperty(
        name="bmtools_width_pct_ctl",
        default=False,
        )
    
    bmtools_width_pct_alt: BoolProperty(
        name="bmtools_width_pct_alt",
        default=False,
        )
    # }}}
    
    # Profile {{{
    bmtools_profile: StringProperty(
        name="bmtools_profile",
        maxlen=1,
        default='',
        )
    
    bmtools_profile_shift: BoolProperty(
        name="bmtools_profile_shift",
        default=False,
        )
    
    bmtools_profile_ctl: BoolProperty(
        name="bmtools_profile_ctl",
        default=False,
        )
    
    bmtools_profile_alt: BoolProperty(
        name="bmtools_profile_alt",
        default=False,
        )
    # }}}
    
    # Double Threshold {{{
    bmtools_double_threshold: StringProperty(
        name="bmtools_double_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_double_threshold_shift: BoolProperty(
        name="bmtools_double_threshold_shift",
        default=False,
        )
    
    bmtools_double_threshold_ctl: BoolProperty(
        name="bmtools_double_threshold_ctl",
        default=False,
        )
    
    bmtools_double_threshold_alt: BoolProperty(
        name="bmtools_double_threshold_alt",
        default=False,
        )
    # }}}
    
    # Frame Duration {{{
    bmtools_frame_duration: StringProperty(
        name="bmtools_frame_duration",
        maxlen=1,
        default='',
        )
    
    bmtools_frame_duration_shift: BoolProperty(
        name="bmtools_frame_duration_shift",
        default=False,
        )
    
    bmtools_frame_duration_ctl: BoolProperty(
        name="bmtools_frame_duration_ctl",
        default=False,
        )
    
    bmtools_frame_duration_alt: BoolProperty(
        name="bmtools_frame_duration_alt",
        default=False,
        )
    # }}}
    
    # Vertex Group Factor {{{
    bmtools_vertex_group_factor: StringProperty(
        name="bmtools_vertex_group_factor",
        maxlen=1,
        default='',
        )
    
    bmtools_vertex_group_factor_shift: BoolProperty(
        name="bmtools_vertex_group_factor_shift",
        default=False,
        )
    
    bmtools_vertex_group_factor_ctl: BoolProperty(
        name="bmtools_vertex_group_factor_ctl",
        default=False,
        )
    
    bmtools_vertex_group_factor_alt: BoolProperty(
        name="bmtools_vertex_group_factor_alt",
        default=False,
        )
    # }}}
    
    # Ratio {{{
    bmtools_ratio: StringProperty(
        name="bmtools_ratio",
        maxlen=1,
        default='',
        )
    
    bmtools_ratio_shift: BoolProperty(
        name="bmtools_ratio_shift",
        default=False,
        )
    
    bmtools_ratio_ctl: BoolProperty(
        name="bmtools_ratio_ctl",
        default=False,
        )
    
    bmtools_ratio_alt: BoolProperty(
        name="bmtools_ratio_alt",
        default=False,
        )
    # }}}
    
    # Split Angle {{{
    bmtools_split_angle: StringProperty(
        name="bmtools_split_angle",
        maxlen=1,
        default='',
        )
    
    bmtools_split_angle_shift: BoolProperty(
        name="bmtools_split_angle_shift",
        default=False,
        )
    
    bmtools_split_angle_ctl: BoolProperty(
        name="bmtools_split_angle_ctl",
        default=False,
        )
    
    bmtools_split_angle_alt: BoolProperty(
        name="bmtools_split_angle_alt",
        default=False,
        )
    # }}}
    
    # Threshold {{{
    bmtools_threshold: StringProperty(
        name="bmtools_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_threshold_shift: BoolProperty(
        name="bmtools_threshold_shift",
        default=False,
        )
    
    bmtools_threshold_ctl: BoolProperty(
        name="bmtools_threshold_ctl",
        default=False,
        )
    
    bmtools_threshold_alt: BoolProperty(
        name="bmtools_threshold_alt",
        default=False,
        )
    # }}}
    
    # Mirror Offset V {{{
    bmtools_mirror_offset_v: StringProperty(
        name="bmtools_mirror_offset_v",
        maxlen=1,
        default='',
        )
    
    bmtools_mirror_offset_v_shift: BoolProperty(
        name="bmtools_mirror_offset_v_shift",
        default=False,
        )
    
    bmtools_mirror_offset_v_ctl: BoolProperty(
        name="bmtools_mirror_offset_v_ctl",
        default=False,
        )
    
    bmtools_mirror_offset_v_alt: BoolProperty(
        name="bmtools_mirror_offset_v_alt",
        default=False,
        )
    # }}}
    
    # Bisect Threshold {{{
    bmtools_bisect_threshold: StringProperty(
        name="bmtools_bisect_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_bisect_threshold_shift: BoolProperty(
        name="bmtools_bisect_threshold_shift",
        default=False,
        )
    
    bmtools_bisect_threshold_ctl: BoolProperty(
        name="bmtools_bisect_threshold_ctl",
        default=False,
        )
    
    bmtools_bisect_threshold_alt: BoolProperty(
        name="bmtools_bisect_threshold_alt",
        default=False,
        )
    # }}}
    
    # Mirror Offset U {{{
    bmtools_mirror_offset_u: StringProperty(
        name="bmtools_mirror_offset_u",
        maxlen=1,
        default='',
        )
    
    bmtools_mirror_offset_u_shift: BoolProperty(
        name="bmtools_mirror_offset_u_shift",
        default=False,
        )
    
    bmtools_mirror_offset_u_ctl: BoolProperty(
        name="bmtools_mirror_offset_u_ctl",
        default=False,
        )
    
    bmtools_mirror_offset_u_alt: BoolProperty(
        name="bmtools_mirror_offset_u_alt",
        default=False,
        )
    # }}}
    
    # Sharpness {{{
    bmtools_sharpness: StringProperty(
        name="bmtools_sharpness",
        maxlen=1,
        default='',
        )
    
    bmtools_sharpness_shift: BoolProperty(
        name="bmtools_sharpness_shift",
        default=False,
        )
    
    bmtools_sharpness_ctl: BoolProperty(
        name="bmtools_sharpness_ctl",
        default=False,
        )
    
    bmtools_sharpness_alt: BoolProperty(
        name="bmtools_sharpness_alt",
        default=False,
        )
    # }}}
    
    # Adaptivity {{{
    bmtools_adaptivity: StringProperty(
        name="bmtools_adaptivity",
        maxlen=1,
        default='',
        )
    
    bmtools_adaptivity_shift: BoolProperty(
        name="bmtools_adaptivity_shift",
        default=False,
        )
    
    bmtools_adaptivity_ctl: BoolProperty(
        name="bmtools_adaptivity_ctl",
        default=False,
        )
    
    bmtools_adaptivity_alt: BoolProperty(
        name="bmtools_adaptivity_alt",
        default=False,
        )
    # }}}
    
    # Voxel Size {{{
    bmtools_voxel_size: StringProperty(
        name="bmtools_voxel_size",
        maxlen=1,
        default='',
        )
    
    bmtools_voxel_size_shift: BoolProperty(
        name="bmtools_voxel_size_shift",
        default=False,
        )
    
    bmtools_voxel_size_ctl: BoolProperty(
        name="bmtools_voxel_size_ctl",
        default=False,
        )
    
    bmtools_voxel_size_alt: BoolProperty(
        name="bmtools_voxel_size_alt",
        default=False,
        )
    # }}}
    
    # Screw Offset {{{
    bmtools_screw_offset: StringProperty(
        name="bmtools_screw_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_screw_offset_shift: BoolProperty(
        name="bmtools_screw_offset_shift",
        default=False,
        )
    
    bmtools_screw_offset_ctl: BoolProperty(
        name="bmtools_screw_offset_ctl",
        default=False,
        )
    
    bmtools_screw_offset_alt: BoolProperty(
        name="bmtools_screw_offset_alt",
        default=False,
        )
    # }}}
    
    # Angle {{{
    bmtools_angle: StringProperty(
        name="bmtools_angle",
        maxlen=1,
        default='',
        )
    
    bmtools_angle_shift: BoolProperty(
        name="bmtools_angle_shift",
        default=False,
        )
    
    bmtools_angle_ctl: BoolProperty(
        name="bmtools_angle_ctl",
        default=False,
        )
    
    bmtools_angle_alt: BoolProperty(
        name="bmtools_angle_alt",
        default=False,
        )
    # }}}
    
    # Branch Smoothing {{{
    bmtools_branch_smoothing: StringProperty(
        name="bmtools_branch_smoothing",
        maxlen=1,
        default='',
        )
    
    bmtools_branch_smoothing_shift: BoolProperty(
        name="bmtools_branch_smoothing_shift",
        default=False,
        )
    
    bmtools_branch_smoothing_ctl: BoolProperty(
        name="bmtools_branch_smoothing_ctl",
        default=False,
        )
    
    bmtools_branch_smoothing_alt: BoolProperty(
        name="bmtools_branch_smoothing_alt",
        default=False,
        )
    # }}}
    
    # Edge Crease Inner {{{
    bmtools_edge_crease_inner: StringProperty(
        name="bmtools_edge_crease_inner",
        maxlen=1,
        default='',
        )
    
    bmtools_edge_crease_inner_shift: BoolProperty(
        name="bmtools_edge_crease_inner_shift",
        default=False,
        )
    
    bmtools_edge_crease_inner_ctl: BoolProperty(
        name="bmtools_edge_crease_inner_ctl",
        default=False,
        )
    
    bmtools_edge_crease_inner_alt: BoolProperty(
        name="bmtools_edge_crease_inner_alt",
        default=False,
        )
    # }}}
    
    # Nonmanifold Merge Threshold {{{
    bmtools_nonmanifold_merge_threshold: StringProperty(
        name="bmtools_nonmanifold_merge_threshold",
        maxlen=1,
        default='',
        )
    
    bmtools_nonmanifold_merge_threshold_shift: BoolProperty(
        name="bmtools_nonmanifold_merge_threshold_shift",
        default=False,
        )
    
    bmtools_nonmanifold_merge_threshold_ctl: BoolProperty(
        name="bmtools_nonmanifold_merge_threshold_ctl",
        default=False,
        )
    
    bmtools_nonmanifold_merge_threshold_alt: BoolProperty(
        name="bmtools_nonmanifold_merge_threshold_alt",
        default=False,
        )
    # }}}
    
    # Thickness Vertex Group {{{
    bmtools_thickness_vertex_group: StringProperty(
        name="bmtools_thickness_vertex_group",
        maxlen=1,
        default='',
        )
    
    bmtools_thickness_vertex_group_shift: BoolProperty(
        name="bmtools_thickness_vertex_group_shift",
        default=False,
        )
    
    bmtools_thickness_vertex_group_ctl: BoolProperty(
        name="bmtools_thickness_vertex_group_ctl",
        default=False,
        )
    
    bmtools_thickness_vertex_group_alt: BoolProperty(
        name="bmtools_thickness_vertex_group_alt",
        default=False,
        )
    # }}}
    
    # Thickness {{{
    bmtools_thickness: StringProperty(
        name="bmtools_thickness",
        maxlen=1,
        default='',
        )
    
    bmtools_thickness_shift: BoolProperty(
        name="bmtools_thickness_shift",
        default=False,
        )
    
    bmtools_thickness_ctl: BoolProperty(
        name="bmtools_thickness_ctl",
        default=False,
        )
    
    bmtools_thickness_alt: BoolProperty(
        name="bmtools_thickness_alt",
        default=False,
        )
    # }}}
    
    # Edge Crease Rim {{{
    bmtools_edge_crease_rim: StringProperty(
        name="bmtools_edge_crease_rim",
        maxlen=1,
        default='',
        )
    
    bmtools_edge_crease_rim_shift: BoolProperty(
        name="bmtools_edge_crease_rim_shift",
        default=False,
        )
    
    bmtools_edge_crease_rim_ctl: BoolProperty(
        name="bmtools_edge_crease_rim_ctl",
        default=False,
        )
    
    bmtools_edge_crease_rim_alt: BoolProperty(
        name="bmtools_edge_crease_rim_alt",
        default=False,
        )
    # }}}
    
    # Bevel Convex {{{
    bmtools_bevel_convex: StringProperty(
        name="bmtools_bevel_convex",
        maxlen=1,
        default='',
        )
    
    bmtools_bevel_convex_shift: BoolProperty(
        name="bmtools_bevel_convex_shift",
        default=False,
        )
    
    bmtools_bevel_convex_ctl: BoolProperty(
        name="bmtools_bevel_convex_ctl",
        default=False,
        )
    
    bmtools_bevel_convex_alt: BoolProperty(
        name="bmtools_bevel_convex_alt",
        default=False,
        )
    # }}}
    
    # Thickness Clamp {{{
    bmtools_thickness_clamp: StringProperty(
        name="bmtools_thickness_clamp",
        maxlen=1,
        default='',
        )
    
    bmtools_thickness_clamp_shift: BoolProperty(
        name="bmtools_thickness_clamp_shift",
        default=False,
        )
    
    bmtools_thickness_clamp_ctl: BoolProperty(
        name="bmtools_thickness_clamp_ctl",
        default=False,
        )
    
    bmtools_thickness_clamp_alt: BoolProperty(
        name="bmtools_thickness_clamp_alt",
        default=False,
        )
    # }}}
    
    # Edge Crease Outer {{{
    bmtools_edge_crease_outer: StringProperty(
        name="bmtools_edge_crease_outer",
        maxlen=1,
        default='',
        )
    
    bmtools_edge_crease_outer_shift: BoolProperty(
        name="bmtools_edge_crease_outer_shift",
        default=False,
        )
    
    bmtools_edge_crease_outer_ctl: BoolProperty(
        name="bmtools_edge_crease_outer_ctl",
        default=False,
        )
    
    bmtools_edge_crease_outer_alt: BoolProperty(
        name="bmtools_edge_crease_outer_alt",
        default=False,
        )
    # }}}
    
    # Crease Weight {{{
    bmtools_crease_weight: StringProperty(
        name="bmtools_crease_weight",
        maxlen=1,
        default='',
        )
    
    bmtools_crease_weight_shift: BoolProperty(
        name="bmtools_crease_weight_shift",
        default=False,
        )
    
    bmtools_crease_weight_ctl: BoolProperty(
        name="bmtools_crease_weight_ctl",
        default=False,
        )
    
    bmtools_crease_weight_alt: BoolProperty(
        name="bmtools_crease_weight_alt",
        default=False,
        )
    # }}}
    
    # Size {{{
    bmtools_size: StringProperty(
        name="bmtools_size",
        maxlen=1,
        default='',
        )
    
    bmtools_size_shift: BoolProperty(
        name="bmtools_size_shift",
        default=False,
        )
    
    bmtools_size_ctl: BoolProperty(
        name="bmtools_size_ctl",
        default=False,
        )
    
    bmtools_size_alt: BoolProperty(
        name="bmtools_size_alt",
        default=False,
        )
    # }}}
    
    # Radius {{{
    bmtools_radius: StringProperty(
        name="bmtools_radius",
        maxlen=1,
        default='',
        )
    
    bmtools_radius_shift: BoolProperty(
        name="bmtools_radius_shift",
        default=False,
        )
    
    bmtools_radius_ctl: BoolProperty(
        name="bmtools_radius_ctl",
        default=False,
        )
    
    bmtools_radius_alt: BoolProperty(
        name="bmtools_radius_alt",
        default=False,
        )
    # }}}
    
    # Mid Level {{{
    bmtools_mid_level: StringProperty(
        name="bmtools_mid_level",
        maxlen=1,
        default='',
        )
    
    bmtools_mid_level_shift: BoolProperty(
        name="bmtools_mid_level_shift",
        default=False,
        )
    
    bmtools_mid_level_ctl: BoolProperty(
        name="bmtools_mid_level_ctl",
        default=False,
        )
    
    bmtools_mid_level_alt: BoolProperty(
        name="bmtools_mid_level_alt",
        default=False,
        )
    # }}}
    
    # Strength {{{
    bmtools_strength: StringProperty(
        name="bmtools_strength",
        maxlen=1,
        default='',
        )
    
    bmtools_strength_shift: BoolProperty(
        name="bmtools_strength_shift",
        default=False,
        )
    
    bmtools_strength_ctl: BoolProperty(
        name="bmtools_strength_ctl",
        default=False,
        )
    
    bmtools_strength_alt: BoolProperty(
        name="bmtools_strength_alt",
        default=False,
        )
    # }}}
    
    # Matrix Inverse {{{
    bmtools_matrix_inverse: StringProperty(
        name="bmtools_matrix_inverse",
        maxlen=1,
        default='',
        )
    
    bmtools_matrix_inverse_shift: BoolProperty(
        name="bmtools_matrix_inverse_shift",
        default=False,
        )
    
    bmtools_matrix_inverse_ctl: BoolProperty(
        name="bmtools_matrix_inverse_ctl",
        default=False,
        )
    
    bmtools_matrix_inverse_alt: BoolProperty(
        name="bmtools_matrix_inverse_alt",
        default=False,
        )
    # }}}
    
    # Falloff Radius {{{
    bmtools_falloff_radius: StringProperty(
        name="bmtools_falloff_radius",
        maxlen=1,
        default='',
        )
    
    bmtools_falloff_radius_shift: BoolProperty(
        name="bmtools_falloff_radius_shift",
        default=False,
        )
    
    bmtools_falloff_radius_ctl: BoolProperty(
        name="bmtools_falloff_radius_ctl",
        default=False,
        )
    
    bmtools_falloff_radius_alt: BoolProperty(
        name="bmtools_falloff_radius_alt",
        default=False,
        )
    # }}}
    
    # Project Limit {{{
    bmtools_project_limit: StringProperty(
        name="bmtools_project_limit",
        maxlen=1,
        default='',
        )
    
    bmtools_project_limit_shift: BoolProperty(
        name="bmtools_project_limit_shift",
        default=False,
        )
    
    bmtools_project_limit_ctl: BoolProperty(
        name="bmtools_project_limit_ctl",
        default=False,
        )
    
    bmtools_project_limit_alt: BoolProperty(
        name="bmtools_project_limit_alt",
        default=False,
        )
    # }}}
    
    # Limits {{{
    bmtools_limits: StringProperty(
        name="bmtools_limits",
        maxlen=1,
        default='',
        )
    
    bmtools_limits_shift: BoolProperty(
        name="bmtools_limits_shift",
        default=False,
        )
    
    bmtools_limits_ctl: BoolProperty(
        name="bmtools_limits_ctl",
        default=False,
        )
    
    bmtools_limits_alt: BoolProperty(
        name="bmtools_limits_alt",
        default=False,
        )
    # }}}
    
    # Lambda Border {{{
    bmtools_lambda_border: StringProperty(
        name="bmtools_lambda_border",
        maxlen=1,
        default='',
        )
    
    bmtools_lambda_border_shift: BoolProperty(
        name="bmtools_lambda_border_shift",
        default=False,
        )
    
    bmtools_lambda_border_ctl: BoolProperty(
        name="bmtools_lambda_border_ctl",
        default=False,
        )
    
    bmtools_lambda_border_alt: BoolProperty(
        name="bmtools_lambda_border_alt",
        default=False,
        )
    # }}}
    
    # Lambda Factor {{{
    bmtools_lambda_factor: StringProperty(
        name="bmtools_lambda_factor",
        maxlen=1,
        default='',
        )
    
    bmtools_lambda_factor_shift: BoolProperty(
        name="bmtools_lambda_factor_shift",
        default=False,
        )
    
    bmtools_lambda_factor_ctl: BoolProperty(
        name="bmtools_lambda_factor_ctl",
        default=False,
        )
    
    bmtools_lambda_factor_alt: BoolProperty(
        name="bmtools_lambda_factor_alt",
        default=False,
        )
    # }}}
    
    # Falloff {{{
    bmtools_falloff: StringProperty(
        name="bmtools_falloff",
        maxlen=1,
        default='',
        )
    
    bmtools_falloff_shift: BoolProperty(
        name="bmtools_falloff_shift",
        default=False,
        )
    
    bmtools_falloff_ctl: BoolProperty(
        name="bmtools_falloff_ctl",
        default=False,
        )
    
    bmtools_falloff_alt: BoolProperty(
        name="bmtools_falloff_alt",
        default=False,
        )
    # }}}
    
    # Damping Time {{{
    bmtools_damping_time: StringProperty(
        name="bmtools_damping_time",
        maxlen=1,
        default='',
        )
    
    bmtools_damping_time_shift: BoolProperty(
        name="bmtools_damping_time_shift",
        default=False,
        )
    
    bmtools_damping_time_ctl: BoolProperty(
        name="bmtools_damping_time_ctl",
        default=False,
        )
    
    bmtools_damping_time_alt: BoolProperty(
        name="bmtools_damping_time_alt",
        default=False,
        )
    # }}}
    
    # Lifetime {{{
    bmtools_lifetime: StringProperty(
        name="bmtools_lifetime",
        maxlen=1,
        default='',
        )
    
    bmtools_lifetime_shift: BoolProperty(
        name="bmtools_lifetime_shift",
        default=False,
        )
    
    bmtools_lifetime_ctl: BoolProperty(
        name="bmtools_lifetime_ctl",
        default=False,
        )
    
    bmtools_lifetime_alt: BoolProperty(
        name="bmtools_lifetime_alt",
        default=False,
        )
    # }}}
    
    # Narrowness {{{
    bmtools_narrowness: StringProperty(
        name="bmtools_narrowness",
        maxlen=1,
        default='',
        )
    
    bmtools_narrowness_shift: BoolProperty(
        name="bmtools_narrowness_shift",
        default=False,
        )
    
    bmtools_narrowness_ctl: BoolProperty(
        name="bmtools_narrowness_ctl",
        default=False,
        )
    
    bmtools_narrowness_alt: BoolProperty(
        name="bmtools_narrowness_alt",
        default=False,
        )
    # }}}
    
    # Time Offset {{{
    bmtools_time_offset: StringProperty(
        name="bmtools_time_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_time_offset_shift: BoolProperty(
        name="bmtools_time_offset_shift",
        default=False,
        )
    
    bmtools_time_offset_ctl: BoolProperty(
        name="bmtools_time_offset_ctl",
        default=False,
        )
    
    bmtools_time_offset_alt: BoolProperty(
        name="bmtools_time_offset_alt",
        default=False,
        )
    # }}}
    
    # Start Position Y {{{
    bmtools_start_position_y: StringProperty(
        name="bmtools_start_position_y",
        maxlen=1,
        default='',
        )
    
    bmtools_start_position_y_shift: BoolProperty(
        name="bmtools_start_position_y_shift",
        default=False,
        )
    
    bmtools_start_position_y_ctl: BoolProperty(
        name="bmtools_start_position_y_ctl",
        default=False,
        )
    
    bmtools_start_position_y_alt: BoolProperty(
        name="bmtools_start_position_y_alt",
        default=False,
        )
    # }}}
    
    # Height {{{
    bmtools_height: StringProperty(
        name="bmtools_height",
        maxlen=1,
        default='',
        )
    
    bmtools_height_shift: BoolProperty(
        name="bmtools_height_shift",
        default=False,
        )
    
    bmtools_height_ctl: BoolProperty(
        name="bmtools_height_ctl",
        default=False,
        )
    
    bmtools_height_alt: BoolProperty(
        name="bmtools_height_alt",
        default=False,
        )
    # }}}
    
    # Start Position X {{{
    bmtools_start_position_x: StringProperty(
        name="bmtools_start_position_x",
        maxlen=1,
        default='',
        )
    
    bmtools_start_position_x_shift: BoolProperty(
        name="bmtools_start_position_x_shift",
        default=False,
        )
    
    bmtools_start_position_x_ctl: BoolProperty(
        name="bmtools_start_position_x_ctl",
        default=False,
        )
    
    bmtools_start_position_x_alt: BoolProperty(
        name="bmtools_start_position_x_alt",
        default=False,
        )
    # }}}
    
    # Speed {{{
    bmtools_speed: StringProperty(
        name="bmtools_speed",
        maxlen=1,
        default='',
        )
    
    bmtools_speed_shift: BoolProperty(
        name="bmtools_speed_shift",
        default=False,
        )
    
    bmtools_speed_ctl: BoolProperty(
        name="bmtools_speed_ctl",
        default=False,
        )
    
    bmtools_speed_alt: BoolProperty(
        name="bmtools_speed_alt",
        default=False,
        )
    # }}}
    
    # Protect {{{
    bmtools_protect: StringProperty(
        name="bmtools_protect",
        maxlen=1,
        default='',
        )
    
    bmtools_protect_shift: BoolProperty(
        name="bmtools_protect_shift",
        default=False,
        )
    
    bmtools_protect_ctl: BoolProperty(
        name="bmtools_protect_ctl",
        default=False,
        )
    
    bmtools_protect_alt: BoolProperty(
        name="bmtools_protect_alt",
        default=False,
        )
    # }}}
    
    # Sharpen Peak Jonswap {{{
    bmtools_sharpen_peak_jonswap: StringProperty(
        name="bmtools_sharpen_peak_jonswap",
        maxlen=1,
        default='',
        )
    
    bmtools_sharpen_peak_jonswap_shift: BoolProperty(
        name="bmtools_sharpen_peak_jonswap_shift",
        default=False,
        )
    
    bmtools_sharpen_peak_jonswap_ctl: BoolProperty(
        name="bmtools_sharpen_peak_jonswap_ctl",
        default=False,
        )
    
    bmtools_sharpen_peak_jonswap_alt: BoolProperty(
        name="bmtools_sharpen_peak_jonswap_alt",
        default=False,
        )
    # }}}
    
    # Wave Scale Min {{{
    bmtools_wave_scale_min: StringProperty(
        name="bmtools_wave_scale_min",
        maxlen=1,
        default='',
        )
    
    bmtools_wave_scale_min_shift: BoolProperty(
        name="bmtools_wave_scale_min_shift",
        default=False,
        )
    
    bmtools_wave_scale_min_ctl: BoolProperty(
        name="bmtools_wave_scale_min_ctl",
        default=False,
        )
    
    bmtools_wave_scale_min_alt: BoolProperty(
        name="bmtools_wave_scale_min_alt",
        default=False,
        )
    # }}}
    
    # Wave Scale {{{
    bmtools_wave_scale: StringProperty(
        name="bmtools_wave_scale",
        maxlen=1,
        default='',
        )
    
    bmtools_wave_scale_shift: BoolProperty(
        name="bmtools_wave_scale_shift",
        default=False,
        )
    
    bmtools_wave_scale_ctl: BoolProperty(
        name="bmtools_wave_scale_ctl",
        default=False,
        )
    
    bmtools_wave_scale_alt: BoolProperty(
        name="bmtools_wave_scale_alt",
        default=False,
        )
    # }}}
    
    # Wave Alignment {{{
    bmtools_wave_alignment: StringProperty(
        name="bmtools_wave_alignment",
        maxlen=1,
        default='',
        )
    
    bmtools_wave_alignment_shift: BoolProperty(
        name="bmtools_wave_alignment_shift",
        default=False,
        )
    
    bmtools_wave_alignment_ctl: BoolProperty(
        name="bmtools_wave_alignment_ctl",
        default=False,
        )
    
    bmtools_wave_alignment_alt: BoolProperty(
        name="bmtools_wave_alignment_alt",
        default=False,
        )
    # }}}
    
    # Choppiness {{{
    bmtools_choppiness: StringProperty(
        name="bmtools_choppiness",
        maxlen=1,
        default='',
        )
    
    bmtools_choppiness_shift: BoolProperty(
        name="bmtools_choppiness_shift",
        default=False,
        )
    
    bmtools_choppiness_ctl: BoolProperty(
        name="bmtools_choppiness_ctl",
        default=False,
        )
    
    bmtools_choppiness_alt: BoolProperty(
        name="bmtools_choppiness_alt",
        default=False,
        )
    # }}}
    
    # Time {{{
    bmtools_time: StringProperty(
        name="bmtools_time",
        maxlen=1,
        default='',
        )
    
    bmtools_time_shift: BoolProperty(
        name="bmtools_time_shift",
        default=False,
        )
    
    bmtools_time_ctl: BoolProperty(
        name="bmtools_time_ctl",
        default=False,
        )
    
    bmtools_time_alt: BoolProperty(
        name="bmtools_time_alt",
        default=False,
        )
    # }}}
    
    # Damping {{{
    bmtools_damping: StringProperty(
        name="bmtools_damping",
        maxlen=1,
        default='',
        )
    
    bmtools_damping_shift: BoolProperty(
        name="bmtools_damping_shift",
        default=False,
        )
    
    bmtools_damping_ctl: BoolProperty(
        name="bmtools_damping_ctl",
        default=False,
        )
    
    bmtools_damping_alt: BoolProperty(
        name="bmtools_damping_alt",
        default=False,
        )
    # }}}
    
    # Wave Direction {{{
    bmtools_wave_direction: StringProperty(
        name="bmtools_wave_direction",
        maxlen=1,
        default='',
        )
    
    bmtools_wave_direction_shift: BoolProperty(
        name="bmtools_wave_direction_shift",
        default=False,
        )
    
    bmtools_wave_direction_ctl: BoolProperty(
        name="bmtools_wave_direction_ctl",
        default=False,
        )
    
    bmtools_wave_direction_alt: BoolProperty(
        name="bmtools_wave_direction_alt",
        default=False,
        )
    # }}}
    
    # Wind Velocity {{{
    bmtools_wind_velocity: StringProperty(
        name="bmtools_wind_velocity",
        maxlen=1,
        default='',
        )
    
    bmtools_wind_velocity_shift: BoolProperty(
        name="bmtools_wind_velocity_shift",
        default=False,
        )
    
    bmtools_wind_velocity_ctl: BoolProperty(
        name="bmtools_wind_velocity_ctl",
        default=False,
        )
    
    bmtools_wind_velocity_alt: BoolProperty(
        name="bmtools_wind_velocity_alt",
        default=False,
        )
    # }}}
    
    # Depth {{{
    bmtools_depth: StringProperty(
        name="bmtools_depth",
        maxlen=1,
        default='',
        )
    
    bmtools_depth_shift: BoolProperty(
        name="bmtools_depth_shift",
        default=False,
        )
    
    bmtools_depth_ctl: BoolProperty(
        name="bmtools_depth_ctl",
        default=False,
        )
    
    bmtools_depth_alt: BoolProperty(
        name="bmtools_depth_alt",
        default=False,
        )
    # }}}
    
    # Foam Coverage {{{
    bmtools_foam_coverage: StringProperty(
        name="bmtools_foam_coverage",
        maxlen=1,
        default='',
        )
    
    bmtools_foam_coverage_shift: BoolProperty(
        name="bmtools_foam_coverage_shift",
        default=False,
        )
    
    bmtools_foam_coverage_ctl: BoolProperty(
        name="bmtools_foam_coverage_ctl",
        default=False,
        )
    
    bmtools_foam_coverage_alt: BoolProperty(
        name="bmtools_foam_coverage_alt",
        default=False,
        )
    # }}}
    
    # Fetch Jonswap {{{
    bmtools_fetch_jonswap: StringProperty(
        name="bmtools_fetch_jonswap",
        maxlen=1,
        default='',
        )
    
    bmtools_fetch_jonswap_shift: BoolProperty(
        name="bmtools_fetch_jonswap_shift",
        default=False,
        )
    
    bmtools_fetch_jonswap_ctl: BoolProperty(
        name="bmtools_fetch_jonswap_ctl",
        default=False,
        )
    
    bmtools_fetch_jonswap_alt: BoolProperty(
        name="bmtools_fetch_jonswap_alt",
        default=False,
        )
    # }}}
    
    # Bake Foam Fade {{{
    bmtools_bake_foam_fade: StringProperty(
        name="bmtools_bake_foam_fade",
        maxlen=1,
        default='',
        )
    
    bmtools_bake_foam_fade_shift: BoolProperty(
        name="bmtools_bake_foam_fade_shift",
        default=False,
        )
    
    bmtools_bake_foam_fade_ctl: BoolProperty(
        name="bmtools_bake_foam_fade_ctl",
        default=False,
        )
    
    bmtools_bake_foam_fade_alt: BoolProperty(
        name="bmtools_bake_foam_fade_alt",
        default=False,
        )
    # }}}
    
    # Particle Amount {{{
    bmtools_particle_amount: StringProperty(
        name="bmtools_particle_amount",
        maxlen=1,
        default='',
        )
    
    bmtools_particle_amount_shift: BoolProperty(
        name="bmtools_particle_amount_shift",
        default=False,
        )
    
    bmtools_particle_amount_ctl: BoolProperty(
        name="bmtools_particle_amount_ctl",
        default=False,
        )
    
    bmtools_particle_amount_alt: BoolProperty(
        name="bmtools_particle_amount_alt",
        default=False,
        )
    # }}}
    
    # Random Rotation {{{
    bmtools_random_rotation: StringProperty(
        name="bmtools_random_rotation",
        maxlen=1,
        default='',
        )
    
    bmtools_random_rotation_shift: BoolProperty(
        name="bmtools_random_rotation_shift",
        default=False,
        )
    
    bmtools_random_rotation_ctl: BoolProperty(
        name="bmtools_random_rotation_ctl",
        default=False,
        )
    
    bmtools_random_rotation_alt: BoolProperty(
        name="bmtools_random_rotation_alt",
        default=False,
        )
    # }}}
    
    # Particle Offset {{{
    bmtools_particle_offset: StringProperty(
        name="bmtools_particle_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_particle_offset_shift: BoolProperty(
        name="bmtools_particle_offset_shift",
        default=False,
        )
    
    bmtools_particle_offset_ctl: BoolProperty(
        name="bmtools_particle_offset_ctl",
        default=False,
        )
    
    bmtools_particle_offset_alt: BoolProperty(
        name="bmtools_particle_offset_alt",
        default=False,
        )
    # }}}
    
    # Random Position {{{
    bmtools_random_position: StringProperty(
        name="bmtools_random_position",
        maxlen=1,
        default='',
        )
    
    bmtools_random_position_shift: BoolProperty(
        name="bmtools_random_position_shift",
        default=False,
        )
    
    bmtools_random_position_ctl: BoolProperty(
        name="bmtools_random_position_ctl",
        default=False,
        )
    
    bmtools_random_position_alt: BoolProperty(
        name="bmtools_random_position_alt",
        default=False,
        )
    # }}}
    
    # Position {{{
    bmtools_position: StringProperty(
        name="bmtools_position",
        maxlen=1,
        default='',
        )
    
    bmtools_position_shift: BoolProperty(
        name="bmtools_position_shift",
        default=False,
        )
    
    bmtools_position_ctl: BoolProperty(
        name="bmtools_position_ctl",
        default=False,
        )
    
    bmtools_position_alt: BoolProperty(
        name="bmtools_position_alt",
        default=False,
        )
    # }}}
    
    # Weight {{{
    bmtools_weight: StringProperty(
        name="bmtools_weight",
        maxlen=1,
        default='',
        )
    
    bmtools_weight_shift: BoolProperty(
        name="bmtools_weight_shift",
        default=False,
        )
    
    bmtools_weight_ctl: BoolProperty(
        name="bmtools_weight_ctl",
        default=False,
        )
    
    bmtools_weight_alt: BoolProperty(
        name="bmtools_weight_alt",
        default=False,
        )
    # }}}
    
    # Projector Count {{{
    bmtools_projector_count: StringProperty(
        name="bmtools_projector_count",
        maxlen=1,
        default='',
        )
    
    bmtools_projector_count_shift: BoolProperty(
        name="bmtools_projector_count_shift",
        default=False,
        )
    
    bmtools_projector_count_ctl: BoolProperty(
        name="bmtools_projector_count_ctl",
        default=False,
        )
    
    bmtools_projector_count_alt: BoolProperty(
        name="bmtools_projector_count_alt",
        default=False,
        )
    # }}}
    
    # Count {{{
    bmtools_count: StringProperty(
        name="bmtools_count",
        maxlen=1,
        default='',
        )
    
    bmtools_count_shift: BoolProperty(
        name="bmtools_count_shift",
        default=False,
        )
    
    bmtools_count_ctl: BoolProperty(
        name="bmtools_count_ctl",
        default=False,
        )
    
    bmtools_count_alt: BoolProperty(
        name="bmtools_count_alt",
        default=False,
        )
    # }}}
    
    # Segments {{{
    bmtools_segments: StringProperty(
        name="bmtools_segments",
        maxlen=1,
        default='',
        )
    
    bmtools_segments_shift: BoolProperty(
        name="bmtools_segments_shift",
        default=False,
        )
    
    bmtools_segments_ctl: BoolProperty(
        name="bmtools_segments_ctl",
        default=False,
        )
    
    bmtools_segments_alt: BoolProperty(
        name="bmtools_segments_alt",
        default=False,
        )
    # }}}
    
    # Material {{{
    bmtools_material: StringProperty(
        name="bmtools_material",
        maxlen=1,
        default='',
        )
    
    bmtools_material_shift: BoolProperty(
        name="bmtools_material_shift",
        default=False,
        )
    
    bmtools_material_ctl: BoolProperty(
        name="bmtools_material_ctl",
        default=False,
        )
    
    bmtools_material_alt: BoolProperty(
        name="bmtools_material_alt",
        default=False,
        )
    # }}}
    
    # Seed {{{
    bmtools_seed: StringProperty(
        name="bmtools_seed",
        maxlen=1,
        default='',
        )
    
    bmtools_seed_shift: BoolProperty(
        name="bmtools_seed_shift",
        default=False,
        )
    
    bmtools_seed_ctl: BoolProperty(
        name="bmtools_seed_ctl",
        default=False,
        )
    
    bmtools_seed_alt: BoolProperty(
        name="bmtools_seed_alt",
        default=False,
        )
    # }}}
    
    # Iterations {{{
    bmtools_iterations: StringProperty(
        name="bmtools_iterations",
        maxlen=1,
        default='',
        )
    
    bmtools_iterations_shift: BoolProperty(
        name="bmtools_iterations_shift",
        default=False,
        )
    
    bmtools_iterations_ctl: BoolProperty(
        name="bmtools_iterations_ctl",
        default=False,
        )
    
    bmtools_iterations_alt: BoolProperty(
        name="bmtools_iterations_alt",
        default=False,
        )
    # }}}
    
    # Levels {{{
    bmtools_levels: StringProperty(
        name="bmtools_levels",
        maxlen=1,
        default='',
        )
    
    bmtools_levels_shift: BoolProperty(
        name="bmtools_levels_shift",
        default=False,
        )
    
    bmtools_levels_ctl: BoolProperty(
        name="bmtools_levels_ctl",
        default=False,
        )
    
    bmtools_levels_alt: BoolProperty(
        name="bmtools_levels_alt",
        default=False,
        )
    # }}}
    
    # Quality {{{
    bmtools_quality: StringProperty(
        name="bmtools_quality",
        maxlen=1,
        default='',
        )
    
    bmtools_quality_shift: BoolProperty(
        name="bmtools_quality_shift",
        default=False,
        )
    
    bmtools_quality_ctl: BoolProperty(
        name="bmtools_quality_ctl",
        default=False,
        )
    
    bmtools_quality_alt: BoolProperty(
        name="bmtools_quality_alt",
        default=False,
        )
    # }}}
    
    # Sculpt Levels {{{
    bmtools_sculpt_levels: StringProperty(
        name="bmtools_sculpt_levels",
        maxlen=1,
        default='',
        )
    
    bmtools_sculpt_levels_shift: BoolProperty(
        name="bmtools_sculpt_levels_shift",
        default=False,
        )
    
    bmtools_sculpt_levels_ctl: BoolProperty(
        name="bmtools_sculpt_levels_ctl",
        default=False,
        )
    
    bmtools_sculpt_levels_alt: BoolProperty(
        name="bmtools_sculpt_levels_alt",
        default=False,
        )
    # }}}
    
    # Render Levels {{{
    bmtools_render_levels: StringProperty(
        name="bmtools_render_levels",
        maxlen=1,
        default='',
        )
    
    bmtools_render_levels_shift: BoolProperty(
        name="bmtools_render_levels_shift",
        default=False,
        )
    
    bmtools_render_levels_ctl: BoolProperty(
        name="bmtools_render_levels_ctl",
        default=False,
        )
    
    bmtools_render_levels_alt: BoolProperty(
        name="bmtools_render_levels_alt",
        default=False,
        )
    # }}}
    
    # Octree Depth {{{
    bmtools_octree_depth: StringProperty(
        name="bmtools_octree_depth",
        maxlen=1,
        default='',
        )
    
    bmtools_octree_depth_shift: BoolProperty(
        name="bmtools_octree_depth_shift",
        default=False,
        )
    
    bmtools_octree_depth_ctl: BoolProperty(
        name="bmtools_octree_depth_ctl",
        default=False,
        )
    
    bmtools_octree_depth_alt: BoolProperty(
        name="bmtools_octree_depth_alt",
        default=False,
        )
    # }}}
    
    # Render Steps {{{
    bmtools_render_steps: StringProperty(
        name="bmtools_render_steps",
        maxlen=1,
        default='',
        )
    
    bmtools_render_steps_shift: BoolProperty(
        name="bmtools_render_steps_shift",
        default=False,
        )
    
    bmtools_render_steps_ctl: BoolProperty(
        name="bmtools_render_steps_ctl",
        default=False,
        )
    
    bmtools_render_steps_alt: BoolProperty(
        name="bmtools_render_steps_alt",
        default=False,
        )
    # }}}
    
    # Steps {{{
    bmtools_steps: StringProperty(
        name="bmtools_steps",
        maxlen=1,
        default='',
        )
    
    bmtools_steps_shift: BoolProperty(
        name="bmtools_steps_shift",
        default=False,
        )
    
    bmtools_steps_ctl: BoolProperty(
        name="bmtools_steps_ctl",
        default=False,
        )
    
    bmtools_steps_alt: BoolProperty(
        name="bmtools_steps_alt",
        default=False,
        )
    # }}}
    
    # Material Offset {{{
    bmtools_material_offset: StringProperty(
        name="bmtools_material_offset",
        maxlen=1,
        default='',
        )
    
    bmtools_material_offset_shift: BoolProperty(
        name="bmtools_material_offset_shift",
        default=False,
        )
    
    bmtools_material_offset_ctl: BoolProperty(
        name="bmtools_material_offset_ctl",
        default=False,
        )
    
    bmtools_material_offset_alt: BoolProperty(
        name="bmtools_material_offset_alt",
        default=False,
        )
    # }}}
    
    # Material Offset Rim {{{
    bmtools_material_offset_rim: StringProperty(
        name="bmtools_material_offset_rim",
        maxlen=1,
        default='',
        )
    
    bmtools_material_offset_rim_shift: BoolProperty(
        name="bmtools_material_offset_rim_shift",
        default=False,
        )
    
    bmtools_material_offset_rim_ctl: BoolProperty(
        name="bmtools_material_offset_rim_ctl",
        default=False,
        )
    
    bmtools_material_offset_rim_alt: BoolProperty(
        name="bmtools_material_offset_rim_alt",
        default=False,
        )
    # }}}
    
    # Min Vertices {{{
    bmtools_min_vertices: StringProperty(
        name="bmtools_min_vertices",
        maxlen=1,
        default='',
        )
    
    bmtools_min_vertices_shift: BoolProperty(
        name="bmtools_min_vertices_shift",
        default=False,
        )
    
    bmtools_min_vertices_ctl: BoolProperty(
        name="bmtools_min_vertices_ctl",
        default=False,
        )
    
    bmtools_min_vertices_alt: BoolProperty(
        name="bmtools_min_vertices_alt",
        default=False,
        )
    # }}}
    
    # Voxel Amount {{{
    bmtools_voxel_amount: StringProperty(
        name="bmtools_voxel_amount",
        maxlen=1,
        default='',
        )
    
    bmtools_voxel_amount_shift: BoolProperty(
        name="bmtools_voxel_amount_shift",
        default=False,
        )
    
    bmtools_voxel_amount_ctl: BoolProperty(
        name="bmtools_voxel_amount_ctl",
        default=False,
        )
    
    bmtools_voxel_amount_alt: BoolProperty(
        name="bmtools_voxel_amount_alt",
        default=False,
        )
    # }}}
    
    # Precision {{{
    bmtools_precision: StringProperty(
        name="bmtools_precision",
        maxlen=1,
        default='',
        )
    
    bmtools_precision_shift: BoolProperty(
        name="bmtools_precision_shift",
        default=False,
        )
    
    bmtools_precision_ctl: BoolProperty(
        name="bmtools_precision_ctl",
        default=False,
        )
    
    bmtools_precision_alt: BoolProperty(
        name="bmtools_precision_alt",
        default=False,
        )
    # }}}
    
    # Subsurf Levels {{{
    bmtools_subsurf_levels: StringProperty(
        name="bmtools_subsurf_levels",
        maxlen=1,
        default='',
        )
    
    bmtools_subsurf_levels_shift: BoolProperty(
        name="bmtools_subsurf_levels_shift",
        default=False,
        )
    
    bmtools_subsurf_levels_ctl: BoolProperty(
        name="bmtools_subsurf_levels_ctl",
        default=False,
        )
    
    bmtools_subsurf_levels_alt: BoolProperty(
        name="bmtools_subsurf_levels_alt",
        default=False,
        )
    # }}}
    
    # Resolution {{{
    bmtools_resolution: StringProperty(
        name="bmtools_resolution",
        maxlen=1,
        default='',
        )
    
    bmtools_resolution_shift: BoolProperty(
        name="bmtools_resolution_shift",
        default=False,
        )
    
    bmtools_resolution_ctl: BoolProperty(
        name="bmtools_resolution_ctl",
        default=False,
        )
    
    bmtools_resolution_alt: BoolProperty(
        name="bmtools_resolution_alt",
        default=False,
        )
    # }}}
    
    # Repeat X {{{
    bmtools_repeat_x: StringProperty(
        name="bmtools_repeat_x",
        maxlen=1,
        default='',
        )
    
    bmtools_repeat_x_shift: BoolProperty(
        name="bmtools_repeat_x_shift",
        default=False,
        )
    
    bmtools_repeat_x_ctl: BoolProperty(
        name="bmtools_repeat_x_ctl",
        default=False,
        )
    
    bmtools_repeat_x_alt: BoolProperty(
        name="bmtools_repeat_x_alt",
        default=False,
        )
    # }}}
    
    # Spatial Size {{{
    bmtools_spatial_size: StringProperty(
        name="bmtools_spatial_size",
        maxlen=1,
        default='',
        )
    
    bmtools_spatial_size_shift: BoolProperty(
        name="bmtools_spatial_size_shift",
        default=False,
        )
    
    bmtools_spatial_size_ctl: BoolProperty(
        name="bmtools_spatial_size_ctl",
        default=False,
        )
    
    bmtools_spatial_size_alt: BoolProperty(
        name="bmtools_spatial_size_alt",
        default=False,
        )
    # }}}
    
    # Viewport Resolution {{{
    bmtools_viewport_resolution: StringProperty(
        name="bmtools_viewport_resolution",
        maxlen=1,
        default='',
        )
    
    bmtools_viewport_resolution_shift: BoolProperty(
        name="bmtools_viewport_resolution_shift",
        default=False,
        )
    
    bmtools_viewport_resolution_ctl: BoolProperty(
        name="bmtools_viewport_resolution_ctl",
        default=False,
        )
    
    bmtools_viewport_resolution_alt: BoolProperty(
        name="bmtools_viewport_resolution_alt",
        default=False,
        )
    # }}}
    
    # Frame End {{{
    bmtools_frame_end: StringProperty(
        name="bmtools_frame_end",
        maxlen=1,
        default='',
        )
    
    bmtools_frame_end_shift: BoolProperty(
        name="bmtools_frame_end_shift",
        default=False,
        )
    
    bmtools_frame_end_ctl: BoolProperty(
        name="bmtools_frame_end_ctl",
        default=False,
        )
    
    bmtools_frame_end_alt: BoolProperty(
        name="bmtools_frame_end_alt",
        default=False,
        )
    # }}}
    
    # Repeat Y {{{
    bmtools_repeat_y: StringProperty(
        name="bmtools_repeat_y",
        maxlen=1,
        default='',
        )
    
    bmtools_repeat_y_shift: BoolProperty(
        name="bmtools_repeat_y_shift",
        default=False,
        )
    
    bmtools_repeat_y_ctl: BoolProperty(
        name="bmtools_repeat_y_ctl",
        default=False,
        )
    
    bmtools_repeat_y_alt: BoolProperty(
        name="bmtools_repeat_y_alt",
        default=False,
        )
    # }}}
    
    # Random Seed {{{
    bmtools_random_seed: StringProperty(
        name="bmtools_random_seed",
        maxlen=1,
        default='',
        )
    
    bmtools_random_seed_shift: BoolProperty(
        name="bmtools_random_seed_shift",
        default=False,
        )
    
    bmtools_random_seed_ctl: BoolProperty(
        name="bmtools_random_seed_ctl",
        default=False,
        )
    
    bmtools_random_seed_alt: BoolProperty(
        name="bmtools_random_seed_alt",
        default=False,
        )
    # }}}
    
    # Particle System Index {{{
    bmtools_particle_system_index: StringProperty(
        name="bmtools_particle_system_index",
        maxlen=1,
        default='',
        )
    
    bmtools_particle_system_index_shift: BoolProperty(
        name="bmtools_particle_system_index_shift",
        default=False,
        )
    
    bmtools_particle_system_index_ctl: BoolProperty(
        name="bmtools_particle_system_index_ctl",
        default=False,
        )
    
    bmtools_particle_system_index_alt: BoolProperty(
        name="bmtools_particle_system_index_alt",
        default=False,
        )
    # }}}
    # }}}
    
    # Settings {{{
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

    bmtool_prop_search_str: StringProperty(
            name="Search through bmtool modal props",
            default=""
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
            layout.prop(self, "cluster_types")

        # keyboard shortcuts viewer {{{
        layout.prop(self, "bmtool_prop_search_str")

        s = []
        s.append(str(self.bmtool_prop_search_str))
        s.append(re.sub('_', ' ', s[0]))
        s.append(s[0].upper())
        s.append(s[0].lower())
        s.append(s[1].upper())
        s.append(s[1].lower())
        s.append(s[1].title())

        # element example: ['a', 'a_shift', 'a_ctl', 'a_alt']
        props_to_display = []

        if len(self.bmtool_prop_search_str) > 1:
            # all props
            for x in self.props_names:
                # props names from bmtool_prop_search_str
                for z in s:
                    if z in x:

                        # mapping element
                        names = [
                                 x,
                                 f'{x}_shift',
                                 f'{x}_alt',
                                 f'{x}_ctl'
                                 ]

                        # check duplicates in props
                        dont_add = False
                        for p in props_to_display:
                            if p == names:
                                dont_add = True

                        if not dont_add:
                            props_to_display.append(names)

            print(len(props_to_display))
            for x in props_to_display:
                kbs_name = re.sub('_', ' ', x[0])
                kbs_name = kbs_name.title()
                layout.label(text=kbs_name)
                for y in x:
                    layout.prop(self, y)

        else:
            layout.label(
                    text="Type modifier property name above to view modal shortcuts.")
            layout.label(text="Example: bevel angle")
        # }}}
