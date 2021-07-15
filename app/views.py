import math

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models import CsvData, query_csv_by_args
from app.serializers import CsvSerializer

@login_required
def home(request):
    return render(request, 'home.html')


class CsvDataViewSet(viewsets.ModelViewSet):
    queryset = CsvData.objects.all()
    serializer_class = CsvSerializer

    def list(self, request, **kwargs):
        try:
            csv = query_csv_by_args(**request.query_params)
            serializer = CsvSerializer(csv['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = csv['draw']
            result['recordsTotal'] = csv['total']
            result['recordsFiltered'] = csv['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
