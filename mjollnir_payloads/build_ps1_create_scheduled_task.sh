#!/usr/bin/bash

# $1: program
# $2: program argument
# $3: frequency
# $4: at time
# $5: task name
# $6: output filename
# $7: source code


P="`dirname \"$0\"`"
P_OUTPUT="public_files"
NAME_OUT=$6
LAUNCHER_NAME=$7

cp $LAUNCHER_NAME $P/../$P_OUTPUT/$NAME_OUT

sed -i "s/{{PROGRAM}}/$1/g" $P/../$P_OUTPUT/$NAME_OUT

# $2 = PROGRAM ARGUMENT
if [[ $2 == "" ]]; then
    sed -i "s/{{PROGRAM_ARG}}//g" $P/../$P_OUTPUT/$NAME_OUT
else
    sed -i "s/{{FREQUENCY}}/-Argument '$2'/g" $P/../$P_OUTPUT/$NAME_OUT
fi



# $3 = FREQUENCY
if [[ $3 == "daily" ]]; then
    sed -i "s/{{FREQUENCY}}/-Daily/g" $P/../$P_OUTPUT/$NAME_OUT
elif [[ $3 == "once" ]]; then
    sed -i "s/{{FREQUENCY}}/-Once/g" $P/../$P_OUTPUT/$NAME_OUT
elif [[ $3 == "atlogon" ]]; then
    sed -i "s/{{FREQUENCY}}/-AtLogon/g" $P/../$P_OUTPUT/$NAME_OUT
    sed -i "s/{{AT_TIME}}//g" $P/../$P_OUTPUT/$NAME_OUT # need to remove the AT_TIME in case of AtLogon !
else
    sed -i "s/{{FREQUENCY}}/-Once/g" $P/../$P_OUTPUT/$NAME_OUT
fi

# $4 = AT_TIME
if [[ $4 == "" ]]; then
    sed -i "s/{{AT_TIME}}//g" $P/../$P_OUTPUT/$NAME_OUT
else
    sed -i "s/{{AT_TIME}}/-At '$4'/g" $P/../$P_OUTPUT/$NAME_OUT
fi

sed -i "s/{{TASK_NAME}}/$5/g" $P/../$P_OUTPUT/$NAME_OUT