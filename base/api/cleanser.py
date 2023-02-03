import pandas as pd
import requests
import numpy
from datetime import datetime
import re
import os
import shutil
import concurrent.futures
import json
from numpyencoder import NumpyEncoder


'''
def convert_to_dataframe(newsheetdata, sheetname):
  dataframe = {
    "ADDRESS1": numpy.array([i['address1'] for i in newsheetdata]),
    "ADDRESS2": numpy.array([i['address2'] for i in newsheetdata]),
    "CITY": numpy.array([i['city'] for i in newsheetdata]),
    "STATE": numpy.array([i['state'] for i in newsheetdata]),
    "COUNTRY": numpy.array([i['country'] for i in newsheetdata]),
    "CONFIDENCE": numpy.array([i['confidence'] for i in newsheetdata]),
    "LONGITUDE": numpy.array([i['longitude'] for i in newsheetdata]),
    "LATITUDE": numpy.array([i['latitude'] for i in newsheetdata]),
  }
  newdataframe = pd.DataFrame.from_dict(dataframe)
  newdataframe.to_csv(sheetname, index=False)
  shutil.move(f'{sheetname}', f'Cleanser files/{sheetname}')
  return newdataframe
'''


def makeaddress(address):
  broken_characters = [',', '.']
  searchaddress = ''
  dividing_character = ' '
  if type(address['address1']) != float:
    if address['address1'] not in broken_characters:
      searchaddress += str(address['address1'])
  if type(address['address2']) != float:
    searchaddress += dividing_character
    if address['address2'] not in broken_characters:
      searchaddress += str(address['address2'])
  if type(address['city']) != float:
    searchaddress += dividing_character
    if address['city'] not in broken_characters:
      searchaddress += str(address['city'])
  if type(address['state']) != float:
    searchaddress += dividing_character
    if address['state'] not in broken_characters:
      searchaddress += str(address['state'])
  if type(address['country']) != float:
    searchaddress += dividing_character
    if address['country'] not in broken_characters:
      searchaddress += str(address['country'])
    searchaddress += dividing_character

  return re.sub(' +', ' ', searchaddress.replace("nan", " ").strip())


def makeaddress2(address):
  address_array = [str(address[i]) for i in address if i != 'index']
  newaddress = ''.join(address_array)
  newaddress = re.sub(' +', ' ', newaddress.replace("nan", " "))
  print(newaddress)


def createArrayDicts(data):
  rows = data.to_dict()
  sheetIndexes = numpy.array([i for i in rows['ADDRESS1']])
  addresses_for_cleansing = [{
    'index': rows[i],
    'address1': rows['ADDRESS1'][i],
    'address2': rows['ADDRESS2'][i],
    'city': rows['CITY'][i],
    'state': rows['STATE'][i],
    'country': rows['COUNTRY'][i]
  } for i in sheetIndexes]
  return numpy.array(addresses_for_cleansing)


def stringify_address(address):
  not_to_be_stringed = ['confidence', 'latitude', 'longitude', 'index']
  for i in address:
    if i not in not_to_be_stringed:
      address[i] = str(address[i])
  return address


def cleanseAddress(address):
  Valid = False
  address_for_search = makeaddress(address)
  try:
    url = f"https://api.geoapify.com/v1/geocode/search?text={address_for_search}&apiKey=d548c5ed24604be6a9dd0d989631f783"
    response = s.get(url)
    result = response.json()
    address['confidence'] = result['features'][0]['properties']['rank'][
      'confidence']
    address['longitude'] = result['features'][0]['properties']['lon']
    address['latitude'] = result['features'][0]['properties']['lat']
    address['type'] = 'geocoded'
    print(
      f" index: {address['index']}\n address1: {address['address1']}\n address2: {address['address2']}\n city: {address['city']}\n state: {address['state']}\n country:{address['country']}\n confidence:{result['features'][0]['properties']['rank']['confidence']}\n longitude:{result['features'][0]['properties']['lon']}\n latitude:{result['features'][0]['properties']['lat']} \n valid:{Valid}\n full-address:{address_for_search} \n\n"
    )

  except:
    address['type'] = 'notgeocodeable'
    address['latitude'] = 'unknown'
    address['longitude'] = 'unknown'
    address['confidence'] = 0
  return stringify_address(address)


