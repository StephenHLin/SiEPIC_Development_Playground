#!/bin/bash

# OSX GitHub repository installation of SiEPIC files for KLayout and Lumerical INTERCONNECT

# assumes that 
# - SiEPIC-* repositories are in ~/Documents/GitHub
# - KLAYOUT_HOME is ~/.klayout

# to run:
# source symbolic_links_from_GitHub_to_KLayout.sh

export SRC=$HOME/Documents/GitHub
export DEST=$HOME/.klayout
export REPO=SiEPIC_Development_Playground

# mkdir $DEST/pymacros/SiEPIC_Development_Playground
ln -s $SRC/$REPO/Stephen_Dev_LIb.py $DEST/pymacros

