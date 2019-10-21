#!/bin/bash
# extracting data from MDB files

echo "Testing the script"

srcFolder="1_rar"
trgFolder="2_bok_TEMP"

mkdir $trgFolder

cd ./$srcFolder
for rarFile in *.rar
do
    echo $rarFile
    mkdir ../$trgFolder/$rarFile
    unrar e $rarFile ../$trgFolder/$rarFile
    #../jetread $rarFile export -fmt json > ../$trgFolder/$rarFile.json
done