def makeAddressSubArray(listofobjects, batch_num):
  arr = []
  numlens = len(listofobjects)
  print(numlens)
  tracker = 0
  while numlens >= 1:
    if numlens >= batch_num:
      numlens = numlens - batch_num
      arr.append((tracker, tracker + batch_num))
      tracker += batch_num
    else:
      arr.append((tracker, tracker + numlens))
      break
  return arr


def cleanseInBatch(batches, address_array):
  start_time = datetime.now().strftime("%H:%M:%S")
  for batch in batches:
    newbatch = [address_array[x] for x in range(batch[0], batch[1])]
    with concurrent.futures.ProcessPoolExecutor() as executor:
      results = executor.map(cleanseAddress, newbatch)
      for result in results:
        if result['type'] == 'high confidence':
          correct_confident.append(result)
        if result['type'] == 'low confidence':
          invalid_confident.append(result)
        all_addresses.append(result)
  print(
    f' StartTime:{start_time} \n EndTime:{datetime.now().strftime("%H:%M:%S")}'
  )


def cleanse_concurrent(data):
  with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(cleanseAddress, data)
    return numpy.array(list(results))


def cleanse_map(data):
  return list(map(cleanseAddress, data))


def namCheck(address):
  address = makeaddress(makeaddress)
  if 'MR' in address or 'mr' in address:
    return True
  if 'Ms' in address or 'ms' in address:
    return True
  if 'Mrs' in address or 'MRS' in address:
    return True
  return False


def badAddress():
  start_time = datetime.now()
  end_time,invalid_confident,all_addresses,correct_confident,successful=0,[],[],[],[]
  s = requests.Session()
  api_key = '13b97bd698ff441fb3e6bf8746f3c2a6'
  print("Cleaning Data...")
  data = pd.read_csv('testdata (1).csv')
  data = data.replace({'JM': 'Jamaica'}, regex=True)
  data = data.replace({' RD': ' Road'}, regex=True)
  data = data.replace({' MT': 'Mount'}, regex=True)
  data = data.replace({'Jm': 'Jamaica'}, regex=True)
  data = data.replace({'KNG': 'Kingston'}, regex=True)
  data = data.replace({'KGN': 'Kingston'}, regex=True)
  
  data = data.drop_duplicates(subset=['ADDRESS1', 'ADDRESS2'])
  data = data.apply(lambda x: x.str.strip())

  print('Formatting Data...')
  formatted_addresses = createArrayDicts(data)

  print('Cleansing...')

  all_addresses = cleanse_concurrent(formatted_addresses)


  print('Reformatting Data...')
  #all_addresses=numpy.array([i for i in all_addresses if type(i)==dict])
  failed = numpy.array(
    [i for i in all_addresses if i['type'] == 'notgeocodeable'])
  successful = numpy.array(
    [i for i in all_addresses if i['type'] == 'geocoded'])
  correct_confident = numpy.array(
    [i for i in successful if i['confidence'] >= 0.5])
  invalid_confident = numpy.array(
    [i for i in successful if i['confidence'] < 0.5])
  if os.path.isdir('Cleanser files') == False:
    os.makedirs('Cleanser files')
  print('Making new sheets...')
  convert_to_dataframe(correct_confident, 'cleansed.csv')
  convert_to_dataframe(invalid_confident, 'failed.csv')
  convert_to_dataframe(all_addresses, 'all addresses.csv')
  convert_to_dataframe(failed, 'notgeocodable.csv')
  print("DONE")
  end_time = datetime.now()
  duration = end_time - start_time
  print("\nCLEANSE STATISTICS")
  print(f"Addresses:{len(all_addresses)}")
  print(f"Duration:{duration}")
  print(f'Cleansed (>=50%):{len(correct_confident)}')
  print(f'Failed (<50%):{len(invalid_confident)}')
  print(f'Notgeocodeable:{len(failed)}')
  #print(f'nameErrors: {len(names)}')
