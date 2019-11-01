r"""
The .bok files are Microsoft Access mdb files.
This script reads the data, saving the text as a .txt file (convert_from_bok()). 
Problem: the texts are encoded in the Windows-1256 format
instead of UTF-8 in the .bok file.
Python 3 has difficulties dealing with this,
because it considers any string a unicode string.
Current (convoluted but working) solution: save the text as a temp file,
open it with Windows-1256 encoding and save it again in utf-8 encoding.

The bok file contains a number of tables, of which the most important are:
* Main: contains the metadata of the book
* bxxxx (in which xxxx is the Shamela id of the book): contains the text,
  one page per row.
* txxxx (in which xxxx is the Shamela id of the book): contains the headings,
  with reference to the page numbers

The script loops through every row in the bxxxx table,
checks whether the page section id is in the txxxx table,
adds the OpenITI structural markup to the headings if it is,
and adds the page numbers in OpenITI format.


To do:
* what with other tables and columns (e.g., on which sura and aya are discussed?)
*

Done (but to check with Maxim):
* remove footnotes in the same way as Maxim does (using the special character?)
* remove editor's introduction? use the ### |EDITOR| tag before it?
* double line break before each paragraph?
* line breaks before page numbers?

Tables

|table name|column name    |present in number of files|data in number of files|
|----------|---------------|--------------------------|-----------------------|
|bxxxx     |               |7509                      |7509                   |
|          |nass           |7509                      |7509                   |
|          |seal           |7509                      |7509                   |
|          |id             |7509                      |7509                   |
|          |page           |7509                      |7451                   |
|          |part           |7509                      |7449                   |
|          |hno            |1748                      |1744                   |
|          |na             |1027                      |100                    |
|          |sora           |1027                      |100                    |
|          |aya            |1027                      |100                    |
|          |b1             |17                        |17                     |
|          |b2             |1                         |1                      |
|          |b3             |1                         |1                      |
|          |b4             |1                         |1                      |
|          |blnk           |16                        |16                     |
|          |ppart1         |40                        |40                     |
|          |ppage1         |40                        |40                     |
|          |ppart2         |7                         |7                      |
|          |ppage2         |7                         |7                      |
|          |ppart3         |7                         |7                      |
|          |ppage3         |7                         |7                      |
|          |ppart4         |2                         |2                      |
|          |ppage4         |2                         |2                      |
|          |done           |3                         |3                      |
|          |bhno           |1                         |1                      |
|Main      |               |7509                      |7509                   |
|          |oauth          |7509                      |7509                   |
|          |auth           |7509                      |7509                   |
|          |bver           |7509                      |7509                   |
|          |oauthver       |7509                      |7509                   |
|          |over           |7509                      |7509                   |
|          |lng            |7509                      |7509                   |
|          |betaka         |7509                      |7509                   |
|          |aseal          |7509                      |7509                   |
|          |seal           |7509                      |7509                   |
|          |bk             |7509                      |7509                   |
|          |onum           |7509                      |7509                   |
|          |bkid           |7509                      |7509                   |
|          |ad             |7509                      |7509                   |
|          |cat            |7509                      |7509                   |
|          |islamshort     |7509                      |7508                   |
|          |authinf        |7509                      |7265                   |
|          |higrid         |7509                      |7265                   |
|          |pdfcs          |7509                      |6711                   |
|          |pdf            |7509                      |6480                   |
|          |inf            |7509                      |5617                   |
|          |shrtcs         |2664                      |2124                   |
|          |tafseernam     |7509                      |183                    |
|          |vername        |7509                      |16                     |
|          |blnk           |7509                      |16                     |
|txxxx     |               |7509                      |7507                   |
|          |sub            |7509                      |7507                   |
|          |id             |7509                      |7507                   |
|          |tit            |7509                      |7507                   |
|          |lvl            |7509                      |7507                   |
|abc       |               |7509                      |397                    |
|          |a              |7509                      |397                    |
|          |b              |7509                      |397                    |
|          |c              |7509                      |397                    |
|Shorts    |               |7509                      |341                    |
|          |nass           |7509                      |341                    |
|          |ramz           |7509                      |341                    |
|          |bk             |7509                      |341                    |
|sPdf      |               |7509                      |236                    |
|          |part           |7509                      |236                    |
|          |sfilename      |7509                      |236                    |
|          |onum           |7509                      |236                    |
|men_u     |               |7509                      |148                    |
|          |id             |7509                      |148                    |
|          |name           |7509                      |148                    |
|          |bk             |7509                      |148                    |
|avPdf     |               |7509                      |28                     |
|          |cs             |7509                      |28                     |
|          |def            |7509                      |28                     |
|          |onum           |7509                      |28                     |
|          |vername        |7509                      |28                     |
|          |pdfver         |7509                      |28                     |
|men_b     |               |7509                      |17                     |
|          |id             |7509                      |17                     |
|          |manid          |7509                      |17                     |
|          |name           |7509                      |17                     |
|          |bk             |7509                      |17                     |
|nBound    |               |7509                      |13                     |
|          |d              |7509                      |13                     |
|          |b              |7509                      |13                     |
|          |dver           |7509                      |13                     |
|          |bver           |7509                      |13                     |
|          |bcode          |7509                      |13                     |
|oShr      |               |7509                      |9                      |
|          |matn           |7509                      |9                      |
|          |sharhid        |7509                      |9                      |
|          |matnid         |7509                      |9                      |
|          |sharh          |7509                      |9                      |
|oShrooh   |               |7509                      |9                      |
|          |matn           |7509                      |9                      |
|          |matnver        |7509                      |9                      |
|          |sharhver       |7509                      |9                      |
|          |sharh          |7509                      |9                      |
|Shrooh    |               |7509                      |0                      |
|          |matn           |7509                      |0                      |
|          |sharhid        |7509                      |0                      |
|          |matnid         |7509                      |0                      |
|          |sharh          |7509                      |0                      |
|com       |               |7509                      |0                      |
|          |id             |7509                      |0                      |
|          |com            |7509                      |0                      |
|          |bk             |7509                      |0                      |
|men_h     |               |7509                      |0                      |
|          |id             |7509                      |0                      |
|          |name           |7509                      |0                      |
|          |upg            |7509                      |0                      |
|10759     |               |1                         |1                      |
|          |wrd            |1                         |1                      |
|          |pos            |1                         |1                      |
|10786     |               |1                         |1                      |
|          |wrd            |1                         |1                      |
|          |pos            |1                         |1                      |
|10772     |               |1                         |1                      |
|          |wrd            |1                         |1                      |
|          |pos            |1                         |1                      |
|10769     |               |1                         |1                      |
|          |wrd            |1                         |1                      |
|          |pos            |1                         |1                      |
|10773     |               |1                         |1                      |
|          |wrd            |1                         |1                      |
|          |pos            |1                         |1                      |

"""

