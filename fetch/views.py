
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import ProductSerializer

class ProductDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
             SELECT pd.productid AS product_id, pd.productName AS product_name, 
                   pd.productDesc AS product_desc, pd.productDate AS product_date, 
                   pd.productRating AS product_rating, pd.productLife AS product_life, 
                   pd.productPrice AS product_price, pd.productImg AS product_img,
                   p.merchantid AS merchant_id
            FROM public.productdetails pd
            JOIN public.products p ON pd.productid = p.productid
            """
            cursor.execute(query)
            result = cursor.fetchall()
            serializer = ProductSerializer(result, many=True)
            return Response(serializer.data)
