from datetime import date, timedelta

from django.db import models


class License(models.Model):
    TYPES = (
        ('hardware', 'hardware'),
        ('software', 'software'),
    )

    name = models.CharField('name', max_length=200)
    type = models.CharField('type', max_length=50, choices=TYPES)
    quantity = models.PositiveIntegerField('quantity', default=0)
    expires = models.DateField('expires', default=date.today() + timedelta(days=365))
    comment = models.CharField('comment', max_length=200, blank=True)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.id})'

    @classmethod
    def _generate(cls, number: int) -> None:
        from random import randint, choice
        from mimesis import Business, Text

        business = Business()
        text = Text()

        for _ in range(number):
            License.objects.create(
                name=business.company(),
                type=choice(cls.TYPES)[0],
                quantity=randint(0, 10000),
                comment=text.quote(),
            )
