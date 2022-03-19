#!/bin/bash

fd -e py -X sed -i 's/EMTKL/libemtk'
fd -e py -X sed -i 's/EMTK/libemtk'
fd -e py -X sed -i 's/emtkl/libemtk'
fd -e py -X sed -i 's/emtk/libemtk'

fd -e py -X sed -i 's/BMTools/EMTK'
fd -e py -X sed -i 's/BMTool/EMTK'
fd -e py -X sed -i 's/bmtools/emtk'
fd -e py -X sed -i 's/bmtool/emtk'

