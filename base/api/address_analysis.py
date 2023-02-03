from base.models import Parishe,Countie,Address
from .serializers import ParishSerializer,CountySerializer,AddressSerializer
from operator import itemgetter
from django.contrib.postgres.search import SearchQuery,SearchVector
import json
from difflib import SequenceMatcher 
from django.db.models import Q
from Levenshtein import distance
import jellyfish
import distance
import concurrent.futures
import requests
import difflib
import re
from collections import Counter
from django.contrib.postgres.search import TrigramSimilarity;
from django.contrib.postgres.search import TrigramDistance;
from django.db.models.functions import Greatest
from django.db.models.functions import Least
from django.db.models import Min
from django.db.models import Aggregate
from functools import reduce
from builtins import min

#from django.db.models.functions import Avg
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
s = requests.Session()
api_key = '13b97bd698ff441fb3e6bf8746f3c2a6'
addresstest={
  
}
def shared_chars(s1, s2):
    return sum((Counter(s1) & Counter(s2)).values())
def makeaddress(address):
  broken_characters = [',', '.']
  searchaddress = ''
  dividing_character = ' '
  if type(address['address1']) != float:
    if address['address1'] not in broken_characters:
      searchaddress += str(address['address1'])
  if 'address2' in address:
    if type(address['address2']) != float:
      searchaddress += dividing_character
      if address['address2'] not in broken_characters:
        searchaddress += str(address['address2'])
  if 'city' in address:
    if type(address['city']) != float:
      searchaddress += dividing_character
      if address['city'] not in broken_characters:
        searchaddress += str(address['city'])
  if 'state' in address:
    if type(address['state']) != float:
      searchaddress += dividing_character
      if address['state'] not in broken_characters:
        searchaddress += str(address['state'])
  searchaddress += dividing_character
  searchaddress += str("Jamaica")
  searchaddress += dividing_character

  return re.sub(' +', ' ', searchaddress.replace("nan", " ").strip())

def addressSetup(address,tempAddress):
   addressfound={
          'address1 after cleanse':tempAddress['address'],
          'address2 after cleanse':tempAddress['comm_sdc'],
          'city after cleanse':tempAddress['dev_area'],
          'state after cleanse':tempAddress['parish'],
          'confidence':tempAddress['similarity']*100,
          'latitude':tempAddress['latitude'],
          'longitude':tempAddress['longitude']
        }
   if 'address1' in address:
     addressfound['address1']=address['address1']
   else:
     addressfound['address1']=' '
   if 'address2' in address:
     addressfound['address2']=address['address2']
   else:
     addressfound['address2']=' '
   if 'city' in address:
     addressfound['city']=address['city']
   else:
     addressfound['city']=' '
   if 'state' in address:
     addressfound['state']=address['state']
   else:
     addressfound['state']=' '
   addressfound['type']="MGI Cleanse"
   return addressfound
 
def cleanseAddress(address):
  addressdata=address

  Valid = False
  address_for_search=makeaddress(address)
  
  try:
    url = f"https://api.geoapify.com/v1/geocode/search?text={address_for_search}&apiKey=d548c5ed24604be6a9dd0d989631f783"
    response = s.get(url)
    result = response.json()
    addressdata['confidence'] = result['features'][0]['properties']['rank'][
      'confidence']
    addressdata['longitude'] = result['features'][0]['properties']['lon']
    addressdata['latitude'] = result['features'][0]['properties']['lat']
    addressdata['type'] = 'geocoded'
    
    if 'address1' in addressdata:
      addressdata['address1 after cleanse']=addressdata['address1']
    else:
       addressdata['address1']=' '
       addressdata['address1 after cleanse']=addressdata['address1']
       
    if 'address2' in addressdata:
      addressdata['address2 after cleanse']=addressdata['address2']
    else:
      addressdata['address2']=' '
      addressdata['address2 after cleanse']=addressdata['address2']
      
    if 'city' in addressdata:
      addressdata['city after cleanse']=addressdata['city']
    else:
      addressdata['city']=' '
      addressdata['city after cleanse']=addressdata['city']
      
    if 'state' in addressdata:
      addressdata['state after cleanse']=addressdata['city']
    else:
      addressdata['state']=' '
      addressdata['state after cleanse']=addressdata['state']
      
  except:
    if 'address1' in addressdata:
      addressdata['address1 after cleanse']=addressdata['address1']
    else:
       addressdata['address1']=' '
       addressdata['address1 after cleanse']=addressdata['address1']
       
    if 'address2' in addressdata:
      addressdata['address2 after cleanse']=addressdata['address2']
    else:
      addressdata['address2']=' '
      addressdata['address2 after cleanse']=addressdata['address2']
      
    if 'city' in addressdata:
      addressdata['city after cleanse']=addressdata['city']
    else:
      addressdata['city']=' '
      addressdata['city after cleanse']=addressdata['city']
      
    if 'state' in addressdata:
      addressdata['state after cleanse']=addressdata['city']
    else:
      addressdata['state']=' '
      addressdata['state after cleanse']=addressdata['state']
     
    addressdata['type'] = 'notgeocodeable'
    addressdata['latitude'] = 'unknown'
    addressdata['longitude'] = 'unknown'
    addressdata['confidence'] = 0
    
  return addressdata

