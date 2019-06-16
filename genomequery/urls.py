from django.urls import path

from genomequery.views import GenomeQueryAPIView

urlpatterns = [
    path('', GenomeQueryAPIView.as_view(), name='genome_query'),
]