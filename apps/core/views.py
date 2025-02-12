from django.shortcuts import render

from apps.core.models import Section
from apps.configs.models import Config


def summary(request, year = 2567):
    sections = Section.objects.order_by("type", "number")
    config_fiscal_year = Config.objects.get(key = "fiscal-year")
    config_fiscal_year.value = year
    config_fiscal_year.save()
    
    context = {
        'sections': sections,
        'fiscal_year': year,
    }
    return render(request, 'core/summary.html', context)