def findAddressNum(address1):
  num=''
  digifound=True
  if type(address1)==str:
    for i in address1:
      if i.isdigit():
        num+=str(i)
      elif digifound and i==' ':
        break
    if num!='':
      return num
  return False
    

  
def addressFinder(address):
  addressNumber=findAddressNum(address['address1'].strip())
  q_objects=Q()  
  
  if 'address1' in address:
    if address['address1']=='nan':
          if 'address2' in address and address['address2']!='nan':
            address['address1'],address['address2']=address['address2'],address['address1']
            addressNumber=findAddressNum(address['address1'].strip())         
    addressNoNumbers= ''.join([i for i in address['address1'] if not i.isdigit()]).strip()
    q_objects.add(Q(address__trigram_similar=str(addressNoNumbers)),Q.OR)
    q_objects.add(Q(name__trigram_similar=str(addressNoNumbers)),Q.OR)
    #q_objects.add(Q(comm_sdc__trigram_similar=str(address['address1'])),Q.OR)
  
  if 'address2' in address:
    if address['address2']!='nan' and address['address2']!='.' :
      q_objects.add(Q(comm_sdc__trigram_similar=str(address['address2'])),Q.OR)
    
    
  if 'state' in address:
    Parishes = [
      'Kingston', 'Clarendon', 'St. Andrew', 'St.James', 'Westmoreland',
      'St.Elizabeth', 'Trelawny', 'St.Ann', 'Portland', 'St.Mary', 'St.Thomas',
      'Manchester','St.Catherine','Hanover'
      ]
  
    parish=difflib.get_close_matches(address['state'].strip(), Parishes)
    print("parish post-correct :",parish)
    if parish!=[]:
      address['state']= parish[0]
      q_objects.add(Q(parish__trigram_similar=address['state']),Q.AND)
   
  q_objects.add(Q(similarity__gte=0.5),Q.AND)
  q_objects.add(Q(distance__lte=0.5),Q.AND)
  
  if addressNumber!=False:
    q_objects.add(Q(address__icontains=addressNumber),Q.AND)
  
  
  print(q_objects)
  if 'address1' in address:
    similarity_measure=Greatest(TrigramSimilarity('address', address['address1']),TrigramSimilarity('name', address['address1']))
    distance_measure=Least(TrigramDistance('address', address['address1']),TrigramDistance('name', address['address1']))
    
  results=Address.objects.annotate(similarity=similarity_measure,distance=distance_measure).prefetch_related('address','name').filter(q_objects).order_by('-similarity').values('address','parish','name','dev_area','comm_sdc','latitude','longitude','distance','similarity')[:10]

  if results==[]:
    return cleanseAddress(address)
  elif results!=[]:
      try:
          return addressSetup(address,results[0])
      except:
         return cleanseAddress(address)
   
 
  print("Number of matches: ", len(results))
  print("Top half of matches: ",len(results)//2)
  #return all_addresses
  def assignScores(single_address):
    prioritiies=['address','name']
    lev_arr=[]
    ham_arr=[]
    seq_arr=[]
    shared_arr=[]
    match_arr=[]
    for i in prioritiies:
      if single_address[i] is not None:
        seq=SequenceMatcher(None, address['address1'].upper(), single_address[i].upper()).ratio()
        lev=jellyfish.levenshtein_distance(address['address1'].upper(),single_address[i].upper())
        ham=jellyfish.hamming_distance(address['address1'].upper(),single_address[i].upper())
        matchbool=jellyfish.match_rating_comparison(address['address1'],single_address[i])
        #shared=shared_chars(address['address1'],single_address[i])
        lev_arr.append(lev)
        seq_arr.append(seq)
        ham_arr.append(ham)
        match_arr.append(matchbool)
        #shared_arr.append(shared)
    single_address['confidence']=max(seq_arr)*100
    single_address['ham']=min(ham_arr)
    single_address['lev']=min(lev_arr)
    #single_address['shared']=max(shared_arr)
    
    if True in match_arr:
      single_address['match-rating']=True
    else:
      single_address['match-rating']=False
    return single_address
  
  scoresAssigned=[assignScores(i) for i in results]
   
  scoresAssignedSorted=sorted([i for i in scoresAssigned if i['match-rating']==True], key=itemgetter('ham'))
  #print(addressSetup(address,scoresAssignedSorted[-1]))
  if scoresAssigned==[]:
    return scoresAssigned[0]
  print("About to end")
  
  return scoresAssignedSorted
#addressSetup(address,scoresAssignedSorted[0])


#

  '''
    addressNumber=findAddressNum(address['address1'])
    searchoptions={
      
    }
    if addressNumber==False:
      if 'name' in address:
        searchoptions['name__trigram_similar']=address['address1']
        if 'address1' in address:
          address['address1'],address['name']=address['name'],address['address1']
      
    else:
      if 'address1' in address:
        if address['address1']=='nan':
          if 'address2' in address and address['address2']!='nan':
            address['address1'],address['address2']=address['address2'],address['address1']
            print("DID SWAPP")
      
      searchoptions['address__trigram_word_similar']=re.sub(' +', ' ',address['address1'].strip())

    if 'state' in address:
      Parishes = [
      'Kingston', 'Clarendon', 'St. Andrew', 'St.James', 'Westmoreland',
      'St.Elizabeth', 'Trelawny', 'St.Ann', 'Portland', 'St.Mary', 'St.Thomas',
      'Manchester','St.Catherine','Hanover'
      ]
  
      parish=difflib.get_close_matches(address['state'].strip(), Parishes)
      print("parish post-correct :",parish)
      if parish!=[]:
        address['state']= parish[0]
        searchoptions['parish__trigram_similar']=address['state']
   
    #if 'city' in address and len(address['city'])>5:
     # searchoptions['dev_area__trigram_similar']=address['city'].strip()
      

      
    all_addresses=[]
    print(searchoptions)
    
    if all_addresses==[]:
        all_addresses=Address.objects.filter(**searchoptions)
       
    address_serializer=AddressSerializer(all_addresses,many=True)   
    all_addresses=json.loads(json.dumps(address_serializer.data))
    
    print('Matches found :',len(all_addresses))
    #print(all_addresses)
    
      
    if all_addresses==[]:
      return cleanseAddress(address) 
    
   
    
    def compare(single_address):
      if re.search(r'\bRd\b', address['address1'], re.I):
        re.sub('\bRd\b?', ' ',address['address1']).strip()
      seq=SequenceMatcher(None, address['address1'].upper(), single_address['address'].upper()).ratio()
      lev=jellyfish.levenshtein_distance(address['address1'].upper(),single_address['address'].upper())
      ham=jellyfish.hamming_distance(address['address1'].upper(),single_address['address'].upper())
      single_address['confidence']=round(seq*100,1)
      single_address['seq']=round(seq,1)
      single_address['ham']=round(ham,1)
      single_address['lev']=round(lev,1)
      single_address['shared']=shared_chars(address['address1'],single_address['address'])
      single_address['match-rating']=jellyfish.match_rating_comparison(address['address1'],single_address['address'])
      return single_address

 
    percent_and_adddress=list(map(compare,all_addresses))
    #print(percent_and_adddress)
    print('Address Number',addressNumber)
    
    if len(percent_and_adddress)<=2:
      topPossible=sorted(percent_and_adddress, key=itemgetter('confidence'))
      return topPossible[-1]
      
      
    
    if addressNumber:
      percent_and_adddress=[i for i in percent_and_adddress if addressNumber in i['address']]
      print("Addresses found with number: ",len(percent_and_adddress))
     
      if percent_and_adddress!=[]:
        addressNumberMatches=sorted(percent_and_adddress, key=itemgetter('seq'))
        
        if addressNumberMatches[-1]['seq']>=0.6 and addressNumberMatches[-1]['match-rating']==True:
          tempAddress=addressNumberMatches[-1]
          addressfound={
          'address1 after cleanse':tempAddress['address'],
          'address2 after cleanse':tempAddress['comm_sdc'],
          'city after cleanse':tempAddress['dev_area'],
          'state after cleanse':tempAddress['parish'],
          'confidence':tempAddress['confidence'],
          'latitude':tempAddress['latitude'],
          'longitude':tempAddress['longitude']
        }
          if 'address1' in address:
            addressfound['address1']=address['address1']
          else:
            addressfound['address1']=' '
          if 'address2' in address:
            addressfound['address2']=address['address2']
          else:
            addressfound['address2']=' '
          if 'city' in address:
            addressfound['city']=address['city']
          else:
            addressfound['city']=' '
          if 'state' in address:
            addressfound['state']=address['state']
          else:
            addressfound['state']=' '
          return addressfound
    
    halffull=len(percent_and_adddress)//2
    hamlist=sorted(percent_and_adddress, key=itemgetter('ham'))
    topham=[hamlist[i] for i in range (0,halffull)]
    
    halfham=len(topham)//2
    levlist = sorted(topham, key=itemgetter('lev'))
    toplev=[levlist[i] for i in range (0,halfham)]
    
    topmatches=[i for i in toplev if i['match-rating']==True]
    print("after matches :",len(topmatches))
    
    topseq=sorted(topmatches, key=itemgetter('seq'))
    
    topCharcount=sorted(topmatches, key=itemgetter('shared'))
    print("after filtering out :",len(topseq))
    if topCharcount==[]:
      return cleanseAddress(address) 
    

        
    if topCharcount!=[]:
      if topCharcount[-1]['seq']<0.4:
        return cleanseAddress(address)  
      else:
        tempAddress=topCharcount[-1]
        
        addressfound={
          'address1 after cleanse':tempAddress['address'],
          'address2 after cleanse':tempAddress['comm_sdc'],
          'city after cleanse':tempAddress['dev_area'],
          'state after cleanse':tempAddress['parish'],
          'confidence':tempAddress['confidence'],
          'latitude':tempAddress['latitude'],
          'longitude':tempAddress['longitude']
        }
        if 'address1' in address:
          addressfound['address1']=address['address1']
        else:
          addressfound['address1']=' '
        if 'address2' in address:
          addressfound['address2']=address['address2']
        else:
          addressfound['address2']=' '
        if 'city' in address:
          addressfound['city']=address['city']
        else:
          addressfound['city']=' '
        if 'state' in address:
          addressfound['state']=address['state']
        else:
          addressfound['state']=' '
        return addressfound
  
    else:
      address['latitude']=0
      address['longitude']=0
      address['confidence']=0
      
      if 'address1' in address:
        address['address1 after cleanse']=address['address1']
      else:
        address['address1']=' '
        address['address1 after cleanse']=address['address1']
        
      if 'address2' in address:
        address['address2 after cleanse']=address['address2']
      else:
        address['address2']=' '
        address['address2 after cleanse']=address['address2']
      
      if 'city' in address:
        address['city after cleanse']=address['city']
      else:
        address['city']=' '
        address['city after cleanse']=address['city']
        
      if 'state' in address:
        address['state after cleanse']=address['city']
      else:
        address['state']=' '
        address['state after cleanse']=address['state']
        
      return address
''' 
  




def convert_to_words(num):
    # Create a dictionary with the numbers from 0 to 19 and their corresponding words
    ones = {
        0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four',
        5 : 'five', 6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine',
        10 : 'ten', 11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
        15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen', 19 : 'nineteen'
    }
    # Create a dictionary with the tens as keys and their corresponding words as values
    tens = {
        2 : 'twenty', 3 : 'thirty', 4 : 'forty', 5 : 'fifty',
        6 : 'sixty', 7 : 'seventy', 8 : 'eighty', 9 : 'ninety'
    }

    # If the number is 0
    if num == 0:
        return ones[num]
    # If the number is between 1 and 19
    elif num > 0 and num < 20:
        return ones[num]
    # If the number is between 20 and 99
    elif num >= 20 and num < 100:
        return tens[num // 10] + ('' if num % 10 == 0 else ' ' + ones[num % 10])
    # If the number is greater than or equal to 100
    else:
        return "number is out of range"

