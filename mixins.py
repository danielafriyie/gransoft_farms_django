from django.core.exceptions import ImproperlyConfigured, FieldError, ObjectDoesNotExist
from django.contrib import messages as msg
from django.shortcuts import redirect, render
from django.db.models.base import ModelBase
from django.http import Http404
from django.core.paginator import Paginator

import re

from utils import dump_to_excel


class GetAttributeDataMixin:
    """
        Return data from class object attributes.
        It checks for attribute data type instance and not None or Null attributes.
        It first check for the attribute data type, it raise TypeError if the
        attribute is not an instance of the data type i.e:(attr_type) provided, then
        it checks if the attribute is not None or Null, if the attribute is None,
        it raise ImproperlyConfigured error.
    """

    def get_attribute_data(self, attribute, attr_type, attr_name):
        """
            :param attribute: class object attribute
            :param attr_type: data type of the attribute
            :param attr_name: attribute name or message to display to the user if attribute is  not provided
            :return: data
        """
        if attribute is not None:
            if isinstance(attribute, attr_type):
                return attribute
            raise TypeError(
                f"{self.__class__.__name__}: {attribute} is not an instance of {attr_type} "
                f"check {attribute} data type: ({attr_type}) or override get_data_attribute() method"
            )
        raise ImproperlyConfigured(
            f"{self.__class__.__name__} is missing {attr_name} attribute, define it or override "
            f"get_attribute_data() method"
        )


class GetModelObjectMixin(GetAttributeDataMixin):
    """
        Provide the ability to retrieve a single object for further manipulation.
    """

    model = None
    query_set = None
    p_key_url_kwarg = 'pk'
    extra_kwargs = None
    extra_kwargs_field = None

    @property
    def get_param_dict(self) -> dict:
        """
            Returns a dictionary to be used to query or get data from the query_set or model.
            The dictionary will be passed in as keyword argument using(**)
            :return: self.params
        """

        self.params = {}

        # check if pk is in the urlconf
        pk = self.kwargs.get(self.p_key_url_kwarg, False)
        if not pk:
            raise AttributeError(
                f'{self.__class__.__name__} is missing {self.p_key_url_kwarg} attribute in the URLConf'
            )
        self.params['pk'] = pk

        # check for extra_kwargs and extra_kwargs_field both of the has to be defined, one can't work
        # without the other, you have to define both or don't define any of them at all
        if self.extra_kwargs_field or self.extra_kwargs is not None:

            # check for extra_kwargs and extra_kwargs_field i.e. one can't work without the other
            if (self.extra_kwargs is None and self.extra_kwargs_field is not None) or (
                    self.extra_kwargs is not None and self.extra_kwargs_field is None):
                raise ImproperlyConfigured(
                    f'{self.__class__.__name__} is missing extra_kwargs or extra_kwargs_fields attribute '
                    f'or you defined only one, you have to define both or override'
                    f' get_param_dict() method or don\'t define any of them')

            # check if the extra_kwargs provided is in the URLConf
            extra_kwargs = self.kwargs.get(self.extra_kwargs, False)
            if not extra_kwargs:
                raise AttributeError(
                    f'{self.__class__.__name__} is missing {self.extra_kwargs} in the URLConf, check extra_kwargs'
                    f' attribute you defined or override get_param_dict() method.'
                )

            # check if extra_kwargs_field exist in the model or queryset
            try:
                self.get_query_set.values_list(self.extra_kwargs_field)
                self.params[self.extra_kwargs_field] = extra_kwargs
            except FieldError:
                raise FieldError(
                    f'{self.__class__.__name__}: {self.extra_kwargs_field} is not a field in'
                    f' {self.model.__name__ if self.model else self.get_query_set} '
                    f'check extra_kwargs_field attribute you defined'
                )

        return self.params

    @property
    def get_query_set(self):
        """
            Returns Queryset to be used to look up for the model object
        """
        return self.get_model._default_manager.all() if self.query_set is None else self.query_set

    @property
    def get_model(self):
        """
            Returns self.model attribute provided by the user
        """
        return self.get_attribute_data(self.model, ModelBase, 'model or query_set')

    @property
    def get_model_object(self):
        """
            Return the model object the view is displaying.

            Require `self.queryset` and a `pk` or `self.extra_kwargs` argument in the URLConf.
            Subclasses can override this to return any object.
        """
        try:
            obj = self.get_query_set.get(**self.get_param_dict)
            return obj
        except ObjectDoesNotExist:
            raise Http404(
                f'No {self.get_query_set.model.__name__} matches the given query: {self.get_param_dict}'
            )


