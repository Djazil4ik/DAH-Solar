from django.db import models

class Contact(models.Model):
    officeAddress = models.CharField(max_length=255)
    factoryAddress = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.officeAddress} | {self.factoryAddress} | {self.tel}"
