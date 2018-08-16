from datetime import date, timedelta

from django.db import models


class License(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    expires = models.DateField(default=date.today() + timedelta(days=365))
    comment = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.id})'

    @classmethod
    def _generate(cls, number: int) -> None:
        from random import randint
        from mimesis import Business, Text

        business = Business()
        text = Text()

        for _ in range(number):
            License.objects.create(
                name=business.company(),
                quantity=randint(0, 10000),
                comment=text.quote(),
            )
