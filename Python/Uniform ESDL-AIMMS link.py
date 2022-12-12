#!/usr/bin/env python
# coding: utf-8

# # Uniform ESDL-Aimms connection

# ## Introduction
# 
# This is a ready made code script that transforms an ESDL to a database that can be imported to into AIMMS. It uses two python packages 'pyesdl' and 'pymysql' made by respectively TNO and Mysql to transform an esdl file to SQL tables that can be read by AIMMS.

# ## **Sensitive Quomare user information**

# In[ ]:





# In[ ]:





# In[1]:
import os
from dotenv import load_dotenv
load_dotenv()


Filename = os.getenv("ESDL_INPUT_FILENAME")
Outputfile = os.getenv("ESDL_OUTPUT_FILENAME")
Host = os.getenv("DATABASE_HOST")
DB = os.getenv("DATABASE_NAME")
User = os.getenv("DATABASE_USER")
PW = os.getenv("DATABASE_PASSWORD")


# In[2]:


import pymysql
import warnings
warnings.filterwarnings("ignore", message= ".*pandas only support SQLAlchemy connectable.*")



conn = pymysql.connect(
    host= Host,
    user=User,
    password=PW)
cursor = conn.cursor()


# In[ ]:





# ### Simple function that runs an SQL command
# 

# In[3]:






import pandas as pd

def get_sql(query):
    try:
        result = pd.read_sql(query, conn)
        return result
    except pymysql.Error as e:
        print("Error: unable to fetch data %d: %s" %(e.args[0], e.args[1]))

# if __name__ == "__main__" :
#     sql = get_sql('SELECT * FROM TESTDB_AIMMS.Arcs')
#     df = pd.DataFrame(sql)
#     print(sql)


# ### Function that creates a new database with DB the new name of the database and with SetofTables a list of all the tables in de database and set of attributes a list of tuples of attributes of every table

# In[4]:


def create_AIMMS_sql(DB, SetofTables,SetofAttributes):
    def __init__(self, DB):
        self.DB = DB
    cursor.execute('DROP DATABASE IF EXISTS ' + DB +';')
    cursor.execute('create database ' + DB +';')
    conn.select_db(DB)

#     query = "SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;') FROM information_schema.tables WHERE table_schema = '"+ DB + "';"
#     cursor.execute(query)
#     Tables = cursor.fetchall()
#     for i in Tables:
#         cursor.execute(i[0])
    
    
    
    try:
        query = []
        for i in range(len(SetofTables)):
            query.append('create table ' + SetofTables[i] + '(' + ','.join(SetofAttributes[i]) +')')
#         query = [
# '        create table Assets(aggregated varchar(100),aggregationCount varchar(100),assetType varchar(100),commissioningDate varchar(100),decommissioningDate varchar(100),description varchar(100),id varchar(100) Primary Key,installationDuration varchar(100),manufacturer varchar(100),name varchar(100),originalIdInSource varchar(100),owner varchar(100),shortName varchar(100),state varchar(100),surfaceArea varchar(100),technicalLifetime varchar(100));',
# '        create table Arcs(NameNode1 varchar(100), idNode1 varchar(100), nameNode2 varchar(100), idNode2 varchar(100), Carrier varchar(100), maxPower varchar(100), simultaneousPower varchar(100),PRIMARY KEY (idNode1, idNode2));',
# '        create table Producers(id varchar(100) Primary Key, name varchar(100), prodType varchar(100), OperationalHours varchar(100), fullLoadHours varchar(100), power varchar(100));',
# '        create table Conversions(id varchar(100) Primary Key,name varchar(100), efficiency varchar(100), power varchar(100));',
# '        create table Consumers(id varchar(100) Primary Key,name varchar(100), consType varchar(100), power varchar(100));',
# '        create table Transports(id varchar(100) Primary Key,name varchar(100), efficiency varchar(100), capacity varchar(100));',
# '        create table Products(stateOfMatter varchar(100), energyCarrierType varchar(100), id varchar(100) Primary Key,  emission varchar(100), name varchar(100), energyContent varchar(100));',
# '        create table Buildings(id varchar(100) Primary Key, floorArea varchar(100), buildingYear varchar(100), originalIdInSource varchar(100),surfaceArea varchar(100), name varchar(100), height varchar(100), asset1 varchar(100), asset2 varchar(100),asset3 varchar(100),asset4 varchar(100));']
        for i in query:
            cursor.execute(i)
        
        #Progress update
        print('SQL-file created from ESDL-file')
        print(query)
    except pymysql.Error as e:
            print("Error: unable to create table %d: %s" %(e.args[0], e.args[1]))
            
