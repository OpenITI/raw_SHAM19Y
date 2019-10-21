import os, sys, re

folder = "./4_openITI_mARkdown/"

def collectTitles(folder):
    lof = os.listdir(folder)

    dataNew = []

    for f in lof:
        if f.startswith("."):
            pass
        else:
            with open(folder + f, "r", encoding="utf8") as f1:
                print(f)
                data = f1.read()

                bk = re.search(r"#META# رم (bk: .*)\n", data).group(1)
                au = re.search(r"#META# رم (authinf: .*)\n", data).group(1)

                if "||" in au:
                    au = re.split("\|\|", au)[0]
                    au = au.replace("\t", " ")

                words = len(re.findall("\w+", data))

                var = "%s\t%d\t%s\t%s\n" % (f, words, bk, au)
                dataNew.append(var)

    with open("SHAM19Y_Metadata.csv", "w", encoding="utf8") as f9:
        f9.write("".join(dataNew))

collectTitles(folder)
