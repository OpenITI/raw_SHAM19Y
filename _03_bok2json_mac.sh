#!/bin/bash
# extracting data from MDB files

# requires https://eggerapps.at/jetread/

srcFolder="2_bok"
trgFolder="3_json"

mkdir $trgFolder

cd ./$srcFolder
for mdbfile in *.bok
do
    echo $mdbfile
    ../jetread $mdbfile export -fmt json > ../$trgFolder/$mdbfile.json
done
```
