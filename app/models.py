from django.db import models
from model_utils import Choices
from django.db.models import Q

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'source_ip'),
    ('2', 'source_port'),
    ('3', 'destination_ip'),
    ('4', 'destination_port'),
    ('5', 'dns_record'),
    ('6', 'datetime_record'),
)


# Create your models here.
class CsvData(models.Model):
    source_ip = models.GenericIPAddressField()
    source_port = models.FloatField(
        blank=True
    )
    destination_ip = models.GenericIPAddressField()
    destination_port = models.FloatField(
        blank=True
    )
    dns_record = models.CharField(
        max_length=500
    )
    datetime_record = models.DateTimeField(
        blank=True
    )


def query_csv_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = CsvData.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(source_ip__icontains=search_value) |
                                   Q(datetime_record__icontains=search_value) |
                                   Q(dns_record__icontains=search_value))

    count = queryset.count()

    if length == -1:
        queryset = queryset.order_by(order_column)
    else:
        queryset = queryset.order_by(order_column)[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
