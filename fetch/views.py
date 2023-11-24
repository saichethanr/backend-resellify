
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import ProductSerializer,ReviewsSerializer,IssuesSerializer,CategorySerializer,CustomerSerializer,MerchantSerializer

class ProductDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
          SELECT
    pd.productid AS product_id,
    pd."productName" AS product_name,
    pd."productDesc" AS product_desc,
    pd."productDate" AS product_date,
    pd."productRating" AS product_rating,
    pd."productLife" AS product_life,
    pd."productPrice" AS product_price,
    pd."productImg" AS product_img,
    p.merchantid AS merchant_id,
    p."categoryid" AS category_id,
    c."categoryName" AS category_name
FROM
    public.productdetails pd
JOIN
    public.products p ON pd.productid = p.productid
JOIN
    public.categories c ON p.categoryid = c.categoryid;


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
            query="""SELECT rev.reviewid, rev."reviewRating", rev."customerid", rev."productid"
                FROM public.reviews rev"""
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
            query = """SELECT iss.issueid, iss."productid", iss."customerid", iss."issueDesc"
            FROM public.issues iss"""
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict=dict(zip([col[0] for col in cursor.description],row))
                serializer=IssuesSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)

class CategoryView(APIView):
    def get(self,request,*args,**kwargs):
        with connection.cursor() as cursor:
            query=""" SELECT c.categoryid,c."categoryName" FROM public.categories c"""
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict=dict(zip([col[0] for col in cursor.description],row))
                serializer=CategorySerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)
        
class CustomerView(APIView):
    def get(self,request,*args,**kwargs):
        with connection.cursor() as cursor:
            query="""SELECT c.customerid,c."customerName",c."customerNo",c."customerMail",c."customerPwd" FROM public.customers c"""
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict=dict(zip([col[0] for col in cursor.description],row))
                serializer=CustomerSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)

class MerchantView(APIView):
    def get(self,request,*args,**kwargs):
        with connection.cursor() as cursor:
            query="""SELECT m.merchantid,m."merchantName",m."merchantNo",m."merchantRating",m."merchantMail",m."merchantPwd" FROM public.merchants m"""
            cursor.execute(query)
            rows=cursor.fetchall()
            serialized_data=[]
            for row in rows:
                data_dict=dict(zip([col[0] for col in cursor.description],row))
                serializer=MerchantSerializer(data_dict)
                serialized_data.append(serializer.data)
            return Response(serialized_data)

