from datetime import date, timedelta

from django.db import models


class License(models.Model):
    name = models.CharField('name', max_length=200)
    category = models.ForeignKey(
        'LicenseCategory',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        'LicenseLocation',
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        'LicenseType',
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

        lic_categories = (
            'software',
            'hardware',
        )

        for lic_category in lic_categories:
            LicenseCategory.objects.create(
                name=lic_category,
            )

        lic_locations = (
            'store',
            'central office',
            'data center',
        )

        for lic_location in lic_locations:
            LicenseLocation.objects.create(
                name=lic_location,
            )

        for _ in range(number):
            License.objects.create(
                name=business.company(),
                category=choice(LicenseCategory.objects.all()),
                location=choice(LicenseLocation.objects.all()),
                quantity=randint(0, 10000),
                comment=text.quote(),
            )

        return None


class LicenseCategory(models.Model):
    name = models.CharField('category', max_length=200, unique=True)

    def __str__(self):
        return self.name


class LicenseLocation(models.Model):
    name = models.CharField('location', max_length=200, unique=True)

    def __str__(self):
        return self.name


class LicenseType(models.Model):
    name = models.CharField('type', max_length=200, unique=True)

    def __str__(self):
        return self.name