import csv
import pypyodbc
import os
import shutil
import re
import rarfile
from collections import defaultdict, OrderedDict
import traceback
import textwrap


rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRaR.exe"
magicValue = "######OpenITI#\n\n"
metaHeaderEnd = "#META#Header#End#"

VERBOSE = True

# SPECIAL_CHARS
# closing ')', '}' and ']'
# '-' (a range in character set)
# '&', '~', (extended character set operations)
# '#' (comment) and WHITESPACE (ignored) in verbose mode
#_special_chars_map = {i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}
_special_chars_map = {i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~#\t\n\r\v\f'}

def escape(pattern):
    """
    Escape special characters in a string.
    From Python module re, changed in version 3.7
    Earlier versions of re.escape() escaped all non-alphanumeric characters
    (thus including all Arabic letters);
    the new version escapes only those with a special function in regex.
    """
    if isinstance(pattern, str):
        return pattern.translate(_special_chars_map)
    else:
        pattern = str(pattern, 'latin1')
        return pattern.translate(_special_chars_map).encode('latin1')

def unzip(source_filename):
    """
    unzips the RAR archive to a new folder in the same directory
    """
    dest_dir = source_filename[:-4]
    if VERBOSE:
        print("unzipping to dest_dir:", dest_dir)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    with rarfile.RarFile(source_filename) as rf:
        rf.extractall(dest_dir)
    return dest_dir

def read_csv_2_dict(fp, sep="\t", idkey = "0.BookIDno"):
    """read a csv file with the csv.DictReader,
    which returns each row in the csv as a dictionary
    (key = column name, value = cell value):
    rowdict{column1_heading : cellR1C1, column2_heading : cellR1C2, ...}
    Then create a new dictionary that uses
    the cell in one of the columns (with heading idkey) as key,
    and the entire row dictionary as value:
    {id1: rowdict1, id2:rowdict2, ...}

    Args:
        fp (str): path to the csv file
        sep (str): separator that delimits field in the csv
        idkey (str): column header in the csv of the column that should
            become the key for the dictionary

    Returns:
        d (dict): a dictionary that has the idkey field of every row as key,
            and a dictionary representation of the row as value.
    """
    with open(fp, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter = sep)
        d=dict()
        for row in reader: # returns row as a dictionary
            #print(row[idkey], type(row[idkey]))
            i = row[idkey].split("/")[-1]
            d[i] = row
    return d

def rename_bok(folder, file):
    """
    The bok files inside the RAR archive usually have Arabic names;
    replace this name with the name of the RAR archive (i.e., the Shamela id)
    """
    for fn in os.listdir(folder):
        if fn.endswith(".bok"):
            os.rename(os.path.join(folder, fn), file)

def print_table_and_column_names(cur):
    """
    print a list of all tables (and their column headings) in the database
    """
    all_tables = cur.tables()
    print()
    for table in list(all_tables):
        if table[3] == "TABLE":
            cur.execute("""SELECT * from {}""".format(table[2]))
            print("Table", table[2], ": column names:")
            for heading in ["   "+d[0] for d in cur.description]:
                print(heading)    

def get_book_metadata(cur, bookURL):
    """
    gets the book metadata from the "Main" table in the database

    Args:
        cur: pypyodbc database cursor object
            (necessary for querying the database)

    Returns:
        metadata (str): a string containing the metadata
            (in the same order as in the Shamela table)
    """

    #meta_dic = dict()
    meta_dic = OrderedDict()
    cur.execute("""SELECT * from Main""")
    meta = list(cur.fetchall())
    col_headers = [x[0] for x in cur.description]
    #print(col_headers)
    for row in meta:
        for i, field in enumerate(row):
            if col_headers[i] == "betaka":
                meta_dic["Shamela_short_metadata_record"] = ""
                betaka = re.split("[\n\r]+", field)
                for b in betaka:
                    b = re.split(": ", b, maxsplit=1)
                    if len(b)>1:
                        meta_dic[b[0]] = b[1]
                    else:
                        meta_dic["digitization_comments"] = b[0]
            else:
                #print(col_headers[i], field)
                #print(re.sub(r"\.?\n+", ". ", str(field)))
                meta_dic[col_headers[i]] = re.sub(r"\.?[\r\n]+", ". ", str(field))
    meta_dic["ScrapeDate"] = "2019-10-16"
    meta_dic["ScrapeURL"] = bookURL
    metadata = "" 
    for x in meta_dic:
        metadata += "#META# {}: {}\n\n".format(x, meta_dic[x])
    return metadata
        
def get_structural_data(cur, title_table):
    """extract the structural data (i.c., indication of titles)
    from the database table (which is named t + the Shamela text number) """

    if VERBOSE:
        print("currently extracting all titles from title_table", title_table)

##    # print all the rows in the title table
##    cur.execute("""SELECT * from {}""".format(title_table))
##    for x in cur.fetchall():
##        print(x)

    #extract the titles, levels and section ids from the table and store in a dictionary:
    cur.execute("""SELECT tit, lvl, sub, id from {}""".format(title_table))

    #NB: sub seems to indicate in the table when an id has more than one title;
    #    if it has only one, sub = 0. We are not using this feature;
    #    instead, for every section id, we will make a list of its titles (and their levels)
    
    struct_dict = dict()
    for row in cur.fetchall():
        if row[3] not in struct_dict:
            struct_dict[row[3]] = []
        struct_dict[row[3]].append([row[0], row[1], row[2]])
    return struct_dict

def deNoise(text):
    """
    Eliminate all diacritics from the text in
    order to faciliate its computational processing
    """
    noise = re.compile(""" َ  | # Fatha
                             ً  | # Tanwin Fath
                             ُ  | # Damma
                             ٌ  | # Tanwin Damm
                             ِ  | # Kasra
                             ٍ  | # Tanwin Kasr
                             ْ  | # Sukun
                             ـ | # Tatwil/Kashida
                             ّ # Tashdid
                             """, re.VERBOSE)
    text = re.sub(noise, "", text)
    text = re.sub("ﭐ", "ا", text) # replace alif-wasla with simple alif
    return text

def add_structural_formatting(passage_text, tit, lvl):
    """
    add formatting based on the level of the titles in the database table.
    """
    #print(" ", tit)
    #tit_regex = re.sub("(\[|\]\(\))", r"\\\1", tit) # replace square brackets with literal square brackets
    tit_regex = escape(tit)
    #print(">", repr(tit_regex))
    tit_regex = re.sub(" ", "\s+", tit_regex) # allow for line break inside title
    #print(">", repr(tit_regex))
    if re.findall(r"\[?\(?{}".format(tit_regex), passage_text, flags=re.DOTALL):
        r = "\n\n### {} AUTO ".format(int(lvl)*"|")+r"\1\n\n"
        passage_text = re.sub(r"(\[?\(?{}\)?\]?)".format(tit_regex), r, passage_text, flags=re.DOTALL)
    else:
        if VERBOSE:
            print("!!!title not inside text", tit)
        passage_text = "\n\n### {} CHECK ".format(int(lvl)*"|") + tit + "\n\n" + passage_text
    return passage_text

def remove_unwanted_new_lines(text):
    """
    remove new lines that do not follow a full stop, colon or semicolon;
    Do not remove newlines after titles (i.e., if multiple newlines follow)
    """
    # remove the new lines before page numbers: 
    text = re.sub(r" *\n+ *(PageV\d+P\d+)\n+", r" \1 ", text)
    # restore new lines when the page number is preceded by a relevant character:
    text = re.sub(r"""([.:!؟|*"]|AUTO|CHECK) (PageV\d+P\d+) """, r"\1\n\n\2\n\n", text)
    # restore new lines when the page number is followed by ###:
    text = re.sub(r"""\s+(PageV\d+P\d+)\s+\#\#\#""", r"\n\n\1\n\n###", text)
    # double the new lines when the page number is preceded by a relevant character
    text = re.sub("""(?<=[.:!؟|*"])\n+(PageV\d+P\d+)""", r"\n\n\1", text)

    text = re.sub("\n{2,}", "\n\n", text)

    return text

def get_text_and_title_table_name(cur):
    # get the names of all the tables in the database:
    all_tables = cur.tables()
    if VERBOSE:
        print("Tables in this file:")
    for table in list(all_tables):
        if VERBOSE:
            print("   ", table)
        if re.match("b\d+$", table[2]):
            text_table = table[2]
        elif re.match("t\d+$", table[2]):
            title_table = table[2]
        # print the content of the other tables;
        # if they are empty, print only the column titles:
        else:
            if VERBOSE:
                if table[3] == "TABLE": # i.e., a data table, not an internal table
                    cur.execute("""SELECT * from {}""".format(table[2]))
                    if cur.fetchall():
                        for y in cur.fetchall():
                            print(y)
                    else:
                        print("NO DATA; column names:", [d[0] for d in cur.description])
    return text_table, title_table

def make_numeric(n):
    if str(n).isnumeric():
        return int(n)
    else:
        return 0

def get_book_text(cur, tempfile):
    """
    in the database, the text is contained in a table named b...
    (... being the number of the text).
    Unfortunately, this text number is not always the same
    as the id number of the rar/bok file
    this function first finds the name of the relevant table
    and then extracts the pages and page numbers from that table,
    writing them to a file    
    """

##    # print the names of all tables (and their column headings) in the dababase:
##    print_table_and_column_names(cur)

    # get the names of the text and title tables in the database:
    text_table, title_table = get_text_and_title_table_name(cur)
    
    # get the title data for the structural markup:
    struct_dict = get_structural_data(cur, title_table)

    # prepare the strings to receive the text and endnotes: 
    text = ""
    endnotes = ""

    # check if the book contains an introduction by the editor:
    editorial = False
    for p in struct_dict:
        for t in struct_dict[p]:
            tit = deNoise(t[0])
            if "مقدمة التحقيق" in tit or "مقدمة المحقق" in tit or "مقدمة الناشر" in tit:
                editorial = True
                text += "### |EDITOR|\n"

    #extract the text and page numbers from the table
    if VERBOSE:
        print("currently extracting all text from text_table", text_table)
    cur.execute("""SELECT nass, part, page, id from {}""".format(text_table))
    
    # format the text and page numbers, and save to the temp file
    #print(editorial)
    page_no = 0
    vol_page = ""
    for row in cur.fetchall():
        if row[2] != None:
            # if the new row contains the text of a new page,
            # (NB: this is not always the case!)
            # add the page number under the text of the previous page: 
            if page_no != make_numeric(row[2]):
                text += vol_page

            # set variables for current row:
            if VERBOSE:
                print("vol {} page {} id {} : {}".format(row[1], row[2], row[3], row[0][:30]))
            passage_text = row[0]
            passage_id = row[3]
            page_no = make_numeric(row[2])
            vol_no = make_numeric(row[1])
            vol_page = "\n\nPageV{:02d}P{:03d}\n\n".format(vol_no, page_no)

            # remove the short vowels etc.:
            passage_text = deNoise(passage_text)
            # clean text:
            passage_text = re.sub("</?رأس>", "", passage_text)

            # remove the footnotes:
            footnotes = re.findall(r"[\r\n]+¬?_+[\r\n]+(.*)", passage_text, flags=re.DOTALL)
            if footnotes:
                endnotes += "PageV{:02d}P{:03d}:\n\n{}\n\n".format(vol_no, page_no, footnotes[0])       
                passage_text = re.sub("[\r\n]+¬?_+[\r\n]+.*", "", passage_text, flags=re.DOTALL)


            # add the structural formatting:
            if passage_id in struct_dict:
##                print(repr(passage_text))
                for el in sorted(struct_dict[passage_id], key= lambda item: item[1], reverse=True):
                    tit = deNoise(el[0])
                    lvl = el[1]
                    #print(tit, lvl)
                    if editorial:
                        #print(lvl, tit, ("مقدمة التحقيق" not in tit and "مقدمة المحقق" not in tit))
                        if lvl == 1 and ("مقدمة التحقيق" not in tit
                                         and "مقدمة المحقق" not in tit
                                         and "مقدمة الناشر" not in tit): # start of the text of the work itself
                            editorial = False
                            passage_text = add_structural_formatting(passage_text, tit, lvl)
                        # do not add structural markup to headings in editorial passages:
                        ## else: passage_text = passage_text 
                    else:
                        passage_text = add_structural_formatting(passage_text, tit, lvl)

                        
            text += passage_text
##            print(text)
##            input()
        else:
            text += row[0] + "\n\n\n----NO PAGE NO------\n\n\n\n"

        # wrap long lines: 
        text = reflow(text)
        
        # deal with unconvertible characters:
        text = re.sub("\x81", "###@###", text)
        text = re.sub("\x90", "###!!!###", text)
        text = re.sub("\x8d", "###~###", text)
        tempfile.write(text)
        text = ""
        # NB: can't put in the Arabic text here yet, because it will mess up the encoding
    if endnotes:
        tempfile.write("\n\n\n\n### |EDITOR|\nEndnotes\n\n"+endnotes)

def reflow(text, max_len=72):
    """wrap long lines, i.e. break long lines down
    by inserting a new line character (and two tildes)
    so that no line is longer than max_len characters.
    See https://docs.python.org/3.1/library/textwrap.html
    Mark the start of paragraphs with "# ".

    Args:
        text (str): text string to be wrapped
        max_len (int): "width" = max number of characters in a line

    Returns:
        newtext (str): wrapped string
    """
    newtext = []
    # split the text, keeping the number of newline characters:
    text = re.sub("\r", "\n", text)
    text = re.split("(\n+)", text)

    # wrap each line: 
    ignoreTuple = ("#000000#", "#NewRec#", "#####", "### ", "#META#", "Page")
    for line in text:
        #print(line[:20])
        if not line.startswith(ignoreTuple):
            if line != "" and "\n" not in line:
                line = "# " + line
                line = "\n~~".join(textwrap.wrap(line, max_len))
        newtext.append(line)
        
    # re-assemble the text: 
    newtext = "".join(newtext)

    # unwrap lines that are less than 10 characters long
    newtext = re.sub(r"[\r\n]+~~(.{1,6}?[\r\n]+)", r" \1", newtext)
    
    return newtext

def convert_to_utf_8():
    """
    the temp file contains the Windows-1256 encoded text;
    By reading it with the right encoding, it is converted to utf-8 automatically
    """
    if VERBOSE:
        print("converting to unicode...")
    with open("temp.txt", mode="r", encoding="cp1256") as file:
        t=file.read()
##        # replace the place holders by the Arabic words for volume and page:
##        t = re.sub("XXXjuzXXX", "الجزء", t)
##        t = re.sub("XXXsafhaXXX", "الصفحة", t)
        # replace the placeholders for the unconvertible characters:
        t = re.sub("###!!!###", "گ", t)
        t = re.sub("###~###", "چ", t)
        t = re.sub ("###@###", "پ", t)
    return t

def get_bookid(cur):
    cur.execute("""SELECT * from {}""".format("Main"))
    bookid=list(cur.fetchall())[0][0]
    return bookid
    

def get_data(path, bookURL):
    """
    makes an empty temporary file, and writes the relevant data
    (text + metadata) from the database to this temp file
    The data cannot be written directly to the final file
    because the database is encoded in the Windows-1256 format
    and Python3 automatically considers the strings that are
    the outcome of the database query as utf-8 strings.
    Therefore we save the data first as a temporary file,
    which we later open again to convert it to utf-8. 
    """
    if VERBOSE:
        print("bok file:", path)
    # empty the temp.txt file:
    with open("temp.txt", mode="w") as tempfile:
        tempfile.write("")

    # connect to the database:
    conn = pypyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                            + r"Dbq={};unicode_results=True".format(path))
    #NB: unicode_results doesn't seem to have any influence: setting it to False
    #or leaving it out gives the exact same result

    # get the metadata
    cur = conn.cursor()
    metadata = get_book_metadata(cur, bookURL)

    # write the metadata to a temporary file:
    with open("temp.txt", mode="a") as tempfile:
        tempfile.write(magicValue + metadata + "\n\n#META#Header#End#\n\n\n\n")
        
        # get the text, format it, and add it to the tempfile:
        get_book_text(cur, tempfile)

    bookid = get_bookid(cur)

    conn.close()
    return bookid


