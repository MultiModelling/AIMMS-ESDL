#!/usr/bin/env python
# coding: utf-8
import os 
from uuid import uuid4 

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
warnings.filterwarnings("ignore", message= ".*pandas only supports SQLAlchemy connectable*")






def get_sql(query):
    try:
        result = pd.read_sql(query, conn)
        return result
    except pymysql.Error as e:
        print("Error: unable to fetch data %d: %s" %(e.args[0], e.args[1]))





# # Class that reads the SQL back in. Used to check if the data is ordered correctly and edits the ESDL

# In[8]:


conn = pymysql.connect(
    host= Host,
    user=User,
    password=PW)
conn.select_db(DB)
cursor = conn.cursor()

class SQLESDL:
    def __init__(self, DB, ApiUser):
        self.tables =  get_sql("Select table_schema as database_name, table_name from information_schema.tables where table_type = 'BASE TABLE' and table_schema = '" + DB+"' and table_name LIKE '" + ApiUser+"_%' order by database_name, table_name;")
        self.ApiUser = ApiUser
        self.DB= DB
        
        for i in self.tables.table_name:
            j = i.replace((ApiUser+'_'), '')
            print((ApiUser+'_'),j)
            setattr(self, j,get_sql('SELECT * FROM '+DB+'.'+i+ ';'))

    
    def getAttributes(self):    
        return dir(self)


    
 
# if __name__ == "__main__":
#     Schema = DB
#     Training = SQLESDL(Schema)
#     print(Training.getAttributes())
#     conn.close()



# # Function that writes output to ESDL

# In[ ]:


def OutputESDL(Schema,context= {'User': 'Test'}):
    ApiUser = context['User']
    
    Training = SQLESDL(Schema,ApiUser)
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
    print(df.state)
    for i,row in df.iterrows():
        changables = esh.get_by_id(row.id)
        print(changables.name, changables.state, row.state)
        changables.state = row.state
        
    
    

            
    df2 = Training.KPIs
    df2 = df2[df2['name_KPI']== "1"]
    print(df2)
    for i,row in df2.iterrows():
        Assetname = row.id_KPI.replace("TEACOS_Was_Optional_",'')
        AssetId = get_sql("SELECT * FROM "+Schema+"."+ApiUser+"_Assets where `name` =  '"+ Assetname.lstrip() +"';").id[0]
        
        changables = esh.get_by_id(AssetId)
        changables_kpi_list = changables.KPIs
        if not changables_kpi_list:
            changables.KPIs = esdl.KPIs(id=str(uuid4()))

        
        kpiwasoptional = esdl.IntKPI(id = row.id_KPI,name = '1', value = 1)
        changables.KPIs.kpi.append(kpiwasoptional)
        print(kpiwasoptional, AssetId,1)
    
    print(esh.to_string())
    esh.save_as(Outputfile)

    conn.close()
    
if __name__ == "__main__":
    OutputESDL(DB,{'User':'Test'})

