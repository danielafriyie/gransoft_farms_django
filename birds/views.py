from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.db.models import RestrictedError
from django.db import connection
from django.contrib import messages as msg

from datetime import datetime as dt

from mixins import (
    ModuleAccesRedirectMixin, PermissionRequiredMixin, ManageModuleViewMixin,
    DeleteModelObjectMixin
)
from .models import PenHouse, BirdsStock, MortalityCull, MedicineFeed
from .forms import PenHouseForm, BirdsStockForm, MortCullForm, MedFeedForm


class MainModule(ModuleAccesRedirectMixin, View):
    perm_link = (
        ('birds:manage_penhouse', 'birds.birds_manage_pen_house',),
        ('birds:manage_stock', 'birds.birds_manage_birds_stock',),
        ('birds:manage_mort_cull', 'birds.birds_can_manage_mortality_cull',),
        ('birds:manage_med_feed', 'birds.birds_manage_medicine_feed',),
    )


class CreateMixin:
    form = None
    module = ''

    def post(self, request):
        form, path = self.form(request.POST), request.POST['path']
        if form.is_valid():
            form.save()
            msg.success(request, f'{self.module} created successfully!')
        else:
            msg.error(request, form.errors)
        return redirect(path if path else 'birds:manage_penhouse')


class UpdateMixin:
    form = None
    model = None
    module = ''

    def post(self, request, pk):
        form, path = self.form(request.POST, instance=get_object_or_404(self.model, pk=pk)), request.POST['path']
        if form.is_valid():
            obj = form.save(commit=False)
            obj.auth_user = request.user
            obj.save()
            msg.success(request, f'{self.module} updated successfully!')
        else:
            msg.error(request, form.errors)
        return redirect(path if path else 'birds:manage_penhouse')


class DeleteMixin(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    module = ''

    @property
    def get_success_url(self):
        if 'path' in self.request.POST and self.request.POST['path']:
            return self.request.POST['path']
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_model_object
        try:
            self.obj.delete()
            msg.success(request, f'{self.module} deleted successfully!')
        except RestrictedError as e:
            msg.error(request, e)
        return redirect(self.get_success_url)


class ManageViewMixin(ManageModuleViewMixin):

    @property
    def query_set(self):
        qs = super().query_set

        if 'date1' and 'date2' not in self.request.GET:
            cd = dt.now().date()
            qs = qs.filter(date_created__gte=cd, date_created__lte=cd)

        return qs

    @property
    def get_context(self):
        context = super().get_context
        context.update({
            'form': self.form(initial={'auth_user': self.request.user}),
            'queryset': zip(context['paginator_pages'], [
                self.form(instance=get_object_or_404(self.model, pk=obj[0])) for obj in context['paginator_pages']
            ])
        })
        return context


####################################
#       PENHOUSE
###################################
class UpdatePenhouseView(PermissionRequiredMixin, UpdateMixin, View):
    perm = 'birds.birds_manage_pen_house'
    model = PenHouse
    form = PenHouseForm
    module = 'Pen'


class ManagePenhouseView(PermissionRequiredMixin, ManageViewMixin, CreateMixin, View):
    perm = 'birds.birds_manage_pen_house'
    template = 'birds/penhouse/manage_penhouse.html'
    model = PenHouse
    values_list_cols = ('id', 'pen_number', 'pen_name', 'date_created', 'birdsstock__quantity')
    module = 'Pen'
    form = PenHouseForm

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
                        LEFT JOIN
                    birds_stock_model b ON p.pen_number = b.pen_house_id
                WHERE pen_name LIKE '%{}%'
                GROUP BY p.id
                ORDER BY p.id ASC;
            """.format(pen_name)
        with connection.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    @property
    def query_set(self):
        if 'search' in self.request.GET and self.request.GET['search']:
            return self.get_query_set(self.request.GET['search'])
        return self.get_query_set()


class DeletePenhouseView(DeleteMixin):
    perm = 'birds.birds_manage_pen_house'
    model = PenHouse
    success_url = 'birds:manage_penhouse'
    module = 'Pen'


###################################
#       STOCK
##################################
class UpdateStockView(PermissionRequiredMixin, UpdateMixin, View):
    perm = 'birds:birds_manage_birds_stock'
    module = 'Stock'
    form = BirdsStockForm
    model = BirdsStock


class ManageStockView(PermissionRequiredMixin, ManageViewMixin, CreateMixin, View):
    perm = 'birds.birds_manage_birds_stock'
    template = 'birds/stock/manage_stock.html'
    model = BirdsStock
    values_list_cols = ('id', 'pen_house__pen_name', 'date_created', 'invoice_no__invoice_no', 'quantity')
    module = 'Stock'
    form = BirdsStockForm
    url_filter_kwargs = (
        ('search', 'pen_house__pen_name__icontains'),
        ('date1', 'date_created__gte'),
        ('date2', 'date_created__lte')
    )

    @property
    def get_context(self):
        context = super().get_context
        context.update({
            'queryset': zip(context['paginator_pages'], [
                self.form(instance=get_object_or_404(self.model, pk=obj[0]),
                          initial={'invoice_no': obj[3]}) for obj in context['paginator_pages']
            ])
        })
        return context


class DeleteStockView(DeleteMixin):
    perm = 'birds.birds_manage_birds_stock'
    model = BirdsStock
    success_url = 'birds:manage_stock'
    module = 'Stock'


###################################
#       MORTALITY / CULLS
###################################
class UpdateMortcullView(PermissionRequiredMixin, UpdateMixin, View):
    perm = 'bird:birds_can_manage_mortality_cull'
    model = MortalityCull
    form = MortCullForm
    module = 'Cull'


class ManageMortCullView(PermissionRequiredMixin, ManageViewMixin, CreateMixin, View):
    perm = 'bird:birds_can_manage_mortality_cull'
    template = 'birds/mort_culls/manage_mort_culls.html'
    model = MortalityCull
    values_list_cols = ('id', 'pen_house__pen_name', 'date_created', 'category', 'quantity')
    module = 'Cull'
    form = MortCullForm
    url_filter_kwargs = (
        ('category', 'category__icontains'),
        ('search', 'pen_house__pen_name__icontains'),
        ('date1', 'date_created__gte'),
        ('date2', 'date_created__lte')
    )


class DeleteMortCullView(DeleteMixin):
    perm = 'birds.birds_can_manage_mortality_cull'
    model = MortalityCull
    success_url = 'birds:manage_mort_cull'
    module = 'Cull'


#####################################
#       MEDICINE / FEED
#####################################
class UpdateMedicineFeedView(PermissionRequiredMixin, UpdateMixin, View):
    perm = 'birds:birds_manage_medicine_feed'
    module = 'Medicine/Feed'
    form = MedFeedForm
    model = MedicineFeed


class ManageMedicineFeedView(PermissionRequiredMixin, ManageViewMixin, CreateMixin, View):
    perm = 'birds:birds_manage_medicine_feed'
    template = 'birds/med_feed/manage_med_feed.html'
    model = MedicineFeed
    values_list_cols = ('id', 'pen_house__pen_name', 'date_created', 'category', 'quantity')
    module = 'Medicine/Feed'
    form = MedFeedForm
    url_filter_kwargs = (
        ('category', 'category__icontains'),
        ('search', 'pen_house__pen_name__icontains'),
        ('date1', 'date_created__gte'),
        ('date2', 'date_created__lte')
    )


class DeleteMedicineView(DeleteMixin):
    perm = 'birds:birds_manage_medicine_feed'
    module = 'Medicine/Feed'
    model = MedicineFeed
    success_url = 'birds:manage_med_feed'
