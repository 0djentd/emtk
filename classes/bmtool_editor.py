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

from .bmtool_input import BMToolModalInput

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ModalClustersEditor(BMToolModalInput):
    """Editor base class"""

    # Constructor {{{
    def __init__(self, *args, name, cluster_types, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(name, str):
            raise TypeError
        if not isinstance(cluster_types, list):
            cluster_types = [cluster_types]
        for x in cluster_types:
            if not isinstance(x, str):
                raise TypeError

        self.props = {
                      # Editor name to be shown in ui
                      'name': name,

                      # List of cluster types that this editor
                      # can be used with.
                      # Example:
                      # ['BEVEL_CLUSTER', 'BEVEL']
                      # Can be 'ANY' as well.
                      'cluster_types': cluster_types
                      }
    # }}}

    # Editor methods {{{
    def editor_switched_to(self, context, clusters):
        """Called every time editor is switched to."""
        return self.switched_to(context, clusters)

    def editor_switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        return self.switched_from(context, clusters)

    def editor_modal_pre(self, context, event, clusters):
        """Modal method 1."""
        return self.modal_pre(context, event, clusters)

    def editor_modal(self, context, event, clusters):
        """Modal method 2"""
        return self.modal(context, event, clusters)
    # }}}

    # Editor-specific method placeholders for subclasses {{{
    def switched_to(self, context, clusters):
        """Called every time editor is switched to."""
        self._no_editor_method()

    def switched_from(self, context, clusters):
        """Called every time editor is switched from."""
        self._no_editor_method()

    def modal_pre(self, context, event, clusters):
        """Modal method 1."""
        self._no_editor_method()

    def modal(self, context, event, clusters):
        """Modal method 2"""
        self._no_editor_method()

    def _no_editor_method(self):
        raise ValueError('No editor-specific method.')
    # }}}
