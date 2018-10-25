from datetime import date

from django.db import models

from license_db.utils import year_after


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
    expires = models.DateField('expires', default=year_after())
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


class ExcelEntry:
    def __init__(
            self,
            name: str,
            category: str,
            location: str,
            expires: date=year_after(),
            lic_type: str='',
            quantity: int=0,
            comment: str='',
            exists: bool=False,
    ):
        self.name = name
        self.category = category
        self.location = location
        self.expires = expires
        self.type = lic_type
        self.quantity = quantity
        self.comment = comment
        self.exists = exists

    def __str__(self):
        return self.name
