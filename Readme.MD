### Installation
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


### Data 

Inside the data folder you can find and explore different version of the Taxonomy Database (SqLite,CSV,Excel).
The subfolder scripts it's helpful if you want to convert the data from the Production Database to different data types.



### Todo

- [ ] Pagination Api
- [ ] Refactoring and performance improvement of application
- [ ] Replace Tagme with SWAT
- [ ] Replace SQLite with Graph Database Knowledge
- [ ] Find and Train a model to replace Tagme/SWAT with GraphDB