def save_file(filename, t):
    with open(filename, mode="w", encoding = "utf-8") as file:
        file.write(t)




def convert_from_bok(fp, md_dir, bookURL):
    """Main function: convert bok file to txt"""
    bookid = get_data(fp, bookURL)
    t = convert_to_utf_8()
    t = remove_unwanted_new_lines(t)
    txt_file = os.path.join(md_dir, "Shamela{:06d}.txt".format(int(bookid)))
    if VERBOSE:
        print("OUTPATH:", txt_file)
    save_file(txt_file, t)


def convert_all_boks_in_folder(sourcedir, outdir, scrapefp):
    """
    Loop through the sourcedir and convert all bok files in it.
    Use the csv at scrapefp to get the url where the file was scraped from.

    Args:
        sourcedir (str): path to the directory where the bok files are stored
        outdir (str): path to the directory where the converted files should be stored
        scrapefp: path to the csv file that contains the scraping data
            (headings: bookTitle,bookUrl,bok_file_Url)
    """
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    scrapedict = read_csv_2_dict(scrapefp, sep=",", idkey = "bookUrl")
    for fn in os.listdir(sourcedir):
        fp = os.path.join(sourcedir, fn)
        if fp.endswith(".bok"):
            bookid = str(int(os.path.splitext(fn)[0]))
            bookURL = scrapedict[bookid]["bookUrl"]
            txt_file = os.path.join(outdir, "Shamela{:06d}.txt".format(int(bookid)))
            if not os.path.exists(txt_file):
                print(fp)
                try:
                    convert_from_bok(fp, outdir, bookURL)
                except Exception as e:
                    print("***", fp, "failed")
                    print("***", e)
                    print(traceback.format_exc())
                    failed.append((fp, repr(e)))
    if failed:
        import json
        fp = os.path.join(outdir, "_failed_conversions.json")
        with open(fp, mode="w", encoding="utf-8") as file:
            json.dump(failed, file)

