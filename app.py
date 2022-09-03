from flask import Flask, send_from_directory, request, render_template,jsonify
from flask_cors import CORS
from autocomplete import Autocomplete
import tagme
import csv
import sqlite3

tagme.GCUBE_TOKEN = "cbaed484-466a-44cd-a27d-610036404f01-843339462"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
autocomplete=Autocomplete()

@app.route('/api/', methods=["GET"])
def template_search():
    return send_from_directory('templates', 'home.html')


@app.route("/api/", methods=["POST"])
def search_api():
   _input = request.form.get('search-input')
   _results = search(_input)
   return jsonify(_results)


@app.route("/api/not_json_add_article", methods=["POST"])
def add_article_template():
   _title = request.form.get('title')
   _abstract = request.form.get('abstract')
   _body = request.form.get('body')
   _annotations=list(tagme.annotate(_title).get_annotations(0.1))+list(tagme.annotate(_abstract).get_annotations(0.1))+list(tagme.annotate(_body).get_annotations(0.1))
   left_side,right_side=search_annotations_on_taxonomy(_annotations)
   return render_template('add_article_results.html',results={"founded_elements":left_side,"not_founded_elements":right_side})

@app.route("/api/add_article", methods=["POST"])
def add_article_json():
   _title = request.form.get('title')
   _abstract = request.form.get('abstract')
   _body = request.form.get('body')
   _annotations=list(tagme.annotate(_title).get_annotations(0.1))+list(tagme.annotate(_abstract).get_annotations(0.1))+list(tagme.annotate(_body).get_annotations(0.1))
   left_side,right_side=search_annotations_on_taxonomy(_annotations)
   return jsonify({"founded_elements":left_side,"not_founded_elements":right_side})

@app.route("/api/add_article", methods=["GET"])
def add_article_form_template():
    return render_template('add_article.html')

@app.route("/api/not_json", methods=["POST"])
def search_api_template():
   _input = request.form.get('search-input')
   _results = search(_input)
   return render_template('results.html',results=_results)


def search(_input):
    _mentions = tagme_api(_input)
    if(len(_mentions) == 0):
        return {}
    else:
       _topics = search_into_taxonomy(_mentions)
       if(len(_topics) == 0):
           return {}
       else:
        _use_cases = find_use_cases(_topics)
        _use_cases_unrelated = unrelated_use_cases(_use_cases, _topics[0][1])
        _use_cases_unrelated = retrieve_link_use_cases(_use_cases_unrelated)
        _use_cases_related = retrieve_link_use_cases(_use_cases)
        return {"topics": _topics, "related_elements": _use_cases_related, "unrelated_elements": _use_cases_unrelated}


def unrelated_use_cases(_use_cases,_category):
    _category=get_opposite_category(_category)
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    _problems=[]
    for _use_case in _use_cases:
        _articles=_use_case[2].split(",")
        for _article in _articles:
            _problems=_problems+list(cur.execute(f"SELECT DISTINCT * FROM relations WHERE (articles LIKE '%,{_article}%' OR articles LIKE '%{_article},%') AND category='{_category}' ").fetchall())
    con.close()
    _parsed_problems=[]
    for _problem in _problems:
        if(_problem not in _parsed_problems):
            _parsed_problems.append({"elem":_problem,"count":_problems.count(_problem)})
    _problems=list(set(_problems))
    for _problem in range(0,len(_problems)):
        _problems[_problem]=list(_problems[_problem])
    return _problems
        
@app.route("/api/search", methods=["GET"])
def suggestion():
    word=request.args['word']
    return jsonify({"word":autocomplete.search(word)})


def get_opposite_category(_category):
    if(_category=="Problems"):
        return "Technology"
    else:
        return "Problems"


def retrieve_link_use_cases(_old_use_cases):
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    _new_use_cases=list(_old_use_cases)
    print(_new_use_cases)
    for i in range(0,len(_old_use_cases)):
        if(len(_old_use_cases[i][2])>0):
            _articles_id=_old_use_cases[i][2].split(",")
            _articles_response=[]
            for _article_id in _articles_id:
                _row=cur.execute(f"SELECT * FROM articles WHERE id={_article_id}").fetchone()
                _articles_response.append([_row[1],_row[2]])
            _new_use_cases[i][2]=_articles_response
    con.close()
    return _new_use_cases

def find_use_cases(_topics):
    con = sqlite3.connect('taxonomy.db')
    cur = con.cursor()
    _use_cases=[]
    for _topic in _topics:
        _topic=_topic[0].strip()
        query= f"SELECT * FROM relations WHERE name LIKE '%{_topic}%' ; "
        rows=cur.execute(query).fetchall()
        for row in rows:
            if(row[2]!=""):
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

def search_annotations_on_taxonomy(_annotations):
    left_side=[]
    right_side=[]
    for _annotation in _annotations:
        if(len(search_into_taxonomy([_annotation.entity_title]))>0):
            for _entity in search_into_taxonomy([_annotation.entity_title]):
                if(_entity not in left_side):
                    left_side.append(_entity)
        else:
            if(_annotation.entity_title not in right_side):
                right_side.append(_annotation.entity_title)
    return [left_side,right_side]



def tagme_api(_input):
    _mentions = tagme.mentions(_input)
    results = []
    #linkprob
    for mention in _mentions.mentions:
	    results.append(mention.mention)
    return results




@app.route('/api/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/api/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

