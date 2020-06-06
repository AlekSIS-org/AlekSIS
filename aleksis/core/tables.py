from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A


class SchoolYearTable(tables.Table):
    """Table to list persons."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("edit_school_year", args=[A("id")])
    date_start = tables.Column()
    date_end = tables.Column()
    edit = tables.LinkColumn(
        "edit_school_year",
        args=[A("id")],
        text=_("Edit"),
        attrs={"a": {"class": "btn-flat waves-effect waves-orange orange-text"}},
        verbose_name=_("Actions"),
    )


class PersonsTable(tables.Table):
    """Table to list persons."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    first_name = tables.LinkColumn("person_by_id", args=[A("id")])
    last_name = tables.LinkColumn("person_by_id", args=[A("id")])


class GroupsTable(tables.Table):
    """Table to list groups."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("group_by_id", args=[A("id")])
    short_name = tables.LinkColumn("group_by_id", args=[A("id")])
    school_year = tables.Column()


class GroupTypesTable(tables.Table):
    """Table to list group types."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("edit_group_type_by_id", args=[A("id")])
    description = tables.LinkColumn("edit_group_type_by_id", args=[A("id")])
    delete = tables.LinkColumn(
        "delete_group_type_by_id", args=[A("id")], verbose_name=_("Delete"), text=_("Delete")
    )
