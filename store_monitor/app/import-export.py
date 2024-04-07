# import_export.py

import csv
from datetime import timedelta
from pytz import timezone as pytz_timezone
from django.utils import timezone
from .models import Store, BusinessHour, StoreStatus
from .serializers import StoreSerializer, BusinessHourSerializer, StoreStatusSerializer


def import_store_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            serializer = StoreSerializer(data=row)
            if serializer.is_valid():
                serializer.save()


def import_business_hour_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            serializer = BusinessHourSerializer(data=row)
            if serializer.is_valid():
                serializer.save()


def import_store_status_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            serializer = StoreStatusSerializer(data=row)
            if serializer.is_valid():
                serializer.save()


def extrapolate_store_status():
    for store in Store.objects.all():
        business_hours = BusinessHour.objects.filter(store=store)
        for business_hour in business_hours:
            start_time_utc = timezone.datetime.combine(timezone.now(), business_hour.start_time_local)
            end_time_utc = timezone.datetime.combine(timezone.now(), business_hour.end_time_local)
            current_time = start_time_utc
            while current_time <= end_time_utc:
                store_status, created = StoreStatus.objects.get_or_create(
                    store=store,
                    timestamp_utc=current_time,
                    defaults={'status': 'inactive'}
                )
                if not created:
                    continue
                current_time += timedelta(hours=1)
