[![Pylint](https://github.com/0djentd/emtk/actions/workflows/pylint.yml/badge.svg)](https://github.com/0djentd/emtk/actions/workflows/pylint.yml)

EMTK Extended Modifiers Tool Kit
=======

## Description

_EMTK_ is a _Blender_ addon that uses _EMTK_ to simplify editing
modifiers stack through modal operators and abstraction layers.

_EMTKM_ is a modal operator that can be used to edit clusters
and modifiers of an object. It has editing modes for
all editable properties of all Blender modifiers.

There is a few operators that invoke UI popups with similar or extended
functionality as well.

EMTK uses [libemtk](https://github.com/0djentd/libemtk), [modal_shortcuts](https://github.com/0djentd/modal_shortcuts) and [class_variables_editor_ui](https://github.com/0djentd/class_variables_editor_ui) as python modules.

To learn more about EMTK concepts, such as modifiers clusters, clusters layers and modifiers reparse check out [libemtk readme](https://github.com/0djentd/libemtk/blob/master/README.md).
Some useful [scripts](https://github.com/0djentd/emtk-dev-scripts).

## Installation
Linux:
```
mkdir -p ~/.config/blender/3.1/scripts/addons/
cd ~/.config/blender/3.1/scripts/addons/
git clone https://github.com/0djentd/emtk.git
```

Windows:
idk

Mac:
idk
