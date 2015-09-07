
# coding: utf-8

# In[ ]:

import requests
import pandas as pd
import sqlalchemy as sa
from pprint import pprint
import numpy as np
import time
import urllib
from skimage.io import imread

## buildReport Code needs refinement
def buildReport(property_id):
    if bool(property_id):
        fields = ["propertyIdPg","propertyName","latitude","longitude","regionCode","districtCode","fullAddress","videosCount","floorplansCount","facilityCodes","listingRentalCount","listingSaleCount","totalUnits","completedYear","description","tenureCode","tenureFullName","floors","virtualToursCount","photosCount","coverImage","coverImageThumbnail","galleryCoverImage"]
        stat_df = pd.DataFrame(columns=fields)
        for pgCondoID in property_id:
            link = "http://info-new.staging.guruestate.com/v1/properties/" + str(pgCondoID) + "?_format=json&region=my&lang=en&fields=all&pgDataSet=false"
            f = requests.get(link)
            data = f.json()
            row = []          
            for c in fields:
                try:
                    if bool(data[c]):
                        if c in ["coverImage","coverImageThumbnail","galleryCoverImage"] and bool(data[c]):
                            path = io.BytesIO(urllib.request.urlopen(data[c]).read())
                            im=Image.open(path)
                            width, height = im.size
                            img_data = data[c] + " ; Size : " + str(width) + " x "+ str(height)
                            row.append(img_data)
                            continue
                        row.append(data[c])
                    else:
                        row.append(None)
                except:
                    pass
            try:
                if bool(row):
                    df_temp = pd.DataFrame(row,fields)
                    df_temp = df_temp.transpose()
                    stat_df = stat_df.append(df_temp)
            except ValueError:
                print(row)
                print(c)
                row.append(0)
                df_temp = pd.DataFrame(row,fields)
                df_temp = df_temp.transpose()
                stat_df = stat_df.append(df_temp)
            if len(stat_df) % 1000 ==0:
                print(len(stat_df))
        return(stat_df)

def buildMYCondoReport(file_name):
    #Include .csv in the file name when the parameter is passed.
    engine = sa.create_engine("mysql://appuser:Powderful4ever!@hg-db1-integration.guruestate.com")
    db_list = engine.execute('SHOW databases')
    #print(db_list.fetchall())
    engine.execute('USE propertydb_my')
    property_list = engine.execute('SELECT id FROM propertydb_my.property')
    property_list = property_list.fetchall()
    condo_experts = engine.execute('SELECT property_id,count(agent_id) FROM propertydb_my.property_specialist WHERE property_id is not null and status_code="ACT" GROUP BY property_id;')
    condo_experts_list = pd.DataFrame(condo_experts.fetchall(),columns=['propertyIdPg','AgentNumCount'])
    db_list.close()
    
    property_id = [p[0] for p in property_list]
    
    x=buildReport(property_id)
    x["CondoSpl"]=0
    x=x.reset_index()
    
    intersection = list(set(x["propertyIdPg"]).intersection(set(condo_experts_list["propertyIdPg"])))
    for idx in intersection:
        x.loc[x[x["propertyIdPg"]==idx].index,'CondoSpl'] = condo_experts_list[condo_experts_list["propertyIdPg"]==idx].AgentNumCount.values
    
    y= x.copy()
    y["listingSaleCount"]=y["listingSaleCount"].astype(float)
    y = y.sort(["listingSaleCount"],ascending=False)
    y.to_csv(file_name,index=False)

