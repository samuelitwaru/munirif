import json
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.filter(name="comma_separator")
def comma_separator(value):
	if isinstance(value, int):
		return f'{value:,}'
	return value


@register.filter(name="multiply")
def multiply(value, arg):
	return value * arg


@register.filter(name="currency")
def currency(value):
	if isinstance(value, int):
		return f'{value:,} {settings.CURRENCY}'
	return value


@register.filter(name="total_cost")
def total_cost(item):
	return item.quantity * item.unit_cost


@register.filter(name="multiply")
def multiply(value, multiplier):
	return value * multiplier


@register.filter(name="has_attr")
def has_attr(object, attribute):
	return hasattr(object, attribute)


@register.filter(name="get_attr")
def get_attr(value, arg):
	if hasattr(value, str(arg)):
		return getattr(value, arg)


@register.filter(name="format_date")
def format_date(date):
	date = date.strftime("%d/%b/%Y %H:%M:%S")
	return date


@register.filter(name="html_date")
def html_date(date):
	date = date.strftime("%Y-%m-%d")
	return date


@register.filter(name='add_css')
def add_css(field, css):
	return field.as_widget(attrs={"class":css})


@register.filter(name='add_attrs')
def add_attrs(field, attrs):
	attrs = json.loads(attrs)
	return field.as_widget(attrs=attrs)


@register.filter(name="equal_to")
def equal_to(value, value2):
	return value == value2


@register.filter(name="not_equal_to")
def not_equal_to(value, value2):
	return value != value2


@register.simple_tag
def render_field(field, **kwargs):
	template_file = 'string-field.html'
	widget = field.field.widget
	context = {}
	if hasattr(widget, 'input_type'):
		if widget.input_type == 'checkbox':
			template_file = 'checkbox-field.html'
		elif field.field.widget.input_type == 'radio':
			template_file = 'radio-field.html'
		elif field.field.widget.input_type == 'number':
			tel_code = kwargs.pop("tel_code", None)
			if tel_code:
				context["tel_code_widget"] = tel_code.as_widget()
			template_file = 'tel-field.html'


	string_field_template = template.loader.get_template(f'widgets/{template_file}')
	as_widget = field.as_widget(attrs=kwargs)
	context["field"] = field
	context["as_widget"] = as_widget
	return string_field_template.render(context)



@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
