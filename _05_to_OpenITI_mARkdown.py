import os, json, re, sys, textwrap, shutil
import ara

magicValue = "######OpenITI#\n\n"

splitter = "### | === RECORD: "
recBeg = "######## BEGofRECORD ################################################### \n#NewRec# "

metaHeaderEnd = "#META#Header#End#"
altSpaceRE = "[^ٱء-ي]+"

# NB: Metadata is to be loaded from the JSON files

mainID = "SHAM19Y"

def matchTest(l1, l2):
    l1 = re.sub(altSpaceRE, "", l1)
    l2 = re.sub(altSpaceRE, "", l2)
    #print("TEST")
    #print("l1: %s" % l1)
    #print("l2: %s" % l2)
    #input()
    if l1 == l2:
        test = 1
    else:
        test = 0
    return(test)

# reformat single book
def reformatBook(srcFolder, trgFolder, file):
    numID = file.split(".")[0]
    shId = mainID+numID
    print("%s >>> %s" % (file, shId))
    
    with open(srcFolder+file, 'r', encoding="utf8") as f1:
        # save current file name
        with open("latest_file.txt", "w", encoding="utf8") as t1:
            t1.write(file)

        data = f1.read()

        # reformat inconsistencies in text:
        data = data.lower()
        data = data.replace(':null', ':"null"')
        data = data.replace(':""', ':"null"')
        data = data.replace(":''", ':"null"')
        data = data.replace("¬", "")

        data = ara.deNoise(data)
        
        # load as JSON into DIC
        data = json.loads(data)

        # for k,v in data.items():
        #     print(k)

        # NEED
        # - book
        if "b"+numID in data:
            book = data["b"+numID]
        else:
            book = 0
            print("\tNo BOOK found")

        # - toc
        if "t"+numID in data:
            toc = data["t"+numID]
        else:
            toc = 0
            print("\tNo TOC found")

        # - metadata
        if "main" in data:
            meta = data["main"][0]
        else:
            meta = 0
            print("\tNo META found")

        if meta == 0 or book == 0 or toc == 0:
            shutil.move(srcFolder+file, failedFolder+file)
            print("\t%s CANNOT BE PROCESSED (MOVED TO FAILED)" % file)
            #sys.exit("\t%s CANNOT BE PROCESSED (MOVED TO FAILED)" % file)

        else:
            newBook = {}
            print("\tNumber of pages: %d" % len(book))

            # build dictionary of pages (by IDs)
            for p in book:
                pageID = p["id"]
                #input(p)
                
                # building page/value
                if str(p["page"]).isnumeric():
                    page = int(p["page"])
                else:
                    page = 0
                if str(p["part"]).isnumeric():
                    vol = int(p["part"])
                else:
                    vol = 0
                    
                pn = "PageV%02dP%04d" % (vol, page)
                pageText = p["nass"]

                pageText = re.sub("\r|\n", "\n", pageText)

                if re.search("\n_+\n", pageText):
                    pageText = re.split("\n_+\n", pageText)[0]

                newBook[pageID] = [pageText, pn]
                #input(newBook[pageID])

            print("\tNumber of pages collected: %d" % len(newBook))

            # insert TOC values into pages
            print("\t%d TOC items" % len(toc))
            toc_count = 0
            proc = 0
            if len(toc) <= 1:
                pass
            else:
                print("mapping TOC...\n\t")
                for t in toc:
                    proc += 1
                    if proc % 100 == 0:
                        print("%d" % proc, end = ' ')
                        #print("%d" % proc)
                    oldHead = t["tit"]
                    #print("OLDHEAD: "+oldHead)
                    newHead = "\n### " + "|"*t["lvl"] + " AUT "

                    if t["id"] in newBook:
                        pageTemp = newBook[t["id"]][0]                        
                        pageTemp = re.split("\r|\n", pageTemp)
                        pageTempNew = []

                        headStatus = 0
                        for line in pageTemp:
                            if matchTest(line, oldHead) == 1:
                                #print(line)
                                #print(oldHead)
                                line = newHead + line
                                headStatus = 1
                            pageTempNew.append(line)

                        # merged page
                        pageTempNew = "\n\n".join(pageTempNew)
                        if headStatus == 0:
                            pageTempNew = newHead + "CHECK " + oldHead + "\n\n" + pageTempNew
                            toc_count += 1

                        #input(pageTempNew)
                        #input(newBook[t["id"]])
                        #input(newBook[t["id"]])
                        newBook[t["id"]][0] = pageTempNew

                    else:
                        toc_count += 1


                print("\n\t%d TOC items do not match" % toc_count)
                    
                #print(newBook[t["id"]])
                #input()

            # form metadata
            metaNew = []
            for k,v in meta.items():
                vNew = re.sub("(\n|\r)+", " || ", str(v))
                val = "#META# رم "+str(k)+": "+str(vNew)
                metaNew.append(val)

            metaNew = "\n".join(metaNew)
            print(metaNew)

            # assemble the book from newBook disctionary
            
            # - sort dic by keys; collect into a list
            newBookList = []
            for k, v in sorted(newBook.items()):
                page = v[0]+" "+v[1]
                newBookList.append(page)

            # insert bitaqa
            #newBook = meta[shId] + "\n\n" + magicValue + "\n".join(newBookList)
            newBook = "\n\n".join(newBookList)
            
            # reflow
            newText = []

            newBook = newBook.split("\n")
            ignoreTuple = ("#000000#", "#NewRec#", "#####", "### ", "#META#")
            lenSymb = 72
            
            for l in newBook:
                if l.startswith(ignoreTuple):
                    pass
                else:
                    if l != "":
                        l = "# " + l
                        l = "\n~~".join(textwrap.wrap(l, lenSymb))

                newText.append(l)
                
            text = "\n".join(newText)
            text = re.sub(r"\n~~(.{1,10})\n", r" \1\n", text)
            text = re.sub(" +", " ", text)
            text = re.sub("\n+", "\n", text)
            print("\t- reFlowing of the text is completed (with %d per line)..." % (lenSymb))

            text = magicValue + metaNew + "\n\n" + metaHeaderEnd + "\n" + text

            # save
            with open(trgFolder+shId, 'w', encoding="utf8") as f9:
                f9.write(text)

            # report
            print("\t%s has been processed" % file)
            shutil.move(srcFolder+file, successFolder+file)
            print("\t%s HAS BEEN SUCCESSFULLY CONVERTED" % file)


