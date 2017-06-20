#!/bin/bash

CWD="$(pwd)"

cd $CWD/blender && sh push.sh
cd $CWD/fsl && sh push.sh
cd $CWD/guacdb && sh push.sh
cd $CWD/itksnap && sh push.sh
cd $CWD/paraview && sh push.sh
