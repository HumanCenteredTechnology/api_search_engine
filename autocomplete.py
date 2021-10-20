from fast_autocomplete import AutoComplete
import csv
import sqlite3

class Autocomplete:
  def __init__(self):
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    entities=cur.execute(f"SELECT name FROM taxonomy ").fetchall()
    words={}
    for entity in entities:
        words[entity[0]]={}
    self.autocomplete = AutoComplete(words=words)
 
  def search(self,_word):
      return self.autocomplete.search(word=_word, max_cost=3, size=3)[0]

