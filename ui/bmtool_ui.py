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

# import bpy
import blf
# import math


# class ClustersListUI():
#     def __init__(self, clusters_list):
#         return


# def draw_bmtool(self, context):
#     displayed_objects = self.bmtool_draw(context)
#     for x in displayed_objects:
#         if isinstance(x, ClustersListUI):
#             draw_clusters_list(x, context)
#         elif isinstance(x, ModifiersListUI):
#             draw_modifiers_list(x, context)
#         elif isinstance(x, PropertiesListUI):
#             draw_properties_list(x, context)
#         elif isinstance(x, OperatorInfoUI):
#             draw_operator_info(x, context)

def bmtool_modifier_ui_draw(self, context):  # {{{
    ui_t = self.bmtool_ui(context)
    offset = 0
    offset_2 = 0
    for x in ui_t:
        font_id = 0
        if isinstance(x, list) and x[1] == 20:
            blf.position(font_id, 400, 600 + offset_2, 0)
        else:
            blf.position(font_id, 30, 450 + offset, 0)

        e = False

        if isinstance(x, str):
            blf.size(font_id, 32, 30)
            blf.color(font_id, 0.95, 0.95, 0.95, 1)
            blf.draw(font_id, x)
            offset -= 18

        elif isinstance(x, list):
            if len(x) == 2:
                if x[1] == 2:
                    blf.size(font_id, 32, 30)
                    blf.color(font_id, 0.8, 0.7, 0.7, 1)
                    blf.draw(font_id, x[0])
                    offset -= 18
                elif x[1] == 1:
                    blf.size(font_id, 32, 30)
                    blf.color(font_id, 0.95, 0.95, 0.95, 1)
                    blf.draw(font_id, x[0])
                    offset -= 18
                elif x[1] == 3:
                    blf.size(font_id, 32, 30)
                    blf.color(font_id, 0.8, 0.8, 0.95, 1)
                    blf.draw(font_id, x[0])
                    offset -= 18
                elif x[1] == 10:
                    blf.size(font_id, 32, 30)
                    blf.color(font_id, 0.8, 0.8, 0.5, 1)
                    blf.draw(font_id, x[0])
                    offset -= 18
                elif x[1] == 20:
                    blf.size(font_id, 32, 30)
                    blf.color(font_id, 0.95, 0.95, 0.95, 1)
                    blf.draw(font_id, x[0])
                    offset_2 -= 18
                else:
                    e = True
            else:
                e = True
        else:
            e = True

        if e:
            blf.size(font_id, 32, 30)
            blf.color(font_id, 0.95, 0.95, 0.2, 1)
            blf.draw(font_id, "Encountered error while drawing text")
            offset -= 18
# }}}


