from django.db import models

# Create your models here.

#### Calculation
class RunModel(models.Model):
    title = models.CharField(max_length=200)
    runID = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    lastedited = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title +'.' + self.runID