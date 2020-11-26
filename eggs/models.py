from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class EggsModel(models.Model):
    pen = models.ForeignKey('birds.PenHouse', on_delete=models.RESTRICT, to_field='pen_number')
    date_created = models.DateField(auto_now_add=True)
    time = models.TimeField()
    quantity = models.IntegerField()
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.id} - {self.pen}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Egg'
        verbose_name_plural = 'Eggs'
        db_table = 'eggs_model'
        permissions = (
            ('manage_eggs', 'Can manage eggs custom'),
        )


class EggsModelAudit(models.Model):
    pen = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    time = models.TimeField()
    egg_id = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    action_flag = models.CharField(max_length=15)
    auth_user = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.pen}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Egg Audit'
        verbose_name_plural = 'Eggs Audit'
        db_table = 'eggs_audit_model'
        permissions = (
            ('manage_eggs_audit', 'Can manage eggs audit custom'),
        )