class BMToolUi:  # {{{
    """
    Base class for BMToolMod operators that use its UI features
    """

    # Create draw handler and remove it after
    _BMTOOL_UI = True

    # Show additional info
    _BMTOOL_UI_V = True

    # Show all objects mods
    _BMTOOL_UI_SHOW_ALL_OBJECTS = False

    # Prints info about operator in statusbar
    # TODO: remove this method.
    def bmtool_stats(self, context):
        """
        Prints info about modifier in statusbar
        """
        ui_t = ""
        for x in self.bmtool_stats_list(context):
            ui_t += x
            ui_t += " "
        context.workspace.status_text_set(ui_t)

    # TODO: remove this method.
    def bmtool_ui(self, context):
        """
        Method that is used by draw handler
        This method should be in operator
        Should return list of strings
        """
        ui_t = []
        for line in self.bmtool_ui_list(context):
            ui_t.append(line)
        ui_t.append(" ")
        ui_t.append("No operator-specific bmtool_ui method")
        return ui_t

    # TODO: remove this method.
    def bmtool_ui_modifier_stats(self, context):
        """
        This method should be in operator
        Should return modifier settings
        Should return list of strings
        """
        ui_t = []
        ui_t.append("No bmtool_ui_modifier_stats method")
        return ui_t

    # TODO: remove this method.
    def bmtool_ui_list(self):
        """
        Returns list of lines with info about modifiers
        """

        ui_t = []

        # List of modifiers
        if self._BMTOOL_UI_SHOW_ALL_OBJECTS:
            for y in self.selected_objects:
                for x in self.bmtool_ui_modifiers_list(y):
                    ui_t.append(x)
                ui_t.append(" ")
        else:
            for x in self.bmtool_ui_modifiers_list(self.m_list):
                ui_t.append(x)
            ui_t.append(" ")
        return ui_t

    # UI utils  {{{
    # TODO: remove this method.
    def bmtool_ui_modifiers_list(self, m_list):
        """
        Returns list of strings with info about m_list
        """

        ui_t = []

        m_name = m_list.get_cluster().name
        m_type = m_list.get_cluster().type

        layer = m_list.get_layer()

        ui_t.append("=============================")
        ui_t.append("       CLUSTERS LIST")
        ui_t.append("=============================")
        for x in m_list:
            ui_t += self._bmtool_ui_get_cluster_ui(
                x, layer.get_selection(), m_list, m_name, m_type)
        ui_t.append("=============================")
        return ui_t

    # TODO: remove this method.
    def _bmtool_ui_get_cluster_ui(
            self, cluster, cluster_selection, m_list, m_name, m_type):

        if cluster in cluster_selection:
            cluster_selected = True
        else:
            cluster_selected = False

        # Info about cluster
        ui_t = []
        if cluster.type == m_type:
            y = "<"
        else:
            y = "  "
        if cluster.name == m_name:
            y2 = ">"
        else:
            y2 = "  "

        y5 = cluster.get_this_cluster_tags()
        if len(y5) == 0:
            y5 = ''

        if cluster.has_clusters():
            y3 = "L"
            if cluster_selected:
                ui_t.append([f"{y2} {cluster.name} {y3} {y} {y5}", 10])
            else:
                ui_t.append([f"{y2} {cluster.name} {y3} {y} {y5}", 1])
        else:
            y3 = "C"
            if cluster_selected:
                ui_t.append([f"{y2} {cluster.name} {y3} {y} {y5}", 10])
            else:
                ui_t.append([f"{y2} {cluster.name} {y3} {y} {y5}", 3])

        # Info about its clusters
        if cluster.has_clusters() and cluster.instance_data['collapsed'] is False:
            ui_t.append("------------------------------")
            for x in cluster:
                ui_t += self._bmtool_ui_get_cluster_ui(
                    x, cluster_selection, m_list, m_name, m_type)

            ui_t.append("------------------------------")
        elif cluster.has_clusters() and cluster.instance_data['collapsed'] is True:
            ui_t.append("layer collapsed")

        # Info about its modifiers
        elif not cluster.has_clusters()\
                and cluster.instance_data['collapsed'] is False:
            ui_t.append("------------------------------")
            for mod in cluster:
                ui_t.append([f"{mod.name}", 2])
            ui_t.append("------------------------------")
        elif not cluster.has_clusters()\
                and cluster.instance_data['collapsed'] is True:
            ui_t.append("modifiers cluster collapsed")

        ui_t.append("")
        return ui_t

    # TODO: remove this method.
    def bmtool_ui_cluster_visibility(self, cluster):
        line = " "
        for x in cluster.get_this_cluster_visibility():
            if x == 'ON':
                y = "+"
            elif x == 'HALF':
                y = "-"
            elif x == 'OFF':
                y = "x"
            line += y
            line += " "
        return line

    # TODO: remove this method.
    def bmtool_ui_modifier_visibility(self, m_list):
        """
        Returns list of strings with info about m_list's active modifier
        """
        ui_t = []
        ui_t.append("Not implemented for modifiers clusters")
        return ui_t
    # }}}
# }}}
