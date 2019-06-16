from rest_framework import serializers


class GenomeQuerySerializer(serializers.Serializer):
    query_text = serializers.CharField(max_length=300)