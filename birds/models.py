from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PenHouse(models.Model):
    date_created = models.DateField(auto_now_add=True)
    pen_number = models.IntegerField(unique=True)
    pen_name = models.CharField(max_length=60)
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f'#{self.pen_number} - {self.pen_name}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Penhouse'
        verbose_name_plural = 'Penhouse'
        db_table = 'penhouse_model'
        permissions = (
            ('birds_manage_pen_house', 'Can manage pen house custom'),
        )


class BaseModel(models.Model):
    date_created = models.DateField(auto_now_add=True)
    pen_house = models.ForeignKey(PenHouse, to_field='pen_number', on_delete=models.RESTRICT)
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f'#{self.id} - {self.pen_house}'

    class Meta:
        abstract = True


class BirdsStock(BaseModel):
    invoice_no = models.ForeignKey('finance.FinanceModel', on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.pen_house} - {self.invoice_no}'

    class Meta:
        verbose_name = 'Birds Stock'
        verbose_name_plural = 'Birds Stock'
        db_table = 'birds_stock_model'
        permissions = (
            ('birds_manage_birds_stock', 'Can manage bird stock custom'),
        )


class MedicineFeed(BaseModel):
    category_choices = (
        ('Medicine', 'Medicine'),
        ('Feed', 'Feed')
    )
    category = models.CharField(max_length=30, choices=category_choices)
    quantity = models.CharField(max_length=10)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Medicine/Feed'
        verbose_name_plural = 'Medicine/Feed'
        db_table = 'medicine_feed_model'
        permissions = (
            ('birds_manage_medicine_feed', 'Can manage medicine/feeds custom'),
        )


class MortalityCull(BaseModel):
    category_choices = (
        ('Mortality', 'Mortality'),
        ('Cull', 'Cull')
    )
    category = models.CharField(max_length=30, choices=category_choices)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Mortality/Cull'
        verbose_name_plural = 'Mortality/Culls'
        db_table = 'mortality_cull_model'
        permissions = (
            ('birds_can_manage_mortality_cull', 'Can manage mortality/culls custom'),
        )
