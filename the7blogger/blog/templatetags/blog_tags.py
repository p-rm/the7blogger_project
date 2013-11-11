from django import template

#import datetime

register = template.Library()


@register.simple_tag
def convert_posted_date(datetime):
    try:
        return datetime.strftime("%B %d, %Y")
    except UnicodeEncodeError:
        return ''


@register.tag(name="upper")
def do_upper(parser, token):
    nodelist = parser.parse(('endupper',))
    parser.delete_first_token()
    return UpperNode(nodelist)


@register.tag
class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()
