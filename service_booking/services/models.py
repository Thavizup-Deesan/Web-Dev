from django.db import models

class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_name