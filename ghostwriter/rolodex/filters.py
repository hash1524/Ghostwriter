"""This contains all the model filters used by the Rolodex application."""

# Django Imports
from django import forms
from django.db import ProgrammingError
from django.db.models import Q
from django.forms.widgets import TextInput

# 3rd Party Libraries
import django_filters
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Column, Div, Layout, Row, Submit

# Ghostwriter Libraries
from ghostwriter.rolodex.models import Client, Project, ProjectType


class ClientFilter(django_filters.FilterSet):
    """
    Filter :model:`rolodex.Client` model.

    **Fields**

    ``name``
        Case insensitive search of the model's ``name`` field
    ``codename``
        Case insensitive search of the model's ``codename`` field
    """

    name = django_filters.CharFilter(
        method="search_all_names",
        label="Application Name Contains",
        # Client -> Application
        widget=TextInput(
            attrs={
                "placeholder": "Partial Name, Short Name, or Code Name",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Client
        fields = ["name", "codename"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        # Layout the form for Bootstrap
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        PrependedText("name", '<i class="fas fa-filter"></i>'),
                        css_class="form-group col-md-12 mb-0",
                    ),
                    css_class="form-row",
                ),
                ButtonHolder(
                    HTML(
                        """
                        <a class="btn btn-info col-md-2" role="button" href="{%  url 'rolodex:client_create' %}">Create</a>
                        """
                    ),
                    Submit(
                        "submit_btn", "Filter", css_class="btn btn-primary col-md-2"
                    ),
                    HTML(
                        """
                        <a class="btn btn-outline-secondary col-md-2" role="button" href="{%  url 'rolodex:clients' %}">Reset</a>
                        """
                    ),
                ),
                css_class="justify-content-center",
            ),
        )

    def search_all_names(self, queryset, name, value):
        """
        Search for a value that appears in the :model:`rolodex.Client`
        `name`, `short_name`, or `codename` fields.
        """
        return queryset.filter(
            Q(name__icontains=value)
            | Q(short_name__icontains=value)
            | Q(codename__icontains=value)
        )


class ProjectFilter(django_filters.FilterSet):
    """
    Filter :model:`rolodex.Project` model.

    **Fields**

    ``start_date``
        Date filter for ``start_date`` values greater than provided value
    ``end_date``
        Date filter for ``end_date`` values less than provided value
    ``start_date_range``
        Date range filter for retrieving entries with matching ``start_date`` values
    ``complete``
        Boolean field for filtering incomplete projects based on the ``complete`` field
    ``codename``
        Case insensitive search of the model's ``codename`` field
    ``client``
        Case insensitive search of the model's ``client`` field
    """

    client = django_filters.CharFilter(
        label="Application Name Contains",
        # Client -> Application,
        method="search_all_client_names",
        widget=TextInput(
            attrs={
                "placeholder": "Partial Application Name",
                "autocomplete": "off",
            }
        ),
    )
    codename = django_filters.CharFilter(
        label="Activity Codename Contains",
        lookup_expr="icontains",
        widget=TextInput(
            attrs={
                "placeholder": "Partial Activity Codename",
                "autocomplete": "off",
            }
        ),
    )
    start_date = django_filters.DateFilter(
        lookup_expr="gte",
        field_name="start_date",
        label="Start Date",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "dateinput form-control"}
        ),
    )
    end_date = django_filters.DateFilter(
        lookup_expr="lte",
        field_name="end_date",
        label="End Date",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "dateinput form-control"}
        ),
    )
    start_date_range = django_filters.DateRangeFilter(
        label="Relative Start Date",
        field_name="start_date",
        empty_label="-- Relative Start Date --",
    )

    STATUS_CHOICES = (
        (0, "Active"),
        (1, "Completed"),
    )

    complete = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES, empty_label="All Projects", label="Activity Status"
    )

    PROJECT_TYPE_CHOICES = []
    try:
        for p_type in ProjectType.objects.all():
            PROJECT_TYPE_CHOICES.append((p_type.pk, p_type))
    # New installs will not have the ``ProjectType`` table yet and throw a ``ProgrammingError`` exception here
    except ProgrammingError:
        pass

    project_type = django_filters.ChoiceFilter(
        choices=PROJECT_TYPE_CHOICES,
        label="Project Type",
        field_name="project_type",
        empty_label="-- Project Type --",
    )

    class Meta:
        model = Project
        fields = [
            "complete",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        # Layout the form for Bootstrap
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        PrependedText("client", '<i class="fas fa-filter"></i>'),
                        css_class="form-group col-md-6 mb-0",
                    ),
                    Column(
                        PrependedText("codename", '<i class="fas fa-filter"></i>'),
                        css_class="form-group col-md-6 mb-0",
                    ),
                ),
                Row(
                    Column("project_type", css_class="form-group col-md-6 mb-0"),
                    Column("complete", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("start_date_range", css_class="form-group col-md-4 mb-0"),
                    Column(
                        PrependedText(
                            "start_date", '<i class="fas fa-hourglass-start"></i>'
                        ),
                        css_class="form-group col-md-4 mb-0",
                    ),
                    Column(
                        PrependedText(
                            "end_date",
                            '<i class="fas fa-hourglass-end"></i>',
                        ),
                        css_class="form-group col-md-4 mb-0",
                    ),
                    css_class="form-row",
                ),
                ButtonHolder(
                    HTML(
                        """
                        <a class="btn btn-info col-md-2" role="button"
                        href="{%  url 'rolodex:project_create_no_client' %}">Create</a>
                        """
                    ),
                    Submit(
                        "submit_btn", "Filter", css_class="btn btn-primary col-md-2"
                    ),
                    HTML(
                        """
                        <a class="btn btn-outline-secondary col-md-2" role="button"
                        href="{%  url 'rolodex:projects' %}">Reset</a>
                        """
                    ),
                ),
                css_class="justify-content-center",
            ),
        )

    def search_all_client_names(self, queryset, name, value):
        """
        Search for a value that appears in the :model:`rolodex.Client`
        `name`, `short_name`, or `codename` fields.
        """
        return queryset.filter(
            Q(client__name__icontains=value)
            | Q(client__short_name__icontains=value)
            | Q(client__codename__icontains=value)
        )
