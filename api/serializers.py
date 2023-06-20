from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import *


class RecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = photos
        fields = '__all__'
        read_only_fields = ['name', 'model_recognition']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = car_model
        fields = ['id', 'title']
        read_only_fields = ['company_id']   # Поле company_id не будет доступно для заполения


class GenerationSerializer(serializers.ModelSerializer):
    engine = serializers.SlugRelatedField(queryset=engines.objects.all(), slug_field='title', many=True)

    class Meta:
        model = generations
        fields = ['id', 'title', 'year_start', 'year_end', 'engine']
        read_only_fields = ['car_model_id']
        # fields = "__all__"

    def validate(self, attrs):
        if attrs['year_start'] > attrs['year_end']:
            raise serializers.ValidationError('Year start must be less than Year end')
        return attrs


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = engines
        fields = '__all__'


class EngineParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = engine_params
        # fields = ['engine']
        fields = '__all__'


