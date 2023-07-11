from django import template
from datetime import date

register = template.Library()

@register.filter
def formatear_numero(value):
    value = round(value)
    value = f'{value:,}'
    value = value.replace(',', '.')
    return value

@register.filter
def formatear_dinero(value):
    value = round(value)
    value = f'${value:,}'
    value = value.replace(',', '.')
    return value

@register.filter
def formatear_porcentaje(value):
    return f'{value}%'

@register.filter
def formatear_fecha(value):
    if value == None:
        value = '--/--/----'
    else:
        value = value.strftime("%d/%m/%Y")
    return f'{value}'
