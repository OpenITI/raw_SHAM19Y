from collections import defaultdict
import pypyodbc
import os
import re
import json


def connect_to_db(path):
    # connect to the database:
    conn = pypyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                            + r"Dbq={};unicode_results=True".format(path))
    #NB: unicode_results doesn't seem to have any influence: setting it to False
    #or leaving it out gives the exact same result

    # get the metadata and the text, and write them to a temporary file
    cur = conn.cursor()
    return cur, conn

def make_book_dict(cur, file_id):
    """check all the tables in the current database
    and find out if the same structure already exists
    in the table_structures list.
    Also, check for every table and column if it contains data,
    and record this in the tables_dict dictionary"""

    # depict the current database's table structure in the form of a dictionary:
    
    book_dict = dict()
    all_tables = cur.tables()
    if VERBOSE:
        print(cur.description)
    for table in list(all_tables):
        if VERBOSE:
            print(table)
        if table[3] == "TABLE":
            table_name = table[2]
            book_dict[table_name] = []
            cur.execute("""SELECT * from {}""".format(table[2]))
            headings = [d[0] for d in cur.description]
            for row in cur.fetchall():
                row_dict = dict()
                for i, heading in enumerate(headings):
                    row_dict[heading] = row[i]
                    
                book_dict[table_name].append(row_dict)
    return book_dict


def save_to_json(d, fp):
    with open(fp, "w", encoding="utf-8") as file:
        json.dump(d, file, sort_keys=True, indent=4, ensure_ascii=False)
    

def load_json(fp):
    with open(fp, "r") as file:
        return json.load(file)


VERBOSE = False
source_folder = "2_bok"
dest_folder = "3_json"

##d = load_json("3_json/122405.json")
##print(d["Main"][0])
##input()

count = 0
for fn in os.listdir(source_folder):
    if fn.endswith(".bok"):
        file_id=os.path.splitext(fn)[0]
        outfp = os.path.join(dest_folder, file_id+".json")
        if not os.path.exists(outfp):
            count += 1
            print(count, fn)
            cur, conn = connect_to_db(os.path.join(source_folder, fn))
            book_dict = make_book_dict(cur, file_id)
            conn.close()
            save_to_json(book_dict, outfp)
        
