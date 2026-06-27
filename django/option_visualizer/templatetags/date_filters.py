import jdatetime
import datetime
from django import template

register = template.Library()

@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return ""
    
    try:
        if hasattr(value, "year"):
            jdate = jdatetime.date.fromgregorian(date=value)
            return jdate.strftime(fmt)
        else:
            return value
    except Exception:
        return value


@register.filter
def days_remaining(value):
    if not value:
        return ""
    
    today = datetime.date.today()
    if hasattr(value, "date"):
        value = value.date()
    
    return (value - today).days
            
    


