from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.db.models import RestrictedError
from django.db import connection
from django.contrib import messages as msg

from mixins import (
    ModuleAccesRedirectMixin, PermissionRequiredMixin, ManageModuleViewMixin,
    DeleteModelObjectMixin
)
from .models import PenHouse


class MainModule(ModuleAccesRedirectMixin, View):
    perm_link = (
        ('birds:manage_penhouse', 'birds.birds_manage_pen_house',),
        ('birds:manage_penhouse', 'birds.birds_manage_birds_stock',),
        ('birds:manage_penhouse', 'birds.birds_manage_medicine_feed',),
        ('birds:manage_penhouse', 'birds.birds_can_manage_mortality_cull',)
    )


class ManagePenhouseView(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'birds.birds_manage_pen_house'
    template = 'birds/penhouse/manage_penhouse.html'
    model = PenHouse
    values_list_cols = ('id', 'pen_number', 'pen_name', 'date_created', 'birdsstock__quantity')

    def get_query_set(self, pen_name=''):
        sql = """
                SELECT 
                    p.id,
                    p.pen_number,
                    p.pen_name,
                    p.date_created,
                    SUM(b.quantity) AS total_birds
                FROM
                    penhouse_model p
                        JOIN
                    birds_stock_model b ON p.pen_number = b.pen_house_id
                WHERE pen_name LIKE '%{}%'
                GROUP BY b.pen_house_id;
            """.format(pen_name)
        with connection.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    @property
    def query_set(self):
        if 'search' in self.request.GET and self.request.GET['search']:
            return self.get_query_set(self.request.GET['search'])
        return self.get_query_set()


class DeletePenhouseView(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'birds.birds_manage_pen_house'
    model = PenHouse
    success_url = 'birds:manage_penhouse'

    @property
    def get_success_url(self):
        if 'path' in self.request.POST and self.request.POST['path']:
            return self.request.POST['path']
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_model_object
        try:
            self.obj.delete()
            msg.success(request, 'Pen deleted successfully!')
        except RestrictedError as e:
            msg.error(request, e)
        return redirect(self.get_success_url)