import random
def processAllBooks(srcFolder, trgFolder):
    lof = os.listdir(srcFolder)
    counter = len(lof)
    random.shuffle(lof)

    for f in lof:
        counter = counter - 1
        if counter % 100 == 0:
            print("=" * 30)
            print("===== %d files left to process " % counter)
            print("=" * 30)
        
        if f[0] != "." and f.endswith(".json"):
            print("="*60)
            print("="*60)
            print("="*60)
            reformatBook(srcFolder, trgFolder, f)
            #shutil.move(srcFolder+f, successFolder+f)
            #print("\t%s HAS BEEN SUCCESSFULLY CONVERTED" % f)
            #input()
        else:
            shutil.move(srcFolder+f, failedFolder+f)
            print("\t%s CANNOT BE PROCESSED (MOVED TO FAILED)" % f)
                
srcFolder     = "./3_json/"
trgFolder     = "./4_openITI_mARkdown/"
successFolder = "./5_successful_conversion/"
failedFolder  = "./5_failed_conversion/"

# move the latest file: this will be the file that has some issues and the execution of the script fails
try:
    with open("latest_file.txt", "r", encoding="utf8") as lf:
        lf_path = lf.read().strip()
        shutil.move(srcFolder+f, failedFolder+f)
        print("\t%s CANNOT BE PROCESSED (MOVED TO FAILED)" % f)
except:
    print("No `latest_file.txt` yet...")  

processAllBooks(srcFolder, trgFolder)

#reformatBook(srcFolder, trgFolder, "1138.bok.json")