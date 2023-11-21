
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import ProductSerializer

class ProductDetailsWithMerchantView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
            SELECT pd.*, p.merchantid AS merchant_id
            FROM public.productdetails pd
            JOIN public.products p ON pd.productid = p.productid
            """
            cursor.execute(query)
            result = cursor.fetchall()
            serializer = ProductSerializer(result, many=True)
            return Response(serializer.data)
