
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework.renderers import JSONRenderer
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
                    encode(pd."productImg", 'base64') AS product_img_base64,
                    pd."productImgType" AS product_img_type,
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
                print(type(data_dict))
                print(data_dict)
               
                if not data_dict['product_img_type']:
                    continue
                data_dict['product_img'] = data_dict['product_img_type'] + ',' + data_dict['product_img_base64']
                del data_dict['product_img_type']
                del data_dict['product_img_base64']
                serializer = ProductSerializer(data=data_dict)
                if serializer.is_valid():
                    serialized_data.append(serializer.validated_data)
                else:
                    print(serializer.errors)
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

class CustomerDetailsView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('customerid')

        with connection.cursor() as cursor:
            query = """
                SELECT * FROM public.customers
                WHERE customerid = %s
            """
            cursor.execute(query, [customer_id])
            customer_details = cursor.fetchone()

        if customer_details:
            response_data = {
                "customerid": customer_details[0],
                "customerName": customer_details[1],
                "customerNo": customer_details[2],
                "customerMail": customer_details[3],
            }
            return Response(response_data)
        else:
            return Response({"error": "Customer not found"}, status=404)
class MerchantDetailsView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, *args, **kwargs):
        data = request.data
        merchant_id = data.get('merchantid')
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM public.merchants
                WHERE merchantid = %s
            """
                cursor.execute(query, [merchant_id])
                merchant_details = cursor.fetchone()
                print("Merchant Details:", merchant_details)

            if merchant_details:
                response_data = {
                    "merchantid": merchant_details[0],
                    "merchantName": merchant_details[1],
                    "merchantNo": merchant_details[2],
                    "merchantRating": merchant_details[3],
                    "merchantMail": merchant_details[4],
                    }
                return Response(response_data)
            else:
                return Response({"error": "Merchant not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
