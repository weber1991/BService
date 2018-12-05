from django import template

register = template.Library()


@register.filter()
def sweat_change(value):
    try:
        if value:
            strlist = value.split('-',1)
            class_int = strlist[0]
            seat_int = strlist[1]
            return '第%s试室%s号'%(class_int, seat_int)
        else:
            return ''
    except:
        return ''

@register.filter()
def zkzh_create(value):
    try:
        if value:
            strlist = value.split('-',1)
            return strlist[0]+strlist[1]
        else:
            return ''
    except:
        return ''


@register.filter()
def get_class(value):
    try:
        strlist = value.split('-',1)
        return '第%s试室'%(strlist[0])
    except:
        return ''

@register.filter()
def get_seat(value):
    try:
        strlist = value.split('-', 1)
        return strlist[1]
    except:
        return ''