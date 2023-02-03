from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from base.models import Parishe,Countie,Address
from .serializers import ParishSerializer,CountySerializer,AddressSerializer
import jellyfish
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from difflib import SequenceMatcher 
import json
from operator import itemgetter
import pandas as pd
from .utils import *
from .address_analysis import *
from .cleanser import *
from Levenshtein import distance
import distance
from multiprocessing import Pool


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        #encrypts user data in token from database
        token['email'] = user.email
        token['first_name']=user.first_name
        token['last_name']=user.last_name
       
        
        # ...

        return token

#extends serializer class
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def testRoute(request):
    routes=['hi']
    return Response(routes)

@api_view(['GET'])
def getParishes(request):
    Parishes=Parishe.objects.all()
    serializer=ParishSerializer(Parishes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCounties(request):
    counties=Countie.objects.all()
    serializer=CountySerializer(counties,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def cleanse(request):
    req_info=request.data
    print(req_info)
    location=addressFinder(req_info)
    return Response(location)

@api_view(['POST'])
def upload(request):
    file=request.FILES['file']
    data=pd.read_csv(file)
    addresses=createArrayDictsForDb(data)
    for i in addresses:
        newAddress=Address(address=i['address'],post_code=i['post_code'],
        latitude=i['latitude'],longitude=i['longitude'],parish=i['parish'],dev_area=i['dev_area'],source=i['source_1'], category=i['category']
        )
        newAddress.save()
    return Response("Success")

@api_view(['GET','POST'])
def getPoints(request):
    all_addresses=Address.objects.all()
    serializer=AddressSerializer(all_addresses,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def reverseGeocode(request):
    geodata=request.data
    lat=geodata['lat']
    lng=geodata['lng']
    print(lng,lat)
    address=Address.objects.filter(latitude=lat,longitude=lng)
    serializer=AddressSerializer(address,many=True)
    return Response(serializer.data)

@api_view(['POST'])   
def cleanseUpload(request):
    file=request.FILES['file']
    data=pd.read_excel(file) 
    data = data.replace({'JM': 'Jamaica'}, regex=True)
    data = data.replace({' RD': ' Road'}, regex=True)
    data = data.replace({' MT': 'Mount'}, regex=True)
    data = data.replace({'Jm': 'Jamaica'}, regex=True)
    data = data.replace({'KNG': 'Kingston'}, regex=True)
    data = data.replace({'KGN': 'Kingston'}, regex=True)
    data = data.drop_duplicates(subset=['ADDRESS1', 'ADDRESS2'])
    data = data.apply(lambda x: x.str.strip())

    print("HERE")
    
    addresses=modifiedDicts(data)
    
    addressescleansed=list(map(addressFinder,addresses))
    #with Pool() as pool:
    #    processed_data_iterator = pool.imap(addressFinder,addresses)

    # Convert the iterator to a list
    #processed_data_list = list(processed_data_iterator)
    #print(addressescleansed)
   
    #excel=convert_to_dataframe(addressescleansed,'file.csv')
    jsonSheet=json.dumps(addressescleansed)
    df_json = pd.read_json(jsonSheet)
    df_json.to_excel("cleanseSheet3.xlsx")
    

    return Response(addressescleansed)