if __name__ == "__main__":
    failed = []
    VERBOSE = False
    sourcedir = r"./2_bok"
    outdir = r"./4_OpenITI_mARkdown"
    scrapefp = r"./0_shamela_scraping/shamelaScrapeList.csv"
    convert_all_boks_in_folder(sourcedir, outdir, scrapefp)

##    if not os.path.exists(outdir):
##        os.mkdir(outdir)
##    scrapedict = read_csv_2_dict(scrapefp, sep=",", idkey = "bookUrl")
##    for fn in os.listdir(sourcedir):
##        fp = os.path.join(sourcedir, fn)
##        if fp.endswith(".bok"):
##            bookid = str(int(os.path.splitext(fn)[0]))
##            bookURL = scrapedict[bookid]["bookUrl"]
##            txt_file = os.path.join(outdir, "Shamela{:06d}.txt".format(int(bookid)))
##            if not os.path.exists(txt_file):
##                print(fp)
##                try:
##                    convert_from_bok(fp, outdir, bookURL)
##                except Exception as e:
##                    print("***", fp, "failed")
##                    print("***", e)
##                    print(traceback.format_exc())
##                    failed.append((fp, repr(e)))
##
##    import json
##    with open("failed_conversions.json", mode="w") as file:
##        json.dump(failed, file)

    

            



