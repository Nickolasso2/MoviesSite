from django import template
from contact_app.forms import ContactForm

register = template.Library()

@register.inclusion_tag('contact_app/tags/_inc_footer.html')
def footer(categories, genres):
    return {'form' : ContactForm(), 'categories':categories, 'genres':genres}
