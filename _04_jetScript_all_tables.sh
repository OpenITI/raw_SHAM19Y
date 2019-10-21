#!/bin/bash
# extracting data from MDB files

#echo "Testing the script"

srcFolder="2_bok"
trgFolder="3_json"

mkdir $trgFolder

cd ./$srcFolder
for mdbfile in *.bok
do
    echo $mdbfile
    ../jetread $mdbfile export -fmt json > ../$trgFolder/$mdbfile.json
    #read -p "Press enter to continue"
done
