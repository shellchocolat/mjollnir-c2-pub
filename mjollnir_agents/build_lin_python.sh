#!/usr/bin/bash


# $1: ip
# $2: port
# $3: sleep time (second)
# $4: jitter (second)
# $5: random fruit (to modify hash)
# $6: folder out 'private or public'
# $7: output_filename
# $8: agent source code path
# $9: agent name (from config.json)

P="`dirname \"$0\"`"

NAME_IN=$8
P_OUTPUT=$6/$7

cp $NAME_IN $P/"a.tmp" # make a copy of the original source code

sed -i "s/{{IP}}/$1/g" $P/a.tmp
sed -i "s/{{PORT}}/$2/g" $P/a.tmp
sed -i "s/{{SLEEP}}/$3/g" $P/a.tmp
sed -i "s/{{JITTER}}/$4/g" $P/a.tmp
sed -i "s/{{FRUIT}}/$5/g" $P/a.tmp
sed -i "s/{{AGENT_NAME}}/$9/g" $P/a.tmp

cp $P/"a.tmp" $P/../$P_OUTPUT

chmod +x $P/../$P_OUTPUT

rm $P/a.tmp
