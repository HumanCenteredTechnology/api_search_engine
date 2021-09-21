from flask import Flask, send_from_directory, request, render_template
import tagme
import csv
from wordhoard import Synonyms

tagme.GCUBE_TOKEN = "cbaed484-466a-44cd-a27d-610036404f01-843339462"

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    return send_from_directory('templates', 'home.html')


@app.route("/", methods=["POST"])
def search_web():
   _input = request.form.get('search-input')
   _results = search(_input)
   print(_results)
   return render_template('results.html', results=_results)


def search(_input):
   _mentions = tagme_api(_input)
   if(len(_mentions) == 0):
    return []
   else:
    return search_into_taxonomy(_mentions)


def search_into_taxonomy(_mentions):
    _results = []
    _taxonomy=get_taxonomy()
    for _mention in _mentions:
            if(_mention in _taxonomy):
                    _results.append(_taxonomy[_mention])
            else:            
                _variations=get_variations(_mention)
                for _variation in _variations:
                    if(_variation in _taxonomy):
                        _results.append(_taxonomy[_variation])
                synonyms = Synonyms(_mention)
                for synonim in synonyms.find_synonyms():
                    if(synonim in _taxonomy):
                        _results.append(_taxonomy[synonim])
    return _results

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

def get_taxonomy():
    _taxonomy = {}
    csv_reader = None
    with open('taxonomy.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            _taxonomy[row[0]]= {"mention": row[0],"category": row[1], "link": row[2]}
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

