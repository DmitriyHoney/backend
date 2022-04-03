from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование МО")

    def __str__(self):
        return f'({self.pk}) - {self.name}'
