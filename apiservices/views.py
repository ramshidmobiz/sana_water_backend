import uuid
import base64
import datetime
from datetime import datetime, date, time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, F
from decimal import Decimal
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

from accounts.models import *
from invoice_management.models import Invoice, InvoiceItems
from client_management.forms import CoupenEditForm
from master.serializers import *
from master.functions import generate_serializer_errors, get_custom_id
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
from sales_management.models import CollectionItems, CollectionPayment
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
from django.db.models import Sum,Value
from django.db.models.functions import Coalesce



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
    van_route = Van_Routes.objects.filter(routes=route).first()
    if van_route:
        van_capacity = van_route.van.capacity
    else:
        van_capacity = 200
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
        sorted_building_gps = sorted(building_gps, key=lambda x: (x[1] if x[1] is not None else '', x[2] if x[2] is not None else ''))
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
                    if current_trip_bottle_count + bottle_count > van_capacity:
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
                if total_bottles <= van_capacity:
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
                            'rate': customer.rate,
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
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from uuid import UUID
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
        serializer = OrderChangeSerializer(order_change, data=request.data, partial=True)
        print(request.data)
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
        print(serializer.data)
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
        serializer = OrderReturnSerializer(order_return, data=request.data, partial=True)
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
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]

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
                customer_data=CustomUser.objects.create(
                    password=hashed_password,
                    username=username,
                    first_name=request.data['customer_name'],
                    email=request.data['email_id'],
                    user_type='Customer')
                data=serializer.save(
                    user_id=customer_data.id,
                    custom_id = get_custom_id(Customers)
                    )
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

        alloted_quantity = Decimal(request.data.get('alloted_quantity', 0))
        coupon_request=request.data.get('coupon_request')
        coupon_request_data = CouponRequest.objects.values('quantity').get(coupon_request_id=coupon_request)
        quantity = Decimal(coupon_request_data['quantity'])
        remaining_quantity=quantity- alloted_quantity


        data ={
           "alloted_quantity":alloted_quantity ,
           "quantity":quantity,
           'remaining_quantity': Decimal(coupon_request_data['quantity']) - Decimal(request.data.get('alloted_quantity', 0)),
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
        # try:
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
        # except Exception as e:
        #     print(e)
        #     return Response({'status': False, 'message': str(e) })


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
                        count = Decimal(data.get("count", 0))
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
            serializer=CustomersSerializers(
                custom_id = get_custom_id(Customers),
                data=request.data
                )

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
            #81
            staff = CustomUser.objects.get(id=userid)
            vans = Van.objects.filter(Q(driver=staff) | Q(salesman=staff)).first()

            if vans is not None:
                van = Van.objects.get(van_make = vans)
                assign_routes = Van_Routes.objects.filter(van=van).values_list('routes', flat=True)
                routes_list = RouteMaster.objects.filter(route_id__in = assign_routes).values_list('route_id',flat=True)
                customer_list = Customers.objects.filter(routes__in=routes_list)
                serializer = self.serializer_class(customer_list, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response({'status': False, 'message': str(e)})

class GetCustodyItem_API(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerCustodyItemSerializer
    def get(self, request, *args, **kwargs):
        try:
            user_id=request.user.id
            customerobj=Customers.objects.filter(sales_staff=user_id)
            for customer in customerobj:
                customerid=customer.customer_id
                custody_items=CustodyCustomItems.objects.filter(customer=customerid)
                serializer=self.serializer_class(custody_items,many=True)
                return Response({'status': True, 'data':serializer.data, 'message': 'custody items lis passed!'})
        except Exception as e:
            return Response({'status': False, 'data': str(e), 'message': str(e)})


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

class CustomerCouponRecharge(APIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                coupons_data = request.data.get('coupons', [])
                payment_data = request.data.get('payment', {})

                coupon_instances = []
                for coupon_data in coupons_data:
                    customer = Customers.objects.get(pk=coupon_data.pop("customer"))
                    salesman = CustomUser.objects.get(pk=coupon_data.pop("salesman"))
                    items_data = coupon_data.pop('items', [])
                    
                    customer_coupon = CustomerCoupon.objects.create(customer=customer, salesman=salesman, **coupon_data)
                    coupon_instances.append(customer_coupon)
                    
                    balance_amount = Decimal(coupon_data.pop("balance"))
                    
                    if balance_amount != 0 :
                        
                        customer_outstanding = CustomerOutstanding.objects.create(
                            customer=customer,
                            product_type="amount",
                            created_by=request.user.id,
                        )

                        outstanding_amount = OutstandingAmount.objects.create(
                            amount=balance_amount,
                            customer_outstanding=customer_outstanding,
                        )
                        outstanding_instance = ""

                        try:
                            outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer,product_type="amount")
                            outstanding_instance.value += Decimal(outstanding_amount.amount)
                            outstanding_instance.save()
                        except:
                            outstanding_instance = CustomerOutstandingReport.objects.create(
                                product_type='amount',
                                value=outstanding_amount.amount,
                                customer=outstanding_amount.customer_outstanding.customer
                            )

                    # Create CustomerCouponItems instances
                    for item_data in items_data:
                        coupon = NewCoupon.objects.get(pk=item_data.pop("coupon"))
                        items = CustomerCouponItems.objects.create(
                            customer_coupon=customer_coupon,
                            coupon=coupon,
                            rate=item_data.pop("rate")
                        )

                        # Update CustomerCouponStock based on coupons
                        for coupon_instance in coupon_instances:
                            coupon_method = coupon.coupon_method
                            customer_id = customer
                            coupon_type_id = CouponType.objects.get(pk=coupon.coupon_type_id)

                            try:
                                customer_coupon_stock = CustomerCouponStock.objects.get(
                                    coupon_method=coupon_method,
                                    customer_id=customer_id.pk,
                                    coupon_type_id=coupon_type_id
                                )
                            except CustomerCouponStock.DoesNotExist:
                                customer_coupon_stock = CustomerCouponStock.objects.create(
                                    coupon_method=coupon_method,
                                    customer_id=customer_id.pk,
                                    coupon_type_id=coupon_type_id,
                                    count=0
                                )

                            customer_coupon_stock.count += Decimal(coupon.no_of_leaflets)
                            customer_coupon_stock.save()
                            
                            van_coupon_stock = VanCouponStock.objects.get(coupon=coupon)
                            van_coupon_stock.count -= 1
                            van_coupon_stock.save()
                    
                    random_part = str(random.randint(1000, 9999))
                    invoice_number = f'WTR-{random_part}'

                    # Create the invoice
                    invoice_instance = Invoice.objects.create(
                        invoice_no=invoice_number,
                        created_date=datetime.today(),
                        net_taxable=customer_coupon.net_amount,
                        discount=customer_coupon.discount,
                        amout_total=customer_coupon.total_payeble,
                        amout_recieved=customer_coupon.amount_recieved,
                        customer=customer_coupon.customer,
                        reference_no=customer_coupon.reference_number
                    )
                    
                    if invoice_instance.amout_total == invoice_instance.amout_recieved:
                        invoice_instance.invoice_status = "paid"
                        invoice_instance.save()
                    
                    coupon_items = CustomerCouponItems.objects.filter(customer_coupon=customer_coupon) 
                    
                    # Create invoice items
                    for item_data in coupon_items:
                        category = CategoryMaster.objects.get(category_name__iexact="coupons")
                        product_item = ProdutItemMaster.objects.get(product_name=item_data.coupon.coupon_type.coupon_type_name)
                        print(product_item)
                        InvoiceItems.objects.create(
                            category=category,
                            product_items=product_item,
                            qty=1,
                            rate=product_item.rate,
                            invoice=invoice_instance,
                            remarks='invoice genereted from recharge coupon items reference no : ' + invoice_instance.reference_no
                        )    

                # Create ChequeCouponPayment instanceno_of_leaflets
                cheque_payment_instance = None
                if payment_data.get('payment_type') == 'cheque':
                    cheque_payment_instance = ChequeCouponPayment.objects.create(**payment_data)
                    
                

                return Response({"message": "Recharge successful"}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            # Handle database integrity error
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle other exceptions
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from django.shortcuts import get_object_or_404


class GetProductAPI(APIView):

    def get(self, request, *args, **kwargs):
        try:
            product_names = ["5 Gallon", "Hot and  Cool", "Dispenser"]
            product_items = ProdutItemMaster.objects.filter(product_name__in=product_names)
            print('product_items',product_items)
            serializer = ProdutItemMasterSerializerr(product_items, many=True)          
            return Response({"products": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e, "error")
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})

# class CustodyCustomItemAPI(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CustodyCustomItemSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             customer_id = request.data['customer_id'] 
#             product_id = request.data['product_id']
#             serial_number = request.data['serialnumber']
#             quantity = request.data['count']
#             deposit_type = request.data['deposit_type'] 
#             agreement_number = request.data['agreement_no']
#             amount = request.data['amount']

#             # Retrieve the ProdutItemMaster instance
#             product_instance = get_object_or_404(ProdutItemMaster, id=product_id)

#             # Create or retrieve CustodyCustom instance
#             custody_custom, _ = CustodyCustom.objects.get_or_create(
#                 customer_id=customer_id,
#                 agreement_no=agreement_number,
#                 deposit_type=deposit_type 
#             )
#             productinstance = CustodyCustomItems.objects.get( product=product_instance)
#             if productinstance:
#                 old_quantity = productinstance.quantity
#                 new_qty = old_quantity + quantity
#                 productinstance.quantity = new_qty
#                 productinstance.save()
#             else :

#                 # Create CustodyCustomItems instance
#                 custody_item = CustodyCustomItems.objects.create(
#                     custody_custom=custody_custom,
#                     product=product_instance,
#                     amount=amount,
#                     serialnumber=serial_number,
#                     quantity=quantity
#                 )


class CustodyCustomItemAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustodyCustomItemSerializer

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.data['customer_id']
            product_id = request.data['product_id']
            serial_number = request.data['serialnumber']
            quantity = request.data['quantity']
            deposit_type = request.data['deposit_type']
            agreement_number = request.data['agreement_no']
            amount = request.data['amount']

            product_instance = get_object_or_404(ProdutItemMaster, id=product_id)

            custody_custom, _ = CustodyCustom.objects.get_or_create(
                customer_id=customer_id,
                agreement_no=agreement_number,
                deposit_type=deposit_type
            )

            existing_custody_item = CustodyCustomItems.objects.filter(
                custody_custom=custody_custom,
                product=product_instance,
                
            ).first()

            if existing_custody_item:
               
                existing_custody_item.quantity += quantity
                existing_custody_item.serialnumber = existing_custody_item.serialnumber  + ',' + serial_number
                existing_custody_item.save()
                custody_item = existing_custody_item

            else:
                custody_item = CustodyCustomItems.objects.create(
                    custody_custom=custody_custom,
                    product=product_instance,
                    amount=amount,
                    serialnumber=serial_number,
                    quantity=quantity
                )

            serializer = self.serializer_class(custody_item)
           

            
            return Response({"status": True, "data": serializer.data, "message": "Data saved successfully!"})
        except Exception as e:
            print(e)
            return Response({"status": False, "message": str(e)})


class supply_product(APIView):
    def get(self, request, *args, **kwargs):
        route_id = request.GET.get("route_id")
        CustomerCouponStock.objects.update(coupon_method="manual")
        NewCoupon.objects.update(coupon_method="manual")
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

class create_customer_supply(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from the request
        customer_supply_data = request.data.get('customer_supply')
        items_data = request.data.get('items')
        collected_empty_bottle = request.data.get('collected_empty_bottle')
        allocate_bottle_to_pending = request.data.get('allocate_bottle_to_pending')
        allocate_bottle_to_custody = request.data.get('allocate_bottle_to_custody')
        allocate_bottle_to_paid = request.data.get('allocate_bottle_to_paid')
        reference_no = request.data.get('reference_number')
        try:
            with transaction.atomic():

                # Create CustomerSupply instance
                customer_supply = CustomerSupply.objects.create(
                    customer_id=customer_supply_data['customer'],
                    salesman_id=customer_supply_data['salesman'],
                    grand_total=customer_supply_data['grand_total'],
                    discount=customer_supply_data['discount'],
                    net_payable=customer_supply_data['net_payable'],
                    vat=customer_supply_data['vat'],
                    subtotal=customer_supply_data['subtotal'],
                    amount_recieved=customer_supply_data['amount_recieved'],
                    reference_number=reference_no,
                    collected_empty_bottle=collected_empty_bottle,
                    allocate_bottle_to_pending=allocate_bottle_to_pending,
                    allocate_bottle_to_custody=allocate_bottle_to_custody,
                    allocate_bottle_to_paid=allocate_bottle_to_paid,
                    created_by=request.user.id,
                    created_date=timezone.now()
                )

                # Create CustomerSupplyItems instances
                total_fivegallon_qty = 0
                
                for item_data in items_data:
                    suply_items = CustomerSupplyItems.objects.create(
                        customer_supply=customer_supply,
                        product_id=item_data['product'],
                        quantity=item_data['quantity'],
                        amount=item_data['amount']
                    )
                    
                    if suply_items.product.product_name == "5 Gallon" :
                        total_fivegallon_qty += Decimal(suply_items.quantity)
                        
                    vanstock = VanProductStock.objects.get(product=suply_items.product,stock_type="opening_stock",van__salesman=request.user)
                    vanstock.count -= suply_items.quantity
                    vanstock.save()
                
                # empty bottle calculate
                if total_fivegallon_qty < Decimal(customer_supply.collected_empty_bottle) :
                    balance_empty_bottle = Decimal(collected_empty_bottle) - total_fivegallon_qty
                    if CustomerOutstandingReport.objects.filter(customer=customer_supply.customer,product_type="emptycan").exists():
                        outstanding_instance = CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="emptycan")
                        outstanding_instance.value -= Decimal(balance_empty_bottle)
                        outstanding_instance.save()
                
                elif total_fivegallon_qty > Decimal(customer_supply.collected_empty_bottle) :
                    balance_empty_bottle = total_fivegallon_qty - Decimal(customer_supply.collected_empty_bottle)
                    customer_outstanding = CustomerOutstanding.objects.create(
                        customer=customer_supply.customer,
                        product_type="emptycan",
                        created_by=request.user.id,
                    )

                    outstanding_product = OutstandingProduct.objects.create(
                        empty_bottle=balance_empty_bottle,
                        customer_outstanding=customer_outstanding,
                    )
                    outstanding_instance = {}

                    try:
                        outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="emptycan")
                        outstanding_instance.value += Decimal(outstanding_product.empty_bottle)
                        outstanding_instance.save()
                    except:
                        outstanding_instance = CustomerOutstandingReport.objects.create(
                            product_type='emptycan',
                            value=outstanding_product.empty_bottle,
                            customer=outstanding_product.customer_outstanding.customer
                        )
            
                supply_items = CustomerSupplyItems.objects.filter(customer_supply=customer_supply) # supply items
                
                # Update CustomerSupplyStock
                for item_data in supply_items:
                    customer_supply_stock, _ = CustomerSupplyStock.objects.get_or_create(
                        customer=customer_supply.customer,
                        product=item_data.product,
                    )
                    
                    customer_supply_stock.stock_quantity += item_data.quantity
                    customer_supply_stock.save()
                    
                    if Customers.objects.get(pk=customer_supply_data['customer']).sales_type == "CASH COUPON" :
                        # print("cash coupon")
                        total_coupon_collected = request.data.get('total_coupon_collected')
                        collected_coupon_ids = request.data.get('collected_coupon_ids')
                        
                        for c_id in collected_coupon_ids:
                            customer_supply_coupon = CustomerSupplyCoupon.objects.create(
                                customer_supply=customer_supply,
                            )
                            leaflet_instance = CouponLeaflet.objects.get(pk=c_id)
                            customer_supply_coupon.leaf.add(leaflet_instance)
                            leaflet_instance.used=True
                            leaflet_instance.save()
                            
                            if CustomerCouponStock.objects.filter(customer__pk=customer_supply_data['customer'],coupon_method="manual",coupon_type_id=leaflet_instance.coupon.coupon_type).exists() :
                                customer_stock = CustomerCouponStock.objects.get(customer__pk=customer_supply_data['customer'],coupon_method="manual",coupon_type_id=leaflet_instance.coupon.coupon_type)
                                customer_stock.count -= Decimal(len(collected_coupon_ids))
                                customer_stock.save()
                                
                        if total_fivegallon_qty < len(collected_coupon_ids):
                            # print("total_fivegallon_qty < len(collected_coupon_ids)", total_fivegallon_qty, "------------------------", len(collected_coupon_ids))
                            balance_coupon = Decimal(total_fivegallon_qty) - Decimal(len(collected_coupon_ids))
                            
                            customer_outstanding = CustomerOutstanding.objects.create(
                                customer=customer_supply.customer,
                                product_type="coupons",
                                created_by=request.user.id,
                            )
                            
                            customer_coupon = CustomerCouponStock.objects.filter(customer__pk=customer_supply_data['customer'],coupon_method="manual").first()
                            outstanding_coupon = OutstandingCoupon.objects.create(
                                count=balance_coupon,
                                customer_outstanding=customer_outstanding,
                                coupon_type=customer_coupon.coupon_type_id
                            )
                            outstanding_instance = ""

                            try:
                                outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="coupons")
                                outstanding_instance.value += Decimal(outstanding_coupon.count)
                                outstanding_instance.save()
                            except:
                                outstanding_instance = CustomerOutstandingReport.objects.create(
                                    product_type='coupons',
                                    value=outstanding_coupon.count,
                                    customer=outstanding_coupon.customer_outstanding.customer
                                )
                        
                        elif total_fivegallon_qty > len(collected_coupon_ids) :
                            balance_coupon = total_fivegallon_qty - len(collected_coupon_ids)
                            try :
                                outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="coupons")
                                outstanding_instance.value += Decimal(balance_coupon)
                                outstanding_instance.save()
                            except:
                                outstanding_instance=CustomerOutstandingReport.objects.create(
                                    product_type="coupons",
                                    value=balance_coupon,
                                    customer=customer_supply.customer,
                                    )
                            
                    elif Customers.objects.get(pk=customer_supply_data['customer']).sales_type == "CREDIT COUPON" :
                        pass
                    elif Customers.objects.get(pk=customer_supply_data['customer']).sales_type == "CASH" or Customers.objects.get(pk=customer_supply_data['customer']).sales_type == "CREDIT" :
                        if customer_supply.amount_recieved < customer_supply.subtotal:
                            balance_amount = customer_supply.subtotal - customer_supply.amount_recieved
                            
                            customer_outstanding = CustomerOutstanding.objects.create(
                                product_type="amount",
                                created_by=request.user.id,
                                customer=customer_supply.customer,
                            )

                            outstanding_amount = OutstandingAmount.objects.create(
                                amount=balance_amount,
                                customer_outstanding=customer_outstanding,
                            )
                            outstanding_instance = {}

                            try:
                                outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="amount")
                                outstanding_instance.value += Decimal(outstanding_amount.amount)
                                outstanding_instance.save()
                            except:
                                outstanding_instance = CustomerOutstandingReport.objects.create(
                                    product_type='amount',
                                    value=outstanding_amount.amount,
                                    customer=outstanding_amount.customer_outstanding.customer
                                )
                                
                        elif customer_supply.amount_recieved > customer_supply.subtotal:
                            balance_amount = customer_supply.amount_recieved - customer_supply.subtotal
                            
                            customer_outstanding = CustomerOutstanding.objects.create(
                                product_type="amount",
                                created_by=request.user.id,
                                customer=customer_supply.customer,
                            )

                            outstanding_amount = OutstandingAmount.objects.create(
                                amount=balance_amount,
                                customer_outstanding=customer_outstanding,
                            )
                            
                            outstanding_instance=CustomerOutstandingReport.objects.get(customer=customer_supply.customer,product_type="amount")
                            outstanding_instance.value -= Decimal(balance_amount)
                            outstanding_instance.save()
                            
                    # elif Customers.objects.get(pk=customer_supply_data['customer']).sales_type == "CREDIT" :
                        # pass
                        
                random_part = str(random.randint(1000, 9999))
                invoice_number = f'WTR-{random_part}'

                # Create the invoice
                invoice = Invoice.objects.create(
                    invoice_no=invoice_number,
                    created_date=datetime.today(),
                    net_taxable=customer_supply.net_payable,
                    vat=customer_supply.vat,
                    discount=customer_supply.discount,
                    amout_total=customer_supply.subtotal,
                    amout_recieved=customer_supply.amount_recieved,
                    customer=customer_supply.customer,
                    reference_no=reference_no
                )

                # Create invoice items
                for item_data in supply_items:
                    item = CustomerSupplyItems.objects.get(pk=item_data.pk)
                    InvoiceItems.objects.create(
                        category=item.product.category,
                        product_items=item.product,
                        qty=item.quantity,
                        rate=item.amount,
                        invoice=invoice,
                        remarks='invoice genereted from supply items reference no : ' + invoice.reference_no
                    )

                DiffBottlesModel.objects.filter(
                    delivery_date__date=date.today(),
                    assign_this_to=customer_supply.salesman_id,
                    customer=customer_supply.customer_id
                    ).update(status='supplied')

                if invoice:
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Customer Supply created successfully and Invoice generated.",
                        "invoice_id": str(invoice.invoice_no)
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Handle database integrity error
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": str(e),
            }

        except Exception as e:
            # Handle other exceptions
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": str(e),
            }
        else:
            response_data = {
                "status": "false",
                "title": "Error",
                "message": "Failed to generate Invoice."
            }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def customer_coupon_stock(request):
