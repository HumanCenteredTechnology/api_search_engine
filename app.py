from flask import Flask, send_from_directory, request, render_template,jsonify
import tagme
import csv
import sqlite3

tagme.GCUBE_TOKEN = "cbaed484-466a-44cd-a27d-610036404f01-843339462"

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    return send_from_directory('templates', 'home.html')


@app.route("/", methods=["POST"])
def search_web_json():
   _input = request.form.get('search-input')
   _results = search(_input)
   return jsonify(_results)


@app.route("/not_json_add_article", methods=["POST"])
def add_article_results():
   _title = request.form.get('title')
   _abstract = request.form.get('abstract')
   _body = request.form.get('body')
   _annotations=list(tagme.annotate(_title).get_annotations(0.1))+list(tagme.annotate(_abstract).get_annotations(0.1))+list(tagme.annotate(_body).get_annotations(0.1))
   left_side,right_side=search_on_taxonomy(_annotations)
   return render_template('add_article_results.html',results={"founded_elements":left_side,"not_founded_elements":right_side})

@app.route("/add_article", methods=["POST"])
def add_article_results_json():
   _title = request.form.get('title')
   _abstract = request.form.get('abstract')
   _body = request.form.get('body')
   _annotations=list(tagme.annotate(_title).get_annotations(0.1))+list(tagme.annotate(_abstract).get_annotations(0.1))+list(tagme.annotate(_body).get_annotations(0.1))
   left_side,right_side=search_on_taxonomy(_annotations)
   return jsonify({"founded_elements":left_side,"not_founded_elements":right_side})

@app.route("/add_article", methods=["GET"])
def add_article():
    return render_template('add_article.html')

@app.route("/not_json", methods=["POST"])
def search_web():
   _input = request.form.get('search-input')
   _results = search(_input)
   return render_template('results.html',results=_results)


def search(_input):
    _mentions = tagme_api(_input)
    if(len(_mentions) == 0):
        return []
    else:
       _topics = search_into_taxonomy(_mentions)
       _use_cases=find_use_cases(_topics)
       _use_cases=retrieve_link_use_cases(_use_cases)
    return {"topics":_topics,"related_elements":_use_cases}


def retrieve_link_use_cases(_old_use_cases):
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    _new_use_cases=list(_old_use_cases)
    for i in range(0,len(_old_use_cases)):
        if(len(_old_use_cases[i][2])>0):
            _articles_id=_old_use_cases[i][2].split(",")
            _links=[]
            for _article_id in _articles_id:
                _links.append(cur.execute(f"SELECT * FROM articles WHERE id={_article_id}").fetchone()[1])
            _new_use_cases[i][2]=_links
    con.close()
    return _new_use_cases

def find_use_cases(_topics):
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    _use_cases=[]
    for _topic in _topics:
        for row in cur.execute(f"SELECT * FROM relations WHERE name LIKE '%{_topic[0]}%'"):
            if(len(row[2])>0):
                if(list(row) not in _use_cases):
                    _use_cases.append(list(row))
    con.close()
    return _use_cases
        

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
    con.close()
    return _results

def search_on_taxonomy(_annotations):
    left_side=[]
    right_side=[]
    for _annotation in _annotations:
        if(len(search_into_taxonomy([_annotation.entity_title]))>0):
            left_side=left_side+search_into_taxonomy([_annotation.entity_title])
        else:
            right_side.append(_annotation.entity_title)
    return [left_side,right_side]



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