# if __name__ == "__main__" :
#     my_list =  [('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)'), ('id varchar(100)','name varchar(100)')]
#     create_AIMMS_sql('TESTDB_AIMMS',['Assets', 'Arcs', 'Producers', 'Conversions', 'Consumers', 'Transports', 'Products', 'Buildings'], my_list
#                     )


# ### Function that writes a tuple (val) of all lengths to database (DB) in Table (Sheet).

# In[5]:


def write_table_to_Sql(DB, Sheet, val):
    # Build query
    numofcol = get_sql(
        "SELECT COUNT(*) as NumberofCol from INFORMATION_SCHEMA.COLUMNS where table_schema = '"+ DB +"' and table_name = '" + Sheet + "';")
    numb = numofcol['NumberofCol'][0]
    query = 'INSERT INTO ' + DB + '.' + Sheet + ' VALUES (' + numb * '%s,'
    query = query[:-1] + ');'
    print(query)
    # Check query
    cursor.executemany(query, val)
    print('INSERT ' +Sheet+ ' COMPLETE')


# In[6]:


# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:29:13 2022

@author: Stijn
"""



from esdl.esdl_handler import EnergySystemHandler
from esdl import esdl



def ExtractDataESDL(TableName, Instances, SetofAttributes, SetofTables, SetofValues):
    
    if Instances == []:
        return
    valInstance =[]
    for m in Instances:
        temp = tuple()
        for d in dir(m):
            e = getattr(m, d)
            if e == None:
                temp+= (None,)
            else:
                if e == object:
                    temp+=(e.id)
                temp+=(e,)
        valInstance.append(temp)
    
    InstanceAttr = tuple()
    for d in dir(Instances[0]):
        if d == 'id':
            InstanceAttr += (d  + ' varchar(100) Primary Key',)
        else:
            InstanceAttr += (d  + ' varchar(100)',)
    
    SetofAttributes.append(InstanceAttr)
    SetofTables.append(TableName)
    SetofValues.append(valInstance)



if __name__ == "__main__":
    esh = EnergySystemHandler()
    es = esh.load_file(Filename)
    # xml_string = esh.to_string()
    #print(xml_string)
    
    SetofTables = []
    SetofAttributes = []
    SetofValues = []
    

    Assets = esh.get_all_instances_of_type(esdl.EnergyAsset)
    valAssets = [[n.id,
                  n.aggregated, 
                  n.aggregationCount, 
                  n.assetType, 
                  n.commissioningDate,
                  n.decommissioningDate, 
                  n.description,  
                  n.installationDuration, 
                  n.manufacturer, 
                  n.name, 
                  n.originalIdInSource, 
                  n.owner,
                  n.shortName, 
                  n.state, 
                  n.surfaceArea, 
                  n.technicalLifetime, 
                  n.costInformation] 
                for n in Assets]
    if(Assets != []):
        SetofTables.append('Assets')
        SetofAttributes.append(('id varchar(100) Primary key' ,
                                'aggregated varchar(100)', 
                                'aggregationCount varchar(100)', 
                                'assetType varchar(100)', 
                                'commissioningDate varchar(100)', 
                                'decommissioningDate varchar(100)' , 
                                'description varchar(100)' ,  
                                'installationDuration varchar(100)' , 
                                'manufacturer varchar(100)' , 
                                'name varchar(100)' , 
                                'originalIdInSource varchar(100)' , 
                                'owner varchar(100)' , 
                                'shortName varchar(100)' ,
                                'state varchar(100)' , 
                                'surfaceArea varchar(100)' , 
                                'technicalLifetime varchar(100)',
                                'costInformation_id varchar(100)'))
        SetofValues.append(valAssets)
    
    Producers = esh.get_all_instances_of_type(esdl.Producer)
    valProducers = [(n.id, 
                     n.name, 
                     n.prodType, 
                     n.operationalHours, 
                     n.fullLoadHours, 
                     n.power)
                for n in Producers]
    if(Producers != []):
        SetofAttributes.append(('id varchar(100) Primary key', 
                                'name varchar(100)', 
                                'prodType varchar(100)', 
                                'operationalHours varchar(100)', 
                                'fullLoadHours varchar(100)', 
                                'power varchar(100)'))
        SetofTables.append('Producers')
        SetofValues.append(valProducers)
    
    Consumers = esh.get_all_instances_of_type(esdl.Consumer)
    valConsumers = [(n.id, n.name, n.consType, n.power) 
                for n in Consumers]

    if(Consumers != []):    
        SetofAttributes.append(('id varchar(100)  Primary Key', 
                                'name varchar(100)', 
                                'consType varchar(100)', 
                                'power varchar(100)'))
        SetofTables.append('Consumers')
        SetofValues.append(valConsumers)
    
    Singlevalueprofiles = esh.get_all_instances_of_type(esdl.SingleValue)
    ConsumerProfiles = []
    valConsumerProfiles = []
    for n in Consumers:
        for p in n.port:
            for pr in p.profile:
                ConsumerProfiles.append(pr)
                if(pr in Singlevalueprofiles):
                    valConsumerProfiles.append((n.id,
                                                n.name,
                                                'null', 
                                                'null', 
                                                'null', 
                                                'null', 
                                                'null', 
                                                pr.id, 
                                                'null', 
                                                'null', 
                                                pr.value,
                                                pr.name,
                                                'null', 
                                                'null', 
                                                'null'))
                else:
                    valConsumerProfiles.append((n.id,
                                                n.name,
                                                pr.dataSource, 
                                                pr.endDate, 
                                                pr.field,pr.filters, 
                                                pr.host,
                                                pr.id, 
                                                pr.interpolationMethod, 
                                                pr.measurement,
                                                pr.multiplier,
                                                pr.name,
                                                pr.profileQuantityAndUnit,
                                                pr.profileType,
                                                pr.startDate))
    if(valConsumerProfiles != []):    
        SetofAttributes.append(('id_consumer varchar(100)', 
                                'name_consumer varchar(100)',
                                'dataSource varchar(100)', 
                                'endDate varchar(100)', 
                                'field varchar(100)', 
                                'filters varchar(100)', 
                                'host varchar(100)', 
                                'id varchar(100)', 
                                'interpolationMethod varchar(100)', 
                                'measurement varchar(100)', 
                                'multiplier varchar(100)', 
                                'name varchar(100)',  
                                'profileQuantityAndUnit varchar(100)', 
                                'profileType varchar(100)', 
                                'startDate varchar(100)'))
        SetofTables.append('ConsumerProfiles')
        SetofValues.append(valConsumerProfiles)
    
    Conversions = esh.get_all_instances_of_type(esdl.Conversion)
    valConversions = [(n.id, n.name, n.efficiency, n.power) 
                for n in Conversions]
    if(Conversions != []):    
        SetofAttributes.append(('id varchar(100)  Primary Key', 
                                'name varchar(100)', 
                                'efficiency varchar(100)', 
                                'power varchar(100)'))
        SetofTables.append('Conversions')
        SetofValues.append(valConversions)
    
    Transports = esh.get_all_instances_of_type(esdl.Transport)
    valTransports = [(n.id, 
                      n.name, 
                      n.efficiency, 
                      n.capacity) 
                for n in Transports]
    if(Transports != []):       
        SetofAttributes.append(('id varchar(100)  Primary Key', 
                                'name varchar(100)', 
                                'efficiency varchar(100)', 
                                'capacity varchar(100)'))
        SetofTables.append('Transports')
        SetofValues.append(valTransports)
    
    Arcs = esh.get_all_instances_of_type(esdl.OutPort)
    valArcs = [(a.energyasset.name,
                a.energyasset.id, 
                a.name, 
                a.id, 
                b.energyasset.name, 
                b.energyasset.id, 
                b.name, 
                b.id,
                a.carrier.name, 
                a.carrier.id, 
                1)
                 for a in Arcs for b in a.connectedTo]
    if(Arcs != []): 
        SetofAttributes.append(('Node1_name varchar(100)', 
                                'Node1_id varchar(100)',
                                'Outport_name varchar(100)',
                                'Outport_id varchar(100)', 
                                'Node2_name varchar(100)', 
                                'Node2_id varchar(100)',
                                'Inport_name varchar(100)', 
                                'Inport_id varchar(100)',
                                'PRIMARY KEY (Node1_id, Node2_id)',
                                'carrier varchar(100)',
                                'carrier_id varchar(100)',
                                'CostDummy varchar(100)'))
        SetofTables.append('Arcs')
        SetofValues.append(valArcs)
#     valArcs = [(a.energyasset.name,
#                 a.energyasset.id, 
#                 a.name, 
#                 a.id, 
#                 b.energyasset.name, 
#                 b.energyasset.id, 
#                 b.name, 
#                 b.id, 
#                 a.carrier.name, 
#                 a.carrier.id, 
#                 a.maxPower, 
#                 b.maxPower,
#                 a.simultaneousPower,
#                 b.simultaneousPower, 
#                 1)
#                  for a in Arcs for b in a.connectedTo]
#     SetofAttributes.append(('Node1_name varchar(100)', 
#                             'Node1_id varchar(100)',
#                             'Outport_name varchar(100)',
#                             'Outport_id varchar(100)', 
#                             'Node2_name varchar(100)', 
#                             'Node2_id varchar(100)',
#                             'Inport_name varchar(100)', 
#                             'Inport_id varchar(100)',
#                             'PRIMARY KEY (Node1_id, Node2_id)',
#                             'carrier varchar(100)',
#                             'carrier_id varchar(100)',
#                             'maxPower_Out varchar(100)',
#                             'maxPower_In varchar(100)', 
#                             'simultaneousPower_Out varchar(100)', 
#                             'simultaneousPower_In varchar(100)', 
#                             'CostDummy varchar(100)'))
#     SetofTables.append('Arcs')
#     SetofValues.append(valArcs)
    
#     Processes = esh.get_all_instances_of_type(esdl.InputOutputRelation)
# #     Processes = [a.behaviour for a in Conversions]
# #     print(Processes)
#     valProcesses = []
#     for a in Processes:
#         for i in a.mainPortRelation:
#             if type(i.port) == esdl.InPort:
#                 itype = 'In'
#             else:  itype = 'Out'
#             tup = (a.mainPort.id, a.name, a.mainPortQuantityAndUnit, a.id, itype)
#             for j in dir(i):
#                 k = getattr(i, j)
#                 if (type(k) == type(None) or type(k) == float):
#                     tup += (k,)
#                     print(j,k)
#                 else: 
#                     tup += (k.id,)
#             valProcesses.append(tup)
#     if(Processes != []):        
#         SetofAttributes.append(('mainPort  varchar(100)',
#                                 'name  varchar(100)',
#                                 'mainPortQuantityAndUnit  varchar(100)',
#                                 'id  varchar(100)',
#                                 'portType varchar(100)',
#                                 'port varchar(100)',
#                                 'quantityAndUnit varchar(100)', 
#                                 'ratio varchar(100)'))        
#         SetofTables.append('Processes')
#         SetofValues.append(valProcesses)
    
    
    Processes = Conversions
    valProcesses = []
    for a in Conversions:
        for b in a.port:
            ratio = 1
            if(a.behaviour):
                for i in a.behaviour:
                    mainport = i.mainPort
                    for j in i.mainPortRelation:
                        if (j.port == b):
                            ratio = j.ratio
                            break;
            
            else:
                ratio = a.efficiency
                mainport = a.port[1]
            if type(a.port[0]) == esdl.InPort:
                atype = 'In'
            else:  atype = 'Out'
            if type(b) == esdl.InPort:
                btype = 'In'
            else: btype = 'Out'
            tup = ('null', mainport.id, mainport.carrier.id, atype, b.id, btype, a.id, a.name, ratio, b.carrier.id, b.carrier.name)
            valProcesses.append(tup)
    if(valProcesses != []):
        SetofAttributes.append(('quantityAndUnit varchar(100)',
                                'mainPortId varchar(100)',
                                'mainPortCarrierId varchar(100)',
                                'mainPortType varchar(100)',
                                'portId varchar(100)',
                                'portType varchar(100)',
                                'conversionId varchar(100)',
                                'conversionName varchar(100)',
                                'ratio varchar(100)',
                                'carrierId varchar(100)',
                                'carrierName varchar(100)'))
        SetofTables.append('Processes')
        SetofValues.append(valProcesses)
    
    Carriers = esh.get_all_instances_of_type(esdl.Carrier)
    valCarriers = [(p.id,
                    p.name)
                for p in Carriers]
    if(Carriers != []):
        SetofAttributes.append(('id varchar(100) Primary Key',
                                'name varchar(100)'))
        SetofTables.append('Carriers')
        SetofValues.append(valCarriers)
    
    EnergyCarriers = esh.get_all_instances_of_type(esdl.EnergyCarrier)
    valEnergyCarriers = [(p.id, 
                    p.stateOfMatter, 
                    p.energyCarrierType, 
                    p.emission, 
                    p.name , 
                    p.energyContent)
                for p in EnergyCarriers]
    if(EnergyCarriers != []):
        SetofAttributes.append(('id varchar(100) Primary Key',
                                'stateOfMatter varchar(100)', 
                                'energyCarrierType varchar(100)',  
                                'emission varchar(100)',
                                'name varchar(100)',
                                'energyContent varchar(100)'))
        SetofTables.append('EnergyCarriers')
        SetofValues.append(valEnergyCarriers)
    
    GasCommodities = esh.get_all_instances_of_type(esdl.GasCommodity)
    if(GasCommodities != []):
        ExtractDataESDL('GasCommodities',GasCommodities, SetofAttributes, SetofTables, SetofValues)
    
    ElectricityCommodities = esh.get_all_instances_of_type(esdl.ElectricityCommodity)
    if(ElectricityCommodities != []):
        ExtractDataESDL('ElectricityCommodities',ElectricityCommodities, SetofAttributes, SetofTables, SetofValues)
    
    EnergyCommodities = esh.get_all_instances_of_type(esdl.EnergyCommodity)
    if(EnergyCommodities != []):
        ExtractDataESDL('EnergyCommodities',EnergyCommodities, SetofAttributes, SetofTables, SetofValues)
    
    Commodities = esh.get_all_instances_of_type(esdl.Commodity)
    valCommodities = [(h.id, h.name)
                 for h in Commodities]
    if(Commodities != []):    
        SetofAttributes.append(('id varchar(100)  Primary Key',
                                 'name varchar(100)'))
        SetofTables.append('Commodities')
        SetofValues.append(valCommodities)
    
    Matters = esh.get_all_instances_of_type(esdl.Matter)
    if(Matters != []): 
        ExtractDataESDL('Matters',Matters, SetofAttributes, SetofTables, SetofValues)
#     Matters = esh.get_all_instances_of_type(esdl.Matter)
#     valMatters =[]
#     for m in Matters:
#         temp = tuple()
#         for d in dir(m):
#             e = getattr(m, d)
#             if e == None:
#                 temp+= (None,)
#             else:
#                 temp+=(e,)
#         valMatters.append(temp)
    
#     MatterAttr = tuple()
#     for d in dir(Matters[0]):
#         if d == 'id':
#             MatterAttr += (d  + ' varchar(100) Primary Key',)
#         else:
#             MatterAttr += (d  + ' varchar(100)',)
#     SetofAttributes.append(MatterAttr)
#     SetofTables.append('Matters')
#     SetofValues.append(valMatters)


#     Buildings = esh.get_all_instances_of_type(esdl.Building)
#     ExtractDataESDL('Buildings',Buildings, SetofAttributes, SetofTables, SetofValues)
    Buildings = esh.get_all_instances_of_type(esdl.Building)
    valBuildings = [(a.id, 
                     a.floorArea, 
                     a.buildingYear, 
                     a.originalIdInSource, 
                     a.surfaceArea,
                     a.name, 
                     a.buildinginformation[0].height,
                     a.geometry.exterior.point[0].lat, 
                     a.geometry.exterior.point[0].lon)
                     for a in Buildings]
    if(Buildings != []):
        SetofAttributes.append(('id varchar(100) Primary Key', 
                                'floorArea varchar(100)', 
                                'buildingYear varchar(100)', 
                                'originalIdInSource varchar(100)',
                                'surfaceArea varchar(100)',
                                'name varchar(100)', 
                                'height varchar(100)', 
                                'Lat varchar(100)', 
                                'Lon varchar(100)'))
        SetofTables.append('Buildings')
        SetofValues.append(valBuildings)
    
        MapAssetToBuilding = [b for a in Buildings for b in a.asset]
        valMapAssetToBuilding = [(b.id, b.name, a.id, a.name, '1') for a in Buildings for b in a.asset]
        SetofAttributes.append(('id_Asset varchar(100) Primary Key', 
                                'name_Asset varchar(100)',  
                                'id_Building varchar(100)',
                                'name_Building varchar(100)', 
                                'Dummy varchar(100)'))
        SetofTables.append('MapAssetToBuilding')
        SetofValues.append(valMapAssetToBuilding)
        
    KPIs = esh.get_all_instances_of_type(esdl.KPI)
    valKPIs = []
    if(KPIs != []):
        for k in KPIs:
            valKPIs.append((k.id,k.name,k.value,'null','null','null','null'))
        SetofAttributes.append(('id_KPI varchar(100)', 
                    'name_KPI varchar(100)', 
                    'value_KPI varchar(100)',
                    'id_building varchar(100)',
                    'name_building varchar(100)',
                    'id_conversion varchar(100)',
                    'name_conversion varchar(100)'))
        SetofTables.append('KPIs')
        SetofValues.append(valKPIs) 
    
    KPIsBuildings = []
    valKPIsBuildings=[]
    if (Buildings != []):
        for b in Buildings:
            ks = b.KPIs           
            if (ks):
                KPIsBuildings.append(ks)
                for i in range(len(ks.kpi)):
                    temp = (ks.kpi[i].id, ks.kpi[i].name, ks.kpi[i].value,b.id, b.name, 'null','null')
                    valKPIsBuildings.append(temp)
    else:
        for k in KPIs:
            tup = (k.id, k.name, k.value,'null','null','null','null')
            valKPIsBuildings.append(tup)
            
    if(valKPIsBuildings != []):    
        SetofAttributes.append(('id_KPI varchar(100)', 
                    'name_KPI varchar(100)', 
                    'value_KPI varchar(100)',
                    'id_building varchar(100)',
                    'name_building varchar(100)',
                    'id_conversion varchar(100)',
                    'name_conversion varchar(100)'))
        SetofTables.append('KPIsBuildings')
        SetofValues.append(valKPIsBuildings)
    
    KPIConversions = []
    valKPIConversions=[]
    if (Conversions != []):        
        for b in Conversions:
            ks = b.KPIs
            if (ks):
                KPIConversions.append(ks)
                for i in range(len(ks.kpi)):
                    temp = (ks.kpi[i].id, ks.kpi[i].name, ks.kpi[i].value,'null','null',b.id, b.name, )
                    valKPIConversions.append(temp)
        
        SetofAttributes.append(('id_KPI varchar(100)', 
                    'name_KPI varchar(100)', 
                    'value_KPI varchar(100)',
                    'id_building varchar(100)',
                    'name_building varchar(100)',
                    'id_conversion varchar(100)',
                    'name_conversion varchar(100)'))
        SetofTables.append('KPIConversions')
        SetofValues.append(valKPIConversions)
        
    CostInformations = esh.get_all_instances_of_type(esdl.CostInformation)
    valCostInformations = []
    for a in Assets:
        c = a.costInformation    
        if(a.costInformation):
            temp = (a.id, a.name)
            for d in dir(c):
                e = getattr(c, d)
                if e == None or type(e) == str:
                    temp+= (None,)
                else:
                    temp+=(e.value,)
            valCostInformations.append(temp)
    CostInformationsAtt = ('AssetId varchar(100)', 'AssetName varchar(100)')
    if(CostInformations != []):    
        for d in dir(CostInformations[0]):
            CostInformationsAtt += (d  + ' varchar(100)',)
        SetofAttributes.append(CostInformationsAtt)
        SetofTables.append('CostInformations')
        SetofValues.append(valCostInformations)    
    

        
    
    Constraints = []
    valConstraints = []
    for a in Assets:
        for b in a.constraint:
            Constraints.append(b)
            print(type(b.attributeReference))
            temp = (a.id,a.name,b.id, b.name, b.attributeReference)
            c = b.range
            if(c):
                temp += (c.id,c.name,c.minValue,c.maxValue)
            else:
                temp += (None,None,None,None)

        
            valConstraints.append(temp)
                
#             ('NodeId varchar(100)',
#                       'NodeName varchar(100)',
#                       ' varchar(100)',
#                       'ConstraintName varchar(100)', 
#                       'ConstraintAttribute varchar(100)',
#                       'RangeId varchar(100)', 
#                       'RangeName varchar(100)', 
#                       'minValue varchar(100)', 
#                       'maxValue varchar(100)')
    if(Constraints != []):
        SetofAttributes.append(('Node_Id varchar(100)',
                      'Node_Name varchar(100)',
                      'Constraint_Id varchar(100)',
                      'Constraint_Name varchar(100)',
                      'Constraint_Attribute varchar(100)', 
                      'range_Id varchar(100)',
                      'range_name varchar(100)', 
                      'max varchar(100)', 
                      'min varchar(100)'))
        SetofTables.append('Constraints')
        SetofValues.append(valConstraints)
    
    
    QuantityAndUnitTypes = esh.get_all_instances_of_type(esdl.QuantityAndUnitType)
    valQuantityAndUnitTypes = []
    valEnergyContentUnit = []
    valEmissionUnits = []
    for c in Carriers:
        e = c.emissionUnit
        if(e):
            temp = (c.id, c.name, 'emissionUnit')
            for d in dir(e):
                a = getattr(e, d)
                if a == None:
                    temp+= (None,)
                else:
                    temp+=(a,)
            valEmissionUnits.append(temp)
            valQuantityAndUnitTypes.append(temp)
        if c not in Commodities:
            f = c.energyContentUnit
            if(f):
                temp = (c.id, c.name, 'energyContentUnit')
                for d in dir(f):
                    a = getattr(f, d)
                    if a == None:
                        temp+= (None,)
                    else:
                        temp+=(a,)
                valEnergyContentUnit.append(temp)
                valQuantityAndUnitTypes.append(temp)
            
            
    
    QuantityAndUnitTypesAtt = ('CarrierId varchar(100)', 'CarrierDescription varchar(100)', 'type varchar(100)')
    if(QuantityAndUnitTypes != []): 
        for d in dir(QuantityAndUnitTypes[0]):
            QuantityAndUnitTypesAtt += (d + ' varchar(100)',)
        SetofAttributes.append(QuantityAndUnitTypesAtt)
        SetofTables.append('QuantityAndUnitTypes')
        SetofValues.append(valQuantityAndUnitTypes)
        
#     GenericProfiles = esh.get_all_instances_of_type(esdl.GenericProfile)
#     valGenericProfiles = [(p.profileType, 
#                            p.profileQuantityAndUnit,
#                            p.name,
#                            p.interpolationMethod,
#                            p.dataSource,
#                            p.setProfile,
#                            p.id,
#                            p.getProfile)
#                            for p in GenericProfiles]              
#     SetofAttributes.append(('profileType varchar(100)',
#                           'profileQuantityAndUnit varchar(100)',
#                           'name varchar(100)',
#                           'interpolationMethod varchar(100)',
#                           'dataSource varchar(100)',
#                           'setProfile varchar(100)',
#                           'id varchar(100) Primary Key',
#                           'getProfile varchar(100)'))
#     SetofTables.append('GenericProfiles')
#     SetofValues.append(valGenericProfiles)
    
#     SingleValues = esh.get_all_instances_of_type(esdl.SingleValue)
#     valSingleValues = [(p.id, p.value) for p in SingleValues]
#     SetofAttributes.append(('id varchar(100) Primary Key', 'value varchar(100)'))
#     SetofTables.append('SingleValues')
#     SetofValues.append(valSingleValues)
    
    

    create_AIMMS_sql(DB,SetofTables,SetofAttributes)
    
#   for loop that writes the tuple of values to the new database in the corresponding table.
    for a in range(len(SetofTables)):
        print('Exporting:',SetofTables[a])
        write_table_to_Sql(DB, SetofTables[a], SetofValues[a])
    conn.commit()
    conn.close()


# ### Main function that loads an Loads an ESDL file and restructures the data such that the function above can write everything in a newly created SQL Database. The restructuring gets set in SetofTables, SetofAttributes    SetofValues. With SetofTables a list, SetofAttributes a list of tuples and SetofValues a list of a list of tuples.

# In[7]:


import sys

conn = pymysql.connect(
    host= Host,
    user=User,
    password=PW)
cursor = conn.cursor()

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def Check_dir(my_class):
    Attributes = [dir(n) for n in my_class]
    AllAttributes = set(sum(Attributes, []))
    return AllAttributes

if __name__ == "__main__" :
    #The next set contains all the ESDL classes that have been included in the last main function
    ThingsInESDL = get_sql("Select table_schema as database_name, table_name from information_schema.tables where table_type = 'BASE TABLE'and table_schema = '" + DB + "' order by database_name, table_name;").table_name
    for i in ThingsInESDL:
        print(i)
        dirThing = Check_dir(str_to_class(i))
        print(i, ': ')
        for j in dirThing:
            print('   ',j)
    
conn.close()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Space for AIMMS Rest API
# 

# In[ ]:





# # Class that reads the SQL back in. Used to check if the data is ordered correctly and edits the ESDL

# In[8]:


conn = pymysql.connect(
    host= Host,
    user=User,
    password=PW)
cursor = conn.cursor()

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
    conn.close()


# In[9]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 
