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

BMTools
=======

_BMTools_ is a _Blender_ addon that uses _EMTKL_ to simplify editing
modifiers stack through modal operators and abstraction layers.

_BMToolM_ is a modal operator that can be used to edit clusters
and modifiers of an object. It has editing modes for
all editable properties of all Blender modifiers.
It can be extended using _ClustersEditor_ class.

_BMToolM_ _lite_ is a modal operator for viewing and basic editing
of clusters and modifiers.
It cant be used to edit modifiers properties.
