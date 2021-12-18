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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from .dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

# This is not correct.
from .lists.modifiers_list import ModifiersList


class ClusterRequest():
    """
    This thing looks like this:
    x = {
         'from': <obj BevelCluster>,
         'require': [<action>, <action>]
         }
    """

    def __init__(self, obj, require):
        if isinstance(require, list):
            for x in require:
                if not isinstance(x, ClustersAction):
                    raise TypeError
            actions = require
        elif isinstance(require, ClustersAction):
            actions = [require]
        else:
            raise TypeError

        self.o = obj
        self.require = actions

    def __str__(self):
        return f"Cluster request from {self.o} is {self.require}"

    def __repr__(self):
        return f"ClusterRequest from {self.o} is {self.require}"


class ClustersAction():
    """
    This thing looks like this:
    x = {
         'verb': 'REMOVE',
         'subject': <obj BevelCluster>
         'status': = 'STILL_NOT_ALLOWED'
         }
    """

    def __init__(self, verb, subject):
        if not isinstance(verb, str):
            raise TypeError(f'{type(verb)}')

        if len(verb) == 0:
            raise ValueError

        if _WITH_BPY:
            modifiers_type = bpy.types.Modifier
        else:
            modifiers_type = DummyBlenderModifier

        if not isinstance(subject, modifiers_type)\
                and not isinstance(subject, ModifiersList):
            raise TypeError(f'{type(subject)}')

        self.verb = verb
        self.subject = subject
        self.status = 'STILL_NOT_ALLOWED'

    def __str__(self):
        return f"Cluster action {self.verb} {self.subject}"

    def __repr__(self):
        return f"ClusterAction [{self.verb} {self.subject}]"
