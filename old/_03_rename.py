import os, shutil

folder = "./2_bok_TEMP/"
folder1 = "./2_bok/"

lof = os.listdir(folder)

count = 0
for sub in lof:
	if sub.endswith(".rar"):
		tlof = os.listdir(folder+sub)
		for t in tlof:
			if t.endswith(".bok"):
				os.rename(folder+sub+"/"+t, folder1+sub.split(".")[0]+".bok")
		shutil.rmtree(folder+sub+"/")


