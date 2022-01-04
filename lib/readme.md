Copyright 2022, Sergey Shapochkin

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


EMTKL, ExtendedModifiersToolKitLibrary.
=======================================

This library provides new level of abstraction for _Blender_ modifiers stack.

Library name is not final and probably will be changed on release.

_EMTKL_ is designed to be used with _BMTools_.

Most classes and methods have docstrings.

There are some unittests for basic operations.

# Main concepts #
_Actual_ _modifier_ is an actual Blender modifier.

_Modifier_ is a cluster or actual modifier.

_Cluster_ is an object that consists of any number
of modifiers or clusters.
Cluster is any subclass of ClusterTrait.

_ModifiersCluster_ is a cluster that only has
actual Blender modifiers in it.

_ClustersLayer_ is a cluster that only has
other clusters in it. This doesnt mean
that it cant contain ModifiersClusters
with actual modifiers.

_ExtendedModifiersList_ is an object representing
first layer of clusters. It is similar to ClustersLayer,
but doesnt have ClusterTrait attributes.
It require all modifiers in it to be on same Blender object.

_Sorting_ _Rule_ is an object that represents set of
rules that can be used to sort clusters in ExtendedModifiersList.

_ModifiersOperator_ is a mix-in class for Operator class.
It has methods for manipulating multiple
ExtendedModifiersList instances.

# Currently supported features # 
All basic editing, like moving, applying, removing,
duplication and switching visibility of clusters.

Serialization and deserialization of clusters state.

Clusters Commands and Actions.

# TODO # 
Buffering for ExtendedModifiersList controller.

Panel type subclass for panels that use
ExtendedModifiersList.

Operators for ExtendedModifiersList controller.

More clusters operation types.
