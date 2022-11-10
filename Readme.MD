# Repo for "Towards a Taxonomy of Industrial Needs and Enabling Technologies in Industry 4.0" data

## Table of contents
* [General Info](#general-info)
* [Abstract](#abstract)
* [Preprint](#preprint)
* [Authors](#authors)
* [Acknowledgments](#acknowledgments)
* [Data](#data)
* [Installation](#installation)



## General Info
This repository collects all the data developed for the journal paper "Towards a Taxonomy of Industrial Needs and Enabling Technologies in Industry 4.0", together with the code that renders those data queryable and usable within a search engine.
An interactive version of the Planet4 Taxonomy is available on http://taxonomy.planet4project.eu/

### Abstract 

One of the biggest challenges for digital transformation in the Industry 4.0 (I4.0) paradigm is the lack of mutual understanding between the academic and the industrial world. On the one hand, this can lead the industry to fail to apply new technologies and innovations from scientific research. At the same time, academics struggle to find and focus on real-world applications for their developing technological solutions. Moreover, the increasing complexity of industrial needs and technological solutions is widening this hiatus. To reduce this knowledge and communication gap, this article proposes a mixed approach of humanistic and engineering techniques applied to the technological and enterprise fields. The result of this study is represented by a taxonomy in which industrial needs and I4.0-focused technologies are categorized and connected so that it is possible to identify candidate solutions for an industrial need. Additionally, from the educational perspective, the taxonomy can help academics identify real-world scenarios to integrate them into the teaching process of digital technologies.


### Preprint 
The preprint version of the paper will be soon available.

### Authors

Roberto Figliè, Riccardo Amadio, Marios Tyrovolas, Chrysostomos Stylios, Łukasz Pa ́sko, Dorota Stadnicka, Anna Carreras-Coch, Agustín Zaballos, Joan
Navarro, and Daniele Mazzei 

### Acknowledgments
This work has been partially funded by Programme Erasmus+, Knowledge Alliances, Application No 621639-EPP-1-2020-1-IT-EPPKA2-KA, PLANET4: Practical Learning of Artificial iNtelligence on the Edge for indusTry 4.0.
More on https://www.planet4project.eu/

## Data 

Inside the [data folder](data/) you can find and explore different version of the Taxonomy Database (SqLite,CSV,Excel).
You can also explore the Taxonomy or know more about its definitions in a PDF format inside [this folder](data/PDF_versions/).
The [subfolder scripts](data/scripts/) is helpful to convert the data from the Production Database to different data types.



## Installation
1. Install requirements : 
```bash
pip install -r requirements.txt
```
2. Set environment variable  for development setup:
```bash
export FLASK_ENV=development 
```
PS: With this feature you can code and the web server is updated live (live-reloading)
3. Run the flask web server :
```bash
python -m flask run 
```
4. Open default browser on page : 

[http://localhost:5000/](http://localhost:5000/)





## Todo

- [ ] Pagination Api
- [ ] Refactoring and performance improvement of application
- [ ] Replace Tagme with SWAT
- [ ] Replace SQLite with Graph Database Knowledge
- [ ] Find and Train a model to replace Tagme/SWAT with GraphDB
