from django import template


register = template.Library()


@register.filter(name="length_is")
def length_is(value, arg):
	"""Compatibility filter: return True if len(value) == int(arg).

	Restores the historic Django 'length_is' filter removed in newer versions,
	so third-party/admin templates that still use it continue to work.
	"""
	try:
		return len(value) == int(arg)
	except (TypeError, ValueError):
		try:
			return len(value) == int(float(arg))
		except Exception:
			return False


