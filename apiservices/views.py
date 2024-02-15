from django.shortcuts import render
from datetime import datetime, date, time
from django.contrib.auth.decorators import login_required
import datetime
import uuid
from datetime import datetime, date, time
from django.utils import timezone
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers
from accounts.models import *
from coupon_management.models import *
from django.db.models import Q

#from .models import *
from django.utils import timezone
from django.contrib.auth import authenticate,login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password


######rest framwework section
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

import base64
from django.http import JsonResponse
from master.serializers import *
from master.models import *
from random import randint
from datetime import datetime as dt
from datetime import timedelta
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from accounts.models import *
from master.models import *
from product.models import *
from van_management.models import *
from customer_care.models import *

from master.serializers import *
from product.serializers import *
from van_management.serializers import *
from accounts.serializers import *
from .serializers import *
from client_management.serializers import VacationSerializer
from coupon_management.serializers import *


import random
import string
from django.core.mail import EmailMessage
import threading
import pytz
import datetime as datim
utc=pytz.UTC
import logging,traceback
from logging import *
from rest_framework.exceptions import (
 APIException,               #for api exception
 ValidationError
)
logger=logging.getLogger(__name__)

from datetime import timedelta



def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class Login_Api(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if username and password:
                print("username and password", username, password)
                user = authenticate(username=username, password=password)
                print(user,"user")
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user_obj = CustomUser.objects.filter(username=username).first()
                        token = generate_random_string(20)  # Adjust the token length as needed
                        data = {
                            'id': user_obj.id,
                            'username': username,
                            'user_type': user_obj.user_type,
                            'token': token
                        }
                        print(data, 'data')
                    else:
                        return Response({'status': False, 'message': 'User Inactive!'})
                    return Response({'status': True, 'data': data, 'message': 'Authenticated User!'})
                else:
                    return Response({'status': False, 'message': 'Unauthenticated User!'})
            else:
                return Response({'status': False, 'message': 'Unauthenticated User!'})
        except CustomUser.DoesNotExist:
            return Response({'status': False, 'message': 'User does not exist!'})
        except Exception as e:
            print(f'Something went wrong: {e}')
            return Response({'status': False, 'message': 'Something went wrong!'})

class RouteMaster_API(APIView):
    serializer_class = RouteMasterSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly] 
    # permission_classes = [IsAuthenticated]
    def get(self,request,id=None):
        try:
            if id :
                queryset=RouteMaster.objects.get(route_id=id)
                serializer=RouteMasterSerializers(queryset)
                return Response(serializer.data)
            queryset=RouteMaster.objects.all()
            serializer=RouteMasterSerializers(queryset,many=True)
            return Response(serializer.data)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def post(self,request):
        try:
            serializer=RouteMasterSerializers(data=request.data)
            if serializer.is_valid():
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                route_master=serializer.save(created_by=request.user.id,branch_id=branch)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id):
        try:
            route = RouteMaster.objects.get(route_id=id)
            serializer = RouteMasterSerializers(route, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = RouteMaster.objects.get(route_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RouteMaster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class LocationMaster_API(APIView):
    serializer_class = LocationMasterSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self,request,id=None):
        try:
            if id :
                queryset=LocationMaster.objects.get(location_id=id)
                serializer=LocationMasterSerializers(queryset)
                return Response(serializer.data)
            queryset=LocationMaster.objects.all()
            serializer=LocationMasterSerializers(queryset,many=True)
            return Response(serializer.data)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def post(self,request):
        try:
            serializer=LocationMasterSerializers(data=request.data)
            if serializer.is_valid():
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                serializer.save(created_by=request.user.id,branch_id=branch)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id):
        try:
            route = LocationMaster.objects.get(location_id=id)
            serializer = LocationMasterSerializers(route, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = LocationMaster.objects.get(location_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LocationMaster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DesignationMaster_API(APIView):
    serializer_class = DesignationMasterSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
   
    def get(self,request,id=None):
        if id :
            queryset=DesignationMaster.objects.get(designation_id=id)
            serializer=DesignationMasterSerializers(queryset)
            return Response(serializer.data)
        queryset=DesignationMaster.objects.all()
        serializer=DesignationMasterSerializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=DesignationMasterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.id)
            data = {'data': 'successfully added'}
            return Response(data,status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        route = DesignationMaster.objects.get(designation_id=id)
        serializer = DesignationMasterSerializers(route, data=request.data)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.id,modified_date = datetime.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = DesignationMaster.objects.get(designation_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LocationMaster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BranchMaster_API(APIView):
        serializer_class = BranchMasterSerializers
        # authentication_classes = [BasicAuthentication] 
        # permission_classes = [IsAuthenticated]
        
        def get(self,request,id=None):
            if id :
                queryset=BranchMaster.objects.get(branch_id=id)
                serializer=BranchMasterSerializers(queryset)
                return Response(serializer.data)
            queryset=BranchMaster.objects.all()
            serializer=BranchMasterSerializers(queryset,many=True)
            return Response(serializer.data)

        def post(self,request):
            serializer=BranchMasterSerializers(data=request.data)
            print(request.data['branch_id'],'branchid')
            if serializer.is_valid():

                saved_data=serializer.save()
                branch = BranchMaster.objects.get(branch_id=saved_data.branch_id)
                username=request.data["username"]
                password=request.data["password"]
                hashed_password=make_password(password)
                email=branch.email
                user_name=branch.name
                branch_data=CustomUser.objects.create(password=hashed_password,username=username,first_name=user_name,email=email,user_type='Branch User',branch_id=branch)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        def put(self, request, id):
            route = BranchMaster.objects.get(branch_id=id)
            serializer = BranchMasterSerializers(route, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, id):
            try:
                # Retrieve the object to be deleted 
                instance = BranchMaster.objects.get(branch_id=id)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except BranchMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)




class CategoryMaster_API(APIView):
    serializer_class = CategoryMasterSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self,request,id=None):
        if id :
            queryset=CategoryMaster.objects.get(category_id=id)
            serializer=CategoryMasterSerializers(queryset)
            return Response(serializer.data)
        queryset=CategoryMaster.objects.all()
        serializer=CategoryMasterSerializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=CategoryMasterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.id)
            data = {'data': 'successfully added'}
            return Response(data,status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        category = CategoryMaster.objects.get(category_id=id)
        serializer = CategoryMasterSerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.id,modified_date = datetime.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = CategoryMaster.objects.get(category_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryMaster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EmirateMaster_API(APIView):
    serializer_class = EmirateMasterSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self,request,id=None):
        try:
            if id :
                queryset=EmirateMaster.objects.get(emirate_id=id)
                serializer=EmirateMasterSerializers(queryset)
                return Response(serializer.data)
            queryset=EmirateMaster.objects.all()
            serializer=EmirateMasterSerializers(queryset,many=True)
            return Response(serializer.data)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def post(self,request):
        try:
            serializer=EmirateMasterSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user.id)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id):
        try:
            category = EmirateMaster.objects.get(emirate_id=id)
            serializer = EmirateMasterSerializers(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = EmirateMaster.objects.get(emirate_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmirateMaster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#########-------------------Product-------------------------############

class Product_API(APIView):
    serializer_class = ProductSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
     
    def get(self,request,id=None):
        try:
            if id :
                queryset=Product.objects.get(product_id=id)
                serializer=ProductSerializers(queryset)
                return Response(serializer.data)
            queryset=Product.objects.all()
            serializer=ProductSerializers(queryset,many=True)
            return Response(serializer.data)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def post(self,request):
        try:
            serializer=ProductSerializers(data=request.data)
            if serializer.is_valid():
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id) 
                serializer.save(created_by=request.user.id,branch_id=branch)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
    
    def put(self, request, id):
        try:
            product = Product.objects.get(product_id=id)
            serializer = ProductSerializers(product, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Product.objects.get(product_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class Product_Default_Price_API(APIView):
    serializer_class = Product_Default_Price_Level_Serializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self,request,id=None):
        if id :
            queryset=Product_Default_Price_Level.objects.get(def_price_id=id)
            serializer=Product_Default_Price_Level_Serializers(queryset)
            return Response(serializer.data)
        queryset=Product_Default_Price_Level.objects.all()
        serializer=Product_Default_Price_Level_Serializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=Product_Default_Price_Level_Serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'data': 'successfully added'}
            return Response(data,status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

     
    def put(self, request, id):
        product = Product_Default_Price_Level.objects.get(def_price_id=id)
        serializer = Product_Default_Price_Level_Serializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Product_Default_Price_Level.objects.get(def_price_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product_Default_Price_Level.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#############-------Van Mangement -------------------###############



class Van_API(APIView):
    serializer_class=VanSerializers
    # authentication_classes = [BasicAuthentication] 
    # permission_classes = [IsAuthenticated]
    
    def get(self,request,id=None):
        if id :
            queryset=Van.objects.get(van_id=id)
            serializer=VanSerializers(queryset)
            return Response(serializer.data)
        queryset=Van.objects.all()
        serializer=VanSerializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        username = request.headers['username']
        print(username,'username')
        serializer=VanSerializers(data=request.data)
        if serializer.is_valid():
            van_driver=Van.objects.filter(driver=request.data['driver']).first()
            van_sales=Van.objects.filter(salesman=request.data['salesman']).first()
            if van_driver :
                data={'data':"Driver is already assigned to van"}
                return Response(data,status=status.HTTP_200_OK)
            elif van_sales :   
                data={'data':"Salesman is already assigned to van"}
                return Response(data,status=status.HTTP_200_OK)
            else :
                user=CustomUser.objects.get(api_token=username)
                branch_id=user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id) 
                serializer.save(created_by=request.user.id,branch_id=branch)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

     
    def put(self, request, id):
        product = Van.objects.get(van_id=id)
        serializer = VanSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.id,modified_date = datetime.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Van.objects.get(van_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Van.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




class Route_Assign(APIView):
    serializer_class=VanRoutesSerializers
    # authentication_classes = [BasicAuthentication] 
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset = Van_Routes.objects.all()
        serializer = VanRoutesSerializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        username = request.headers['username']
        van_data = Van.objects.get(van_id = request.data['van'])
        serializer=VanRoutesSerializers(data=request.data)
        if serializer.is_valid():
            route_exists = Van_Routes.objects.filter(van = van_data,routes = request.data['routes']).exists()
            if route_exists:
                data = {'data':'Route is already assigned to this van'}
                return Response(data,status=status.HTTP_200_OK)
            else :
                user=CustomUser.objects.get(username=username)
                serializer.save(created_by=user.id)
                data = {'data':'Route is assigned'}
                return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Van_Routes.objects.get(van_route_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Van_Routes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class Licence_API(APIView):
    serializer_class=Van_LicenseSerializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):
        queryset = Van_License.objects.all()
        serializer = Van_LicenseSerializers(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        van_data = Van.objects.get(van_id = request.data['van'])
        serializer=Van_LicenseSerializers(data=request.data)
        if serializer.is_valid():
            licence_exists = Van_License.objects.filter(van = van_data,emirate = request.data['emirate']).exists()
            if licence_exists:
                data = {'data':'Licence is already assigned to this van from this emirate'}
                return Response(data,status=status.HTTP_200_OK)
            else :
                serializer.save(created_by=request.user.id)
                data = {'data':'Licence is created'}
                return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Van_License.objects.get(van_route_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Van_License.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


#  Trip Schedule       

def find_customers(request, def_date, route_id):
    date_str = def_date
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date.strftime('%A')
        week_num = (date.day - 1) // 7 + 1
        week_number = f'week{week_num}'
    route = RouteMaster.objects.get(route_id=route_id)

    todays_customers = []

    buildings = []
    for customer in Customers.objects.filter(routes = route):
        if customer.visit_schedule and day_of_week in customer.visit_schedule and week_number in customer.visit_schedule[day_of_week]:
            todays_customers.append(customer)
            if customer.building_name not in buildings:
                buildings.append(customer.building_name)

    
    # Customers on vacation
    date = datetime.strptime(def_date, '%Y-%m-%d').date()
    for vacation in Vacation.objects.all():
        if vacation.start_date <= date <= vacation.end_date:
            if vacation.customer in todays_customers:
                todays_customers.remove(vacation.customer)
    

    # Emergency customer
    special_customers = DiffBottlesModel.objects.filter(delivery_date = date)
    emergency_customers = []
    for client in special_customers:
        if client.customer in todays_customers:
            emergency_customers.append(client.customer)
        else:
            if client.customer.routes == route:
                todays_customers.append(client.customer)
                emergency_customers.append(client.customer)
                if client.customer.building_name not in buildings:
                    buildings.append(client.customer.building_name)

    

    building_count = {}
    for building in buildings:
        for customer in todays_customers:
            if customer.building_name == building:
                if building in building_count:
                    building_count[building] += customer.no_of_bottles_required
                else:
                    building_count[building] = customer.no_of_bottles_required
    sorted_building_count = dict(sorted(building_count.items(), key=lambda item: item[1]))

    trips = {}
    trip_count = 1
    current_trip_bottle_count = 0
    trip_buildings = []

    for building, bottle_count in sorted_building_count.items():
        if current_trip_bottle_count + bottle_count > 200:
            trip_buildings = [building]
            trips[f"Trip{trip_count+1}"] = trip_buildings
            current_trip_bottle_count = bottle_count
        else:
            trip_buildings.append(building)
            trips[f"Trip{trip_count}"] = trip_buildings
            current_trip_bottle_count += bottle_count
        
    # List to store trip-wise customer details
    trip_customers = []
    for trip in trips:
        for customer in todays_customers:
            if customer.building_name in trips[trip]:
                trip_customer = {
                    "customer_name" : customer.customer_name,
                    "trip":trip,
                    "building":customer.building_name,
                    "route" : customer.routes.route_name,
                    "no_of_bottles": customer.no_of_bottles_required,
                    "location" : customer.location.location_name,
                }
                if customer in emergency_customers:
                    trip_customer['type'] = 'Emergency'
                else:
                    trip_customer['type'] = 'Default'
                trip_customers.append(trip_customer)
    return trip_customers


class ScheduleView(APIView):
    def get(self, request, date_str):
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        routes = RouteMaster.objects.all()
        route_details = []
        for route in routes:
            trip_count = 0
            customer_count = 0
            bottle_count=0
            todays_customers = find_customers(request, date_str, route.route_id)
            trips=[]
            for customer in todays_customers:
                customer_count+=1
                bottle_count+=customer['no_of_bottles']
                if customer['trip'] not in trips:
                    trips.append(customer['trip'])
            route_details.append({
                'route_name':route.route_name,
                'route_id':route.route_id,
                'no_of_customers':customer_count,
                'no_of_bottles':bottle_count,
                'no_of_trips':len(trips),
                'trips': trips
            })
        return Response({'def_date': date_str, 'details': route_details}, status=status.HTTP_200_OK)


class ScheduleByRoute(APIView):
    def get(self, request, date_str, route_id, trip):
        route = RouteMaster.objects.get(route_id=route_id)
        todays_customers = find_customers(request, date_str, route_id)
        customers = [customer for customer in todays_customers if customer['trip'] == trip]
        return Response({
            'def_date': date_str,
            'route': {
                'route_id': route.route_id,
                'route_name': route.route_name,
                'trip' : trip
            },
            'todays_customers': customers,
        }, status=status.HTTP_200_OK)






####################################Account####################################


class UserSignUpView(APIView):
    
    serializer_class=CustomUserSerializers
    def get(self, request,id=None):
        if id :
            queryset=Customers.objects.get(customer_id=id)
            serializer=CustomersSerializers(queryset)
            return Response(serializer.data)
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializers(queryset,many=True)
        return Response({'data':serializer.data})

    def post(self, request, *args, **kwargs):
        serializer=CustomUserSerializers(data=request.data)
        if serializer.is_valid():
            
            passw = make_password(request.data['password'])
            serializer.save(password=passw)
            data = {'data':"Succesfully registerd"}
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data={'data':serializer.errors}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        product = CustomUser.objects.get(id=id)
        serializer = CustomUserSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.id,modified_date = datetime.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------Sign Up Api--------------------------------------#

class Customer_API(APIView):
    serializer_class = CustomersSerializers
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[BasicAuthentication]

    def get(self,request,id=None):
        try:
            if id :
                queryset=Customers.objects.get(customer_id=id)
                serializer=CustomersSerializers(queryset)
                return Response(serializer.data)
            queryset= Customers.objects.all()
            serializer= CustomersSerializers(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
    def post(self,request):
        try:
            serializer=CustomersSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username=request.data["mobile_no"]
                password=request.data["password"]
                hashed_password=make_password(password)
                if Customers.objects.filter(mobile_no=request.data["mobile_no"]).exists() :
                    data = {'data': 'Customer with this mobile number already exist !! Try another number'}
                    return Response(data,status=status.HTTP_201_CREATED)
                customer_data=CustomUser.objects.create(password=hashed_password,username=username,first_name=request.data['customer_name'],email=request.data['email_id'],user_type='Customer')
                data=serializer.save(user_id=customer_data.id)
                Staff_Day_of_Visit.objects.create(customer = data)
                data = {'data': 'successfully added'}
                return Response(data,status=status.HTTP_201_CREATED)
            return Response({'status': False,'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            user_exist = CustomUser.objects.filter(username=request.data['mobile_no']).exists()
            if user_exist:
                user_obj = CustomUser.objects.get(username=request.data['mobile_no'])
                user_obj.delete()
                return Response({"status": False, 'data': e, "message": "Something went wrong!"})
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})


    def put(self, request, id):
        try:
            product = Customers.objects.get(customer_id=id)
            serializer = CustomersSerializers(product, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
    

class Customer_Custody_Item_API(APIView):
    serializer_class = CustomerCustodyItemSerializers
    def get(self,request):
        customer = request.data['customer_id']
        custodyitems = Customer_Custody_Items.objects.filter(customer=customer).all()
        cus_list=list(custodyitems)
        customerser=CustomerCustodyItemSerializers(cus_list,many=True).data
        return JsonResponse({'customerser':customerser})


#############-------------- Coupon Management ----------------#########################

class CouponType_API(APIView):
    serializer_class = couponTypeserializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset = CouponType.objects.all()
        serializer = couponTypeserializers(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        couponType_data = CouponType.objects.filter(coupon_type_id = request.data['coupon_type_id'])
        for i in couponType_data:
            coupontypedata=i.coupon_type_id
        serializer=couponTypeserializers(data=request.data)
        if serializer.is_valid():
            coupon_Typess = CouponType.objects.filter(coupon_type_id = coupontypedata).exists()
            if coupon_Typess:
                data = {'data':'CouponType already created'}
                return Response(data,status=status.HTTP_200_OK)
            else :
                serializer.save(created_by=request.user.id)
                data = {'data':'Coupon Type created successfully!'}
                return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
            coupon_TYPE = CouponType.objects.get(coupon_type_id=id)
            serializer = couponTypeserializers(coupon_TYPE, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = CouponType.objects.get(coupon_type_id=id)
            instance.delete()
            data={"data":"successfully deleted"}
            return Response(data,status=status.HTTP_204_NO_CONTENT)
        except CouponType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Coupon_API(APIView):
    serializer_class = couponserializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset = Coupon.objects.all()
        serializer = couponserializers(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        coupon_data = Coupon.objects.filter(coupon_id = request.data['coupon_id'])
        for i in coupon_data:
            coupondata=i.coupon_id
        serializer=couponserializers(data=request.data)
        if serializer.is_valid():
            coupon= Coupon.objects.filter(coupon_id = coupondata).exists()
            if coupon:
                data = {'data':'Coupon already created'}
                return Response(data,status=status.HTTP_200_OK)
            else :
                serializer.save(created_by=request.user.id)
                data = {'data':'Coupon created successfully!'}
                return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        coupon = Coupon.objects.get(coupon_id=id)
        serializer = couponTypeserializers(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.id,modified_date = datetime.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            # Retrieve the object to be deleted 
            instance = Coupon.objects.get(coupon_id=id)
            instance.delete()
            data={"data":"successfully deleted"}

            return Response(data,status=status.HTTP_204_NO_CONTENT)
        except Coupon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class CouponRequest_API(APIView):
    serializer_class = couponRequestserializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]
    def get(self,request):
            queryset = CouponRequest.objects.all()
            serializer = couponRequestserializers(queryset,many=True)
            return Response(serializer.data)
    def post(self,request):
        print("HIIIIIIIIIIIIIIII",request.data)
        quantity = request.data.get('quantity')
        print("quantity",quantity)
        coupon_type_id = request.data.get('coupon_type_id')
        print("coupon_type_id",coupon_type_id)

        # Create a dictionary with the required data
        data = {
            'quantity': quantity,
            'coupon_type_id': coupon_type_id,
        }
        # Use the serializer to create a new CouponRequest instance
        serializer=couponRequestserializers(data=request.data)
        print("serializerDATAAAAAAAAAAAAA",serializer)
        if serializer.is_valid():
            # Check if a CouponRequest with the same quantity and coupon_type_id already exists
            coupon_request_exists = CouponRequest.objects.filter(quantity=quantity, coupon_type_id=coupon_type_id).exists()

            if coupon_request_exists:
                data = {'detail': 'CouponRequest already exists with the same quantity and coupon_type_id.'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Save the new CouponRequest
                serializer.save()
                data = {'detail': 'CouponRequest created successfully!'}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AssignStaffCoupon_API(APIView):
    serializer_class = assignStaffCouponserializers
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self,request):
            queryset = AssignStaffCoupon.objects.all()
            serializer = assignStaffCouponserializers(queryset,many=True)
            return Response(serializer.data)
    def post(self,request):

        alloted_quantity = int(request.data.get('alloted_quantity', 0))
        coupon_request=request.data.get('coupon_request')
        coupon_request_data = CouponRequest.objects.values('quantity').get(coupon_request_id=coupon_request)
        quantity = int(coupon_request_data['quantity'])
        remaining_quantity=quantity- alloted_quantity


        data ={
           "alloted_quantity":alloted_quantity ,
           "quantity":quantity,
           'remaining_quantity': int(coupon_request_data['quantity']) - int(request.data.get('alloted_quantity', 0)),
           'status': 'Pending' if remaining_quantity > 0 else 'Closed',
           'coupon_request':coupon_request,
           'created_by': str(request.user.id),
           'modified_by': str(request.user.id),
           'modified_date': datetime.now(),
           'created_date': datetime.now()

        }


        serializer=assignStaffCouponserializers(data=data)
        if serializer.is_valid():
            # Check if a CouponRequest with the same quantity and coupon_type_id already exists
            assignstaff = AssignStaffCoupon.objects.filter(alloted_quantity=alloted_quantity, coupon_request=coupon_request).exists()

            if assignstaff:
                data = {'detail': ' already exists '}
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Save the new CouponRequest
                serializer.save()
                data = {'detail': ' created successfully!'}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssigntoCustomer_API(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializers = assigncustomerCouponserializers
    def get(self,request):
            queryset = AssignStaffCouponDetails.objects.all()
            serializer = assigncustomerCouponserializers(queryset,many=True)
            return Response(serializer.data)
    def post(self,request):
        print("DATA",request.data)
        staff_coupon_assign=request.data.get('staff_coupon_assign')
        print("staff_coupon_assign",staff_coupon_assign)
        
        to_customer=request.data.get('to_customer')
        print("to_customer",to_customer)
        coupon=request.data.get('coupon')
        print("coupon",coupon)

        assign_staff_coupon_instance = AssignStaffCoupon.objects.get(assign_id=staff_coupon_assign)
        print("assign_staff_coupon_instance",assign_staff_coupon_instance)
        if to_customer:
            status_value = 'Assigned To Customer'
        else:
            if assign_staff_coupon_instance.status == 'Closed':
                status_value = 'Assigned To Staff'
            else:
                status_value = 'Pending'
        print("status_value",status_value)
        initial_status = status_value  # Set the initial status value




        data ={
            'staff_coupon_assign':staff_coupon_assign,
            'to_customer':to_customer,
            'created_by': str(request.user.id),
            'modified_by': str(request.user.id),
            'modified_date': datetime.now(),
            'created_date': datetime.now(),
            'status':status_value
            

        }
        serializer=assigncustomerCouponserializers(data=data,initial={'status': initial_status})
        if serializer.is_valid():
                # Save the new CouponRequest
                serializer.save()
                print("VALID")
                data = {'detail': ' created successfully!'}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------Attendance Log------------------------------------#

class PunchIn_Api(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializers = Attendance_Serializers

    def post(self, request, *args, **kwargs):
        try:
            userid = request.data["id"]
            staff = CustomUser.objects.get(id=userid)
            check_already_logged = Attendance_Log.objects.filter(staff=staff, punch_in_date=date.today())
            if len(check_already_logged) >= 1:
                return Response({'status': False, 'message': 'Already Logged In!'})
            else:
                data = Attendance_Log.objects.create(staff=staff, created_by=staff.first_name)
                return_data = Attendance_Log.objects.filter(attendance_id=data.attendance_id).select_related('staff')
                result = self.serializers(return_data, many=True)
                return Response({'status': True, 'data': result.data, 'message': 'Successfully Logged In!'})
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})


class PunchOut_Api(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializers = Attendance_Serializers

    def post(self, request, *args, **kwargs):
        try:
            userid = request.data["id"]
            staff = CustomUser.objects.get(id=userid)
            Attendance_Log.objects.filter(staff=staff, punch_in_date=datetime.now().date()).update(
                staff=staff,
                created_by=staff.first_name,
                punch_out_date=datetime.now().date(),
                punch_out_time=datetime.now().time())
            return_data = Attendance_Log.objects.filter(punch_out_date=datetime.now().date()).select_related('staff')
            result = self.serializers(return_data, many=True)
            return Response({'status': True, 'data': result.data, 'message': 'Successfully Logged In!'})
        except Exception as e:
            print(e)            
            return Response({'status': False, 'message': 'Something went wrong!'})

#----------------------------------------Customer --------------------------------------------#

@api_view(['GET'])
def location_based_on_emirates(request):
    emirate = request.query_params.get('emirate', None)
    if emirate is None:
        return Response({'error': 'Emirate parameter is required'}, status=status.HTTP_400_BAD_REQUEST)    
    location_list = LocationMaster.objects.filter(emirate=emirate).all()
    locations = LocationMasterSerializers(location_list, many=True).data
    return Response({'locations': locations})

class Route_Assign_Staff_Api(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = Staff_Assigned_Route_Details_Serializer

    def post(self, request, *args, **kwargs):
        try:
            userid = request.data["id"]
            staff = CustomUser.objects.get(id=userid)
            vans = Van.objects.filter(Q(driver=staff) | Q(salesman=staff)).first()
            if vans is not None: 
                van = Van.objects.get(van_make = vans)
                assign_routes = Van_Routes.objects.filter(van=van).values_list('routes', flat=True)
                routes_list = RouteMaster.objects.filter(route_id__in = assign_routes)
                serializer = self.serializer_class(routes_list, many=True)
                data = {
                    'id':staff.id,
                    'staff':staff.first_name,
                    'van_id':van.van_id,
                    'van_name':van.van_make,
                    'branch':van.branch_id.name,
                    'branch_id':van.branch_id.branch_id,
                    'assigned_routes':serializer.data
                }
                return Response({'status': True, 'data':data, 'message': 'Assigned Routes List!'})
            else:
                return Response({'status': False, 'data':[],'message': 'No van found for the given staff.'})
        except Exception as e:
            print(e)            
            return Response({'status': False, 'message': 'Something went wrong!'})


class Create_Customer(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomersSerializers

    def post(self, request, *args, **kwargs):
        try:
            username = request.headers['username']
            user=CustomUser.objects.get(username=username)
            print(request.data,"<--request.data")
            serializer=Create_Customers_Serializers(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=user.id,branch_id=user.branch_id)
                return Response({'status':True,'message':'Customer Succesfully Created'},status=status.HTTP_201_CREATED)
            else :
                return Response({'status':False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def get(self,request,id=None):
        try:
            if id :
                queryset = Customers.objects.get(customer_id=id)
                serializer = Create_Customers_Serializers(queryset)
                return Response(serializer.data)
            queryset = Customers.objects.all()
            serializer = Create_Customers_Serializers(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Fetched Customer Details'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id):
        try:
            customers = Customers.objects.get(customer_id=id)
            serializer = Create_Customers_Serializers(customers, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,branch_id=request.user.branch_id,modified_date = datetime.now())
                return Response({'status':True,'data':serializer.data,'message':'Customer Succesfully Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'status':True,'data':[],'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
class Get_Items_API(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated] 
    serializer_class = Items_Serializers
    product_serializer = Products_Serializers

    def get(self,request,id=None):
        try:
            #customer = request.data['id']
            customer_exists = Customers.objects.filter(customer_id=id).exists()
            if customer_exists:
                customer_data = Customers.objects.get(customer_id=id)
                print(customer_data.branch_id)
                branch_id = customer_data.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                products = Product.objects.filter(branch_id=branch).exists()
                if products:
                    products = Product.objects.filter(branch_id=branch)
                    data = []
                    for product in products:
                        item_price_level_list = Product_Default_Price_Level.objects.filter(product_id=product,customer_type=customer_data.customer_type).exists()
                        if item_price_level_list:
                            item_price_level = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer_data.customer_type)
                            serializer = self.serializer_class(item_price_level)
                            data.append(serializer.data)
                        else:
                            serializer_1 = self.product_serializer(product)
                            data.append(serializer_1.data)
                    data2 = {'customer_id':customer_data.customer_id,'customer_name':customer_data.customer_name,
                             'default_water_rate':customer_data.rate, 'items_count':len(data)}
                    return Response({'status': True, 'data': {'items':data,'customer':data2}, 'message': 'Data fetched Successfully'})
                else:
                    return Response({'status': True, 'data': [], 'message': 'Data fetched Successfully'})
            else:
                return Response({'status': False,'message': 'Customer Not Exists'})

        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
class Add_Customer_Custody_Item_API(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    customer_custody_item = CustomerCustodyItemSerializers
    get_custody_item = CustodyItemSerializers

    def post(self,request, *args, **kwargs):
        try:
            username = request.headers['username']
            print("username")
            user = CustomUser.objects.get(username=username)
            data_list = request.data.get('data_list', [])
            serializer = CustomerCustodyItemSerializer(data=data_list, many=True)
            if serializer.is_valid():
                serializer.save(created_by=user.id)
                return Response({'status': True,'message':'Customer Custody Item Succesfully Created'},status=status.HTTP_201_CREATED)
            else :
                return Response({'status': False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
    def get(self,request,id=None):
        try:
            customer_exists = Customers.objects.filter(customer_id=id).exists()
            print("customer_exists")
            if customer_exists:
                customer_exists = Customers.objects.get(customer_id=id)
                custody_list = Customer_Custody_Items.objects.filter(customer=customer_exists.customer_id)
                if custody_list:
                    serializer = CustodyItemSerializers(custody_list, many=True)
                    print(serializer.data)
                    return Response({'status': True,'data':serializer.data,'message':'data fetched successfully'},status=status.HTTP_200_OK)    
                else:
                    return Response({'status': True,'data':[],'message':'No custody items'},status=status.HTTP_200_OK)
            else :
                return Response({'status': False,'message':'Customer not exists'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, *args, **kwargs):
        try:
            data_list = request.data.get('data_list', [])
            objects_to_update = Customer_Custody_Items.objects.filter(pk__in=[item['id'] for item in data_list])

            for data_item in data_list:
                obj = objects_to_update.get(pk=data_item['id'])
                serializer = CustomerCustodyItemSerializer(obj, data=data_item, partial=True)
                if serializer.is_valid():
                    serializer.save()

            return Response({'status': True, 'message': 'Customer custody item Updated Successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Add_No_Coupons(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerInhandCouponsSerializers

    def post(self,request, *args, **kwargs):
        try:
            username = request.headers['username']
            user = CustomUser.objects.get(username=username)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=user.id)
                return Response({'status': True,'data':serializer.data,'message':'data added Succesfully'},status=status.HTTP_201_CREATED)
            else :
                return Response({'status': False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,id=None):
        try:
            customer_exists = Customers.objects.filter(customer_id=id).exists()
            if customer_exists:
                customer_exists = Customers.objects.get(customer_id=id)
                custody_list = Customer_Inhand_Coupons.objects.filter(customer=customer_exists.customer_id)
                if custody_list:
                    serializer = GetCustomerInhandCouponsSerializers(custody_list, many=True)
                    print(serializer.data)
                    return Response({'status': True,'data':serializer.data,'message':'data fetched successfully'},status=status.HTTP_200_OK)    
                else:
                    return Response({'status': True,'data':[],'message':'No coupons available'},status=status.HTTP_200_OK)
            else :
                return Response({'status': False,'message':'Customer not exists'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id, *args, **kwargs):
        try:
            customers_coupon = Customer_Inhand_Coupons.objects.get(cust_inhand_id=id)
            serializer = CustomerInhandCouponsSerializers(customers_coupon,data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,branch_id=request.user.branch_id,modified_date = datetime.now())
                return Response({'status':True,'data':serializer.data,'message':'Update coupons successfully'},status=status.HTTP_201_CREATED)
            else :
                return Response({'status': False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

class Staff_New_Order(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    staff_order_serializer = StaffOrderSerializers
    staff_order_details_serializer = StaffOrderDetailsSerializers
    def post(self, request, *args, **kwargs):
        try:
            data_list = request.data.get('data_list', [])
            uid = uuid.uuid4()
            uid = str(uid)[:5]
            dtm = date.today().month
            dty = date.today().year
            dty = str(dty)[2:]
            num = str(uid) + str(dtm) + str(dty)
            print(num,"<===num")
            request.data["order_num"]=num
            print(request.data,"<===request.data")
            created_by = request.data["id"]
            print(created_by,"created_by")
            serializer_1 = self.staff_order_serializer(data=request.data)
            if serializer_1.is_valid(raise_exception=True):
                data=serializer_1.save(created_by=created_by)
                staff_order = data.staff_order_id
                for datas in data_list:
                    datas["staff_order_id"] = staff_order
                serializer_2 = self.staff_order_details_serializer(data=data_list, many=True)
                if serializer_2.is_valid(raise_exception=True):
                    data=serializer_2.save(created_by=created_by)
                    return Response({'status': True,'message':'Order Placed Succesfully'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'status':False,'message':serializer_2.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':serializer_1.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
class Customer_Create(APIView):
    serializer_class = CustomersSerializers

    def post(self, request, *args, **kwargs):
        try:
            username=request.data["mobile_no"]
            print('username',username)
            password=request.data["password"]
            print('password',password)
            hashed_password=make_password(password)
            if Customers.objects.filter(mobile_no=request.data["mobile_no"]).exists():
                return Response({'status':True,'message':'Customer with this mobile number already exist !! Try another number'},status=status.HTTP_201_CREATED)
            customer_data=CustomUser.objects.create(password=hashed_password,username=username,first_name=request.data['customer_name'],email=request.data['email_id'],user_type='Customer')
            request.data["user_id"]=customer_data.id
            request.data["created_by"]=str(request.data["customer_name"])
            serializer=CustomersSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status':True, 'data':request.data, 'message':'Customer Succesfully Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'status': False,'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            user_exist = CustomUser.objects.filter(phone=request.data['mobile_no']).exists()
            if user_exist:
                user_obj = CustomUser.objects.get(phone=request.data['mobile_no'])
                user_obj.delete()
                return Response({"status": False, 'data': e, "message": "Something went wrong!"})
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})
        
class CustomerDetails(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        try:
            if id :
                queryset = Customers.objects.get(customer_id=id)
                serializer = CustomersSerializers(queryset)
                return Response(serializer.data)
            queryset = Customers.objects.all()
            serializer = CustomersSerializers(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Fetched Customer Details'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

    def put(self, request, id):
        try:
            customers = Customers.objects.get(customer_id=id)
            serializer = CustomersSerializers(customers, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.id,modified_date = datetime.now())
                return Response({'status':True,'data':serializer.data,'message':'Customer Succesfully Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'status':True,'data':[],'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})

def is_valid_mobile(mobile):
    return len(mobile) == 10 and mobile.isdigit()

class Check_Customer(APIView):
    def post(self, request, *args, **kwargs):
        try:
            mobile = request.data['mobile']
            user_exists = Customers.objects.filter(mobile_no=mobile).exists()
            if user_exists:
                user = Customers.objects.get(mobile_no=mobile)
                custom_user_instance = user.user_id
                if is_valid_mobile(mobile):
                    number = randint(1111, 9999)
                    future_time = dt.now() + timedelta(minutes=5)
                    usr_otpcheck = UserOTP.objects.filter(user=custom_user_instance).first()
                    print("usr_otpcheck", usr_otpcheck)
                    if usr_otpcheck is None:
                        usr_otp = UserOTP.objects.create(
                            expire_time=future_time, user=custom_user_instance, mobile=mobile, otp=str(number),
                            created_on=timezone.now()
                        )
                        return Response({'status':True,'message': 'OTP sent successfully', 'otp': str(number)},
                                        status=status.HTTP_200_OK)
                    else:
                        usr_otpcheck.otp = str(number)
                        usr_otpcheck.expire_time = future_time
                        usr_otpcheck.created_on = timezone.now()
                        usr_otpcheck.save()
                        return Response({'status':True,'message': 'OTP sent successfully', 'otp': str(number)},
                                        status=status.HTTP_200_OK)
                else:
                    return Response({'status':False,'error': 'Invalid mobile number'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status':False,'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})


class Verify_otp(APIView):
    def post(self, request, *args, **kwargs):
        try:
            mobile = request.data['mobile']
            code = request.data['code']
            cust_user = Customers.objects.get(mobile_no=mobile).user_id
            if cust_user is not None:
                user_id = CustomUser.objects.get(username=cust_user).id
                usr_otpcheck = UserOTP.objects.filter(user=user_id).first()
                if usr_otpcheck and usr_otpcheck.expire_time > str(timezone.now()):
                    if usr_otpcheck.otp == code:
                        return Response({'status':True,'message': 'OTP validation successful'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':False,'error': 'OTP has expired or not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'status':False,'error': 'OTP has expired or not found'}, status=status.HTTP_404_NOT_FOUND)
            else:    
                return Response({'status':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})


##################################  Client Management #################################
        

# Vacation

class VacationListAPI(APIView):
    def get(self, request):
        vacation = Vacation.objects.all()
        serializer = VacationSerializer(vacation, many=True)
        return Response(serializer.data)
    
class VacationAddAPI(APIView):
    def post(self, request):
        serializer=VacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VacationEditAPI(APIView):
    def put(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        serializer = VacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VacationDeleteAPI(APIView):
    def delete(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        vacation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleView(APIView):
    def get(self, request, date_str):
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        routes = RouteMaster.objects.all()
        route_trip_details = []
        for route in routes:
            todays_route_wise_customers = find_customers(request, date_str, route.route_id)
            if todays_route_wise_customers:
                trips = set(customer['trip'] for customer in todays_route_wise_customers)
                for trip in trips:
                    trip_customers = [customer['customer_name'] for customer in todays_route_wise_customers if customer['trip'] == trip]
                    route_trip_details.append({
                        'route_id': route.route_id,
                        'route_name': route.route_name,
                        'trip': trip,
                        'customers': trip_customers,
                    })
            else:
                route_trip_details.append({
                    'route_id': route.route_id,
                    'route_name': route.route_name,
                    'trip': 'No trip',  # Indicate no trip
                    'customers': []  # Indicate no customers
                })
        return Response({'def_date': date_str, 'details': route_trip_details}, status=status.HTTP_200_OK)


class ScheduleByRoute(APIView):
    def get(self, request, date_str, route_id, trip):
        route = RouteMaster.objects.get(route_id=route_id)
        todays_customers = find_customers(request, date_str, route_id)
        customers = [customer for customer in todays_customers if customer['trip'] == trip]
        return Response({
            'def_date': date_str,
            'route': {
                'route_id': route.route_id,
                'route_name': route.route_name,
                'trip' : trip
            },
            'todays_customers': customers,
        }, status=status.HTTP_200_OK)

class Get_Category_API(APIView):
    def get(self, request):
        category_id = request.GET.get('category_id')
        products = Product.objects.filter(category_id=category_id).values('product_id', 'product_name','rate')
        return JsonResponse({'products': list(products)})

class Myclient_API(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomersSerializers

    def post(self, request, *args, **kwargs):
        try:
            userid = request.data["id"]
            print('userid',userid)
            #81
            staff = CustomUser.objects.get(id=userid)
            print(staff,'staff')
            vans = Van.objects.filter(Q(driver=staff) | Q(salesman=staff)).first()
            print(staff,'staff')

            if vans is not None: 
                van = Van.objects.get(van_make = vans)
                print("van",van)
                assign_routes = Van_Routes.objects.filter(van=van).values_list('routes', flat=True)
                print("assign_routes",assign_routes)
                routes_list = RouteMaster.objects.filter(route_id__in = assign_routes).values_list('route_id',flat=True)
                print("routes_list",routes_list)
                customer_list = Customers.objects.filter(routes__in=routes_list)
                serializer = self.serializer_class(customer_list, many=True)
                return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Something went wrong!'})



# class CustomerCustody_API(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     customer_custody_item = CustomerCustodyItemSerializers
#     get_custody_item = CustodyItemSerializers

    # def post(self,request, *args, **kwargs):
    #     try:
    #         username = request.headers['username']
    #         print("username")
    #         user = CustomUser.objects.get(username=username)
    #         data_list = request.data.get('data_list', [])
    #         serializer = CustomerCustodyItemSerializer(data=data_list, many=True)
    #         if serializer.is_valid():
    #             serializer.save(created_by=user.id)
    #             return Response({'status': True,'message':'Customer Custody Item Succesfully Created'},status=status.HTTP_201_CREATED)
    #         else :
    #             return Response({'status': False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as e:
    #         print(e)
    #         return Response({'status': False, 'message': 'Something went wrong!'})


    #         class Add_Customer_Custody_Item_API(APIView):
    # def post(self, request, *args, **kwargs):
    #     try:
    #         # Get the data from the request
    #         category = request.data.get['category']
    #         product = request.data.get['product']
    #         serial_no = request.data.get['serial_no']
    #         quantity = request.data.get['quantity']

    #         # Create a new customer custody item
    #         customer_custody_item = Customer_Custody_Items.objects.create(
    #             category=category,
    #             product=product,
    #             serial_no=serial_no,
    #             quantity=quantity
    #         )

    #         # Serialize the customer custody item
    #         serializer = CustomerCustodyItemSerializer(customer_custody_item)

    #         # Return the serialized data
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         # If there's an error, return a 400 Bad Request response
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from client_management.models import Customer_Custody_Items
from .serializers import CustomerCustodyItemSerializer



class GetCustodyItem_API(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerCustodyItemSerializer
    def get(self, request, *args, **kwargs):
        try:
            custody_items=Customer_Custody_Items.objects.all()
            serializer=self.serializer_class(custody_items,many=True)
            return Response({'status': True, 'data':serializer.data, 'message': 'custody items lis passed!'})            
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})



class GetCategoryAPI(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = SelectCategorySerializer
    def get(self, request, *args, **kwargs):
        try:
            category=CategoryMaster.objects.all()
            print(category,'category')
            serializer=self.serializer_class(category,many=True)
            return Response({'status': True, 'data':serializer.data, 'message': 'category items lis passed!'})            
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})
        
class GetProductsAPI(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = SelectProductSerializer
    def get(self, request, *args, **kwargs):
        try:
            product=Product.objects.all()
            print(product,'product')
            serializer=self.serializer_class(product,many=True)
            return Response({'status': True, 'data':serializer.data, 'message': 'product items lis passed!'})
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})

class AddCustomerCustodyItem(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerCustodyItemSerializer
    def post(self, request, *args, **kwargs):
        try:
            print("kkkk")
            serializer = CustomerCustodyItemSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("kkkkk",e)
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})
            

class Custody_Add_API(APIView):
    serializer_class = CustomerCustodyItemSerializer
    def post(self, request, *args, **kwargs):
        try:
            
            serializer = CustomerCustodyItemSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data=serializer.save()
                
                return Response({"status": True, "data": serializer.data, "message": "Custody Items Added  Successfully!"})
            else:
                return Response({"status": True, "data": serializer.data, "message": "Data not valid!"})
        except Exception as e:
            print(e,"errror")
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})      

        

