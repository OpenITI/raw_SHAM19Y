import os, json, re, sys, textwrap, shutil
import ara

folderList = ["./3_json/", "./5_failed_conversion/", "./5_successful_conversion/"]

def getData(folder, file):
    with open(folder + file, "r", encoding="utf8") as f1:
        data = f1.read()

        # reformat inconsistencies in text:
        data = data.lower()
        data = data.replace(':null', ':"null"')
        data = data.replace(':""', ':"null"')
        data = data.replace(":''", ':"null"')
        data = data.replace("¬", "")

        data = ara.deNoise(data)
        
        # load as JSON into DIC
        dataJ = json.loads(data)

        # - metadata
        if "main" in dataJ:
            meta = dataJ["main"][0]

            if "bk" in meta:
                bk = meta["bk"]
            else:
                bk = "NONE"

            if "au" in meta:
                au = meta["au"]
            else:
                au = "NONE"

            if "ca" in meta:
                ca = meta["ca"]
            else:
                ca = "NONE"

            if "ii" in meta:
                ii = meta["ii"]
            else:
                ii = "NONE"

            if "||" in au:
                au = re.split("\|\|", au)[0]
                au = au.replace("\t", " ")

            words = len(re.findall("\w+", data))

            var = "\t".join([file, au, bk, ca])
        else:
            var = "\t".join([file, "au", "bk", "ca"])

        return(var)

exceptions

def collectTitles(folderList):
    dataMeta = []
    count = 0

    for sub in folderList:
        lof = os.listdir(sub)

        for f in lof:
            if not f.startswith("."):
                count += 1
                if count % 100 == 0:
                    print(count)
                print(f)
                var = getData(sub, f)

                print(var)
                dataMeta.append(var)

    with open("SHAM19Y_Metadata.csv", "w", encoding="utf8") as f9:
        f9.write("\n".join(dataMeta))

collectTitles(folderList)
