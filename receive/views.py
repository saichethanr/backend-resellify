from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.db import connection
import random
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.hashers import check_password 
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
        print(is_merchant)
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
                return Response({'authenticated': True,'merchantid':new_merchant_id}, status=status.HTTP_201_CREATED)
            else:
                new_customer_id = self.generate_unique_customer_id()
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO customers  VALUES (%s, %s, %s, %s, %s)",
                                   [new_customer_id, name, phone_number, email, password])
                return Response({'authenticated': True,'customerid':new_customer_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            import logging
            logging.error(f"Error creating user: {e}", exc_info=True)
            return Response({'message': 'Error creating user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_valid_merchant_code(merchant_code):
        merchant_codes = ["123", "456", "789", "234", "567","890", "345", "678", "901", "432","765", "189", "543", "876", "210","654", "987", "321", "876", "543","210", "987", "654", "321", "123","456", "789", "234", "567", "890","345", "678", "901", "432", "765",
        "189", "543", "876", "210", "654","987", "321", "876", "543", "210","987", "654", "321", "123", "456"]  
        return merchant_code in merchant_codes



class LoginUserView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        mail = data.get('mail')
        password = data.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE \"customerMail\" = %s", [mail])
            customer_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM merchants WHERE \"merchantMail\"  = %s", [mail])
            merchant_exists = cursor.fetchone()

        if customer_exists:
            with connection.cursor() as cursor:
                cursor.execute("SELECT customerid, customerPwd FROM customers WHERE \"customerMail\" = %s", [mail])
                customer_data = cursor.fetchone()

            if customer_data and check_password(password, customer_data[1]):
                return Response({
                    'authenticated': True,
                    'customerid': customer_data[0],
                    'merchant': False,
                    'customer': True
                })
        elif merchant_exists:
            with connection.cursor() as cursor:
                cursor.execute("SELECT merchantid, merchantPwd FROM merchants WHERE \"merchantMail\" = %s", [mail])
                merchant_data = cursor.fetchone()

            if merchant_data and check_password(password, merchant_data[1]):
                return Response({
                    'authenticated': True,
                    'merchantid': merchant_data[0],
                    'merchant': True,
                    'customer': False
                })
        return Response({'authenticated': False})

class ProductView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        data = request.data
        product_id = generate_unique_product_id()
        product_name = data.get('product_name')
        product_desc = data.get('product_desc')
        product_date = data.get('product_date')
        product_rating = data.get('product_rating')
        product_life = data.get('product_life')
        product_price = data.get('product_price')
        product_img = data.get('product_img')
        category_name = data.get('category_name')
        merchant_id = data.get('merchant_id')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT categoryid FROM public.categories
                    WHERE "categoryName" = %s
                """, [category_name])
                result = cursor.fetchone()
                if result:
                    category_id = result[0]
                else:
                    return Response({"error": f"Category '{category_name}' not found."}, status=status.HTTP_400_BAD_REQUEST)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO public.products
                    VALUES (%s, %s, %s)
                """, [product_id, 2608, category_id])

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO public.productdetails VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [product_id, product_name, product_desc, product_date, product_rating, product_life, product_price, product_img])
            return Response({"productadd": "true",'productid':product_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def generate_unique_product_id():
    while True:
        product_id = random.randint(4000, 4999)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM public.productdetails WHERE productid = %s", [product_id])
            count = cursor.fetchone()[0]
        if count == 0:
            return product_id

