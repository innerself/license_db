from datetime import date, timedelta

from django.db import models


class License(models.Model):
    name = models.CharField('name', max_length=200)
    type = models.ForeignKey(
        'LicenseType',
        on_delete=models.CASCADE,
    )
    subtype = models.ForeignKey(
        'LicenseSubtype',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField('quantity', default=0)
    expires = models.DateField('expires', default=date.today() + timedelta(days=365))
    comment = models.CharField('comment', max_length=200, blank=True)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def _generate(cls, number: int) -> None:
        from random import randint, choice
        from mimesis import Business, Text

        business = Business()
        text = Text()

        lic_types = (
            'software',
            'hardware',
        )

        for lic_type in lic_types:
            LicenseType.objects.create(
                name=lic_type,
            )

        for _ in range(number):
            License.objects.create(
                name=business.company(),
                type=choice(LicenseType.objects.all()),
                quantity=randint(0, 10000),
                comment=text.quote(),
            )

        return None


class LicenseType(models.Model):
    name = models.CharField('type', max_length=200)

    def __str__(self):
        return self.name


class LicenseSubtype(models.Model):
    name = models.CharField('subtype', max_length=200)

    def __str__(self):
        return self.name
