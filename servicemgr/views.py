from django.shortcuts import render
from django.views.generic import (View, ListView, DetailView, TemplateView)
from djangohelpers.views import FilterByQueryParamsMixin

# import models
from servicemgr.models import (Owner, Service)


class ServicemgrBaseListView(FilterByQueryParamsMixin, ListView):
    """ base view for servicemgr list pages """
    title = None
    table = None
    modals = None

    def get(self, request, *args, **kwargs):
        context = dict()
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = self.title
        context['sub_title'] = self.page_description
        context['table'] = self.table
        context['modals'] = self.modals
        return render(request, template, context=context)


class ListOwners(ServicemgrBaseListView):
    """ list available Owners entries """
    queryset = Owner.objects.all()
    title = "Owners"
    page_description = ""
    table = "table/table_owners.htm"


class ListServices(ServicemgrBaseListView):
    """ list available Service entries """
    queryset = Service.objects.all().select_related('owner').prefetch_related('host_set')
    title = "Services"
    page_description = ""
    table = "table/table_services.htm"


class DetailServiceControls(DetailView):
    """ display control details of a specific service """
    model = Service
    template_name = "detail/detail_service_controls.html"
    queryset = model.objects.all()


class DetailServiceStatus(DetailView):
    """ display status details of a specific service """
    model = Service
    template_name = "detail/detail_service_status.html"
    queryset = model.objects.all()

