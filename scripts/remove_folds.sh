#!/bin/sh
fd -e py --exec sed -i "s/#\ }\}\}//g"
fd -e py --exec sed -i s/#\ \{\{\{//g
fd -e py --exec sed -i s/\ \{\{\{//g
fd -e py --exec sed -i s/\{\{\{//g