class DeleteMixin(GetModelObjectMixin):

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_model_object
        self.get_success_message()
        self.obj.delete()
        return redirect(self.get_success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class DeleteModelObjectMixin(DeleteMixin):
    """
        Deletes model instance or data or object from a model
    """
    success_url = None
    values_list = None

    def get_success_message(self) -> msg:
        """
            Return success message to display to the user on the frontend
        """
        name = self.get_name if self.get_name else ""
        return msg.success(self.request, f'{name} deleted successfully!')

    @property
    def get_success_url(self) -> str:
        """
            Check if success url is provided then returns it
        """
        return self.get_attribute_data(self.success_url, str, 'success_url')

    @property
    def get_name(self) -> str:
        if self.values_list:
            try:
                name = self.get_query_set.values_list(self.values_list).get(**self.get_param_dict)[0]
                return name
            except IndexError:
                pass
            except ObjectDoesNotExist:
                pass
            except FieldError:
                pass
            except Http404:
                pass


class PermissionRequiredMixin(GetAttributeDataMixin):
    """
        check if user has required permission privileges
    """

    perm = None
    perms = None
    permission_denied_message = 'Access Denied!'

    def _has_perm(self, user):
        if self.perm and self.perms:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__}: both 'perm' and 'perms' defined. Define only one."
            )
        if self.perm:
            return user.has_perm(self.perm)
        if self.perms:
            for perm in self.perms:
                if user.has_perm(perm):
                    return True

    def dispatch(self, request, *args, **kwargs):
        assert hasattr(request, 'user')
        if not self._has_perm(request.user):
            msg.warning(request, self.permission_denied_message)
            return redirect('home:homepage')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        assert hasattr(request, 'user')
        if not request.user.is_admin:
            msg.warning(request, 'Access Denied!')
            return redirect('home:homepage')
        return super().dispatch(request, *args, **kwargs)


class ExcludeUrlKwargsMixin:
    """
    Exclude kwargs in urls from the url.
    >>> url = '/someurl/?page=4'
    >>> url = self._exclude_url_kwargs(url)
    >>> url
    >>> '/someurl/'
    """
    exclude_url_kwargs_pattern = r'&page=\d*'

    def _any(self, *args):
        for arg in args:
            if arg in self.request.GET:
                return True

    def _exclude_url_kwargs(self, *url_kwargs):
        if self._any(*url_kwargs):
            query_path = self.request.get_full_path()
            exclude_url_kwargs = re.compile(self.exclude_url_kwargs_pattern).findall(query_path)
            if exclude_url_kwargs:
                for url_kwarg in exclude_url_kwargs:
                    query_path = query_path.strip(url_kwarg)
            return query_path


