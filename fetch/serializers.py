from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_desc = serializers.CharField()
    product_date = serializers.DateField()
    product_rating = serializers.FloatField()
    product_life = serializers.IntegerField()
    product_price = serializers.IntegerField()
    product_img = serializers.ImageField()  
    merchant_id = serializers.IntegerField()
    category_id=serializers.IntegerField()

class ReviewsSerializer(serializers.Serializer):
    reviewid=serializers.IntegerField()
    reviewRating=serializers.IntegerField()
    customerid=serializers.IntegerField()
    productid=serializers.IntegerField()

class IssuesSerializer(serializers.Serializer):
    issueid = serializers.IntegerField()
    productid = serializers.IntegerField()
    customerid = serializers.IntegerField()
    issueDesc = serializers.CharField()

class CategorySerializer(serializers.Serializer):
    categoryid=serializers.IntegerField()
    categoryName=serializers.CharField()

class CustomerSerializer(serializers.Serializer):
    customerid=serializers.IntegerField()
    customerName=serializers.CharField()
    customerNo=serializers.IntegerField()
    customerMail=serializers.CharField()
    customerPwd=serializers.CharField()

class MerchantSerializer(serializers.Serializer):
    merchantid=serializers.IntegerField()
    merchantName=serializers.CharField()
    merchantNo=serializers.IntegerField()
    merchantRating=serializers.IntegerField()
    merchantMail=serializers.CharField()
    merchantPwd=serializers.CharField()

         