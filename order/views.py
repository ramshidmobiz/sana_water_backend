from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer_Order
from .serializers import CustomerOrderSerializer

# class CustomerOrder(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = CustomerOrderSerializer(data=request.data)
#         print(serializer,"serializer")
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)