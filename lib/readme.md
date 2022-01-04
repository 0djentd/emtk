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

Library name is not final and probably will be changed on release.

This library provides new level of abstraction for Blender modifiers stack.

EMTKL is designed to be used with BMTools.

Most classes and methods have docstrings.

Main concepts:
    Actual modifier is an actual Blender modifier.

    Modifier is a cluster or actual modifier.

    Cluster is an object that consists of any number
    of modifiers or clusters.
    Cluster is any subclass of ClusterTrait.

    ModifiersCluster is a cluster that only has
    actual Blender modifiers in it.

    ClustersLayer is a cluster that only has
    other clusters in it. This doesnt mean
    that it cant contain ModifiersClusters
    with actual modifiers.

    ExtendedModifiersList is an object representing
    first layer of clusters. It is similar to ClustersLayer,
    but doesnt have ClusterTrait attributes.
    It require all modifiers in it to be on same Blender object.

    ModifiersOperator is a mix-in class for Operator class.
    It has methods for manipulating multiple
    ExtendedModifiersList instances.

Currently supported features:
    All basic editing, like moving, applying, removing,
    duplication and switching visibility of clusters.

    Serialization and deserialization of clusters state.

    Clusters Commands and Actions.

TODO:
    Buffering for ExtendedModifiersList controller.
    Panel type subclass for panels that use
    ExtendedModifiersList.
    Operators for ExtendedModifiersList controller.
    This will be required for new panel type.
