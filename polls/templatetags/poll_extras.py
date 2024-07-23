from django import template
import calendar
import datetime
register = template.Library()


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
@register.filter
def date_Pro(date):
    return f'{date} sasdasd'
