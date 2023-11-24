from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.db import connection
import random
from django.db import connection
from django.db import connection
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
class RegisterUserView(APIView):
    renderer_classes = [JSONRenderer]
    def generate_unique_merchant_id(self):
        while True:
            new_merchant_id = random.randint(2000, 2999)
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM merchants WHERE merchantid = %s", [new_merchant_id])
                count = cursor.fetchone()[0]
            if count == 0:
                break
        return new_merchant_id

    def generate_unique_customer_id(self):
        while True:
            new_customer_id = random.randint(1000, 1999)
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM customers WHERE customerid = %s", [new_customer_id])
                count = cursor.fetchone()[0]
            if count == 0:
                break
        return new_customer_id

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        is_merchant = data.get('isMerchant')
        phone_number = data.get('phoneNumber')
        password = data.get('password')
        merchant_code = data.get('merchantCode')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE \"customerMail\" = %s", [email])
            customer_exists = cursor.fetchone()

            cursor.execute("SELECT * FROM merchants WHERE \"merchantMail\"  = %s", [email])
            merchant_exists = cursor.fetchone()

        try:
            if customer_exists or merchant_exists:
                return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            if is_merchant and is_valid_merchant_code(merchant_code):
                new_merchant_id = self.generate_unique_merchant_id()
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO merchants VALUES (%s, %s, %s, %s, %s, %s)",
                                   [new_merchant_id, name, phone_number, 0, email, password])
            else:
                new_customer_id = self.generate_unique_customer_id()
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO customers  VALUES (%s, %s, %s, %s, %s)",
                                   [new_customer_id, name, phone_number, email, password])

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            import logging
            logging.error(f"Error creating user: {e}", exc_info=True)
            return Response({'message': 'Error creating user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_valid_merchant_code(merchant_code):
    
    merchant_codes = [123, 456, 789, 234, 567,890, 345, 678, 901, 432,765, 189, 543, 876, 210,654, 987, 321, 876, 543,210, 987, 654, 321, 123,456, 789, 234, 567, 890,345, 678, 901, 432, 765,
    189, 543, 876, 210, 654,
    987, 321, 876, 543, 210,
    987, 654, 321, 123, 456]  
    return merchant_code in merchant_codes

