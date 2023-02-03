import pandas as pd
from .utils import *
from .address_analysis import *
from .cleanser import *
def createArrayDictsForDb(data):
  rows = data.to_dict()
  sheetIndexes = [i for i in rows['ADDRESS']]
  Projects =[{
    'index': i,
    'category': rows['CATEGORY'][i],
    'address':rows['ADDRESS'][i],
    'settlement':rows['SETTLEMENT'][i],
    'comm_pioj': rows['COMM_PIOJ'][i],
    'comm_sdc': rows['COMM_SDC'][i],
    'post_code': rows['POST_CODE'][i],
    'parish': rows['PARISH'][i],
    'latitude': rows['LATITUDE'][i],
    'longitude': rows['LONGITUDE'][i],
    'id': rows['ID'][i],
    'dev_area': rows['DEV_AREA'][i],
    'source_1': rows['SOURCE'][i],
    'name':rows['NAME'][i]
    } for i in sheetIndexes]
  return Projects

def modifiedDicts(data):
  rows=data.to_dict()
  sheetIndexes=[i for i in rows['ADDRESS1']]
  badProjects=[{
    'address1':str(rows['ADDRESS1'][i]),
    'address2':str(rows['ADDRESS2'][i]),
    'city':str(rows['CITY'][i]),
    'state':str(rows['STATE'][i]),
    # 'comm_pioj': rows['COMM_PIOJ'][i],
    # 'comm_sdc': rows['COMM_SDC'][i],
    # 'parish': rows['PARISH'][i],
    # 'dev_area': rows['DEV_AREA'][i],
    'postalcode':str(rows['POSTAL_CODE'][i]),
    # 'dev_area': rows['DEV_AREA'][i],
  } for i in sheetIndexes]
  return badProjects

  
def convert_to_dataframe(newsheetdata, sheetname):
  dataframe = {
    # "ID":[i['id'] for i in newsheetdata],
    # "ID":[i['id'] for i in newsheetdata],
    "ADDRESS1":[i['address1'] for i in newsheetdata],
    "ADDRESS2":[i['address2'] for i in newsheetdata],
    "CONFIDENCE": [i['confidence'] for i in newsheetdata],
    "NEW ADDRESS1":[i['address1 after cleanse'] for i in newsheetdata],
    # "PARISH": [i['parish'] for i in newsheetdata],
    "LONGITUDE":[i['longitude'] for i in newsheetdata],
    "LATITUDE":[i['latitude'] for i in newsheetdata],
    # "DEV_AREA":[i['dev_area'] for i in newsheetdata],
    # "COUNTRY":[i['dev_area'] for i in newsheetdata],
    # "POST CODE":[i['post_code'] for i in newsheetdata]
  }
  #"COMM_PIOJ": [i['comm_pioj'] for i in newsheetdata],
  #"DEV_AREA":[i['dev_area'] for i in newsheetdata],
  #"COUNTRY":[i['country'] for i in newsheetdata],
  #"COMM_SDC": [i['comm_sdc'] for i in newsheetdata],
  newdataframe = pd.DataFrame.from_dict(dataframe)
  newdataframe.to_csv(sheetname, index=False)
  return newdataframe
def concurrentcleanse(file):
  with concurrent.futures.ProcessPoolExecutor() as executor:
      results = executor.map(addressFinder,file)
      return list(results)