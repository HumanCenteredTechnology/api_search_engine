from flask import Flask, send_from_directory, request, render_template,jsonify
import tagme
import csv
from wordhoard import Synonyms
import sqlite3

tagme.GCUBE_TOKEN = "cbaed484-466a-44cd-a27d-610036404f01-843339462"

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    return send_from_directory('templates', 'home.html')


@app.route("/json", methods=["POST"])
def search_web_json():
   _input = request.form.get('search-input')
   _results = search(_input)
   return jsonify(_results)

@app.route("/", methods=["POST"])
def search_web():
   _input = request.form.get('search-input')
   _results = search(_input)
   return render_template('results.html',results=_results)

def search(_input):
   _mentions = tagme_api(_input)
   if(len(_mentions) == 0):
    return []
   else:
       _topics=search_into_taxonomy(_mentions)

    return 


def search_into_taxonomy(_mentions):
    _results = []
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    for _mention in _mentions:
        _words_mention=_mention.split(" ")
        for _word in _words_mention:
            for row in cur.execute(f"SELECT * FROM taxonomy WHERE name LIKE '%{_word}%'"):
                if(row not in _results):
                    _results.append(row)
    return _results


def get_related_topics(_topics):
    

def get_variations(_word):
    _variations=[]
    if(_word[len(_word)-1]=="s"):
        _variations.append(_word[0:-1])
    else:
        _variations.append(_word+"s")
    if(_word[0].isupper()):
        _variations.append(_word[0].lower()+_word[1:len(_word)])
    else:
        _variations.append(_word.capitalize())
    return _variations

def get_taxonomy_lower_striped():
    _taxonomy = {}
    csv_reader = None
    with open('taxonomy.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            _taxonomy[row[0].lower().strip()]= {"mention": row[0],"category": row[1], "link": row[2]}
    return _taxonomy

def get_taxonomy():
    _taxonomy = {}
    csv_reader = None
    with open('taxonomy.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            _taxonomy[row[0].lower()]= {"mention": row[0],"category": row[1], "link": row[2]}
    return _taxonomy

def tagme_api(_input):
    _mentions = tagme.mentions(_input)
    results = []
    #linkprob
    for mention in _mentions.mentions:
	    results.append(mention.mention)
    return results




@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

