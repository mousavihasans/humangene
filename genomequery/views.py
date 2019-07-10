import datetime
import random

from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import generics, status

from genomequery.models import GenomeQuery, QueryItem, QueryTypeChoices
from genomequery.serializers import GenomeQuerySerializer


class GenomeQueryAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenomeQuerySerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        result = dict()
        req_status = status.HTTP_201_CREATED

        # check user have validate search query (free daily and available purched)
        genome_query = GenomeQuery.objects.filter(name='genome query').first()
        if not genome_query:
            return Response({'result': 'there is no query available'}, status=status.HTTP_400_BAD_REQUEST)

        num_of_daily_query_by_user = QueryItem.objects.filter(type=QueryTypeChoices.free_daily,
                                                              performed_by=request.user,
                                                              performed_at__gt=yesterday).count()

        if num_of_daily_query_by_user < genome_query.free_daily_number:
            #perform free
            q_result = self.perform_query(request, genome_query, 'sdfsdf', query_type=QueryTypeChoices.free_daily)
            result['q_result'] = q_result
            result['result'] = 'performed free daily query'

        elif QueryItem.objects.filter(type=QueryTypeChoices.created_manually,
                                      performed_by=request.user, performed_at=None).count() > 0:
            # performe a manually created
            q_result = self.perform_query(request, genome_query, 'sdfsdf', query_type=QueryTypeChoices.created_manually)
            result['q_result'] = q_result
            result['result'] = 'performed a manually created'
        elif QueryItem.objects.filter(type=QueryTypeChoices.bought_by_credit,
                                        performed_by=request.user, performed_at=None).count() > 0:
            # perform credit
            q_result = self.perform_query(request, genome_query, 'sdfsdf', query_type=QueryTypeChoices.bought_by_credit)
            result['q_result'] = q_result
            result['result'] = 'performe cridit'
        else:
            # return that the user should buy query item
            result['result'] = 'buy some query item'
            req_status = status.HTTP_200_OK

        headers = self.get_success_headers(serializer.data)

        return Response(result, status=req_status, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_query(self, request, genome_query, query_text, query_type=QueryTypeChoices.free_daily):
        if query_type == QueryTypeChoices.free_daily:
            QueryItem.objects.create(
                genome_query=genome_query,
                type=query_type,
                performed_by=request.user,
                performed_at=now(),
            )
        else:
            query_item = QueryItem.objects.filter(type=query_type,
                                                  performed_by=request.user,
                                                  performed_at=None).first()
            query_item.performed_at = now()
            query_item.save()

        # fake query result
        fake_items = [
            {
                'Sample ID': 'MOT2503',
                'Age': 'UNK',
                'Sex': 'UNK',
                'Phenotype': 'UNK',
                'family History': 'UNK',
                'Zygosity': 'hom',
                'Depth': '58',
                'Alt': 'T',
                'Diagnosis': '[617827]Immunodeficiency 55'
            },
            {
                'Sample ID': 'MOT2503',
                'Age': '25',
                'Sex': 'UNK',
                'Phenotype': 'H',
                'family History': 'Family Marriage-gangliosidosis-Mental Retardation-Congenital Heart Disease-Paralysis-Seizure-Blindness-Speech Problem',
                'Zygosity': 'hom',
                'Depth': '51',
                'Alt': 'T',
                'Diagnosis': '[616118]Macular degeneration, early-onset'
            },
            {
                'Sample ID': 'MOT2503',
                'Age': '1.5',
                'Sex': 'UNK',
                'Phenotype': 'Nephrotic Syndrome',
                'family History': 'Family Marriage-Paralysis',
                'Zygosity': 'hom',
                'Depth': '5',
                'Alt': 'T',
                'Diagnosis': '[603546]Spondyloepimetaphyseal dysplasia with joint laxity, type 2'
            },
            {
                'Sample ID': 'MOT2503',
                'Age': 'UNK',
                'Sex': 'UNK',
                'Phenotype': 'UNK',
                'family History': 'UNK',
                'Zygosity': 'hom',
                'Depth': '70',
                'Alt': 'T',
                'Diagnosis': '[616118]Macular degeneration, early-onset'
            },
        ]
        return [fake_items[random.randint(0, 3)] for x in range(0, random.randint(0, 50))]
