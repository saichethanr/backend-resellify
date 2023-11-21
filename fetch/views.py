# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import ProductDetailsWithMerchantSerializer

class ProductDetailsWithMerchantView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # Write your SQL query to fetch data from the database
            sql_query = """
            SELECT pd.*, p.merchantid AS merchant_id
            FROM public.productdetails pd
            JOIN public.products p ON pd.productid = p.productid
            """
            cursor.execute(sql_query)

            # Fetch all rows from the query result
            result = cursor.fetchall()

            # Serialize the data
            serializer = ProductDetailsWithMerchantSerializer(result, many=True)

            return Response(serializer.data)
