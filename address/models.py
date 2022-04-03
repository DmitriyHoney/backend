from django.db import models


class AddressInfo(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return self.address