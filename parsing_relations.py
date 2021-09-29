import csv
from os import read
import sqlite3



def read_csv():
    _relations=None
    with open("taxonomy_problems_technology.csv", newline='') as csvfile:
        _relations = list(csv.reader(csvfile, delimiter=','))
    return _relations

def create_table(cur,con):
    cur.execute('''CREATE TABLE relations
               (name text, parent text, articles text, category text)''')
    con.commit()

def save_data(_relations,cur,con):
    for row in _relations:
        print(row)
        cur.execute(f"INSERT INTO relations VALUES ('{row[0]}','{row[1]}','{row[2]}','{row[3]}')")
    con.commit()

def main():
    _relations=read_csv()
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    # create_table(cur,con)
    save_data(_relations,cur,con)

    
            
        
                


if __name__ == "__main__":
    main()
