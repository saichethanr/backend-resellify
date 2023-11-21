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

    class Meta:
        fields = '__all__'
