from django import template
import re

register = template.Library()

@register.filter(name='getdate')
def getdate(value):
    print str(value)
    matchObj = re.match(r'([0-9]{4})-([0-9]{2})-([0-9]{2}).*', str(value), re.I | re.M)
    if matchObj:
        return "{}%{}%{}".format(matchObj.group(1),matchObj.group(2),matchObj.group(3))

