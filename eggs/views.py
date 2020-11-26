from django.shortcuts import render, redirect
from django.contrib import messages as msg
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db.models import RestrictedError

from datetime import datetime as dt

from mixins import ModuleAccesRedirectMixin, PermissionRequiredMixin, ManageModuleViewMixin, DeleteModelObjectMixin
from .models import EggsModel
from .forms import EggsForm


class MainModuleView(ModuleAccesRedirectMixin, View):
    perm_link = (('eggs:manage_eggs', 'eggs.manage_eggs'),)


class ManageEggsView(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'eggs.manage_eggs'
    template = 'eggs/manage_eggs.html'
    model = EggsModel
    values_list_cols = ('id', 'pen__pen_name', 'date_created', 'time', 'quantity')
    order_col = 'id'
    form = EggsForm
    url_filter_kwargs = (
        ('search', 'pen'),
    )

    def post(self, request):
        path, form = request.POST['path'], self.form(request.POST)
        if form.is_valid():
            form.save()
            msg.success(request, 'Saved Successfully!')
        else:
            msg.error(request, form.errors)
        return redirect(path)

    @property
    def query_set(self):
        qs = super().query_set

        if ('date1' and 'date2') not in self.request.GET:
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


class UpdateEggView(PermissionRequiredMixin, View):
    perm = 'eggs.manage_eggs'

    def post(self, request, pk):
        path, form = request.POST['path'], EggsForm(request.POST, instance=get_object_or_404(EggsModel, pk=pk))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.auth_user = request.user
            obj.save()
            msg.success(request, 'Saved successfully!')
        else:
            msg.error(request, form.errors)
        return redirect(path)


class DeleteEggView(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'eggs.manage_eggs'
    model = EggsModel
    success_url = 'eggs:manage_eggs'

    @property
    def get_success_url(self):
        if 'path' in self.request.POST and self.request.POST['path']:
            return self.request.POST['path']
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_model_object
        try:
            self.obj.delete()
            msg.success(request, 'Deleted successfully!')
        except RestrictedError as e:
            msg.error(request, e)
        return redirect(self.get_success_url)
