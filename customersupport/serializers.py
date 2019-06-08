from rest_framework import serializers

from customersupport.models import TrackTask


class TrackTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackTask
        fields = ('id', 'state', 'result', 'created_at', 'upload_result_at')
