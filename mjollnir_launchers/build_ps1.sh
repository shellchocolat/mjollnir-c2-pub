#!/usr/bin/bash

# $1: ip
# $2: port
# $3: payload name
# $4: output filename
# $5: launcher source


P="`dirname \"$0\"`"
P_OUTPUT="public_files"
NAME_OUT=$4
LAUNCHER_NAME=$5

cp $LAUNCHER_NAME $P/../$P_OUTPUT/$NAME_OUT

sed -i "s/{{IP}}/$1/g" $P/../$P_OUTPUT/$NAME_OUT
sed -i "s/{{PORT}}/$2/g" $P/../$P_OUTPUT/$NAME_OUT
sed -i "s/{{PAYLOAD_NAME}}/$3/g" $P/../$P_OUTPUT/$NAME_OUT