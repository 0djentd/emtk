Copyright 2022, Sergey Shapochkin

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.


# TODO #
Most important task at this point is rework of clusters reparser.
This includes ObjectState subclasses, ReparseConfig and ClusterConfig.

# CLUSTER TRAIT SERIALIZATION#
_data_: list[modifier]    ->  ClusterState
_default_data_: dict      ->  ClusterConfig
_instance_data_: dict     ->  ClusterState

# Design. #
What is default data?
Well, basically, this is ClusterState that is reused in multiple
cluster instances and can be stored in settings and scene as well
as in object props.

So what is cluster state?
This is dump of modifiers and clusters properties. It can include
as many items as needed by ReparseConfig. It can include multiple
layers as well.

What is ReparseConfig?
This is parser config that describes how parser should
compare ClusterState and existing objects.

So where is ReparseConfig should be stored?
It should be stored with _default_data_ in ClusterTypePreset.
Cluster instance can also have its own ReparseConfig,
that is stored with ClusterState.
