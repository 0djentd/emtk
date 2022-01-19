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

# What features required to be implemented? #

Modifier presets.

Clusters.
Clusters presets.
Different cluster subtypes support.

UI for presets.
UI for clusters.
UI for default cluster settings (a.k.a. cluster_type,
cluster_definition, parser_variables ...)

Full modal input support.
Full View3D support.

What this means?
Basically, all modifiers and clusters editing should be
possible in View3D, with minimum of menus, panels and as
fast as using built-in modal operators.
This should not limit customization of toolkit in any way
and can be ignored when some feature is too complex to customize
through single modal operator or popup.
Example:
    Cluster subtypes editing should not be implemented using
    modal operator, because it will not be possible to
    visualize changes made to cluster subtype using
    current clusters library implementation.

Support for storing cluster subtypes in preferences, scene and object.

# SERIALIZATION #
# How serialization/deserialization/reparse/parse works #
TODO: this explaination of reparse is not too good.
When cluster is first created (for example when new modifier is added)
it is being parsed. On this stage, it has no ObjectState instance.
ObjectState is being created when clusters list is removed (for example
when operator returns {'FINISHED'}).
This is required to later reparse clusters.

Reparsing clusters is a process of instantiating clusters with same
modifiers and clusters in them. It requires at least some of
list's objects variables to be stored in ObjectState associated with
cluster.
Reparsing clusters is required to associate stored cluster variables with
actual modifiers.

Example: ModifiersClusterState that has information about
names of modifiers in it and some of their properties.

ReparseConfig is an object that defines how stored variables should be
compared with existing ones.

Example: reparse_config.Delta can be used to allow successfully
reparsing objects with their int/float variables slightly different.

After finishing reparsing clusters, ObjectState objects are no longer used
and would be created again on operator finish.
When serialized ObjectState already exists at this stage, it is copied
to backup property of object.

# Pros and cons: #
Whole thing uses json instead of bpy.type.Property. Editing variables in UI
can be done using ui_class_variables_editor module.
Why whole thing uses json then?
Because blender collections does not support more than one object type.
Implementing everything through pointer properties and collections will
be much harder and probably will require using a lot
of usual variables anyway.
Example:
ClustersLayer can have both ModifiersClusters and ClustersLayers in it.

# CLUSTER PRESETS #
Default cluster settings is basically presets.
Default cluster settings and presets are the same thing.
Default cluster settings is ClusterConfig.
it is different from 

Initial cluster settings is what 'default cluster settings' should
be called instead.

Presets can be 'layered' on initial cluster settings.
Presets are used to modify objects.
Initial cluster settings are to parse cluster when it is created and
when modifiers were changed outside of clusters list.

Modal input.

Data that can be used in reparse and should be configurable
through reparse config class:
    Cluster default data.
    Cluster instance data.
    Cluster items.

Data that should never be used:
    Cluster state.

# INTERFACES #
How cluster can be created using constructor?
items = ModifierState(data={'angle_limit': 30, 'type'='BEVEL'},
                      name='')
reparse = ReparseConfig(data={'type': reparse_config.Basic(True)})
state = ListObjectState(data={'type': 'BEVEL_CLUSTER'}, name='Bevel',
                        items_data=items)
config = ClusterConfig(reparse, state)
cluster = ModifiersCluster(config)