#     if (instances:=CustomerCouponStock.objects.all()).exists():

#         serializer = CustomerCouponStockSerializer(instances, many=True, context={"request": request})

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

class customerCouponStock(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if (customers:=Customers.objects.filter(sales_staff=request.user)).exists():
            route_id = request.GET.get("route_id")
            
            if route_id :
                customers = customers.filter(routes__pk=route_id)
                
            serialized_data = CustomerCouponStockSerializer(customers, many=True)
            
            status_code = status.HTTP_200_OK
            response_data = {
                "status": status_code,
                "StatusCode": 6000,
                "data": serialized_data.data,
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
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            print("user_id", user_id)
            customer_objs = Customers.objects.filter(sales_staff=user_id)
            
            serialized_data = []
            
            for customer_obj in customer_objs:
                custody_custom_objects = CustodyCustom.objects.filter(customer_id=customer_obj.customer_id)
                
                customer_products = []
                
                for custody_custom_obj in custody_custom_objects:
                    serialized_custody_custom = CustodyCustomSerializer(custody_custom_obj).data
                    
                    custody_items = CustodyCustomItems.objects.filter(custody_custom=custody_custom_obj).prefetch_related('product')
                    serialized_items = []
                    
                    for custody_item in custody_items:
                        product_name = custody_item.product.product_name if custody_item.product else None
                        serialized_item = CustodyCustomItemsSerializer(custody_item).data
                        serialized_item['product_name'] = product_name
                        serialized_items.append(serialized_item)
                    
                    customer_products.extend(serialized_items)
                
                serialized_data.append({
                    'customer': customer_obj.customer_id,
                    'products': customer_products
                })
            
            return Response({'status': True, 'data': serialized_data, 'message': 'Customer products list passed!'})
        
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
            custody_items = CustodyCustomItems.objects.filter(customer=customer_id)
            total_amount = custody_items.aggregate(total_amount=Sum('amount'))['total_amount']
            amount_paid = request.data['amount_paid']
            amount_paid = Decimal(amount_paid)
            balance = total_amount - amount_paid
            product = custody_items.first().product
            
            outstanding_amount = OutstandingAmount.objects.create(
                customer_id=customer_id,
                product=product,
                balance_amount=balance,
                amount_paid=amount_paid
            )

            serializer = self.serializer_class(outstanding_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": False, "data": str(e), "message": str(e) })


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

class VanStockAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        coupon_stock = VanCouponStock.objects.filter(van__salesman=request.user).exclude(count=0)
        product_stock = VanProductStock.objects.filter(van__salesman=request.user).exclude(count=0)
        coupon_serializer = VanCouponStockSerializer(coupon_stock, many=True)
        product_serializer = VanProductStockSerializer(product_stock, many=True)
        
        return Response({
            'coupon_stock': coupon_serializer.data,
            'product_stock': product_serializer.data
        }, status=status.HTTP_200_OK)

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
        customers = Customers.objects.filter(sales_staff=request.user)
        route_id = request.GET.get("route_id")
        
        if route_id :
            customers = customers.filter(routes__pk=route_id)
            
        serialized_data = CustomerOutstandingSerializer(customers, many=True)
        
        customer_outstanding = CustomerOutstandingReport.objects.filter(customer__in=customers)
        total_amount = customer_outstanding.filter(product_type="amount").aggregate(total=Coalesce(Sum('value'), Value(0)))['total']
        total_coupons = customer_outstanding.filter(product_type="coupons").aggregate(total=Coalesce(Sum('value'), Value(0)))['total']
        total_emptycan = customer_outstanding.filter(product_type="emptycan").aggregate(total=Coalesce(Sum('value'), Value(0)))['total']

        return Response({
            'status': True,
            'data': serialized_data.data,
            "total_amount": total_amount,
            "total_coupons": total_coupons,
            "total_emptycan": total_emptycan,
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

class ProductAndBottleAPIView(APIView):
    def get(self, request):
        date_string = request.query_params.get('date')
        try:
            if date_string:
                date = datetime.strptime(date_string, '%Y-%m-%d')
                product_items = ProdutItemMaster.objects.filter(created_date__date=date)
                customer_supply = CustomerSupply.objects.filter(created_date__date=date)
                van_coupon_stock = VanCouponStock.objects.filter(created_date__date=date)
            else:
                product_items = ProdutItemMaster.objects.all()
                customer_supply = CustomerSupply.objects.all()
                van_coupon_stock = VanCouponStock.objects.all()

            product_serializer = ProdutItemMasterSerializer(product_items, many=True)
            bottle_serializer = CustomerSupplySerializer(customer_supply, many=True)
            van_coupon_stock_serializer = VanCouponStockSerializer(van_coupon_stock, many=True)

            return Response({
                'product_name': product_serializer.data,
                'collected_empty_bottle': bottle_serializer.data,
                'van_coupon_stock': van_coupon_stock_serializer.data
            })
        except ValueError:
            return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=400)

class CollectionAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({
                'status': False,
                'message': 'User ID is required!'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter CustomerSupply objects based on the user
        collection = Customers.objects.filter(sales_staff=user)

        if collection.exists():
            collection_serializer = CollectionCustomerSerializer(collection, many=True)
            return Response({
                'status': True,
                'data': collection_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': 'No data found',
            }, status=400)

# class AddCollectionPayment(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         # Extract data from request
#         payment_method = request.data.get("payment_method")
#         amount_received = request.data.get("amount_received")
#         invoice_ids = request.data.get("invoice_ids")
#         customer_id = request.data.get("customer_id")
        
#         # Retrieve customer object
#         try:
#             customer = Customers.objects.get(pk=customer_id)
#         except Customers.DoesNotExist:
#             return Response({"message": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
#         # Create collection payment instance
#         collection_payment = CollectionPayment.objects.create(
#             payment_method=payment_method,
#             customer=customer,
#             salesman=request.user,
#             amount_received=amount_received,
#         )
        
#         # If payment method is cheque, handle cheque details
#         if payment_method == "CHEQUE":
#             cheque_data = request.data.get("cheque_details", {})
#             cheque_serializer = CollectionChequeSerializer(data=cheque_data)
#             if cheque_serializer.is_valid():
#                 cheque = cheque_serializer.save(collection_payment=collection_payment)
#             else:
#                 return Response(cheque_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         remaining_amount = amount_received
        
#         # Distribute the received amount among invoices
#         for invoice_id in invoice_ids:
#             invoice = Invoice.objects.get(pk=invoice_id)
#             balance_invoice_amount = invoice.amout_total - invoice.amout_recieved
            
#             # Check if a CollectionItems instance already exists for this invoice and collection payment
#             existing_collection_item = CollectionItems.objects.filter(invoice=invoice, collection_payment=collection_payment).first()
#             if existing_collection_item:
#                 # Update existing CollectionItems instance
#                 existing_collection_item.amount_received += min(balance_invoice_amount, remaining_amount)
#                 existing_collection_item.balance = invoice.amout_recieved - existing_collection_item.amount_received
#                 existing_collection_item.save()
#             else:
#                 # Create new CollectionItems instance
#                 CollectionItems.objects.create(
#                     invoice=invoice,
#                     amount=invoice.amout_total,
#                     balance=balance_invoice_amount,
#                     amount_received=min(balance_invoice_amount, remaining_amount),
#                     collection_payment=collection_payment
#                 )
            
#             remaining_amount -= min(balance_invoice_amount, remaining_amount)
            
#             # Update invoice status if fully paid
#             if invoice.amout_recieved >= invoice.amout_total:
#                 invoice.invoice_status = 'paid'
#                 print("paid")
            
#             invoice.save()
            
#             if remaining_amount <= 0:
#                 break

        
#         return Response({"message": "Collection payment saved successfully."}, status=status.HTTP_201_CREATED)

class AddCollectionPayment(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Extract data from request
        payment_method = request.data.get("payment_method")
        amount_received = Decimal(request.data.get("amount_received"))
        invoice_ids = request.data.get("invoice_ids")
        customer_id = request.data.get("customer_id")
        
        # Retrieve customer object
        try:
            customer = Customers.objects.get(pk=customer_id)
        except Customers.DoesNotExist:
            return Response({"message": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Use atomic transaction to ensure data consistency
        with transaction.atomic():
            # Create collection payment instance
            collection_payment = CollectionPayment.objects.create(
                payment_method=payment_method,
                customer=customer,
                salesman=request.user,
                amount_received=amount_received,
            )
            
            remaining_amount = amount_received
            # Iterate over invoice IDs
            for invoice_id in invoice_ids:
                try:
                    invoice = Invoice.objects.get(pk=invoice_id, customer=customer)
                except Invoice.DoesNotExist:
                    continue
                
                # Calculate the amount due for this invoice
                due_amount = invoice.amout_total - invoice.amout_recieved
                
                # If remaining_amount is greater than zero and there is still due amount for the current invoice
                if remaining_amount > Decimal('0') and due_amount > Decimal('0'):
                    # Calculate the payment amount for this invoice
                    payment_amount = min(due_amount, remaining_amount)
                    
                    # Update the invoice balance and amount received
                    invoice.amout_recieved += payment_amount
                    invoice.save()
                    
                    # Create CollectionItems instance
                    CollectionItems.objects.create(
                        invoice=invoice,
                        amount=invoice.amout_total,
                        balance=invoice.amout_total - invoice.amout_recieved,
                        amount_received=payment_amount,
                        collection_payment=collection_payment
                    )
                    
                    # Update the remaining amount
                    remaining_amount -= payment_amount
                    
                    # If the invoice is fully paid, update its status
                    if invoice.amout_recieved == invoice.amout_total:
                        invoice.invoice_status = 'paid'
                        invoice.save()
                else:
                    # Break the loop if there is no remaining amount or the current invoice is fully paid
                    break
            
            # If there is remaining amount after paying all invoices, adjust it with the outstanding balance
            # if remaining_amount > Decimal('0') :
            print("after brke")
            customer_outstanding = CustomerOutstanding.objects.create(
                        product_type="amount",
                        created_by=request.user.id,
                        customer=customer,
                    )

            outstanding_amount = OutstandingAmount.objects.create(
                    amount=remaining_amount,
                    customer_outstanding=customer_outstanding,
                )
            
            if CustomerOutstandingReport.objects.filter(customer=customer, product_type="amount").exists():
                    # Update the outstanding balance
                    outstanding_instance = CustomerOutstandingReport.objects.get(customer=customer, product_type="amount")
                    outstanding_instance.value -= remaining_amount
                    outstanding_instance.save()
            else:
                CustomerOutstandingReport.objects.create(
                    customer=customer, 
                    product_type="amount",
                    value=remaining_amount,
                    )
    
        return Response({"message": "Collection payment saved successfully."}, status=status.HTTP_201_CREATED)

    
class CouponTypesAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if not user:
            return Response({'status': False,'message': 'User ID is required!'}, status=status.HTTP_400_BAD_REQUEST)

        instances = CouponType.objects.all()

        if instances.exists():
            serialized = CouponTypeSerializer(instances, many=True)
            return Response({'status': True,'data': serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,'message': 'No data found'}, status=400)

class EmergencyCustomersAPI(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        
        emergency_customers = DiffBottlesModel.objects.all()
        print(emergency_customers,"emergency_customers")
        if emergency_customers.exists():
            serialized = EmergencyCustomersSerializer(emergency_customers, many=True)
            return Response({'status': True,'data': serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,'message': 'No data found'}, status=400)

