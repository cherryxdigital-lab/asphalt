# Import signals to ensure they are registered when app loads
try:
	from . import signals  # noqa
except Exception:
	pass
