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

import math


class ModifierEditor():
    """
    Modifier editor base class
    Designed to be used with BMToolM
    """

    props = {
             'name': None,              # Editor name
             'cluster_types': [None],   # Clusters types
                                        # this editor can be used with
             }

    _mappings = [{'mapping_name': '1',
                 'cluster': 'BEVEL_CLUSTER',
                 'mods': ['get_first', '']}]

    _attributes = [
                   {'attr': 'segments',
                    'map': '1',
                    'type': 'int',
                    'kb': 'S',
                    'sens': 0.00005},
                   {'attr': 'harden_normals',
                    'map': '1',
                    'type': 'int',
                    'kb': 'S',
                    'sens': 0.00005},
                   ]

    def _get_mod_mapping(self, mapping_name):
        for x in self._mappings:
            if x['name'] == mapping_name:
                return x

    def _get_mods_for_attr(self, x, cluster):
        mapping = self._get_mod_mapping(x['map'])
        mods = []
        for m in mapping['mods']:
            result = getattr(cluster, m['attr'])(m['args'])
            if not isinstance(result, list):
                result = [result]
            for y in result:
                if not isinstance(y, bpy.types.Modifier):
                    raise TypeError
            mods.extend(result)
        return mods

    def modal_attrs(self, context, event, cluster):
        for x in self._attributes:
            # Switch to mode
            if self.mode == self._DEFAULT_MODE\
                    and event.type == x['kb']\
                    and event.value == 'PRESS':
                self.mode = x['attr']
                return

            # Get modifiers for this attr
            mods = self._get_mods_for_attr(x, cluster)

            # Toggle attrs
            if x['type'] == 'bool':
                if event.type = x['kb']\
                        and event.value == 'PRESS':
                    setattr(mod, x['attr'], not getattr(mod, x['attr']))
                    return

            # Modal editing
            if self.mode == x['attr']:
                if x['type'] == 'int':
                    for x in mods:
                        setattr(x, x['attr'], self.delta_d())
                        return
                if x['type'] == 'float':
                    for x in mods:
                        setattr(x, x['attr'], self.delta_d())
                        return
        return

    _DEFAULT_MODE = 'SELECT_MODE'

    # {{{
    """
    Type example:
    EDITOR_TYPE = ['BEVEL_CLUSTER', 'BEVEL', 'BEVELED_BOOLEAN']

    Modal mapping decides what modifiers to use when editing.
    TODO: this is kinda bad
    Examples:
    MODIFIER_MAPPING = {'cluster': BEVEL_CLUSTER,
                        'modifiers': ['get_first()', 'get_first().get_last()']
                        }

    MODIFIER_MAPPING = {'cluster': DOUBLE_BEVEL,
                        'modifiers': ['get_list()[1]']
                        }

    Attributes example:
    [
     {'attr': 'segments',  # Attribut name
      'mods': [<MODIFIER_MAPPING>, <MODIFIER_MAPPING>]  # Modal mappings
      'type': 'int',  # Attribute type
      'min': 0,  # Min value
      'kb': 'S',  # Shortcut
      'sens': 0.00005},  # Sens for modal editing

     {'attr': 'harden_normals',
      'mods': [<MODIFIER_MAPPING>, <MODIFIER_MAPPING>]
      'type': 'bool',
      'kb': 'H',
      'sens': 0.00005},

     {'attr': 'angle',
      'mods': [<MODIFIER_MAPPING>]
      'type': 'float',
      'min': 0,
      'kb': 'A',
      'sens': 0.0005}
      ]
    """  # }}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = self._DEFAULT_MODE

    # ==========================================
    # Editor method placeholders
    # ==========================================
    def bmtool_editor_inv(
            self, context, m_list, selected_objects):
        """
        Editor invoke method, called every time editor is switched to
        """
        self.bmtool_mode = self._DEFAULT_EDITOR_MODE
        return

    def bmtool_editor_remove(
            self, context, m_list, selected_objects):
        """
        Editor remove method, called every time editor is switched from
        """
        # Resets editor's mode, kinda should be in every editor
        self.bmtool_mode = self._DEFAULT_EDITOR_MODE
        return

    def bmtool_editor_modal_1(
            self, context, event, m_list, selected_objects, delta_d):
        """
        Modal method 1
        """
        return

    def bmtool_editor_modal_2(
            self, context, event, m_list, selected_objects, delta_d):
        """
        Modal method 2
        """
        if self._BMTOOL_EDITOR_OPERATOR:
            self.delta_d = delta_d
            self.m_list = m_list
            self.bmtool_modal_2(context, event)
        return

    def bmtool_editor_modifier_defaults(
            self, context, m_list, selected_objects):
        """
        Modifier defaults
        """
        if self._BMTOOL_EDITOR_OPERATOR:
            return self.bmtool_modifier_defaults(context)
        return

    def bmtool_editor_modifier_stats(
            self, context, m_list, selected_objects):
        """
        UI info about modifier
        """
        ui_t = []
        ui_t.append("No editor-specific modifier stats")
        if self._BMTOOL_EDITOR_OPERATOR:
            self.m_list = m_list
            return self.bmtool_modifier_stats(context)
        return ui_t

    # TODO: should be in utils
    # Returns VL
    # VL = vector length
    # VL from object center (currently from initialisation)
    # TODO: should take into consideration distance to object center.
    # TODO: should use object center as center.
    # TODO: should not change settings when changing mode
    def delta_d(self, context, event):
        x = self.vec_len(self.first_x, event.mouse_x,
                         self.first_y, event.mouse_y
                         )
        y = pow(x, 2)
        return y

    # Vector length
    def vec_len(self, x1, x2, y1, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    # ==========================================
    # Compat. method placeholders for bmtool operators
    # ==========================================
    def bmtool_modal_2(self, context, event):
        self.report({'INFO'}, "No editor-specific operator modal 2 method")
        return

    def bmtool_modifier_defaults(self, context):
        self.report({'INFO'}, "No editor-specific operator mod defaults")
        return

    def bmtool_modifier_stats(self, context):
        ui_t = []
        ui_t.append(
                "No editor-specific modifier stats. No operator-editor stats.")
        return ui_t
