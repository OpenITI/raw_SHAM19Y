import rarfile
import os
import shutil

# point Python to the location of the Unrar.exe program on your machine:
# (the program can be downloaded from https://www.win-rar.com/download.html)
rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRaR.exe" 

def unRAR(source_fp, bok_dir):
    # extract the bok file into a temporary directory:
    bookid = os.path.splitext(os.path.basename(source_fp))[0]
    temp_dir = source_fp[:-4]
    with rarfile.RarFile(source_fp) as rf:
        rf.extractall(temp_dir)
    # move the file to the bok directory
    for fn in os.listdir(temp_dir):
        if fn.endswith(".bok"):
            os.rename(os.path.join(temp_dir, fn), os.path.join(bok_dir, bookid+".bok"))
    # remove the temp_dir:
    shutil.rmtree(temp_dir)

src_folder=r".\1_rar"
bok_folder=r".\2_bok"
for fn in os.listdir(src_folder):
    unRAR(os.path.join(src_folder, fn), bok_folder)
