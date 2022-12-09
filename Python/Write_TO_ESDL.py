#!/usr/bin/env python
# coding: utf-8
import os

# In[1]:
from dotenv import load_dotenv
load_dotenv()


Filename = os.getenv("ESDL_INPUT_FILENAME")
Outputfile = os.getenv("ESDL_OUTPUT_FILENAME")
Host = os.getenv("DATABASE_HOST")
DB = os.getenv("DATABASE_NAME")
User = os.getenv("DATABASE_USER")
PW = os.getenv("DATABASE_PASSWORD")

from esdl.esdl_handler import EnergySystemHandler
from esdl import esdl
import pymysql
import pandas as pd
import warnings
warnings.filterwarnings("ignore", message= ".*pandas only support SQLAlchemy connectable.*")



conn = pymysql.connect(
    host= Host,
    user=User,
    password=PW)
cursor = conn.cursor()



def get_sql(query):
    try:
        result = pd.read_sql(query, conn)
        return result
    except pymysql.Error as e:
        print("Error: unable to fetch data %d: %s" %(e.args[0], e.args[1]))

class SQLESDL:
    def __init__(self, DB):
        self.tables = get_sql("Select table_schema as database_name, table_name from information_schema.tables where table_type = 'BASE TABLE'and table_schema = '" + DB + "' order by database_name, table_name;")
        self.DB= DB
        
        for i in self.tables.table_name:
            setattr(self, i,get_sql('SELECT * FROM '+DB+'.'+i+ ';'))

    
    def getAttributes(self):    
        return dir(self)


    
 
if __name__ == "__main__":
    Schema = DB
    Training = SQLESDL(Schema)
    print(Training.getAttributes())
    print(Training.Assets)
    


# In[3]:


def OutputESDL(Schema):
    Training = SQLESDL(Schema)
    esh = EnergySystemHandler()
    es = esh.load_file(Filename)
    asset = esh.get_all_instances_of_type(esdl.Asset)
    proj = []
    for a in asset:
        if a.state.value == 2:
#             kpiwasoptional = esdl.IntKPI(name = 'TEACOS_was_optional',value = 1)
#             a.kpi = kpiwasoptional
#             print(a.name, a.kpi.name)
            proj.append(a.id)
    
    df = Training.Assets
    df = df[df['id'].isin(proj)]
    print(df)
    for i,row in df.iterrows():
        changables = esh.get_by_id(row.id)
        changables.state = row.state
#         print(changables.name, changables.state, row.state)
    
    
    esh.save_as(Outputfile)

    
    
if __name__ == "__main__":
    OutputESDL(DB)


# In[ ]:





# In[ ]:




