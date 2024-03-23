import uuid
import base64
import datetime
from datetime import datetime, date, time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.generics import DestroyAPIView
from rest_framework.utils import serializer_helpers
from accounts.models import *
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse
from django.db import transaction, IntegrityError

#from .models import *
from django.utils import timezone
from django.contrib.auth import authenticate,login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
######rest framwework section
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import BasePermission, IsAuthenticated,IsAuthenticatedOrReadOnly

from client_management.forms import CoupenEditForm
from master.serializers import *
from master.functions import generate_serializer_errors
from master.models import *
from random import randint
from datetime import datetime as dt
from coupon_management.models import *
from datetime import timedelta
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from accounts.models import *
from master.models import *
from product.models import *
from van_management.models import *
from customer_care.models import *
from order.models import *


from master.serializers import *
from product.serializers import *
from van_management.serializers import *
from accounts.serializers import *
from .serializers import *
from client_management.serializers import VacationSerializer
from coupon_management.serializers import *
from order.serializers import *


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
from django.db.models import Sum



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
        week_number = f'Week{week_num}'
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

    
    if not len(buildings) == 0:
        building_count = {}

        for building in buildings:
            for customer in todays_customers:
                if customer.building_name == building:
                    if building in building_count:
                        building_count[building] += customer.no_of_bottles_required
                    else:
                        building_count[building] = customer.no_of_bottles_required


        building_gps = []

        for building, bottle_count in building_count.items():
        # Fetch GPS longitude and latitude for each building
            c = Customers.objects.filter(building_name=building, routes=route).first()
            gps_longitude = c.gps_longitude
            gps_latitude = c.gps_latitude
        # Append tuple of building name and its GPS coordinates
            building_gps.append((building, gps_longitude, gps_latitude, bottle_count))

            # Sort buildings based on GPS longitude and latitude
        sorted_building_gps = sorted(building_gps, key=lambda x: (x[1], x[2]))
        sorted_buildings = [item[0] for item in sorted_building_gps]
        sorted_building_count = dict(sorted(building_count.items(), key=lambda item: item[1]))

        trips = {}
        trip_count = 1
        current_trip_bottle_count = 0
        trip_buildings = []
        
        # for building, bottle_count in sorted_buildings.items():
        # for building, bottle_count in sorted_building_count.items():
        for building in sorted_buildings:
          
            for building_data in sorted_building_gps:
                if building_data[0]==building:
                    building = building_data[0]
                    bottle_count = building_data[3]
                    if current_trip_bottle_count + bottle_count > 232:
                        trip_buildings = [building]
                        trip_count+=1
                        trips[f"Trip{trip_count}"] = trip_buildings
                        # print(route,"trip",trip_count)
                        current_trip_bottle_count = bottle_count
                    else:
                        
                        trip_buildings.append(building)
                        trips[f"Trip{trip_count}"] = trip_buildings
                        current_trip_bottle_count += bottle_count
            
        

        # Merge trips if possible to optimize
        merging_occurred = False
        for trip_num in range(1, trip_count + 1):
            for other_trip_num in range(trip_num + 1, trip_count + 1):
                trip_key = f"Trip{trip_num}"
                other_trip_key = f"Trip{other_trip_num}"
                combined_buildings = trips.get(trip_key, []) + trips.get(other_trip_key, [])
                total_bottles = sum(sorted_building_count.get(building, 0) for building in combined_buildings)
                if total_bottles <= 232:
                    trips[trip_key] = combined_buildings
                    del trips[other_trip_key]
                    merging_occurred = True
                    break
            if merging_occurred:  
                break
            
        # List to store trip-wise customer details
        trip_customers = []
        for trip in trips:
            for building in trips[trip]:
                for customer in todays_customers:
                    if customer.building_name ==building:
                        trip_customer = {
                            "customer_name" : customer.customer_name,
                            "customer_id" : customer.customer_id,
                            "trip":trip,
                            "building":customer.building_name,
                            "route" : customer.routes.route_name,
                            "no_of_bottles": customer.no_of_bottles_required,
                            "location" : customer.location.location_name,
                            "location_id" : customer.location.location_id,
                            "gps_latitude": customer.gps_latitude,
                            "gps_longitude": customer.gps_longitude,
                            "building": customer.building_name,
                            "door_house_no": customer.door_house_no,
                            "floor_no": customer.floor_no,
                            "customer_type": customer.customer_type,
                            "sales type" : customer.sales_type,
                            'mobile_no': customer.mobile_no,
                            'whats_app': customer.whats_app,
                            'email_id': customer.email_id,
                        }
                        if customer in emergency_customers:
                            trip_customer['type'] = 'Emergency'
                            trip_customer['emergency'] = 1
                            dif = DiffBottlesModel.objects.filter(customer=customer, delivery_date=date).latest('created_date')
                            trip_customer['no_of_bottles'] = dif.quantity_required
                        else:
                            trip_customer['type'] = 'Default'
                            trip_customer['emergency'] = 0
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

# Expense
    
class ExpenseHeadListAPI(APIView):
    def get(self, request):
        expense_heads = ExpenseHead.objects.all()
        serializer = ExpenseHeadSerializer(expense_heads, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExpenseHeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseHeadDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return ExpenseHead.objects.get(pk=pk)
        except ExpenseHead.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expense_head = self.get_object(pk)
        serializer = ExpenseHeadSerializer(expense_head)
        return Response(serializer.data)

    def put(self, request, pk):
        expense_head = self.get_object(pk)
        serializer = ExpenseHeadSerializer(expense_head, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_head = self.get_object(pk)
        expense_head.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ExpenseListAPI(APIView):
    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailAPI(APIView):
    def get(self, request, expense_id):
        expense = Expense.objects.get(expense_id = expense_id)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, expense_id):
        expense = Expense.objects.get(expense_id = expense_id)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id):
        expense = Expense.objects.get(expense_id = expense_id)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 ####################################Order####################################
    
# Reason
class ChangeReasonListAPI(APIView):
    def get(self, request):
        change_reason = Change_Reason.objects.all()
        serializer = ChangeReasonSerializer(change_reason, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChangeReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeReasonDetailAPI(APIView):
    def get(self, request, change_reason_id):
        change_reason = Change_Reason.objects.get(id = change_reason_id)
        serializer = ChangeReasonSerializer(change_reason)
        return Response(serializer.data)

    def put(self, request, change_reason_id):
        change_reason = Change_Reason.objects.get(id = change_reason_id)
        serializer = ChangeReasonSerializer(change_reason, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, change_reason_id):
        change_reason = Change_Reason.objects.get(id = change_reason_id)
        change_reason.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# order Change 
class OrderChangeListAPI(APIView):
    def get(self, request):
        order_change = Order_change.objects.all()
        serializer = OrderChangeSerializer(order_change, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderChangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderChangeDetailAPI(APIView):
    def get_object(self, order_change_id):
        try:
            return Order_change.objects.get(order_change_id=order_change_id)
        except Order_change.DoesNotExist:
            raise Http404

    def get(self, request, order_change_id):
        order_change = self.get_object(order_change_id)
        serializer = OrderChangeSerializer(order_change)
        return Response(serializer.data)

    def put(self, request, order_change_id):
        order_change = self.get_object(order_change_id)
        existing_data = OrderChangeSerializer(order_change).data  # Get existing data

        # Merge existing data with request data
        merged_data = {**existing_data, **request.data}
        serializer = OrderChangeSerializer(order_change, data=merged_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_change_id):
        order_change = self.get_object(order_change_id)
        order_change.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Return
class OrderReturnListAPI(APIView):
    def get(self, request):
        order_retrn = Order_return.objects.all()
        serializer = OrderReturnSerializer(order_retrn, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderReturnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderReturnDetailAPI(APIView):
    def get_object(self, order_return_id):
        try:
            return Order_return.objects.get(order_return_id=order_return_id)
        except Order_return.DoesNotExist:
            raise Http404

    def get(self, request, order_return_id):
        order_return = self.get_object(order_return_id)
        serializer = OrderReturnSerializer(order_return)
        return Response(serializer.data)

    def put(self, request, order_return_id):
        order_return = self.get_object(order_return_id)
        existing_data = OrderReturnSerializer(order_return).data  

        merged_data = {**existing_data, **request.data}
        serializer = OrderReturnSerializer(order_return, data=merged_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_return_id):
        order_return = self.get_object(order_return_id)
        order_return.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






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
        custodyitems = CustodyCustomItems.objects.filter(customer=customer).all()
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
                custody_list = CustodyCustomItems.objects.filter(customer=customer_exists.customer_id)
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
            objects_to_update = CustodyCustomItems.objects.filter(pk__in=[item['id'] for item in data_list])

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
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

from collections import defaultdict

@api_view(['GET'])
def product_items(request):
    if (instances:=ProdutItemMaster.objects.all()).exists():
        serializer = ProdutItemMasterSerializer(instances, many=True, context={"request": request})

        status_code = status.HTTP_200_OK  
        response_data = {
            "status": status_code,
            "StatusCode": 6000,
            "data": serializer.data,
        }
    else:
        status_code = status.HTTP_400_BAD_REQUEST 
        response_data = {
            "status": status_code,
            "StatusCode": 6001,
            "message": "No data",
        }

    return Response(response_data, status_code)

class Staff_New_Order(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    staff_order_serializer = StaffOrderSerializers
    staff_order_details_serializer = StaffOrderDetailsSerializers
    
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data_list = request.data.get('data_list', [])
                uid = uuid.uuid4()
                uid = str(uid)[:5]
                dtm = date.today().month
                dty = date.today().year
                dty = str(dty)[2:]
                num = str(uid) + str(dtm) + str(dty)
                request.data["order_num"] = num
                
                serializer_1 = self.staff_order_serializer(data=request.data)
                if serializer_1.is_valid(raise_exception=True):
                    order_data = serializer_1.save(
                        created_by=request.user.id,
                        order_number=num
                    )
                    staff_order = order_data.staff_order_id
                    
                    # Aggregate products by ID
                    product_dict = defaultdict(int)
                    for data in data_list:
                        product_id = data.get("product_id")
                        count = int(data.get("count", 0))
                        product_dict[product_id] += count
                    
                    # Create order details for each product
                    order_details_data = []
                    for product_id, count in product_dict.items():
                        order_details_data.append({
                            "created_by": request.user.id,
                            "staff_order_id": staff_order,
                            "product_id": product_id,
                            "count": count
                        })
                    
                    serializer_2 = self.staff_order_details_serializer(data=order_details_data, many=True)
                    
                    if serializer_2.is_valid(raise_exception=True):
                        serializer_2.save()
                        return Response({'status': True, 'message': 'Order Placed Successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'status': False, 'message': serializer_2.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': False, 'message': serializer_1.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as e:
                # Handle database integrity error
                response_data = {"status": "false","title": "Failed","message": str(e),}

        except Exception as e:
            # Handle other exceptions
            response_data = {"status": "false","title": "Failed","message": str(e),}
        return Response(response_data)


        
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
            
            customer_data=CustomUser.objects.create(
                password=hashed_password,
                username=username,
                first_name=request.data['customer_name'],
                email=request.data['email_id'],
                user_type='Customer'
                )
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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, date_str):
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        # print(staff_id)
        
        staff = CustomUser.objects.get(id=request.user.id)
        if staff.user_type not in ['Driver', 'Salesman', 'Supervisor', 'Manager']:
            return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if staff.user_type == "Driver":
            van = Van.objects.filter(driver = staff)
        elif staff.user_type == "Salesman":
            van = Van.objects.filter(salesman = staff)
            
        routes=[]
        for v in van:
            van_routes = Van_Routes.objects.filter(van=v)
            for v_r in van_routes:
                if v_r.routes not in routes:
                    routes.append(v_r.routes)
                    
        # routes = RouteMaster.objects.all()
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
            if bottle_count > 0:
                route_details.append({
                    'route_name':route.route_name,
                    'route_id':route.route_id,
                    'no_of_customers':customer_count,
                    'no_of_bottles':bottle_count,
                    'no_of_trips':len(trips),
                    'trips': trips
                })
        return Response({'def_date': date_str,'staff': staff.first_name, 'details': route_details}, status=status.HTTP_200_OK)


class ScheduleByRoute(APIView):
    
    def get(self, request, date_str, route_id, trip):
        route = RouteMaster.objects.get(route_id=route_id)
        print(route)
        todays_customers = find_customers(request, date_str, route_id)
        
        if todays_customers:
            customers = [customer for customer in todays_customers if customer['trip'] == trip.capitalize()]
            print(customers)
            
            totale_bottle=0
            for customer in customers:
                totale_bottle+=customer['no_of_bottles']
            return Response({
                'def_date': date_str,
                'totale_bottle':totale_bottle,
                'route': {
                    'route_id': route.route_id,
                    'route_name': route.route_name,
                    'trip' : trip
                },
                'todays_customers': customers,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No customers found for today'}, status=status.HTTP_404_NOT_FOUND)

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

class GetCustodyItem_API(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerCustodyItemSerializer
    def get(self, request, *args, **kwargs):
        try:
            user_id=request.user.id
            print(user_id)
            customerobj=Customers.objects.filter(sales_staff=user_id)
            print(customerobj)
            for customer in customerobj:
                customerid=customer.customer_id
                print(customerid,"kkkk")
                custody_items=CustodyCustomItems.objects.filter(customer=customerid)
                print(custody_items)
                serializer=self.serializer_class(custody_items,many=True)
                return Response({'status': True, 'data':serializer.data, 'message': 'custody items lis passed!'})            
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})


# coupon sales
@api_view(['GET'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
def get_lower_coupon_customers(request):
    if (inhand_instances:=CustomerCouponStock.objects.filter(count__lte=5)).exists():
        customers_ids = inhand_instances.values_list('customer__customer_id', flat=True)
        instances = Customers.objects.filter(pk__in=customers_ids)
        
        serialized = LowerCouponCustomersSerializer(instances, many=True, context={"request": request})
        
        status_code = status.HTTP_200_OK  
        response_data = {
            "status": status_code,
            "StatusCode": 6000,
            "data": serialized.data,
        }
    else:
        status_code = status.HTTP_400_BAD_REQUEST 
        response_data = {
            "status": status_code,
            "StatusCode": 6001,
            "message": "No data",
        }

    return Response(response_data, status_code)

@api_view(['GET'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
def fetch_coupon(request):
    coupon_type = request.GET.get("coupon_type")
    book_no = request.GET.get("book_no")
    
    van_stocks = VanCouponStock.objects.filter(coupon__coupon_type_id__coupon_type_name=coupon_type,coupon__book_num=book_no)

    if van_stocks.exists():
        coupons = van_stocks.first().coupon.all()
        
        serialized = VanCouponStockSerializer(coupons, many=True, context={"request": request})
            
        status_code = status.HTTP_200_OK  
        response_data = {
            "status": status_code,
            "StatusCode": 6000,
            "data": serialized.data,
        }
    else:
        status_code = status.HTTP_400_BAD_REQUEST 
        response_data = {
            "status": status_code,
            "StatusCode": 6001,
            "message": "No data",
        }

    return Response(response_data, status_code)


class customer_coupon_recharge(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer_verified = False
        
        recharge_customer_coupon_serializer = RechargeCustomerCouponSerializer(data=request.data)
        customer_coupon_payment_serializer = CustomerCouponPaymentSerializer(data=request.data)
        cash_coupon_payment_serializer = CashCouponPaymentSerializer(data=request.data)
        cheque_coupon_payment_serializer = ChequeCouponPaymentSerializer(data=request.data)
        
        # Validate serializers before accessing errors
        if (recharge_customer_coupon_serializer.is_valid() and
                customer_coupon_payment_serializer.is_valid()):
            if customer_coupon_payment_serializer.validated_data.get('coupon_type') == "credit_coupon":
                serializer_verified = True
            else:
                if customer_coupon_payment_serializer.validated_data.get('payment_type') == "cash":
                    if cash_coupon_payment_serializer.is_valid():
                        serializer_verified = True
                else:
                    if customer_coupon_payment_serializer.validated_data.get('payment_type') == "cheque":
                        if cheque_coupon_payment_serializer.is_valid():
                            serializer_verified = True
        
        if serializer_verified:
            customer_coupon = recharge_customer_coupon_serializer.save(created_by=request.user.id,salesman=request.user)
            customer_coupon_payment = customer_coupon_payment_serializer.save(customer_coupon=customer_coupon)
            
            if not customer_coupon_payment_serializer.validated_data.get('coupon_type') == "credit_coupon":
                if customer_coupon_payment_serializer.validated_data.get('payment_type') == "cash":
                    cash_coupon_payment_serializer.save(customer_coupon_payment=customer_coupon_payment)
                elif customer_coupon_payment_serializer.validated_data.get('payment_type') == "cheque":
                    cheque_coupon_payment_serializer.save(customer_coupon_payment=customer_coupon_payment)
                    
            if (update_customer_coupon_stock:=CustomerCouponStock.objects.filter(
                    coupon_type_id=customer_coupon.coupon.coupon_type).exists()):
                stock = CustomerCouponStock.objects.filter(coupon_type_id=customer_coupon.coupon.coupon_type).latest('id')
                stock.count += 1
                stock.save()
            else:
                CustomerCouponStock.objects.create(
                    coupon_type_id=customer_coupon.coupon.coupon_type,
                    customer=customer_coupon.customer,
                    count=1,
                )
            
            status_code = status.HTTP_200_OK
            response_data = {
                "status": status_code,
                "StatusCode": 6000,
                "message": "recharge successful"
            }
        else:
            recharge_customer_coupon_serializer.is_valid()
            customer_coupon_payment_serializer.is_valid()
            cash_coupon_payment_serializer.is_valid()
            cheque_coupon_payment_serializer.is_valid()
            
            recharge_customer_coupon_error = generate_serializer_errors(recharge_customer_coupon_serializer.errors)
            customer_coupon_payment_error = generate_serializer_errors(customer_coupon_payment_serializer.errors)
            cash_coupon_payment_error = generate_serializer_errors(cash_coupon_payment_serializer.errors)
            cheque_coupon_payment_error = generate_serializer_errors(cheque_coupon_payment_serializer.errors)

            combined_errors = "\n".join([recharge_customer_coupon_error, customer_coupon_payment_error,
                                        cash_coupon_payment_error, cheque_coupon_payment_error])

            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {
                "status": status_code,
                "StatusCode": 6001,
                "message": combined_errors,
            }

        return Response(response_data, status=status_code)


    
from django.shortcuts import get_object_or_404


class GetProductAPI(APIView):
   
    def get(self, request, *args, **kwargs):
        try:
            product_names = ["5 Gallon", "Water Cooler", "Dispenser"]
            product_items = ProdutItemMaster.objects.filter(product_name__in=product_names)
            print('product_items',product_items)
            serializer = ProdutItemMasterSerializer(product_items, many=True)          
            return Response({"products": serializer.data}, status=status.HTTP_200_OK)
           
        except Exception as e:
            print(e, "error")
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})

class CustodyCustomItemAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustodyCustomItemSerializer

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.data['customer_id'] 
            product_id = request.data['product_id']
            serial_number = request.data['serialnumber']
            quantity = request.data['count']
            deposit_type = request.data['deposit_type'] 
            agreement_number = request.data['agreement_no']
            amount = request.data['amount']
            # total_amount = request.data['total_amount']
            
            custody_custom, _ = CustodyCustom.objects.get_or_create(
                customer_id=customer_id,
                agreement_no=agreement_number,
                deposit_type=deposit_type
            )

            # Set total_amount only if a deposit is made
            # if is_deposit:
            #     custody_custom.total_amount = total_amount
            #     custody_custom.save()

            # Create CustodyCustomItems instance
            custody_item = CustodyCustomItems.objects.create(
                custody_custom=custody_custom,
                product_id=product_id,
                amount=amount,
                serialnumber=serial_number,
                quantity=quantity
            )

            serializer = self.serializer_class(custody_item, many=False)
            return Response({"status": True, "data": serializer.data, "message": "Data saved successfully!"})
        except Exception as e:
            print(e)
            return Response({"status": False, "message": str(e)})

class supply_product(APIView):
    def get(self, request, *args, **kwargs):
        route_id = request.GET.get("route_id")
        customers = Customers.objects.all()
        
        if route_id:
            customers = customers.filter(routes__pk=route_id)
        
        serializer = SupplyItemCustomersSerializer(customers, many=True, context={"request": request})
        
        status_code = status.HTTP_200_OK  
        response_data = {
            "status": status_code,
            "StatusCode": 6000,
            "data": serializer.data,
        }
        
        return Response(response_data, status_code)
        
# @api_view(['GET'])
# def supply_product(request):
#     if (instances:=VanProductStock.objects.filter(product__pk=product_id)).exists():
#         product = instances.first().product
#         customer = Customers.objects.get(pk=customer_id)

#         if product.product_name.product_name=="5 Gallon":
#             serializer = SupplyItemFiveCanWaterProductGetSerializer(product, many=False, context={"request": request,"customer":customer.pk})
#         else:
#             serializer = SupplyItemProductGetSerializer(product, many=False, context={"request": request,"customer":customer.pk})

#         status_code = status.HTTP_200_OK  
#         response_data = {
#             "status": status_code,
#             "StatusCode": 6000,
#             "data": serializer.data,
#         }
#     else:
#         status_code = status.HTTP_400_BAD_REQUEST 
#         response_data = {
#             "status": status_code,
#             "StatusCode": 6001,
#             "message": "No data",
#         }

#     return Response(response_data, status_code)

# @api_view(['POST'])
# def create_customer_supply(request):
class create_customer_supply(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        customer_supply_serializer = CustomerSupplySerializer(data=request.data.get('customer_supply'))
        customer_supply_items_serializer = CustomerSupplyItemsSerializer(data=request.data.get('items'), many=True)

        if customer_supply_serializer.is_valid() and customer_supply_items_serializer.is_valid():
            # with transaction.atomic():
            customer_supply = customer_supply_serializer.save(created_by=request.user.id)
            items_data = customer_supply_items_serializer.validated_data

            for item_data in items_data:
                if item_data['product'].name == "5 Gallon":
                    item_data['collected_empty_bottle'] = request.data.get('collected_empty_bottle')
                    item_data['allocate_bottle_to_pending'] = request.data.get('allocate_bottle_to_pending')
                    item_data['allocate_bottle_to_custody'] = request.data.get('allocate_bottle_to_custody')
                    item_data['allocate_bottle_to_paid'] = request.data.get('allocate_bottle_to_paid')
                item_data['customer_supply'] = customer_supply.id

            customer_supply_items_serializer.save()

            # Update customer supply stock
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                customer = customer_supply.customer
                customer_supply_stock, _ = CustomerSupplyStock.objects.get_or_create(customer=customer, product=product)
                customer_supply_stock.stock_quantity += quantity
                customer_supply_stock.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Customer Supply created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('customer_supply:customer_supply_list')
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            errors.update(customer_supply_serializer.errors)
            errors.update(customer_supply_items_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def customer_coupon_stock(request):
    if (instances:=CustomerCouponStock.objects.all()).exists():
        
        serializer = CustomerCouponStockSerializer(instances, many=True, context={"request": request})

        status_code = status.HTTP_200_OK  
        response_data = {
            "status": status_code,
            "StatusCode": 6000,
            "data": serializer.data,
        }
    else:
        status_code = status.HTTP_400_BAD_REQUEST 
        response_data = {
            "status": status_code,
            "StatusCode": 6001,
            "message": "No data",
        }

    return Response(response_data, status_code)

    

# class CustodyCustomItemListAPI(APIView):
    
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CustodyCustomItemsSerializer
    
#     def get(self, request, *args, **kwargs):
#         try:
#             user_id = request.user.id
#             customer_obj = Customers.objects.filter(sales_staff=user_id)
#             custody_items = CustodyCustomItems.objects.filter(customer__in=customer_obj)
#             serializer = self.serializer_class(custody_items, many=True)
            
#             grouped_data = {}
            
#             # Group items by customer id
#             for item in serializer.data:
#                 customer_id = item['customer']['customer_id']
#                 customer_name = item['customer']['customer_name']
#                 if customer_id not in grouped_data:
#                     grouped_data[customer_id] = {
#                         'customer_id': customer_id,
#                         'customer_name': customer_name,
#                         'products': []
#                     }
#                 grouped_data[customer_id]['products'].append({
#                     'product_name': item['product_name'],
#                     'product': item['product'],
#                     'rate': item['rate'],
#                     'count': item['count'],
#                     'serialnumber': item['serialnumber'],
#                     'deposit_type': item['deposit_type'],
#                     'deposit_form_number': item['deposit_form_number']
#                 })
            
#             final_response = list(grouped_data.values())
            
#             return Response({'status': True, 'data': final_response, 'message': 'Custody items list passed!'})
        
#         except Exception as e:
#             return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'})
    
class CustodyCustomItemListAPI(APIView):
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustodyCustomItemsSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            # Fetch all CustodyCustom objects for the current user
            custody_custom_objects = CustodyCustom.objects.filter(customer__sales_staff=user_id)
            
            # Initialize a dictionary to store grouped data
            grouped_data = {}
            
            # Iterate over each CustodyCustom object
            for custody_custom_obj in custody_custom_objects:
                # Fetch CustodyCustomItems related to the CustodyCustom object
                custody_items = CustodyCustomItems.objects.filter(custody_custom=custody_custom_obj)
                
                # Serialize CustodyCustomItems data
                serialized_items = self.serializer_class(custody_items, many=True).data
                
                # Get customer_id
                customer_id = custody_custom_obj.customer.customer_id
                
                # Add customer_id and serialized items to grouped_data
                grouped_data[customer_id] = {
                    'customer_id': customer_id,
                    'customer_name': custody_custom_obj.customer.customer_name,
                    'products': serialized_items
                }
            
            # Convert dictionary values to a list
            final_response = list(grouped_data.values())
            
            return Response({'status': True, 'data': final_response, 'message': 'Custody items list passed!'})
        
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustodyItemReturnAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustodyCustomReturnSerializer

    def post(self, request, *args, **kwargs):
        try:
            id = request.data['id']
            customer_id = request.data['customer_id'] 

            product_id = request.data['product_id']
            serial_number = request.data['serialnumber']
            quantity = request.data['count']
            agreement_number = request.data['deposit_form_number']
            amount = request.data['amount'] 

            custody_item_return = CustomerReturn.objects.create(
                
                customer_id = customer_id,
                product_id=product_id,
                serialnumber=serial_number,
                count=quantity,
                amount=amount,
                deposit_form_number=agreement_number
            )
            print("hgdghfhfjhfj",custody_item_return)


            CustodyCustomItems.objects.get(id=id).delete()

            serializer = self.serializer_class(custody_item_return)
            return Response({"status": True, "data": serializer.data, "message": "Data saved successfully!"})
        except KeyError as e:
            return Response({"status": False, "message": f"Missing required parameter: {e}"})
        except ValueError as e:
            return Response({"status": False, "message": f"Invalid value: {e}"})
        except Product.DoesNotExist:
            return Response({"status": False, "message": "Product not found"})
        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {e}"})

class OutstandingAmountAPI(APIView):

    serializer_class = OutstandingAmountSerializer

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.data['customer_id'] 
            print(customer_id)
            custody_items = CustodyCustomItems.objects.filter(customer=customer_id)
            print("custody_items", custody_items)
            total_amount = custody_items.aggregate(total_amount=Sum('amount'))['total_amount']
            print("total_amount", total_amount)
            amount_paid = request.data['amount_paid']
            print("amount_paid", amount_paid)
            amount_paid = int(amount_paid)
            balance = total_amount - amount_paid
            print('balance', balance)
            product = custody_items.first().product
            print("product", product)
            outstanding_amount = OutstandingAmount.objects.create(
                customer_id=customer_id,
                product=product,
                balance_amount=balance,
                amount_paid=amount_paid
            )

            serializer = self.serializer_class(outstanding_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
           
        except Exception as e:
            print(e,"errror")
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
        

class VanStockAPI(APIView):
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        salesman_id = request.user.id 
        coupon_stock = VanCouponStock.objects.all()
        product_stock = VanProductStock.objects.all()

        if salesman_id:
            coupon_stock = coupon_stock.filter(van__salesman_id=salesman_id)
            product_stock = product_stock.filter(van__salesman_id=salesman_id)

        coupon_serializer = VanCouponStockSerializer(coupon_stock, many=True)
        product_serializer = VanProductStockSerializer(product_stock, many=True)

        return Response({
            'coupon_stock': coupon_serializer.data,
            'product_stock': product_serializer.data
        }, status=status.HTTP_200_OK)
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    
    # def get(self, request, *args, **kwargs):
    #     # id = request.user.id
    #     # print("id",id)
    #     # customer=Customers.objects.filter(sales_staff__id = id)
    #     # print("customer",customer)
    #     coupon_stock = VanCouponStock.objects.all()
    #     product_stock = VanProductStock.objects.all()
    #     # if product_stock:
    #     #     salesman=product_stock.van.salesman
    #     #     print("salesman",salesman)
    #     coupon_serializer = VanCouponStockSerializer(coupon_stock, many=True)
    #     product_serializer = VanProductStockSerializer(product_stock, many=True)
    #     print("coupon_serializer",coupon_serializer)
    #     print("product_serializer",product_serializer)
    #     return Response({
    #         # 'customer':customer,
    #         'coupon_stock': coupon_serializer.data,
    #         'product_stock': product_serializer.data
    #     }, status=status.HTTP_200_OK)

class OutstandingAmountListAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        id = request.user.id
        print("id",id)
        customer=Customers.objects.filter(sales_staff__id = id)
        print("customer",customer)

        custody_items = CustodyCustomItems.objects.filter(customer__in =customer)
        print("custody_items",custody_items)

        serializer =CustodyCustomItemListSerializer(custody_items, many=True)
        return Response(serializer.data)







class CouponCountList(APIView):

    def get(self, request, pk, format=None):
        print("View accessed with customer_id:ssssssssssssssssssssssssssss", pk)  # Print statement for debugging
        try:
            customer = Customers.objects.get(customer_id=pk)
            customers = CustomerCouponStock.objects.filter(customer=customer)

            data = []
            for customer_stock in customers:
                data.append({
                    'customer_name': customer_stock.customer.customer_name,
                    'coupon_count': customer_stock.count,
                    'coupon_type':customer.coupon_type_id.coupon_type_name
                })

            return Response(data, status=status.HTTP_200_OK)
        except Customers.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewCouponCreateAPI(APIView):
    def post(self, request, format=None):
        serializer = CustomerCouponStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewCouponCountAPI(APIView):
    def post(self, request, pk):
        form = CoupenEditForm(request.data)
        if form.is_valid():
            data = form.save(commit=False)
            try:
                data.customer = Customers.objects.get(pk=pk)
                data.save()
                return Response({'message': 'New coupon count added successfully!'}, status=status.HTTP_201_CREATED)
            except Customers.DoesNotExist:
                return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCouponCount(APIView):
    def delete(self, request, pk):
        customer_coupon_stock = get_object_or_404(CustomerCouponStock, pk=pk)
        customer_pk = customer_coupon_stock.customer.pk
        customer_coupon_stock.delete()
        return Response({'message': 'Coupon count deleted successfully!', 'customer_pk': str(customer_pk)}, status=status.HTTP_200_OK)


class customer_outstanding(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        reports = CustomerOutstandingReport.objects.all()
        
        route_id = request.GET.get("route_id")
        if route_id :
            reports = reports.filter(customer__routes__pk=route_id)
        
        # if request.user and request.user.user_type=="Salesman":
        customer_data = {}
        for report in reports:
            customer_id = report.customer.pk
            if customer_id not in customer_data:
                customer_data[customer_id] = {
                    'customer': report.customer.pk,
                    'customer_name': report.customer.customer_name,
                    'building_name': report.customer.building_name,
                    'route_name': report.customer.routes.route_name,
                    'route_id': report.customer.routes.pk,
                    'door_house_no': report.customer.door_house_no,
                    'floor_no': report.customer.floor_no,
                    'amount': 0,
                    'empty_can': 0,
                    'coupons': 0
                }
            
            # Add product values based on product type
            if report.product_type == 'amount':
                customer_data[customer_id]['amount'] += report.value
            elif report.product_type == 'emptycan':
                customer_data[customer_id]['empty_can'] += report.value
            elif report.product_type == 'coupons':
                customer_data[customer_id]['coupons'] += report.value
                
        # print(customer_data)
        
        serialized_data = CustomerOutstandingSerializer(data=list(customer_data.values()), many=True)
        serialized_data.is_valid()  # Ensure data is valid
        
        return Response({
            'status': True, 
            'data': serialized_data.data,  # Access serialized data
            'message': 'success'
        },)
        
class CustomerCouponListAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        customers = Customers.objects.all()
        
        route_id = request.GET.get("route_id")
        if route_id:
            customers = customers.filter(routes__pk=route_id)
        serializer = CustomerDetailSerializer(customers, many=True, context={'request': request})
        
        return Response(serializer.data)

