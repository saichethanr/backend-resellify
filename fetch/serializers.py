from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source='productid')
    product_name = serializers.CharField(source='productName')
    product_desc = serializers.CharField(source='productDesc')
    product_date = serializers.DateField(source='productDate')
    product_rating = serializers.FloatField(source='productRating')
    product_life = serializers.IntegerField(source='productLife')
    product_price = serializers.IntegerField(source='productPrice')
    product_img = serializers.ImageField(source='productImg') 
    merchant_id = serializers.IntegerField(source='merchant_id')

    class Meta:
        fields = '__all__'
