from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    """
    A custom serializer field to handle base64-encoded images.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temporary_image.{ext}')
        elif data is None:
            data = ContentFile('', name='empty_file.txt')

        return super().to_internal_value(data)


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_desc = serializers.CharField()
    product_date = serializers.DateField()
    product_rating = serializers.FloatField()
    product_life = serializers.IntegerField()
    product_price = serializers.IntegerField()
    product_img =serializers.CharField()
    merchant_id = serializers.IntegerField()
    category_id=serializers.IntegerField()
    category_name=serializers.CharField()

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

         