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
from rest_framework.exceptions import APIException
import base64
import datetime
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
        email = data.get('email')
        password = data.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE \"customerMail\" = %s", [email])
            customer_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM merchants WHERE \"merchantMail\"  = %s", [email])
            merchant_exists = cursor.fetchone()

        if customer_exists:
            with connection.cursor() as cursor:
                cursor.execute("SELECT \"customerid\",\"customerName\",\"customerPwd\" FROM customers WHERE \"customerMail\" = %s", [email])
                customer_data = cursor.fetchone()

            if customer_data and self.verify_password(password, customer_data[2]):
                return Response({
                    'name': customer_data[1],
                    'authenticated': True,
                    'customerid': customer_data[0],
                    'merchant': False,
                    'customer': True
                })
        elif merchant_exists:
            with connection.cursor() as cursor:
                cursor.execute("SELECT \"merchantid\", \"merchantName\",\"merchantPwd\" FROM merchants WHERE \"merchantMail\" = %s", [email])
                merchant_data = cursor.fetchone()

            if merchant_data and self.verify_password(password, merchant_data[2]):
                return Response({
                    'name': merchant_data[1],
                    'authenticated': True,
                    'merchantid': merchant_data[0],
                    'merchant': True,
                    'customer': False
                })

       
        return Response({'authenticated': False})
    
    def verify_password(self, input_password, stored_password):
        return input_password == stored_password


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
        print(len(product_img))
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
                """, [product_id, merchant_id, category_id])
            product_img_type, product_img_str = product_img.split(',')
            product_img_bytes = base64.b64decode(product_img_str)
            
            with open('test.png', 'wb') as f:
                f.write(product_img_bytes)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO public.productdetails VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [product_id, product_name, product_desc, product_date, product_rating, product_life, product_price, product_img_bytes, product_img_type])
            return Response({"productadd": "true",'productid':product_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def generate_unique_product_id():
    while True:
        product_id = random.randint(4000, 4999)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM public.productdetails WHERE productid = %s", [product_id])
            count = cursor.fetchone()[0]
        if count == 0:
            return product_id

class CustomerOrdersView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('customerid')

       
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT o.orderid, pd."productName", p.merchantid, pd."productPrice"
            FROM public.orders o
            JOIN public.products p ON o.productid = p.productid
            JOIN public.productdetails pd ON p.productid = pd.productid
            WHERE o.customerid = %s""", [customer_id])
            orders = cursor.fetchall()

        response_data = [
            {
                "orderid": order[0],
                "productName": order[1],
                "merchantid": order[2],
                "productPrice": order[3]
            } for order in orders
        ]
        return Response(response_data)
    
class MerchantOrdersView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            merchant_id = data.get('merchantid')
            print(merchant_id)
            query = """
                SELECT o.orderid, o.customerid, c."customerName", pd."productName", pd."productPrice"
                FROM public.orders o
                JOIN public.customers c ON o.customerid = c.customerid
                JOIN public.products p ON o.productid = p.productid
                JOIN public.productdetails pd ON p.productid = pd.productid
                WHERE p.merchantid = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [merchant_id])
                orders = cursor.fetchall()
            response_data = [
                {
                    "orderid": order[0],
                    "customerid": order[1],
                    "customerName": order[2],
                    "ProductName": order[3],
                    "Price": order[4]
                } for order in orders
            ]
            return Response(response_data)

        except Exception as e:
            raise APIException(detail=str(e), code=500)
        


class RaiseIssueView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('customerid')
        product_id = data.get('productid')
        issue_desc = data.get('issueDesc')
        issue_id = self.generate_unique_issue_id()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO public.issues VALUES (%s, %s, %s, %s)",
                    [issue_id, product_id, customer_id, issue_desc]
                )
            return Response({"message": "Issue raised successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def generate_unique_issue_id(self):
        for issue_id in range(8000, 9000):
            if not self.issue_id_exists(issue_id):
                return issue_id
        raise ValueError("Unable to find a unique issueid in the specified range")

    def issue_id_exists(self, issue_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM public.issues WHERE issueid = %s", [issue_id])
            return cursor.fetchone()[0] > 0

class ViewIssuesView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('customerid')
        merchant_id = data.get('merchantid')

        if customer_id is not None:
            issues = self.get_issues_for_customer(customer_id)
        elif merchant_id is not None:
            issues = self.get_issues_for_merchant(merchant_id)
        else:
            return Response({"error": "Provide either customerid or merchantid"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"issues": issues}, status=status.HTTP_200_OK)

    def get_issues_for_customer(self, customer_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM public.issues WHERE customerid = %s",
                [customer_id]
            )
            columns = [col[0] for col in cursor.description]
            issues = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return issues

    def get_issues_for_merchant(self, merchant_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT i.* FROM public.issues i JOIN public.products p ON i.productid = p.productid WHERE p.merchantid = %s",
                [merchant_id]
            )
            columns = [col[0] for col in cursor.description]
            issues = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return issues
class OrdersView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('customerid')
        product_id = data.get('productid')
        order_id = self.generate_unique_order_id()
        order_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO public.orders VALUES (%s, %s, %s, %s)",
                [order_id, customer_id, product_id, order_date]
            )
        return Response({"orderid": order_id, "orderDate": order_date}, status=status.HTTP_201_CREATED)

    def generate_unique_order_id(self):
        while True:
            order_id = random.randint(5000, 5999)
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM public.orders WHERE orderid = %s", [order_id])
                if not cursor.fetchone():
                    break
        return order_id

class ReviewsView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            customer_id = data.get('customerid')
            product_id = data.get('productid')
            rating = data.get('rating')
            review_id = None
            with connection.cursor() as cursor:
                while review_id is None or self.review_id_exists(cursor, review_id):
                    review_id = random.randint(7000, 7999)
                cursor.execute(
                    """
                    INSERT INTO public.reviews
                    VALUES (%s, %s, %s, %s)
                    """,
                    [review_id, rating, customer_id, product_id]
                )

            return Response({'message': 'Review added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def review_id_exists(self, cursor, review_id):
        cursor.execute("SELECT COUNT(*) FROM public.reviews WHERE reviewid = %s", [review_id])
        return cursor.fetchone()[0] > 0

