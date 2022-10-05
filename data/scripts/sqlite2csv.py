import sqlite3
import pandas as pd



if __name__=="__main__":
    con = sqlite3.connect("../taxonomy.db")
    art_df=pd.read_sql_query("select * from articles",con)
    rel_df=pd.read_sql_query("select * from relations",con)
    tax_df=pd.read_sql_query("select * from taxonomy",con)
    art_df.to_csv("../articles.csv",index=False)
    rel_df.to_csv("../relations.csv",index=False)
    tax_df.to_csv("../taxonomy.csv",index=False)