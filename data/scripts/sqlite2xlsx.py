import sqlite3
import pandas as pd



if __name__=="__main__":
    con = sqlite3.connect("../taxonomy.db")
    art_df=pd.read_sql_query("select * from articles",con)
    rel_df=pd.read_sql_query("select * from relations",con)
    tax_df=pd.read_sql_query("select * from taxonomy",con)
    with pd.ExcelWriter('../Taxonomy.xlsx') as writer:
        # art_df.to_excel(writer, sheet_name='Articles')
        rel_df.to_excel(writer, sheet_name='Relations',index=False)
        tax_df.to_excel(writer, sheet_name='Taxonomy',index=False)
    