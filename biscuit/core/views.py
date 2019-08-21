from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.utils.translation import ugettext_lazy as _
from .models import Person, Group
from .tables import PersonsTable, GroupsTable


def index(request):
    context = {}
    return render(request, 'core/index.html', context)

def error_handler(status):
    def real_handler(request, *args, **kwargs):
        context = {}

        context['status'] = status
        context['caption'] = _('Page not found')
        context['admins'] = settings.ADMINS

        if status == 404:
            context['message'] = _('This page does not exist. If you were redirected by a link on an external page, it is possible that that link was outdated.')
        elif status == 500:
            context['message'] = _('An unexpected error has occurred.')

        return render(request, 'error.html', context, status=status)

    return real_handler

@login_required
def persons(request):
    context = {}

    # Get all persons
    persons = Person.objects.all()

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context['persons_table'] = persons_table

    return render(request, 'core/persons.html', context)


@login_required
def person(request, id_, template):
    context = {}

    # Get person and check access
    try:
        person = Person.objects.get(pk=id_)
    except Person.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context['person'] = person

    # Get groups where person is member of
    groups = Group.objects.filter(members=id_)

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context['groups_table'] = groups_table

    return render(request, 'core/person_%s.html' % template, context)

@login_required
def group(request, id_, template):
    context = {}

    # Get group and check if it exist
    try:
        group = Group.objects.get(pk=id_)
    except Group.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context['group'] = group

    # Get group
    group = Group.objects.get(pk=id_)

    # Get members
    persons = group.members

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context['persons_table'] = persons_table

    return render(request, 'core/group_%s.html' % template, context)

@login_required
def groups(request):
    context = {}

    # Get all groups
    groups = Group.objects.all()

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context['groups_table'] = groups_table

    return render(request, 'core/groups.html', context)
