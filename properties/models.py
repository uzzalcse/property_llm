# properties/models.py
from django.db import models

class Property(models.Model):
    property_title = models.CharField(max_length=255)
    rating = models.FloatField(null=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    room_type = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'hotels'
        managed = False

class PropertySummary(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    summary = models.TextField()
    
    class Meta:
        db_table = 'property_summaries'

class PropertyReview(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField()
    
    class Meta:
        db_table = 'property_reviews'