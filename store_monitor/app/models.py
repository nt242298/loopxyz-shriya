# models.py

from django.db import models
from django.utils import timezone


class Store(models.Model):
    store_id = models.CharField(max_length=50, unique=True)
    timezone_str = models.CharField(max_length=100, default='America/Chicago')

    def __str__(self):
        return self.store_id


class BusinessHour(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day = models.IntegerField()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store} - {self.day}"


class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)  # active or inactive
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"{self.store} - {self.status} - {self.timestamp_utc}"