class ReportViewMixin(ExcludeUrlKwargsMixin):
    """
    View for creating report with a return rendered by template attribute.
    """
    template = None  # template to render
    excel_cols = None  # column names for the excel file
    query_cols = None  # columns to select from
    request_kwarg = 'export'
    model = None
    exclude_kwargs = None  # columns or rows to exclude from the queryset
    order_col = 'id'
    export_filename = None
    date1_request_kwarg = 'date1'
    date2_request_kwarg = 'date2'
    filter_date_field = 'date_created'
    url_filter_kwargs = None

    def get(self, request):
        if self.request_kwarg in request.GET:
            return dump_to_excel(self.query_set, self.excel_cols, self.export_filename)
        return render(request, self.template, self.context)

    def query_set_data(self, **extra_filtering):
        extra_filtering.update(self.exclude_kwargs) if self.exclude_kwargs else None
        return self.model.objects.order_by(self.order_col).values_list(
            *self.query_cols).filter(**extra_filtering)

    @property
    def query_set(self):
        if (self.date1_request_kwarg and self.date2_request_kwarg) in self.request.GET:
            filter_dict = {}
            filter_dict.update({
                f"{self.filter_date_field}__gte": self.request.GET[self.date1_request_kwarg],
                f'{self.filter_date_field}__lte': self.request.GET[self.date2_request_kwarg]
            })

            if self.url_filter_kwargs:
                for kwarg, field in self.url_filter_kwargs:
                    if kwarg in self.request.GET and self.request.GET[kwarg]:
                        filter_dict.update({field: self.request.GET[kwarg]})

            return self.query_set_data(**filter_dict)

    @property
    def context(self):
        try:
            paginator, page = Paginator(self.query_set, 25), self.request.GET.get('page')
            paginator_pages = paginator.get_page(page)

            query_path = self._exclude_url_kwargs(self.date1_request_kwarg, self.date2_request_kwarg)

            return {
                'paginator_pages': paginator_pages,
                'values': self.request.GET,
                'query_path': query_path
            }
        except TypeError:
            return {}


class ManageModuleViewMixin(ExcludeUrlKwargsMixin):
    template = None  # template to render
    model = None  # model to use
    values_list_cols = None  # list columns to select from
    order_col = None  # column to use to order the queryset
    url_filter_kwargs = None  # extra filtering kwarg and field in the database
    extra_context = None  # additional context to pass to the template

    def get(self, request):
        return render(request, self.template, self.get_context)

    @property
    def query_set(self):
        qs = self.model.objects.all()
        if self.order_col:
            qs = qs.order_by(self.order_col)
        if self.values_list_cols:
            qs = qs.values_list(*self.values_list_cols)

        filter_kwargs = {}

        if self.url_filter_kwargs:
            for kwarg, field in self.url_filter_kwargs:
                if kwarg in self.request.GET and self.request.GET[kwarg]:
                    filter_kwargs.update({field: self.request.GET[kwarg]})

        return qs.filter(**filter_kwargs) if filter_kwargs else qs

    @property
    def get_context(self):
        page = self.request.GET.get('page')
        paginator = Paginator(self.query_set, 25)
        paginator_pages = paginator.get_page(page)

        exclude_url_kwargs = [i[0] for i in self.url_filter_kwargs] if self.url_filter_kwargs else None

        context = {
            'paginator_pages': paginator_pages,
            'values': self.request.GET,
            'query_path': self._exclude_url_kwargs(*exclude_url_kwargs) if exclude_url_kwargs else None
        }
        context.update(self.extra_context) if self.extra_context else None

        return context


class ModuleAccesRedirectMixin:
    """
    Redirects a user to requested module (the user will be redirected to the earliest or first
    available sub module which he has access or has required permission to access in the main module).
    perm_link attribute is a tuple containing tuples of sub modules link and their required permission
    """
    perm_link = None
    permission_denied_message = 'Access Denied!'

    @property
    def _get_latest_sub_module_link(self):
        if not self.perm_link:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing 'perm_link' attribute, define it"
                f"or override '_get_latest_sub_module_link' method."
            )
        user = self.request.user
        for link, perm in self.perm_link:
            if user.has_perm(perm):
                return redirect(link)
        msg.warning(self.request, self.permission_denied_message)
        return redirect('home:homepage')

    def get(self, request):
        return self._get_latest_sub_module_link
