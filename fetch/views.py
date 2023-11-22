
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import ProductSerializer,ReviewsSerializer,IssuesSerializer

class ProductDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
          SELECT pd.productid AS product_id, pd."productName" AS product_name, 
       pd."productDesc" AS product_desc, pd."productDate" AS product_date, 
       pd."productRating" AS product_rating, pd."productLife" AS product_life, 
       pd."productPrice" AS product_price, pd."productImg" AS product_img,
       p.merchantid AS merchant_id
FROM public.productdetails pd
JOIN public.products p ON pd.productid = p.productid;

            """
            cursor.execute(query)
            rows = cursor.fetchall()
            serialized_data = []
            for row in rows:
                data_dict = dict(zip([col[0] for col in cursor.description], row))
                serializer = ProductSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)
        
class ReviewsView(APIView):
    def get(self,request,*args,**kwargs):
        with connection.cursor() as cursor:
            query="""SELECT reviewid, reviewRating, customerid, productid
            FROM public.reviews"""
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict =dict(zip([col[0] for col in cursor.description],row))
                serializer=ReviewsSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)
        
class IssuesView(APIView):
    def get(self,request,*args,**kwargs):
        with connection.cursor() as cursor:
            query = """SELECT issueid, productid, customerid, issueDesc
            FROM public.issues """
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict=dict(zip([col[0] for col in cursor.description]),row)
                serializer=IssuesSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)

