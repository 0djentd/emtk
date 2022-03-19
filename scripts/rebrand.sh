#!/bin/bash

fd -e py -X sed -i 's/emtkl/libemtk/g'
fd -e py -X sed -i 's/emtk/libemtk/g'
fd -e py -X sed -i 's/EMTKL/libemtk/g'
fd -e py -X sed -i 's/EMTK/libemtk/g'

fd -e py -X sed -i 's/bmtools/emtk/g'
fd -e py -X sed -i 's/bmtool/emtk/g'
fd -e py -X sed -i 's/BMTools/EMTK/g'
fd -e py -X sed -i 's/BMTool/EMTK/g'
