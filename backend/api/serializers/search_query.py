from rest_framework import serializers
from ..models import SearchQuery

class SearchQuerySerializer(serializers.ModelSerializer):
    """Serializer for SearchQuery model"""
    class Meta:
        model = SearchQuery
        fields = '__all__'
