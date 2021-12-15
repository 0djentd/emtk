from modifiers_list import ModifiersList

class ExtendedClustersList(
                           FirstLayerClustersList,
                           ObjectClustersList,
                           SortableClustersList,
                           ActiveCluster,
                           ModifiersList
                           ):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

class ClustersList(
                   ObjectClustersList,
                   SortableClustersList,
                   ActiveCluster,
                   ModifiersList
                   ):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

class ExtendedModifiersList(
                            FirstLayerModifiersList,
                            ObjectClustersList,
                            ActiveModifier,
                            ModifiersList
                            ):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

class ModifiersList(
                   ObjectClustersList,
                   ActiveModifier,
                   ModifiersList
                   ):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
